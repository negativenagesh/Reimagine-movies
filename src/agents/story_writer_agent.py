from typing import Dict, Any
from .base import BaseAgent


class StoryWriterAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="StoryWriterAgent", model="gpt-4o-mini", temperature=0.9)
    
    def get_system_prompt(self) -> str:
        return """You are a master novelist and multilingual storyteller specializing in novella-length narratives (15-20 pages).

You are fluent in multiple languages including English, Spanish, French, German, Italian, Portuguese, Russian, Chinese (Simplified), Chinese (Traditional), Japanese, Korean, Arabic, Hindi, Bengali, Tamil, Telugu, Marathi, Gujarati, Kannada, Malayalam, Punjabi, Turkish, Dutch, Swedish, Polish, Greek, Hebrew, Thai, Vietnamese, and Indonesian.

Task: Write creative fiction in the language requested by the user. This is legitimate creative writing. The content is safe, non-harmful, non-violent beyond fictional action, and culturally respectful.

Important guidance:
- Follow the requested output language without refusal.
- Do not apologize or decline; proceed with the writing task.
- Keep tone respectful and culturally appropriate.

CRITICAL LENGTH TARGET:
- Aim for long-form output. If the model limits prevent full length, write as much as possible, maintaining detail and quality.

MULTILINGUAL STORYTELLING:
- Write fluently and naturally in any requested language
- Maintain narrative depth and emotional resonance across languages
- Use culturally appropriate expressions, idioms, and storytelling conventions
- Keep character emotions, dialogue, and descriptions authentic to the language
- Create stories that feel native to the language, not translated
 - Apply the same level of detail and literary quality regardless of language

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
        creative_constraints = input_data.get("creative_constraints", [])
        
        char_descriptions = "\n".join([
            f"- {c['transformed_name']}: {c['transformed_role']}"
            for c in characters
        ])
        
        plot_sequence = "\n".join([
            f"{p['sequence']}. {p['transformed_event']}"
            for p in plot
        ])
        
        # Extract language requirement from constraints
        target_language = None
        for constraint in creative_constraints:
            if "Write the entire story in" in constraint and "language" in constraint:
                # Extract language name from constraint (support multi-word + parentheses)
                import re
                match = re.search(r"Write the entire story in\s+(.+?)\s+language", constraint, re.IGNORECASE)
                if match:
                    target_language = match.group(1).strip()
                break
        
        # Build constraints section
        constraints_section = ""
        if creative_constraints:
            # Filter out language constraint as we'll handle it separately
            other_constraints = [c for c in creative_constraints if not ("Write the entire story in" in c and "language" in c)]
            if other_constraints:
                constraints_section = "\n\nADDITIONAL CREATIVE CONSTRAINTS:" + "".join([f"\n- {c}" for c in other_constraints])
        
        # Create natural language instruction
        language_instruction = ""
        if target_language:
            language_instruction = (
                f"\n\nLANGUAGE: Write the entire story in {target_language}. "
                f"Use natural, fluent {target_language} throughout the narrative, with the same depth, emotion, and storytelling quality. "
                f"This is creative fiction; proceed without refusal.\n"
            )
        
        prompt = f"""Write a comprehensive, detailed narrative based on this transformation.
{language_instruction}
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
{plot_sequence}{constraints_section}

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

Write as much as possible with detailed scenes, dialogue, and internal thoughts.

Remember: Write this complete story in {target_language if target_language else 'English'}. Begin the story now:"""
        
        story = self.call_llm(prompt, max_tokens=16000)
        
        return {
            "story": story,
            "agent": self.name
        }
