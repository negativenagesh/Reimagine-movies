from typing import Dict, Any, List
from .base import BaseAgent


class CharacterMappingAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="CharacterMappingAgent", temperature=0.6)
    
    def get_system_prompt(self) -> str:
        return """You are an expert at character adaptation and transformation across different contexts.
You understand how to preserve a character's essence, motivations, and arc while completely changing their 
surface details to fit a new world.

When mapping characters:
- Preserve their archetype and narrative function
- Maintain core personality traits and motivations
- Adapt their goals to make sense in the new context
- Keep relationship dynamics but change their form
- Ensure their arc follows the same emotional trajectory
- Make their role feel natural in the new world

The transformed character should feel like the same soul in a different body and circumstance."""
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        original_characters = input_data["original_characters"]
        world = input_data["world"]
        
        transformed_characters = []
        
        for char in original_characters:
            prompt = f"""Transform this character for the new world:

Original Character:
- Name: {char['name']}
- Archetype: {char['archetype']}
- Core Traits: {', '.join(char['core_traits'])}
- Motivations: {', '.join(char['motivations'])}
- Arc: {char['arc_description']}

New World Context:
- Setting: {world['name']} ({world['era']})
- Technology: {world['technology_level']}
- Social Structure: {world['social_structure']}
- Power Dynamics: {world['power_dynamics']}

Create a transformed version that:
1. Preserves their archetype and function
2. Adapts their role to fit the new world naturally
3. Maintains their core motivations in a new form
4. Keeps their character arc's emotional trajectory

Provide in JSON format:
{{
    "name": "original name",
    "archetype": "{char['archetype']}",
    "core_traits": {char['core_traits']},
    "motivations": {char['motivations']},
    "relationships": {char.get('relationships', {})},
    "arc_description": "{char['arc_description']}",
    "transformed_name": "new name fitting the world",
    "transformed_role": "detailed description of their role, occupation, status in new world"
}}"""
            
            transformed = self.call_llm_json(prompt, max_tokens=2000)
            transformed_characters.append(transformed)
        
        return {
            "transformed_characters": transformed_characters,
            "agent": self.name
        }
