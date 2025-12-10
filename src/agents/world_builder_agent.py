from typing import Dict, Any
from .base import BaseAgent
from src.models.domain import World


class WorldBuilderAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="WorldBuilderAgent", temperature=0.8)
    
    def get_system_prompt(self) -> str:
        return """You are a world-building expert who creates rich, internally consistent alternate realities.
Your expertise spans different eras, cultures, technologies, and social structures. You understand how to 
create worlds that feel lived-in and have their own logic.

When building a world, consider:
- Historical/temporal context and how it shapes society
- Technology level and its societal implications
- Power structures and hierarchies
- Cultural norms and taboos
- Physical and social constraints
- How conflicts naturally arise from the world's rules
- Economic systems and resource distribution
- Communication methods and information flow

Create worlds that are specific enough to be believable but flexible enough to support narrative transformation.
The world should create natural parallels to the original story's conflicts while feeling authentic to its own logic."""
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        target_description = input_data["target_world_description"]
        original_analysis = input_data.get("original_analysis", {})
        
        prompt = f"""Create a detailed world based on this description: {target_description}

Consider the original story's themes and conflicts:
- Core theme: {original_analysis.get('core_theme', 'N/A')}
- Primary conflict: {original_analysis.get('primary_conflict', 'N/A')}
- Key symbols: {original_analysis.get('key_symbols', [])}

Build a world that can naturally support these thematic elements in a new context.

Provide the world details in valid JSON format:
{{
    "name": "world name",
    "era": "time period or setting era",
    "technology_level": "detailed description of technology",
    "social_structure": "how society is organized",
    "key_rules": ["rule1", "rule2", "rule3"],
    "cultural_norms": ["norm1", "norm2", "norm3"],
    "power_dynamics": "who has power and why",
    "constraints": ["what limits exist", "what's forbidden", "what's impossible"]
}}

Make the world detailed and specific. Include at least 5 key rules and 5 cultural norms."""
        
        world_data = self.call_llm_json(prompt, max_tokens=3000)
        
        return {
            "world": world_data,
            "agent": self.name
        }
