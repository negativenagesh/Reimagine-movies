from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Literal
from enum import Enum


class CharacterArchetype(str, Enum):
    HERO = "hero"
    MENTOR = "mentor"
    ALLY = "ally"
    GUARDIAN = "guardian"
    TRICKSTER = "trickster"
    SHAPESHIFTER = "shapeshifter"
    SHADOW = "shadow"
    HERALD = "herald"
    VICTIM = "victim"
    LOVER = "lover"
    INNOCENT = "innocent"
    EXPLORER = "explorer"
    REBEL = "rebel"
    CREATOR = "creator"
    CAREGIVER = "caregiver"
    SAGE = "sage"


class ConflictType(str, Enum):
    MAN_VS_MAN = "man_vs_man"
    MAN_VS_SELF = "man_vs_self"
    MAN_VS_SOCIETY = "man_vs_society"
    MAN_VS_NATURE = "man_vs_nature"
    MAN_VS_TECHNOLOGY = "man_vs_technology"
    MAN_VS_FATE = "man_vs_fate"


class Character(BaseModel):
    name: str
    archetype: CharacterArchetype
    core_traits: List[str]
    motivations: List[str]
    relationships: Dict[str, str] = Field(default_factory=dict)
    arc_description: str
    transformed_name: Optional[str] = None
    transformed_role: Optional[str] = None


class World(BaseModel):
    name: str
    era: str
    technology_level: str
    social_structure: str
    key_rules: List[str]
    cultural_norms: List[str]
    power_dynamics: str
    constraints: List[str]


class PlotPoint(BaseModel):
    sequence: int
    original_event: str
    emotional_weight: str
    narrative_function: str
    transformed_event: Optional[str] = None
    stakes: str


class NarrativeStructure(BaseModel):
    act_one: List[str]
    act_two: List[str]
    act_three: List[str]
    inciting_incident: str
    midpoint: str
    climax: str
    resolution: str


class StoryAnalysis(BaseModel):
    title: str
    core_theme: str
    moral_lesson: str
    emotional_journey: str
    characters: List[Character]
    narrative_structure: NarrativeStructure
    primary_conflict: ConflictType
    secondary_conflicts: List[ConflictType]
    key_symbols: List[str]
    plot_points: List[PlotPoint]


class TransformationRequest(BaseModel):
    source_story: str
    target_world_description: str
    maintain_elements: List[str] = Field(default_factory=list)
    creative_constraints: List[str] = Field(default_factory=list)


class TransformationResult(BaseModel):
    original_analysis: StoryAnalysis
    transformed_world: World
    transformed_characters: List[Character]
    transformed_plot: List[PlotPoint]
    full_story: str
    transformation_notes: Dict[str, str]
    consistency_score: float


class AgentMessage(BaseModel):
    agent_name: str
    message_type: Literal["request", "response", "error"]
    content: Dict
    metadata: Dict = Field(default_factory=dict)
