from typing import Dict, Any
from .base import BaseAgent
from src.models.domain import StoryAnalysis, Character, PlotPoint, NarrativeStructure, CharacterArchetype, ConflictType


class StoryAnalysisAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="StoryAnalysisAgent", temperature=0.3)
    
    def get_system_prompt(self) -> str:
        return """You are an expert literary analyst specializing in narrative structure and storytelling patterns.
Your task is to deeply analyze stories and extract their core structural elements, themes, character archetypes, 
and narrative patterns. You understand the hero's journey, three-act structure, character arcs, and universal 
storytelling elements.

Focus on identifying:
- Core themes and moral lessons that transcend context
- Character archetypes and their narrative functions
- Plot structure and key turning points
- Emotional journey and stakes
- Symbols and their meanings
- Conflict types and their resolution patterns

Be precise and systematic. Extract the essence that makes the story work, not just surface details."""
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        source_story = input_data["source_story"]
        
        prompt = f"""Analyze this story comprehensively: {source_story}

Provide a complete structural analysis in valid JSON format with these exact keys:
{{
    "title": "story title",
    "core_theme": "the universal theme",
    "moral_lesson": "the lesson or message",
    "emotional_journey": "the emotional arc",
    "characters": [
        {{
            "name": "character name",
            "archetype": "hero|mentor|ally|guardian|trickster|shapeshifter|shadow|herald",
            "core_traits": ["trait1", "trait2"],
            "motivations": ["motivation1", "motivation2"],
            "relationships": {{"character": "relationship type"}},
            "arc_description": "how they change"
        }}
    ],
    "narrative_structure": {{
        "act_one": ["setup point 1", "setup point 2"],
        "act_two": ["complication 1", "complication 2"],
        "act_three": ["resolution 1", "resolution 2"],
        "inciting_incident": "what starts the story",
        "midpoint": "the major turning point",
        "climax": "the peak conflict",
        "resolution": "how it ends"
    }},
    "primary_conflict": "man_vs_man|man_vs_self|man_vs_society|man_vs_nature|man_vs_technology|man_vs_fate",
    "secondary_conflicts": ["conflict type 1", "conflict type 2"],
    "key_symbols": ["symbol1", "symbol2"],
    "plot_points": [
        {{
            "sequence": 1,
            "original_event": "what happens",
            "emotional_weight": "high|medium|low",
            "narrative_function": "its purpose in the story",
            "stakes": "what's at risk"
        }}
    ]
}}

Make sure to include at least 8-10 major plot points that capture the story's progression."""
        
        analysis_data = self.call_llm_json(prompt, max_tokens=6000)
        
        return {
            "analysis": analysis_data,
            "agent": self.name
        }
