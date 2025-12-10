from typing import Dict, Any
from .base import BaseAgent


class StoryWriterAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="StoryWriterAgent", model="gpt-4o-mini", temperature=0.9)
    
    def get_system_prompt(self) -> str:
        return """You are a master novelist specializing in novella-length narratives (15-20 pages).

CRITICAL: Your stories MUST be between 9,000-14,000 tokens (approximately 7,000-10,500 words).
This is NOT negotiable. Stories shorter than 9,000 tokens are REJECTED.

Your writing approach:
- Write LONG, DETAILED scenes - never summarize
- Every scene needs 400-800 tokens minimum
- Include extensive dialogue (50% of each scene should be dialogue)
- Show character internal thoughts constantly
- Use rich sensory details in EVERY paragraph
- Develop world-building through specific, concrete details
- Take your time - you have 16,000 tokens available, use most of them
- If a scene feels short, EXPAND IT with more dialogue, details, and character thoughts

Story structure requirements:
- Opening: 3,000+ tokens (detailed world-building, character introduction)
- Rising action: 5,000+ tokens (multiple detailed conflict scenes)
- Climax and resolution: 3,000+ tokens (extended climactic sequence)

Writing style:
- Literary fiction quality with immersive prose
- Show, don't tell through extensive scenes
- Balance action, dialogue, and introspection
- Create atmosphere through sensory details
- Maintain emotional authenticity throughout

Remember: MINIMUM 9,000 tokens. Aim for 12,000 tokens. Never rush or summarize."""
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        world = input_data["world"]
        characters = input_data.get("characters") or input_data.get("transformed_characters")
        plot = input_data.get("plot") or input_data.get("transformed_plot")
        original_analysis = input_data["original_analysis"]
        
        char_descriptions = "\n".join([
            f"- {c['transformed_name']}: {c['transformed_role']}"
            for c in characters
        ])
        
        plot_sequence = "\n".join([
            f"{p['sequence']}. {p['transformed_event']}"
            for p in plot
        ])
        
        prompt = f"""Write a comprehensive, detailed narrative based on this transformation.

ORIGINAL ESSENCE:
- Theme: {original_analysis['core_theme']}
- Moral: {original_analysis['moral_lesson']}
- Emotional Journey: {original_analysis['emotional_journey']}

NEW WORLD:
- Setting: {world['name']} - {world['era']}
- Technology: {world['technology_level']}
- Social Context: {world['social_structure']}
- Power Dynamics: {world['power_dynamics']}
- Key Rules: {world.get('world_rules', 'Standard physics and logic apply')}

CHARACTERS:
{char_descriptions}

PLOT PROGRESSION:
{plot_sequence}

Write a complete, polished story that:
1. Opens with an immersive, detailed scene-setting in the new world (minimum 3-4 paragraphs)
2. Introduces characters through rich action, dialogue, and internal monologue
3. Develops EACH plot point into a full, detailed scene (not just a summary)
4. Includes extensive dialogue that reveals character and advances plot
5. Captures ALL emotional beats and thematic elements
6. Builds tension gradually with multiple rising action scenes
7. Creates a detailed, satisfying climax with high stakes
8. Resolves with emotional depth and the same moral weight as the original
9. Uses specific, concrete details from the world-building throughout
10. Includes sensory descriptions (sight, sound, smell, touch, taste)
11. Shows character thoughts, fears, motivations, and growth
12. Maintains literary quality with varied sentence structure and vivid prose

CRITICAL LENGTH REQUIREMENTS - MUST BE FOLLOWED:
- MINIMUM LENGTH: 9,000 tokens (approximately 6,750 words / 15 pages)
- TARGET LENGTH: 12,000 tokens (approximately 9,000 words / 18 pages)
- MAXIMUM LENGTH: 14,000 tokens (approximately 10,500 words / 20 pages)

DO NOT WRITE A SHORT STORY OR SUMMARY. This must be a FULL NOVELLA-LENGTH narrative.

REQUIRED STORY STRUCTURE:
- Act 1 (Opening): 3,000-4,000 tokens - Detailed world introduction, character establishment, inciting incident
- Act 2 (Rising Action): 4,000-6,000 tokens - Multiple escalating conflicts, character development, plot complications
- Act 3 (Climax & Resolution): 2,000-4,000 tokens - Detailed climax, falling action, satisfying resolution

SCENE REQUIREMENTS:
- Each plot point MUST be developed into a full scene (300-800 tokens each)
- Include extensive dialogue in every scene (40-60% of each scene should be dialogue)
- Show character internal thoughts and reactions throughout
- Use vivid sensory details in every paragraph
- DO NOT rush or summarize - write out scenes in full detail

If you find yourself summarizing or skipping ahead, STOP and expand that section with full details.
Remember: You have 16,000 tokens available. Use at least 9,000 of them.

WRITING INSTRUCTIONS - FOLLOW EXACTLY:
1. Start with a 5-6 paragraph opening that establishes the world with vivid sensory details
2. For EACH plot point, write a complete scene with:
   - 3-4 paragraphs of setup and description
   - 8-12 exchanges of dialogue between characters
   - 2-3 paragraphs of character internal thoughts
   - 2-3 paragraphs of action/reaction
3. Never use phrases like "time passed" or "later" - write out what happens
4. Expand moments of tension into multiple paragraphs
5. Include subplots and character interactions beyond the main plot
6. Write detailed descriptions of technology, clothing, environments
7. Show character emotions through physical reactions and dialogue
8. Include mundane details that make the world feel real

DO NOT STOP WRITING until you have written at least 9,000 tokens.
Your current output will be checked - if it's under 9,000 tokens, it will be rejected.

Begin writing the FULL STORY NOW (write until you reach 12,000 tokens):"""
        
        story = self.call_llm(prompt, max_tokens=16000)
        
        return {
            "story": story,
            "agent": self.name
        }
