from typing import Dict, Any
from .base import BaseAgent


class QualityAssuranceAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="QualityAssuranceAgent", temperature=0.2)
    
    def get_system_prompt(self) -> str:
        return """You are a rigorous quality assurance specialist for narrative transformations.
You evaluate transformations on multiple dimensions:

1. Thematic Fidelity: Does it preserve the core theme and moral?
2. Structural Integrity: Does the plot structure remain sound?
3. Character Consistency: Do characters maintain their essence?
4. World Coherence: Does everything make sense in the new world?
5. Emotional Authenticity: Does it capture the same emotional journey?
6. Creative Success: Is it genuinely reimagined, not just reskinned?

Be critical but fair. Identify both strengths and weaknesses. Provide actionable feedback."""
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        original_analysis = input_data["original_analysis"]
        world = input_data["world"]
        characters = input_data.get("characters") or input_data.get("transformed_characters")
        plot = input_data.get("plot") or input_data.get("transformed_plot")
        story = input_data["story"]
        
        prompt = f"""Evaluate this narrative transformation:

ORIGINAL:
- Title: {original_analysis['title']}
- Theme: {original_analysis['core_theme']}
- Moral: {original_analysis['moral_lesson']}
- Characters: {len(original_analysis['characters'])} character archetypes
- Plot Points: {len(original_analysis['plot_points'])} major events

TRANSFORMATION:
- New World: {world['name']} ({world['era']})
- Transformed Characters: {len(characters)}
- Transformed Plot Points: {len(plot)}

FINAL STORY (excerpt):
{story[:1000]}...

Evaluate on these criteria (score 0-10 for each):
1. Thematic Fidelity - preserves core theme/moral
2. Structural Integrity - maintains plot structure
3. Character Consistency - preserves character essences
4. World Coherence - new world logic holds
5. Emotional Authenticity - captures same feelings
6. Creative Reimagining - truly transformed, not just renamed

Also check for:
- Logical inconsistencies
- Thematic drift
- Character behavior mismatches
- World rule violations
- Lost narrative elements

Provide response in JSON:
{{
    "scores": {{
        "thematic_fidelity": 0-10,
        "structural_integrity": 0-10,
        "character_consistency": 0-10,
        "world_coherence": 0-10,
        "emotional_authenticity": 0-10,
        "creative_reimagining": 0-10
    }},
    "overall_score": 0-10,
    "strengths": ["strength1", "strength2"],
    "weaknesses": ["weakness1", "weakness2"],
    "recommendations": ["recommendation1", "recommendation2"],
    "consistency_issues": ["issue1", "issue2"],
    "transformation_notes": {{
        "best_adaptation": "what worked best",
        "most_creative": "most creative element",
        "needs_work": "what could improve"
    }}
}}"""
        
        evaluation = self.call_llm_json(prompt, max_tokens=3000)
        
        return {
            "evaluation": evaluation,
            "agent": self.name
        }
