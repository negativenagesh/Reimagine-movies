from typing import Dict, Any
from .base import BaseAgent

class PlotTransformationAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="PlotTransformationAgent", temperature=0.7)
    
    def get_system_prompt(self) -> str:
        return """You are an expert at adapting plot events across different contexts while maintaining 
narrative structure and emotional impact.

When transforming plot points:
- Preserve the narrative function of each event
- Maintain emotional weight and stakes
- Adapt conflicts to fit the new world's logic
- Keep cause-and-effect relationships intact
- Ensure events arise naturally from the world's rules
- Preserve dramatic tension and pacing
- Transform symbols into context-appropriate equivalents

Each transformed event should feel inevitable in the new world while serving the same story purpose."""
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        plot_points = input_data["plot_points"]
        world = input_data["world"]
        characters = input_data["transformed_characters"]
        
        character_map = {c['name']: c['transformed_name'] for c in characters}
        
        transformed_plot = []
        
        prompt = f"""Transform these plot points for the new world context:

World: {world['name']} ({world['era']})
Technology: {world['technology_level']}
Social Structure: {world['social_structure']}
Key Rules: {', '.join(world['key_rules'])}
Constraints: {', '.join(world['constraints'])}

Characters in new world:
{chr(10).join([f"- {old} → {new}: {c['transformed_role']}" for old, new, c in [(c['name'], c['transformed_name'], c) for c in characters]])}

Original Plot Points:
{chr(10).join([f"{i+1}. {p['original_event']} (Function: {p['narrative_function']}, Stakes: {p['stakes']})" for i, p in enumerate(plot_points)])}

Transform each plot point to fit the new world. Maintain:
- The same sequence and causal relationships
- Equivalent emotional weight
- The narrative function
- Stakes that matter in the new context

Return JSON format:
{{
    "transformed_plot": [
        {{
            "sequence": 1,
            "original_event": "original event",
            "emotional_weight": "high|medium|low",
            "narrative_function": "purpose in story",
            "transformed_event": "detailed event in new world context",
            "stakes": "what's at risk in new context"
        }}
    ]
}}

Make each transformed event specific, vivid, and grounded in the new world's reality."""
        
        result = self.call_llm_json(prompt, max_tokens=6000)
        
        return {
            "transformed_plot": result["transformed_plot"],
            "agent": self.name
        }
