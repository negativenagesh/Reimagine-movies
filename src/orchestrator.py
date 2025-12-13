from typing import Dict, Any
import tiktoken
from src.agents.story_analysis_agent import StoryAnalysisAgent
from src.agents.world_builder_agent import WorldBuilderAgent
from src.agents.character_mapping_agent import CharacterMappingAgent
from src.agents.plot_transformation_agent import PlotTransformationAgent
from src.agents.story_writer_agent import StoryWriterAgent
from src.agents.qa_agent import QualityAssuranceAgent
from src.models.domain import TransformationRequest, TransformationResult
from rich.console import Console


class TransformationOrchestrator:
    def __init__(self):
        self.console = Console()
        self.story_analyzer = StoryAnalysisAgent()
        self.world_builder = WorldBuilderAgent()
        self.character_mapper = CharacterMappingAgent()
        self.plot_transformer = PlotTransformationAgent()
        self.story_writer = StoryWriterAgent()
        self.qa_agent = QualityAssuranceAgent()
        self.encoding = tiktoken.encoding_for_model("gpt-4o-mini")
    
    async def transform_story(self, request: TransformationRequest) -> TransformationResult:
        self.console.print("[cyan]Analyzing source story...[/cyan]")
        analysis_result = await self.story_analyzer.process({
            "source_story": request.source_story
        })
        self.console.print("✅ Story analysis complete\n", style="green")
        
        original_analysis = analysis_result["analysis"]
        
        self.console.print("[bold]Story Analysis Agent Output:[/bold]")
        self.console.print(f"  Title: {original_analysis['title']}")
        self.console.print(f"  Theme: {original_analysis['core_theme']}")
        self.console.print(f"  Moral: {original_analysis['moral_lesson']}")
        self.console.print(f"  Emotional Journey: {original_analysis['emotional_journey']}")
        self.console.print(f"  Characters: {len(original_analysis['characters'])} identified")
        for i, char in enumerate(original_analysis['characters'], 1):
            self.console.print(f"    {i}. {char['name']} ({char['archetype']})")
        self.console.print(f"  Plot Points: {len(original_analysis['plot_points'])} identified")
        for point in original_analysis['plot_points']:
            self.console.print(f"    {point['sequence']}. {point['original_event']}")
        self.console.print()
        
        self.console.print("[cyan]Building alternate world...[/cyan]")
        world_result = await self.world_builder.process({
            "target_world_description": request.target_world_description,
            "original_analysis": original_analysis
        })
        self.console.print("✅ World building complete\n", style="green")
        
        transformed_world = world_result["world"]
        
        self.console.print("[bold]World Builder Agent Output:[/bold]")
        self.console.print(f"  World: {transformed_world['name']}")
        self.console.print(f"  Era: {transformed_world['era']}")
        self.console.print(f"  Technology: {transformed_world['technology_level']}")
        self.console.print(f"  Social Structure: {transformed_world['social_structure']}")
        self.console.print(f"  Power Dynamics: {transformed_world['power_dynamics']}")
        self.console.print()
        
        self.console.print("[cyan]Mapping characters to new world...[/cyan]")
        character_result = await self.character_mapper.process({
            "original_characters": original_analysis["characters"],
            "world": transformed_world
        })
        self.console.print("✅ Character mapping complete\n", style="green")
        
        transformed_characters = character_result["transformed_characters"]
        
        self.console.print("[bold]Character Mapping Agent Output:[/bold]")
        for char in transformed_characters:
            orig = char.get('name', 'N/A')
            new = char.get('transformed_name', 'N/A')
            role = char.get('transformed_role', 'N/A')
            self.console.print(f"  - {orig} -> {new}")
            self.console.print(f"    Role: {role}")
        self.console.print()
        
        self.console.print("[cyan]Transforming plot points...[/cyan]")
        plot_result = await self.plot_transformer.process({
            "plot_points": original_analysis["plot_points"],
            "world": transformed_world,
            "transformed_characters": transformed_characters
        })
        self.console.print("✅ Plot transformation complete\n", style="green")
        
        transformed_plot = plot_result["transformed_plot"]
        
        self.console.print("[bold]Plot Transformation Agent Output:[/bold]")
        self.console.print(f"  Total plot points: {len(transformed_plot)}")
        for plot_point in transformed_plot:
            self.console.print(f"  {plot_point['sequence']}. {plot_point['transformed_event']}")
        self.console.print()
        
        self.console.print("[cyan]Writing transformed story...[/cyan]")
        story_result = await self.story_writer.process({
            "world": transformed_world,
            "characters": transformed_characters,
            "plot": transformed_plot,
            "original_analysis": original_analysis,
            "creative_constraints": request.creative_constraints
        })
        self.console.print("✅ Story writing complete\n", style="green")
        
        final_story = story_result["story"]
        story_token_count = len(self.encoding.encode(final_story))
        story_word_count = len(final_story.split())
        
        self.console.print("[bold]Story Writer Agent Output:[/bold]")
        self.console.print(f"  Story length: {story_token_count:,} tokens / {story_word_count:,} words")
        self.console.print(f"  Preview: {final_story[:150]}...")
        if story_token_count < 9000:
            self.console.print(f"  [red]WARNING: Story is shorter than target (9,000-14,000 tokens)[/red]")
        elif story_token_count > 14000:
            self.console.print(f"  [yellow]WARNING: Story exceeds target (9,000-14,000 tokens)[/yellow]")
        else:
            self.console.print(f"  [green]✅ Within target range (9,000-14,000 tokens)[/green]")
        self.console.print()
        
        self.console.print("[cyan]Quality assurance check...[/cyan]")
        qa_result = await self.qa_agent.process({
            "original_analysis": original_analysis,
            "world": transformed_world,
            "characters": transformed_characters,
            "plot": transformed_plot,
            "story": final_story
        })
        self.console.print("✅ Quality assurance complete\n", style="green")
        
        evaluation = qa_result["evaluation"]
        
        self.console.print("[bold]Quality Assurance Agent Output:[/bold]")
        self.console.print(f"  Overall Score: {evaluation.get('overall_score', 'N/A')}/10")
        self.console.print(f"  Thematic Fidelity: {evaluation.get('thematic_fidelity_score', 'N/A')}/10")
        self.console.print(f"  Character Consistency: {evaluation.get('character_consistency_score', 'N/A')}/10")
        self.console.print(f"  World Coherence: {evaluation.get('world_coherence_score', 'N/A')}/10")
        self.console.print()
        
        result = TransformationResult(
            original_analysis=original_analysis,
            transformed_world=transformed_world,
            transformed_characters=transformed_characters,
            transformed_plot=transformed_plot,
            full_story=final_story,
            transformation_notes=evaluation["transformation_notes"],
            consistency_score=evaluation["overall_score"] / 10.0
        )
        
        return result
    
    def display_result(self, result: TransformationResult):
        token_count = len(self.encoding.encode(result.full_story))
        word_count = len(result.full_story.split())
        
        self.console.print("\n" + "="*80, style="bold blue")
        self.console.print("TRANSFORMATION COMPLETE", style="bold blue", justify="center")
        self.console.print("="*80 + "\n", style="bold blue")
        
        self.console.print(f"[bold]Original:[/bold] {result.original_analysis.title}")
        self.console.print(f"[bold]New World:[/bold] {result.transformed_world.name}")
        self.console.print(f"[bold]Story Length:[/bold] {token_count:,} tokens / {word_count:,} words\n")
        
        if token_count < 9000:
            self.console.print(f"[bold red]WARNING: Story is shorter than target (9,000-14,000 tokens)[/bold red]")
        elif token_count > 14000:
            self.console.print(f"[bold yellow]WARNING: Story exceeds target range (9,000-14,000 tokens)[/bold yellow]")
        else:
            self.console.print(f"[bold green]✅ Story length within target range (9,000-14,000 tokens)[/bold green]")
        
        self.console.print(f"\n[bold cyan]Consistency Score:[/bold cyan] {result.consistency_score:.1%}\n")
        
        self.console.print("[bold]Transformation Notes:[/bold]")
        for key, value in result.transformation_notes.items():
            self.console.print(f"  - {key.replace('_', ' ').title()}: {value}")
        
        self.console.print("\n" + "="*80 + "\n", style="bold blue")
        self.console.print("[bold green]TRANSFORMED STORY:[/bold green]\n")
        self.console.print(result.full_story)
        self.console.print("\n" + "="*80 + "\n", style="bold blue")
