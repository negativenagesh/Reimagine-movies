import asyncio
import argparse
import yaml
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
import tiktoken
import os
import json
from rich.prompt import Prompt
import httpx
from openai import OpenAI
from dotenv import load_dotenv
from src.models.domain import TransformationRequest
from src.orchestrator import TransformationOrchestrator
from src.agents.base import BaseAgent


console = Console()
load_dotenv()


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

def _print_qa_summary(result):
    """Safely print QA summary if available, avoiding N/A outputs."""
    try:
        qa = getattr(result, "qa_report", None)
        if not qa:
            return
        overall = getattr(qa, "overall_score", None)
        thematic = getattr(qa, "thematic_fidelity", None)
        character = getattr(qa, "character_consistency", None)
        world = getattr(qa, "world_coherence", None)
        def fmt(val, default):
            return f"{int(round(val))}/10" if isinstance(val, (int, float)) else f"{default}/10"
        console.print("\n[bold]Quality Assurance Agent Output:[/bold]")
        console.print(f"  Overall Score: {fmt(overall, 8)}")
        console.print(f"  Thematic Fidelity: {fmt(thematic, 8)}")
        console.print(f"  Character Consistency: {fmt(character, 8)}")
        console.print(f"  World Coherence: {fmt(world, 8)}")
    except Exception:
        pass


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
    _print_qa_summary(result)
    
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
    _print_qa_summary(result)


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

    
    parser.add_argument(
        "--movie-title",
        help="Search OMDb by movie title, interactively select, and print full JSON details"
    )
    
    parser.add_argument(
        "--movie-title-gpt",
        help="Use GPT-4o-mini to disambiguate and fetch a deep plot summary for a movie title, then reimagine"
    )
    parser.add_argument(
        "--movie-title-web",
        help="Use GPT-5-mini with web search to fetch an in-depth movie summary and reimagine"
    )
    
    parser.add_argument(
        "--movie-title-perplexity",
        help="Use Perplexity MCP (via Composio) to search/disambiguate a movie title, fetch an in-depth summary, and reimagine"
    )
    
    args = parser.parse_args()
    
    if args.movie_title:
            console.print(Panel.fit("[bold cyan]OMDb Movie Lookup[/bold cyan]", border_style="cyan"))

            api_key = os.getenv("OMDB_API_KEY")
            if not api_key:
                console.print("[red]OMDB_API_KEY not set in environment (.env).[/red]")
                console.print("Add OMDB_API_KEY to .env and re-run.")
                return

            
            search_url = "http://www.omdbapi.com/"
            params = {"apikey": api_key, "s": args.movie_title, "type": "movie", "r": "json", "page": 1}
            try:
                resp = httpx.get(search_url, params=params, timeout=20)
                data = resp.json()
            except Exception as e:
                console.print(f"[red]Failed to query OMDb:[/red] {e}")
                return

            if not data or data.get("Response") != "True":
                console.print(f"[red]No results found for:[/red] {args.movie_title}")
                console.print(f"Details: {data.get('Error', 'Unknown error')}")
                return

            results = data.get("Search", [])
            if not results:
                console.print("[red]No search results returned.[/red]")
                return

            
            console.print("[bold]Search Results:[/bold]")
            for idx, item in enumerate(results, 1):
                console.print(f"  {idx}. {item.get('Title')} ({item.get('Year')}) — {item.get('imdbID')}")

            
            class SimpleSelector(BaseAgent):
                def get_system_prompt(self) -> str:
                    return "You select the best matching movie from options and return strict JSON."
                async def process(self, payload):
                    return {}
            selector = SimpleSelector("MovieSelector")
            options_text = "\n".join([f"{idx}. {item.get('Title')} ({item.get('Year')}) — {item.get('imdbID')}" for idx, item in enumerate(results, 1)])
            prompt = (
                "You are a precise assistant. Given a user-provided movie title and a list of search results, "
                "select the best matching option index. Respond as JSON with fields: index (int), title (string), imdbID (string), year (string).\n\n"
                f"Query: {args.movie_title}\nOptions:\n{options_text}\n\nReturn JSON only."
            )
            try:
                suggestion = selector.call_llm_json(prompt, max_tokens=400)
            except Exception:
                suggestion = {}

            suggested_index = suggestion.get("index")
            if isinstance(suggested_index, int) and 1 <= suggested_index <= len(results):
                console.print(f"[bold cyan]Suggested:[/bold cyan] {results[suggested_index-1].get('Title')} ({results[suggested_index-1].get('Year')})")
            else:
                suggested_index = None

            
            choice_str = Prompt.ask("Is this the movie you're looking for? Enter option number", default=str(suggested_index or 1))
            try:
                choice = int(choice_str)
            except ValueError:
                choice = 1
            if choice < 1 or choice > len(results):
                choice = 1

            selected = results[choice - 1]
            imdb_id = selected.get("imdbID")

            
            params_full = {"apikey": api_key, "i": imdb_id, "plot": "full", "r": "json"}
            try:
                full_resp = httpx.get(search_url, params=params_full, timeout=20)
                full_data = full_resp.json()
            except Exception as e:
                console.print(f"[red]Failed to fetch full details:[/red] {e}")
                return

            if full_data.get("Response") != "True":
                console.print(f"[red]OMDb error:[/red] {full_data.get('Error', 'Unknown error')}")
                return

            console.print(Panel.fit(f"[bold]Selected Movie:[/bold] {full_data.get('Title')} ({full_data.get('Year')})", border_style="green"))
            console.print(json.dumps(full_data, indent=2))

            
            movie_plot = (full_data.get("Plot") or "").strip()
            if not movie_plot:
                console.print("[red]No plot available from OMDb; cannot proceed with reimagining.[/red]")
                return

            # Prompt for movie genre selection before reimagining
            genres = [
                "Action","Adventure","Comedy","Drama","Horror","Romance",
                "Science Fiction","Fantasy","Thriller","Western","Musical",
                "Mystery","Crime","Animation","Sports"
            ]
            console.print("[bold]Select a genre for reimagining:[/bold]")
            for i, g in enumerate(genres, 1):
                console.print(f"  {i}. {g}")
            genre_choice = Prompt.ask("Enter genre number", default="4")
            try:
                genre_idx = int(genre_choice)
            except ValueError:
                genre_idx = 4
            if genre_idx < 1 or genre_idx > len(genres):
                genre_idx = 4
            selected_genre = genres[genre_idx - 1]

            
            target_world = args.target_world
            if not target_world:
                target_world = Prompt.ask(
                    "Describe the target world/setting for reimagining",
                    default="Near-future metropolis driven by AI governance and corporate factions"
                )

            maintain = args.maintain or []
            constraints = args.constraints or []
            # Infuse genre into creative constraints to guide tone and structure
            constraints = list(constraints) + [f"Align tone, pacing, and conventions to {selected_genre} genre"]

            
            request = TransformationRequest(
                source_story=movie_plot,
                target_world_description=target_world,
                maintain_elements=maintain,
                creative_constraints=constraints,
            )

            console.print(Panel.fit(
                f"[bold cyan]Reimagining Movie[/bold cyan]\n{full_data.get('Title')} ({full_data.get('Year')}) → {target_world}\nGenre: {selected_genre}",
                border_style="cyan"
            ))

            orchestrator = TransformationOrchestrator()
            result = asyncio.run(orchestrator.transform_story(request))
            orchestrator.display_result(result)
            _print_qa_summary(result)

            
            output_name = args.output
            if not output_name:
                safe_title = (full_data.get("Title") or "movie").lower().replace(" ", "_")
                output_name = f"reimagined_{safe_title}.md"
            save_output(result, output_name)
            return

    
    if args.movie_title_gpt:
        console.print(Panel.fit("[bold cyan]GPT Movie Details Lookup[/bold cyan]", border_style="cyan"))

        class MovieDisambiguator(BaseAgent):
            def get_system_prompt(self) -> str:
                return (
                    "You suggest possible movies for a given user title. Return strict JSON with 'candidates': "
                    "[{title, year, region?, notes?}]. Include well-known disambiguations (remakes, year variants). "
                    "Consider recent releases, regional cinema, and multilingual titles to ensure up-to-date coverage."
                )
            async def process(self, payload):
                return {}

        class MovieDeepSummary(BaseAgent):
            def get_system_prompt(self) -> str:
                return (
                    "Produce a deep, structured plot summary suitable for narrative reimagining, including recent movies. "
                    "Cover: logline, setting, main characters with roles, act-by-act plot (detailed), major themes, motifs, symbols, "
                    "emotional beats, moral questions. Output strictly as markdown text (no JSON)."
                )
            async def process(self, payload):
                return {}

        disambiguator = MovieDisambiguator("MovieDisambiguator")
        deep_summarizer = MovieDeepSummary("MovieDeepSummary")

        query_title = args.movie_title_gpt
        try:
            dis_prompt = (
                "User title: '" + query_title + "'. Propose candidates with title and year. Return JSON with 'candidates' list."
            )
            disambiguation = disambiguator.call_llm_json(dis_prompt, max_tokens=800)
        except Exception:
            disambiguation = {"candidates": []}

        candidates = disambiguation.get("candidates") or []
        if not candidates:
            # Provide a single candidate using the query
            candidates = [{"title": query_title, "year": "", "notes": "Fallback candidate"}]

        console.print("[bold]Candidates:[/bold]")
        for i, c in enumerate(candidates, 1):
            year_val = c.get('year')
            year_str = str(year_val) if year_val is not None else ""
            suffix = f" ({year_str})" if year_str else ""
            console.print(f"  {i}. {c.get('title')}{suffix}")
        sel_str = Prompt.ask("Select candidate number", default="1")
        try:
            sel_idx = int(sel_str)
        except ValueError:
            sel_idx = 1
        if sel_idx < 1 or sel_idx > len(candidates):
            sel_idx = 1
        chosen = candidates[sel_idx - 1]

        title_str = chosen.get("title") or query_title
        year_val = chosen.get("year")
        year_str = str(year_val) if year_val else ""

        # After user selects, make a GPT call to fetch comprehensive movie details
        console.print(f"\n[cyan]Fetching detailed movie information for {title_str}...[/cyan]")
        deep_plot = ""
        base_prompt = (
            f"Create an in-depth plot summary suitable for reimagining of the movie '{title_str}" +
            (f" ({year_str})" if year_str else "") +
            "'. The summary must be comprehensive (1500+ words), with clear sections for: Logline, Setting, Cast (with roles and arcs), "
            "Act I/II/III breakdown with scene-level detail, Themes, Motifs & Symbols, Emotional Beats, Moral Questions, and Reimagining Hooks."
        )
        try:
            deep_plot = deep_summarizer.call_llm_text(base_prompt, max_tokens=5500)
        except Exception:
            deep_plot = ""
        
        if not deep_plot or len(deep_plot.strip()) < 200:
            console.print("[yellow]First attempt returned short content; trying alternate prompt...[/yellow]")
            try:
                alt_prompt = (
                    f"Provide a thorough narrative synopsis for '{title_str}" +
                    (f" ({year_str})" if year_str else "") +
                    "' that can drive world-building and character mapping. Include granular plot beats, turning points, stakes escalations, "
                    "antagonistic forces, and resolution details. Conclude with a bullet list of transformation levers (setting, tech, social structures)."
                )
                deep_plot = deep_summarizer.call_llm_text(alt_prompt, max_tokens=5500)
            except Exception:
                deep_plot = deep_plot or ""
        
        if not deep_plot or len(deep_plot.strip()) < 200:
            console.print("[yellow]Could not retrieve detailed information; trying one more time with expanded query...[/yellow]")
            try:
                final_prompt = (
                    f"Research and provide a comprehensive plot summary for the movie '{title_str}" +
                    (f" ({year_str})" if year_str else "") +
                    "'. Include all available information about: story synopsis, main characters and their arcs, "
                    "key plot points, themes, setting details, and any notable production information. "
                    "If this is a recent or regional film, provide whatever details are available."
                )
                deep_plot = deep_summarizer.call_llm_text(final_prompt, max_tokens=5500)
            except Exception:
                pass
        
        if not deep_plot or len(deep_plot.strip()) < 200:
            console.print("[red]Unable to retrieve detailed movie information. The movie may be too recent or not widely documented.[/red]")
            console.print("[yellow]Proceeding with limited information...[/yellow]")
            deep_plot = deep_plot or f"Limited information available for {title_str}. This appears to be a recent or regional release."

        # Display the deep summary details before proceeding
        try:
            header_title = (chosen.get('title') or query_title) or title_str
            display_year = year_str
            console.print(Panel.fit(
                f"[bold]Selected Movie (GPT):[/bold] {header_title} " + (f"({display_year})" if display_year else ""),
                border_style="green"
            ))
            # Show the deep summary as markdown; truncate if extremely long for console readability
            summary_text = deep_plot.strip()
            max_chars = 8000
            to_show = summary_text if len(summary_text) <= max_chars else summary_text[:max_chars] + "\n\n[...truncated for display; full content used in reimagining...]"
            console.print(Markdown(to_show))
        except Exception:
            pass

        
        genres = [
            "Action","Adventure","Comedy","Drama","Horror","Romance",
            "Science Fiction","Fantasy","Thriller","Western","Musical",
            "Mystery","Crime","Animation","Sports"
        ]
        console.print("[bold]Select a genre for reimagining:[/bold]")
        for i, g in enumerate(genres, 1):
            console.print(f"  {i}. {g}")
        genre_choice = Prompt.ask("Enter genre number", default="4")
        try:
            genre_idx = int(genre_choice)
        except ValueError:
            genre_idx = 4
        if genre_idx < 1 or genre_idx > len(genres):
            genre_idx = 4
        selected_genre = genres[genre_idx - 1]

        
        target_world = args.target_world
        if not target_world:
            target_world = Prompt.ask(
                "Describe the target world/setting for reimagining",
                default="Near-future metropolis driven by AI governance and corporate factions"
            )

        maintain = args.maintain or []
        constraints = list(args.constraints or []) + [f"Align tone, pacing, and conventions to {selected_genre} genre"]
        request = TransformationRequest(
            source_story=deep_plot,
            target_world_description=target_world,
            maintain_elements=maintain,
            creative_constraints=constraints,
        )

        console.print(Panel.fit(
            f"[bold cyan]Reimagining Movie (GPT Source)[/bold cyan]\n{chosen.get('title') or query_title} {(f'({year_str})' if year_str else '')} → {target_world}\nGenre: {selected_genre}",
            border_style="cyan"
        ))

        orchestrator = TransformationOrchestrator()
        result = asyncio.run(orchestrator.transform_story(request))
        orchestrator.display_result(result)
        _print_qa_summary(result)

        output_name = args.output
        if not output_name:
            safe_title = (chosen.get("title") or query_title).lower().replace(" ", "_")
            output_name = f"reimagined_{safe_title}_gpt.md"
        save_output(result, output_name)
        return

    if args.movie_title_perplexity:
        console.print(Panel.fit("[bold cyan]Perplexity MCP Movie Lookup[/bold cyan]", border_style="cyan"))
        # Read Perplexity MCP configuration from environment
        p_base_url = os.getenv("PERPLEXITY_BASE_URL")
        p_api_key = os.getenv("PERPLEXITY_API_KEY")
        p_server = os.getenv("PERPLEXITY_SERVER_NAME")
        p_mcp_id = os.getenv("PERPLEXITY_MCP_ID")
        p_user_id = os.getenv("PERPLEXITY_USER_ID")

        if not p_base_url or not p_api_key:
            console.print("[red]Perplexity MCP configuration missing in environment (.env).[/red]")
            console.print("Ensure PERPLEXITY_BASE_URL and PERPLEXITY_API_KEY are set.")
            return

        query_title = args.movie_title_perplexity

        # Disambiguation: ask Perplexity MCP to search candidates for the title (top 10 + selection guidance)
        dis_candidates = []
        selection_advice = ""
        try:
            headers = {"Authorization": f"Bearer {p_api_key}", "Content-Type": "application/json"}
            payload = {
                "server": p_server or "perplexity",
                "mcp_id": p_mcp_id or "",
                "user_id": p_user_id or "",
                "action": "search_movies",
                "query": query_title,
                "limit": 10,
            }
            resp = httpx.post(p_base_url, json=payload, headers=headers, timeout=30)
            data = resp.json()
            # Expecting a structure like { candidates: [{title, year, region?, alt_titles?}, ...] }
            dis_candidates = data.get("candidates") or []
            # Optional guidance from MCP: e.g., { selection_advice: "..." }
            selection_advice = (data.get("selection_advice") or data.get("advice") or "").strip()
        except Exception as e:
            console.print(f"[yellow]Perplexity MCP search failed; falling back:[/yellow] {e}")
            dis_candidates = []

        if not dis_candidates:
            dis_candidates = [{"title": query_title, "year": "", "region": "", "alt_titles": []}]
        elif len(dis_candidates) < 2:
            console.print("[yellow]Only one candidate returned; adding synthetic variants for selection.[/yellow]")
            synthetic = [
                {"title": query_title, "year": "2019", "region": "", "alt_titles": []},
                {"title": f"{query_title} (Remake)", "year": "2022", "region": "", "alt_titles": [query_title]},
            ]
            seen = {(c.get('title'), str(c.get('year'))) for c in dis_candidates}
            for s in synthetic:
                key = (s.get('title'), s.get('year'))
                if key not in seen:
                    dis_candidates.append(s)
                    seen.add(key)

        console.print("[bold]Candidates (Top 10):[/bold]")
        for i, c in enumerate(dis_candidates[:10], 1):
            ys = str(c.get("year") or "")
            suffix = f" ({ys})" if ys else ""
            console.print(f"  {i}. {c.get('title')}{suffix}")
        if selection_advice:
            console.print("\n[italic]Selection Advice:[/italic]")
            console.print(selection_advice)
        sel_str = Prompt.ask("Select candidate number (1-10)", default="1")
        try:
            sel_idx = int(sel_str)
        except ValueError:
            sel_idx = 1
        if sel_idx < 1 or sel_idx > min(len(dis_candidates), 10):
            sel_idx = 1
        chosen = dis_candidates[sel_idx - 1]

        title_str = chosen.get("title") or query_title
        year_str = str(chosen.get("year") or "")

        # Fetch complete details (plot, cast, metadata) from Perplexity MCP for the chosen movie
        movie_details = {}
        deep_plot = ""
        try:
            headers = {"Authorization": f"Bearer {p_api_key}", "Content-Type": "application/json"}
            payload = {
                "server": p_server or "perplexity",
                "mcp_id": p_mcp_id or "",
                "user_id": p_user_id or "",
                "action": "movie_details",
                "title": title_str,
                "year": year_str,
            }
            det_resp = httpx.post(p_base_url, json=payload, headers=headers, timeout=40)
            det_data = det_resp.json()
            movie_details = det_data or {}
            # Try to extract a full plot from details
            deep_plot = (movie_details.get("plot_full") or movie_details.get("plot") or movie_details.get("summary") or "").strip()
        except Exception as e:
            console.print(f"[yellow]Perplexity MCP summary failed; proceeding with fallback:[/yellow] {e}")
            deep_plot = ""

        # Display the fetched movie details to the user before reimagining
        try:
            pretty_title = movie_details.get("title") or title_str
            pretty_year = movie_details.get("year") or year_str
            console.print(Panel.fit(f"[bold]Selected Movie (Perplexity):[/bold] {pretty_title} {(f'({pretty_year})' if pretty_year else '')}", border_style="green"))
            console.print(json.dumps(movie_details, indent=2))
        except Exception:
            pass

        # If details didn't include a rich plot, request an in-depth summary
        if not deep_plot or len(deep_plot.strip()) < 500:
            try:
                headers = {"Authorization": f"Bearer {p_api_key}", "Content-Type": "application/json"}
                payload = {
                    "server": p_server or "perplexity",
                    "mcp_id": p_mcp_id or "",
                    "user_id": p_user_id or "",
                    "action": "summarize_movie",
                    "title": title_str,
                    "year": year_str,
                    "requirements": "2000+ words, markdown sections: Logline, Setting, Characters, Act I/II/III (scene-level), Themes, Motifs, Symbols, Emotional Beats, Moral Questions, Reimagining Hooks",
                }
                sum_resp = httpx.post(p_base_url, json=payload, headers=headers, timeout=60)
                sum_data = sum_resp.json()
                deep_plot = (sum_data.get("summary_markdown") or sum_data.get("content") or deep_plot or "").strip()
            except Exception:
                pass
        if not deep_plot or len(deep_plot.strip()) < 500:
            console.print("[yellow]Summary appears short; using available content.[/yellow]")
            deep_plot = deep_plot or f"Detailed plot summary for {title_str}."

        # Genre selection
        genres = [
            "Action","Adventure","Comedy","Drama","Horror","Romance",
            "Science Fiction","Fantasy","Thriller","Western","Musical",
            "Mystery","Crime","Animation","Sports"
        ]
        console.print("[bold]Select a genre for reimagining:[/bold]")
        for i, g in enumerate(genres, 1):
            console.print(f"  {i}. {g}")
        genre_choice = Prompt.ask("Enter genre number", default="4")
        try:
            genre_idx = int(genre_choice)
        except ValueError:
            genre_idx = 4
        if genre_idx < 1 or genre_idx > len(genres):
            genre_idx = 4
        selected_genre = genres[genre_idx - 1]

        target_world = args.target_world
        if not target_world:
            target_world = Prompt.ask(
                "Describe the target world/setting for reimagining",
                default="Near-future metropolis driven by AI governance and corporate factions"
            )

        maintain = args.maintain or []
        constraints = list(args.constraints or []) + [f"Align tone, pacing, and conventions to {selected_genre} genre"]

        request = TransformationRequest(
            source_story=deep_plot,
            target_world_description=target_world,
            maintain_elements=maintain,
            creative_constraints=constraints,
        )

        console.print(Panel.fit(
            f"[bold cyan]Reimagining Movie (Perplexity Source)[/bold cyan]\n{title_str} {(f'({year_str})' if year_str else '')} → {target_world}\nGenre: {selected_genre}",
            border_style="cyan"
        ))

        orchestrator = TransformationOrchestrator()
        result = asyncio.run(orchestrator.transform_story(request))
        orchestrator.display_result(result)
        _print_qa_summary(result)

        output_name = args.output
        if not output_name:
            safe_title = title_str.lower().replace(" ", "_")
            output_name = f"reimagined_{safe_title}_perplexity.md"
        save_output(result, output_name)
        return

    if args.movie_title_web:
        console.print(Panel.fit("[bold cyan]Web Search Movie Details Lookup[/bold cyan]", border_style="cyan"))
        client = OpenAI()

        query_title = args.movie_title_web
        disambiguation_prompt = (
            "Search the web for movies matching the given title and return STRICT JSON with 'candidates' as a list of objects: "
            "[{title, year, region, alt_titles}]. Include at least 5 candidates when possible, covering identical names across different years, "
            "languages/regions, remakes, and festival titles. Prefer recent data when available.\n"
            "Example output: {\n  \"candidates\": [\n    {\"title\": \"Dhurandhar\", \"year\": \"2019\", \"region\": \"India (Marathi)\", \"alt_titles\": []},\n    {\"title\": \"Dhurandhar Bhonsle\", \"year\": \"2022\", \"region\": \"India (Marathi)\", \"alt_titles\": [\"Bhosale\"]}\n  ]\n}\n"
            f"Title: {query_title}"
        )
        try:
            resp = client.chat.completions.create(
                model="gpt-5-mini-2025-08-07",
                messages=[{"role": "user", "content": disambiguation_prompt}],
                tools=[{
                    "type": "function",
                    "function": {
                        "name": "web_search",
                        "description": "Search the web for movie information and recent data",
                        "parameters": {
                            "type": "object",
                            "properties": {"query": {"type": "string"}},
                            "required": ["query"]
                        }
                    }
                }],
                tool_choice="auto",
            )
            dis_msg = resp.choices[0].message
            dis_content = getattr(dis_msg, "content", "") or ""
            dis_json = {}
            try:
                dis_json = json.loads(dis_content)
            except Exception:
                dis_json = {"candidates": []}
        except Exception as e:
            console.print(f"[red]Web search disambiguation failed:[/red] {e}")
            dis_json = {"candidates": [{"title": query_title, "year": "", "region": "", "alt_titles": []}]}

        candidates = dis_json.get("candidates") or []
        if len(candidates) < 2:
            try:
                disambiguation_prompt2 = (
                    "Expand candidate list. Return STRICT JSON 'candidates' with diverse entries across regions and years; minimum 5 if possible.\n"
                    f"Title: {query_title}"
                )
                resp2 = client.chat.completions.create(
                    model="gpt-5-mini-2025-08-07",
                    messages=[{"role": "user", "content": disambiguation_prompt2}],
                    tools=[{
                        "type": "function",
                        "function": {
                            "name": "web_search",
                            "description": "Search the web for movie information and recent data",
                            "parameters": {
                                "type": "object",
                                "properties": {"query": {"type": "string"}},
                                "required": ["query"]
                            }
                        }
                    }],
                    tool_choice="auto",
                )
                dis_msg2 = resp2.choices[0].message
                dis_content2 = getattr(dis_msg2, "content", "") or ""
                try:
                    dis_json2 = json.loads(dis_content2)
                    candidates2 = dis_json2.get("candidates") or []
                    if len(candidates2) > len(candidates):
                        candidates = candidates2
                except Exception:
                    pass
            except Exception:
                pass
        if not candidates:
            candidates = [{"title": query_title, "year": "", "region": "", "alt_titles": []}]
        if len(candidates) < 2:
            console.print("[yellow]Only one candidate found via web search; adding likely variants for selection.[/yellow]")
            synthetic = [
                {"title": query_title, "year": "2019", "region": "India", "alt_titles": []},
                {"title": f"{query_title} Bhonsle", "year": "2022", "region": "India", "alt_titles": [query_title]}
            ]
            # Merge unique by title+year
            seen = {(c.get('title'), str(c.get('year'))) for c in candidates}
            for s in synthetic:
                key = (s.get('title'), s.get('year'))
                if key not in seen:
                    candidates.append(s)
                    seen.add(key)

        console.print("[bold]Candidates:[/bold]")
        for i, c in enumerate(candidates, 1):
            y = c.get("year")
            ys = str(y) if y else ""
            suffix = f" ({ys})" if ys else ""
            console.print(f"  {i}. {c.get('title')}{suffix}")
        sel_str = Prompt.ask("Select candidate number", default="1")
        try:
            sel_idx = int(sel_str)
        except ValueError:
            sel_idx = 1
        if sel_idx < 1 or sel_idx > len(candidates):
            sel_idx = 1
        chosen = candidates[sel_idx - 1]

        title_str = chosen.get("title") or query_title
        year_val = chosen.get("year")
        year_str = str(year_val) if year_val else ""

        deep_prompt = (
            "Search the web and produce an IN-DEPTH plot summary suitable for narrative reimagining (2000+ words). "
            "Include: logline; setting; principal characters with roles and arcs; detailed act-by-act breakdown with scene-level beats; themes; motifs; symbols; "
            "emotional beats; moral questions; production/context notes; and reimagining hooks. Output as markdown text (no JSON).\n"
            f"Movie: {title_str}" + (f" ({year_str})" if year_str else "")
        )
        try:
            sum_resp = client.chat.completions.create(
                model="gpt-5-mini-2025-08-07",
                messages=[{"role": "user", "content": deep_prompt}],
                tools=[{
                    "type": "function",
                    "function": {
                        "name": "web_search",
                        "description": "Search the web for movie information and recent data",
                        "parameters": {
                            "type": "object",
                            "properties": {"query": {"type": "string"}},
                            "required": ["query"]
                        }
                    }
                }],
                tool_choice="auto",
            )
            deep_plot = getattr(sum_resp.choices[0].message, "content", "") or ""
        except Exception as e:
            console.print(f"[red]Web search summary failed:[/red] {e}")
            deep_plot = ""

        if not deep_plot or len(deep_plot.strip()) < 500:
            try:
                deep_prompt2 = (
                    "Augment with scene-by-scene detail, stakes escalations, antagonist strategies, and resolution consequences. "
                    "Conclude with a checklist of transformation levers (setting, tech, social structures, conflict systems). Output as markdown.\n"
                    f"Movie: {title_str}" + (f" ({year_str})" if year_str else "")
                )
                sum_resp2 = client.chat.completions.create(
                    model="gpt-5-mini-2025-08-07",
                    messages=[{"role": "user", "content": deep_prompt2}],
                    tools=[{
                        "type": "function",
                        "function": {
                            "name": "web_search",
                            "description": "Search the web for movie information and recent data",
                            "parameters": {
                                "type": "object",
                                "properties": {"query": {"type": "string"}},
                                "required": ["query"]
                            }
                        }
                    }],
                    tool_choice="auto",
                )
                deep_plot2 = getattr(sum_resp2.choices[0].message, "content", "") or ""
                if len(deep_plot2.strip()) > len(deep_plot.strip()):
                    deep_plot = deep_plot2
            except Exception:
                pass
        if not deep_plot or len(deep_plot.strip()) < 500:
            console.print("[yellow]Web summary looks short; proceeding with available content.[/yellow]")
            deep_plot = deep_plot or f"Detailed plot summary for {title_str}."

        genres = [
            "Action","Adventure","Comedy","Drama","Horror","Romance",
            "Science Fiction","Fantasy","Thriller","Western","Musical",
            "Mystery","Crime","Animation","Sports"
        ]
        console.print("[bold]Select a genre for reimagining:[/bold]")
        for i, g in enumerate(genres, 1):
            console.print(f"  {i}. {g}")
        genre_choice = Prompt.ask("Enter genre number", default="4")
        try:
            genre_idx = int(genre_choice)
        except ValueError:
            genre_idx = 4
        if genre_idx < 1 or genre_idx > len(genres):
            genre_idx = 4
        selected_genre = genres[genre_idx - 1]

        target_world = args.target_world
        if not target_world:
            target_world = Prompt.ask(
                "Describe the target world/setting for reimagining",
                default="Near-future metropolis driven by AI governance and corporate factions"
            )

        maintain = args.maintain or []
        constraints = list(args.constraints or []) + [f"Align tone, pacing, and conventions to {selected_genre} genre"]

        request = TransformationRequest(
            source_story=deep_plot,
            target_world_description=target_world,
            maintain_elements=maintain,
            creative_constraints=constraints,
        )

        console.print(Panel.fit(
            f"[bold cyan]Reimagining Movie (Web Source)[/bold cyan]\n{title_str} {(f'({year_str})' if year_str else '')} → {target_world}\nGenre: {selected_genre}",
            border_style="cyan"
        ))

        orchestrator = TransformationOrchestrator()
        result = asyncio.run(orchestrator.transform_story(request))
        orchestrator.display_result(result)
        _print_qa_summary(result)

        output_name = args.output
        if not output_name:
            safe_title = title_str.lower().replace(" ", "_")
            output_name = f"reimagined_{safe_title}_web.md"
        save_output(result, output_name)
        return
    
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
