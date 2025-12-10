<div align="center">

# Reimagine Movies

[![GitHub Stars](https://img.shields.io/github/stars/negativenagesh/Reimagine-movies?style=flat-square)](https://github.com/negativenagesh/Reimagine-movies/stargazers)
[![License](https://img.shields.io/github/license/negativenagesh/Reimagine-movies?style=flat-square)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11%2B-blue?style=flat-square)](pyproject.toml)
[![CI](https://img.shields.io/badge/CI-ready-success?style=flat-square)]()

AI-powered narrative transformation using a multi-agent microservice architecture. Transform classic stories into new worlds while preserving their core essence.

</div>

## Documentation

- **[Quick Start Guide](docs/QUICKSTART.md)** – Get running in minutes
- **[Project Summary](docs/PROJECT_SUMMARY.md)** – Executive overview
- **[Complete Solution Design](docs/SOLUTION.md)** – Full technical documentation
- **[Example Transformation](docs/EXAMPLE_TRANSFORMATION.md)** – Romeo & Juliet → AI Labs
- **[System Diagrams](docs/SYSTEM_DIAGRAM.md)** – Visual architecture
- **[File Listing](docs/FILE_LISTING.md)** – Complete project structure

## Overview

This system uses specialized AI agents to systematically transform narratives across contexts. Each agent handles a specific aspect of the transformation process, working together through a central orchestrator.

### System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                  Transformation Orchestrator                │
└─────────────────────────────────────────────────────────────┘
                           │
           ┌───────────────┼───────────────┐
           ▼               ▼               ▼
    ┌──────────┐    ┌──────────┐    ┌──────────┐
    │  Story   │───▶│  World   │───▶│Character │
    │ Analysis │    │ Builder  │    │ Mapping  │
    └──────────┘    └──────────┘    └──────────┘
           │               │               │
           └───────────────┼───────────────┘
                           ▼
                    ┌──────────┐
                    │   Plot   │
                    │Transform │
                    └──────────┘
                           │
           ┌───────────────┼───────────────┐
           ▼               ▼               ▼
    ┌──────────┐    ┌──────────┐    ┌──────────┐
    │  Story   │    │ Quality  │    │  Final   │
    │  Writer  │───▶│Assurance │───▶│  Result  │
    └──────────┘    └──────────┘    └──────────┘
```

## How It Works

The system **does NOT use movie subtitles**. Instead, it works from:
- Public domain story synopses and plot summaries
- Structured knowledge about narrative patterns (Hero's Journey, character archetypes)
- Transformation examples and world-building templates
- Few-shot learning with carefully crafted prompts

### Agent Pipeline

1. **Story Analysis Agent** (`temperature=0.3`)
   - Extracts core themes, character archetypes, plot structure
   - Identifies emotional beats and narrative functions
   - Maps story to universal patterns (Hero's Journey, three-act structure)

2. **World Builder Agent** (`temperature=0.8`)
   - Creates internally consistent alternate reality
   - Defines rules, technology, social structures
   - Ensures world can support original story's conflicts in new form

3. **Character Mapping Agent** (`temperature=0.6`)
   - Transforms characters while preserving archetypes
   - Adapts motivations to new context
   - Maintains relationship dynamics

4. **Plot Transformation Agent** (`temperature=0.7`)
   - Reimagines events to fit new world
   - Preserves narrative function and emotional weight
   - Maintains cause-effect relationships

5. **Story Writer Agent** (`temperature=0.85`)
   - Synthesizes all elements into cohesive narrative
   - Uses vivid prose appropriate to new setting
   - Balances showing vs. telling

6. **Quality Assurance Agent** (`temperature=0.2`)
   - Validates thematic fidelity
   - Checks consistency and coherence
   - Scores transformation quality

## Installation

### Prerequisites
- Python 3.11+
- OpenAI API key
- `uv` Python package manager (fast environment + installs)

### Setup (using uv)

```bash
cd Reimagine-movies

uv init
uv venv
source .venv/bin/activate

uv sync

touch .env
```

Edit `.env` and add your OpenAI API key:
```
OPENAI_API_KEY=sk-your-key-here
```

## Usage

### Command Line Interface

#### Run Example Transformation
```bash
uv run main.py --example
```

Transforms Romeo and Juliet into a Silicon Valley AI labs rivalry.

#### Transform a Predefined Story
```bash
uv run main.py \
  --story-name DRACULA \
  --target-world "Modern cybersecurity landscape where a mysterious hacker collective drains companies" \
  --output dracula_cyber.txt
```

#### List Available Stories
```bash
uv run main.py --list-stories
```

#### Custom Story Transformation
```bash
uv run main.py \
  --custom-story "Your story text here..." \
  --target-world "Description of target world" \
  --maintain "element1" "element2" \
  --constraints "no magic" "realistic tech" \
  --output my_transformation.txt
```

### API Server

Start the FastAPI server:
```bash
uv run main.py --api
```

Access at `http://localhost:8000`

#### API Endpoints

- `GET /` - Health check
- `GET /source-stories` - List available stories
- `GET /source-stories/{name}` - Get specific story
- `POST /transform` - Transform a story
- `GET /knowledge-base/archetypes` - Get character archetypes
- `GET /knowledge-base/narrative-patterns` - Get narrative patterns
- `GET /knowledge-base/examples` - Get transformation examples

#### Example API Usage

```python
import requests

response = requests.post("http://localhost:8000/transform", json={
    "source_story": "Story text here...",
    "target_world_description": "A cyberpunk megacity in 2077",
    "maintain_elements": ["themes of revenge", "character arc"],
    "creative_constraints": ["grounded in technology", "no deus ex machina"]
})

result = response.json()
print(result["full_story"])
```

## Project Structure

```
Reimagine-movies/
├── main.py                      # CLI entry point
├── pyproject.toml              # Dependencies
├── src/
│   ├── models/
│   │   └── domain.py           # Pydantic models
│   ├── agents/
│   │   ├── base.py            # Base agent class
│   │   ├── story_analysis_agent.py
│   │   ├── world_builder_agent.py
│   │   ├── character_mapping_agent.py
│   │   ├── plot_transformation_agent.py
│   │   ├── story_writer_agent.py
│   │   └── qa_agent.py
│   ├── orchestrator.py         # Agent coordination
│   └── api.py                  # FastAPI service
├── data/
│   ├── source_stories.yaml     # Story database
│   └── knowledge_base.yaml     # Narrative patterns & examples
├── output/                     # Generated stories
└── docs/
    └── architecture.mermaid    # System diagram
```

## Design Decisions

### Microservice Architecture
Each agent is independent and communicates through message passing. This allows:
- Parallel development and testing
- Independent scaling of agents
- Easy addition of new agent types
- Clear separation of concerns

### Agent Roles, I/O, and Communication

The system coordinates six specialized agents via the `TransformationOrchestrator`. Each agent exposes a `process(payload)` method and returns structured JSON conforming to Pydantic models in `src/models/domain.py`. The orchestrator passes outputs downstream, ensuring type-safe handoffs.

- Story Analysis Agent (`src/agents/story_analysis_agent.py`)
   - Role: Extracts story semantics — title, core theme, moral, emotional journey, character archetypes, narrative structure, and plot points.
   - Input: `{ source_story: string }`
   - Output: `{ analysis: StoryAnalysis }`
   - Downstream: Feeds `analysis` to World Builder and later to Story Writer and QA.

- World Builder Agent (`src/agents/world_builder_agent.py`)
   - Role: Constructs an alternate world with consistent rules, tech level, social structure, norms, constraints, and power dynamics.
   - Input: `{ target_world_description: string, original_analysis: StoryAnalysis }`
   - Output: `{ world: World }`
   - Downstream: Provides `world` to Character Mapping, Plot Transformation, and Story Writer.

- Character Mapping Agent (`src/agents/character_mapping_agent.py`)
   - Role: Translates original characters to the new world while preserving archetypes, core traits, motivations, and relationships.
   - Input: `{ original_characters: Character[], world: World }`
   - Output: `{ transformed_characters: Character[] }`
   - Downstream: Supplies `transformed_characters` to Plot Transformation and Story Writer.

- Plot Transformation Agent (`src/agents/plot_transformation_agent.py`)
   - Role: Reimagines plot points to fit the new world, preserving sequence, stakes, emotional weight, and narrative function.
   - Input: `{ plot_points: PlotPoint[], world: World, transformed_characters: Character[] }`
   - Output: `{ transformed_plot: PlotPoint[] }`
   - Downstream: Provides `transformed_plot` to the Story Writer.

- Story Writer Agent (`src/agents/story_writer_agent.py`)
   - Role: Synthesizes world, characters, and plot into a full-length narrative targeting 9,000–14,000 tokens.
   - Input: `{ world: World, characters: Character[], plot: PlotPoint[], original_analysis: StoryAnalysis }`
   - Output: `{ story: string }`
   - Downstream: Supplies `story` to QA and final result composition.

- Quality Assurance Agent (`src/agents/qa_agent.py`)
   - Role: Evaluates thematic fidelity, character consistency, and world coherence; produces notes and a quantitative score.
   - Input: `{ original_analysis: StoryAnalysis, world: World, characters: Character[], plot: PlotPoint[], story: string }`
   - Output: `{ evaluation: { overall_score: number, transformation_notes: Dict, ... } }`
   - Downstream: Combined into the `TransformationResult` for display and serialization.

### Orchestrator Flow and Message Passing
- The `TransformationOrchestrator` (`src/orchestrator.py`) invokes agents in sequence, prints their outputs, and computes token/word counts.
- All inter-agent communications are via structured dict payloads, validated against Pydantic models at result assembly.
- The orchestrator reports warnings when story length is outside the 9k–14k token target and surfaces QA notes.
- CLI and API consume the orchestrator, and `main.py` handles saving results to text or Markdown with computed metadata.

### Multi-Agent Approach
Different agents with different temperatures optimize for different goals:
- Analysis agents (low temp) → precise extraction
- Creative agents (high temp) → novel combinations
- QA agents (low temp) → objective evaluation

### Prompt Engineering Strategy
- **Structured outputs**: JSON schema enforcement for consistency
- **Few-shot learning**: Examples in knowledge base
- **Chain of thought**: Sequential refinement through pipeline
- **Context preservation**: Rich context passed between agents

### Why Not Subtitles?
Subtitles capture dialogue but miss:
- Narrative structure and pacing
- Character arcs and motivations
- Thematic elements and symbols
- Visual storytelling

Our approach uses plot summaries that capture these essential elements.

## Evaluation Criteria Addressed

### System Thinking
- Abstracted transformation into reusable agent pipeline
- Each agent handles one concern
- Orchestrator manages coordination
- Knowledge base provides reusable patterns

### Technical Execution
- Clean, modular code
- Type-safe with Pydantic models
- Scalable microservice architecture
- RESTful API design

### AI Engineering
- Temperature tuning per agent role
- Structured output with JSON schema
- Few-shot examples in knowledge base
- Chain-of-thought through pipeline

### Problem Decomposition
- 6 specialized agents
- Clear interfaces between components
- Separation of analysis, generation, validation
- Reusable knowledge base

### Bias Toward Action
- Working demo with example
- Multiple interfaces (CLI, API)
- Predefined stories for quick testing
- Complete end-to-end system

### Ownership & Innovation
**Clever addition**: Quality Assurance Agent that:
- Validates thematic fidelity automatically
- Provides quantitative consistency scores
- Identifies strengths and weaknesses
- Enables iterative refinement

This addition wasn't in the original requirements but adds:
- Objective quality measurement
- Debugging capability
- Trust in transformations
- Foundation for auto-improvement

## Challenges & Mitigations

### Challenge: Maintaining Thematic Fidelity
**Solution**: Dedicated analysis agent extracts core themes before transformation. QA agent validates theme preservation.

### Challenge: World Coherence
**Solution**: World Builder creates comprehensive rule set. Plot Transformer must respect these constraints.

### Challenge: Creative vs. Faithful
**Solution**: Separate agents for analysis (faithful) and creation (creative) with different temperatures.

### Challenge: Consistency Across Long Narratives
**Solution**: Structured data models passed between agents maintain context. QA agent catches inconsistencies.

### Challenge: Reproducibility
**Solution**: Temperature settings, structured prompts, and JSON schemas ensure consistent outputs.

## Future Improvements

### Scale to Full Product
1. **Iterative Refinement**: Loop feedback from QA agent back to Story Writer
2. **User Feedback Loop**: Learn from human preferences
3. **Multi-Model Support**: Compare GPT-4, Claude, Gemini outputs
4. **Caching Layer**: Redis for intermediate results
5. **Batch Processing**: Transform multiple stories in parallel
6. **Web Interface**: Interactive UI for exploration
7. **Version Control**: Track transformation history
8. **A/B Testing**: Compare transformation strategies

### Enhanced Features
- Character dialogue generation
- Scene-by-scene breakdown
- Multiple ending variations
- Interactive story branching
- Visual style suggestions
- Soundtrack recommendations

### Production Readiness
- Authentication & authorization
- Rate limiting
- Monitoring & observability
- Error recovery
- Model fine-tuning
- Cost optimization

## Example Transformations

### Romeo and Juliet → Silicon Valley AI Labs
- Feuding families → Rival tech companies
- Star-crossed lovers → Engineers from competing firms
- Poison → Malicious code
- Death → Career destruction and blacklisting

### Dracula → Silicon Valley VC
- Vampire → Predatory investor
- Blood-sucking → Equity extraction
- Transylvania → Exclusive investor compound
- Stakes → SEC regulations

### Odyssey → Deep Space Mission
- Journey home → Navigation through space
- Cyclops → Hostile alien entity
- Sirens → Malicious AI signals
- Ithaca → Home space station

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contact

For questions about this system's design or implementation, see the code and documentation.
