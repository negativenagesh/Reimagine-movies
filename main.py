import asyncio
import argparse
import yaml
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
import tiktoken
from src.models.domain import TransformationRequest
from src.orchestrator import TransformationOrchestrator


console = Console()


def load_source_story(story_name: str) -> str:
    stories_path = Path("data/source_stories.yaml")
    if not stories_path.exists():
        console.print("[red]Error: source_stories.yaml not found[/red]")
        exit(1)
    
    with open(stories_path, "r") as f:
        stories = yaml.safe_load(f)
    
    if story_name not in stories:
        console.print(f"[red]Error: Story '{story_name}' not found[/red]")
        console.print(f"Available stories: {', '.join(stories.keys())}")
        exit(1)
    
    return stories[story_name]


def save_output(result, output_file: str):
    Path("output").mkdir(exist_ok=True)
    
    output_path = Path("output") / output_file
    
    is_markdown = output_path.suffix.lower() == ".md"
    # Compute story length metrics locally to avoid relying on missing attributes
    try:
        encoding = tiktoken.encoding_for_model("gpt-4o-mini")
        story_tokens = len(encoding.encode(result.full_story))
    except Exception:
        # Fallback in case encoding model isn't available
        story_tokens = len(result.full_story.split())
    story_words = len(result.full_story.split())
    
    with open(output_path, "w") as f:
        if is_markdown:
            # Write a Markdown header with minimal front matter style metadata
            f.write(f"# {getattr(result, 'final_title', 'Transformed Story')}\n\n")
            f.write(f"- Original: {result.original_analysis.title}\n")
            f.write(f"- New World: {result.transformed_world.name}\n")
            f.write(f"- Story Length: {story_tokens} tokens / {story_words} words\n")
            f.write(f"- Consistency Score: {result.consistency_score:.1%}\n\n")
            f.write(result.full_story)
        else:
            f.write("="*80 + "\n")
            f.write("TRANSFORMATION RESULT\n")
            f.write("="*80 + "\n\n")
            
            f.write(f"Original: {result.original_analysis.title}\n")
            f.write(f"New World: {result.transformed_world.name}\n")
            f.write(f"Story Length: {story_tokens} tokens / {story_words} words\n")
            f.write(f"Consistency Score: {result.consistency_score:.1%}\n\n")
            
            f.write("="*80 + "\n")
            f.write("TRANSFORMED STORY\n")
            f.write("="*80 + "\n\n")
            
            f.write(result.full_story)
            
            f.write("\n\n" + "="*80 + "\n")
            f.write("TRANSFORMATION ANALYSIS\n")
            f.write("="*80 + "\n\n")
            
            f.write("Original Theme: " + result.original_analysis.core_theme + "\n")
            f.write("Moral Lesson: " + result.original_analysis.moral_lesson + "\n\n")
            
            f.write("World Details:\n")
            f.write(f"  Era: {result.transformed_world.era}\n")
            f.write(f"  Technology: {result.transformed_world.technology_level}\n")
            f.write(f"  Social Structure: {result.transformed_world.social_structure}\n\n")
            
            f.write("Character Mappings:\n")
            for char in result.transformed_characters:
                # Handle both dicts and Pydantic models gracefully
                if isinstance(char, dict):
                    name = char.get('name') or char.get('original_name') or ''
                    transformed_name = char.get('transformed_name', '')
                    transformed_role = char.get('transformed_role', '')
                else:
                    name = getattr(char, 'name', '') or getattr(char, 'original_name', '')
                    transformed_name = getattr(char, 'transformed_name', '')
                    transformed_role = getattr(char, 'transformed_role', '')
                f.write(f"  {name} → {transformed_name}\n")
                f.write(f"    Role: {transformed_role}\n")
            
            f.write("\nTransformation Notes:\n")
            for key, value in result.transformation_notes.items():
                f.write(f"  {key.replace('_', ' ').title()}: {value}\n")
    
    console.print(f"\n[green]✓ Output saved to {output_path}[/green]")


async def run_transformation(args):
    if args.story_name:
        source_story = load_source_story(args.story_name)
    else:
        source_story = args.custom_story
    
    if not source_story:
        console.print("[red]Error: Must provide either --story-name or --custom-story[/red]")
        exit(1)
    
    console.print(Panel.fit(
        "[bold cyan]Story Transformation System[/bold cyan]\n"
        "Multi-Agent Microservice Architecture",
        border_style="cyan"
    ))
    
    request = TransformationRequest(
        source_story=source_story,
        target_world_description=args.target_world,
        maintain_elements=args.maintain or [],
        creative_constraints=args.constraints or []
    )
    
    orchestrator = TransformationOrchestrator()
    result = await orchestrator.transform_story(request)
    
    orchestrator.display_result(result)
    
    if args.output:
        save_output(result, args.output)


async def run_example():
    console.print(Panel.fit(
        "[bold cyan]Running Example Transformation[/bold cyan]\n"
        "Romeo and Juliet → Silicon Valley AI Labs",
        border_style="cyan"
    ))
    
    source_story = load_source_story("ROMEO_AND_JULIET")
    
    request = TransformationRequest(
        source_story=source_story,
        target_world_description="""Silicon Valley in 2024, where two rival AI research companies - 
        Montague AI and Capulet Labs - are locked in fierce competition for AI supremacy. 
        The world is one of venture capital, patent wars, corporate espionage, and the race 
        to achieve AGI. Success means billions in valuation; failure means obsolescence.""",
        maintain_elements=["star-crossed love", "family feud consequences", "tragic miscommunication"],
        creative_constraints=["keep it grounded in realistic tech", "no magic solutions"]
    )
    
    orchestrator = TransformationOrchestrator()
    result = await orchestrator.transform_story(request)
    
    orchestrator.display_result(result)
    save_output(result, "romeo_juliet_ai_labs.txt")


def main():
    parser = argparse.ArgumentParser(
        description="AI-Powered Narrative Transformation System"
    )
    
    parser.add_argument(
        "--story-name",
        help="Name of predefined story from data/source_stories.yaml"
    )
    
    parser.add_argument(
        "--custom-story",
        help="Custom story text to transform"
    )
    
    parser.add_argument(
        "--target-world",
        help="Description of the target world/setting"
    )
    
    parser.add_argument(
        "--maintain",
        nargs="+",
        help="Elements to maintain in transformation"
    )
    
    parser.add_argument(
        "--constraints",
        nargs="+",
        help="Creative constraints to apply"
    )
    
    parser.add_argument(
        "--output",
        help="Output filename (saved to output/ directory). Use .md to save Markdown"
    )

    parser.add_argument(
        "--preview",
        help="Preview a predefined story summary by name (no transformation)",
    )

    parser.add_argument(
        "--preview-file",
        help="Preview a saved output file (e.g., output/*.md) rendered in console",
    )
    
    parser.add_argument(
        "--example",
        action="store_true",
        help="Run example transformation (Romeo & Juliet → AI Labs)"
    )
    
    parser.add_argument(
        "--list-stories",
        action="store_true",
        help="List available predefined stories"
    )
    
    parser.add_argument(
        "--api",
        action="store_true",
        help="Start API server"
    )
    
    args = parser.parse_args()
    
    if args.list_stories:
        stories_path = Path("data/source_stories.yaml")
        with open(stories_path, "r") as f:
            stories = yaml.safe_load(f)
        console.print("[bold]Available Stories:[/bold]")
        for story in stories.keys():
            console.print(f"  • {story}")
        return

    if args.preview:
        stories_path = Path("data/source_stories.yaml")
        with open(stories_path, "r") as f:
            stories = yaml.safe_load(f)
        name = args.preview
        if name not in stories:
            console.print(f"[red]Story '{name}' not found[/red]")
            console.print(f"Available stories: {', '.join(stories.keys())}")
            return
        console.print(Panel.fit(f"[bold]Preview: {name}[/bold]", border_style="cyan"))
        console.print(Markdown(stories[name][:2000]))
        return

    if args.preview_file:
        file_path = Path(args.preview_file)
        if not file_path.exists():
            console.print(f"[red]File not found:[/red] {file_path}")
            return
        try:
            content = file_path.read_text(encoding="utf-8")
        except Exception as e:
            console.print(f"[red]Failed to read file:[/red] {e}")
            return
        console.print(Panel.fit(f"[bold]Preview File:[/bold] {file_path}", border_style="cyan"))
        # Render as Markdown if it looks like Markdown, else plain text
        if file_path.suffix.lower() in {".md", ".markdown"}:
            console.print(Markdown(content))
        else:
            console.print(content)
        return
    
    if args.api:
        import uvicorn
        from src.api import app
        console.print("[bold cyan]Starting API server on http://localhost:8000[/bold cyan]")
        uvicorn.run(app, host="0.0.0.0", port=8000)
        return
    
    if args.example:
        asyncio.run(run_example())
    elif args.target_world:
        asyncio.run(run_transformation(args))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
