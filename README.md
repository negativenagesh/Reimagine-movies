<div align="center">

# Reimagine Movies

[![GitHub Stars](https://img.shields.io/github/stars/negativenagesh/Reimagine-movies?style=flat-square)](https://github.com/negativenagesh/Reimagine-movies/stargazers)
[![License](https://img.shields.io/github/license/negativenagesh/Reimagine-movies?style=flat-square)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11%2B-blue?style=flat-square)](pyproject.toml)
[![CI](https://img.shields.io/badge/CI-ready-success?style=flat-square)]()
</div>

**Demo:** Click to preview a sample transformation video

[▶️ Demo1 – KGF Chapter 1 reimagined into Vedic Era (English)](Demo/Demo1-KGF_Chapter1-VedicEra_English.mov)

<div align="center">
   <video src="Demo/Demo1-KGF_Chapter1-VedicEra_English.mov" controls preload="metadata" style="max-width: 100%; height: auto;">
      Your browser does not support the video tag.
   </video>
</div>

AI-powered narrative transformation using a multi-agent microservice architecture. Reimagine movies into entirely different worlds while preserving their core essence. The system can also transform predefined classic stories from the data folder. Using specialized multi-agents, it systematically transforms narratives across contexts. Each agent handles a specific aspect of the transformation process, working together through a central orchestrator.

<div align="center">

```
                    ┌──────────────────────────────────────────────────────────────┐
                    │          TRANSFORMATION ORCHESTRATOR                         │
                    │   (Coordinates agent pipeline, validates outputs,            │
                    │    computes metrics, passes structured data)                 │
                    └──────────────────────────────────────────────────────────────┘
                                            │
                                            │ Source Story
                                            ▼
                    ┌──────────────────────────────────────────────────────────────┐
                    │         1. STORY ANALYSIS AGENT (temp=0.3)                   │
                    │   Extracts: themes, archetypes, plot structure,              │
                    │   emotional beats, narrative patterns (Hero's Journey)       │
                    └──────────────────────────────────────────────────────────────┘
                                            │
                                            │ StoryAnalysis
                                            ▼
                    ┌──────────────────────────────────────────────────────────────┐
                    │         2. WORLD BUILDER AGENT (temp=0.8)                    │
                    │   Creates: alternate world with rules, tech level,           │
                    │   social structures, norms, power dynamics                   │
                    └──────────────────────────────────────────────────────────────┘
                                            │
                                            │ World + StoryAnalysis
                                            ▼
                    ┌──────────────────────────────────────────────────────────────┐
                    │         3. CHARACTER MAPPING AGENT (temp=0.6)                │
                    │   Transforms: characters preserving archetypes,              │
                    │   core traits, motivations, relationship dynamics            │
                    └──────────────────────────────────────────────────────────────┘
                                            │
                                            │ Characters + World
                                            ▼
                    ┌──────────────────────────────────────────────────────────────┐
                    │         4. PLOT TRANSFORMATION AGENT (temp=0.7)              │
                    │   Reimagines: plot points for new world,                     │
                    │   preserves narrative function, emotional weight, causality  │
                    └──────────────────────────────────────────────────────────────┘
                                            │
                                            │ Plot + Characters + World
                                            ▼
                    ┌──────────────────────────────────────────────────────────────┐
                    │         5. STORY WRITER AGENT (temp=0.85)                    │
                    │   Synthesizes: full narrative (9k-14k tokens)                │
                    │   with vivid prose, world-appropriate tone                   │
                    └──────────────────────────────────────────────────────────────┘
                                            │
                                            │ Full Story + All Context
                                            ▼
                    ┌──────────────────────────────────────────────────────────────┐
                    │         6. QUALITY ASSURANCE AGENT (temp=0.2)                │
                    │   Validates: thematic fidelity, character consistency,       │
                    │   world coherence, scores transformation quality             │
                    └──────────────────────────────────────────────────────────────┘
                                            │
                                            │ TransformationResult
                                            ▼
                    ┌──────────────────────────────────────────────────────────────┐
                    │              FINAL OUTPUT (Markdown/Text)                    │
                    │   Complete reimagined story with QA metrics                  │
                    │   (consistency score, transformation notes)                  │
                    └──────────────────────────────────────────────────────────────┘

        Data Flow: Pydantic models ensure type-safe handoffs between agents
        Temperature Tuning: Low (precise) → High (creative) → Low (validation)
```

</div>

## How It Works

The system **does NOT use movie subtitles**. Instead, it works from:
- Movie plots fetched via OMDb API, GPT-generated summaries, or web search
- Predefined classic stories from `data/source_stories.yaml` (Romeo and Juliet, Dracula, etc.)
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
 - OMDb API key (for `--movie-title` flow)

### Setup (using uv)

```bash
cd Reimagine-movies

uv init
uv venv
source .venv/bin/activate

uv sync

touch .env
```

Edit `.env` and add your OpenAI and OMDb API keys:
```
OPENAI_API_KEY=sk-your-key-here
OMDB_API_KEY=your-omdb-key
```
To obtain an OMDb API key:
- Visit http://www.omdbapi.com/apikey.aspx
- Choose the free tier (1,000 daily requests)
- Verify your email and copy the key into `.env`

## Usage

### Command Line Interface
#### Run Example Transformation

Reimagine movies by title (OMDb, GPT, or web search) or use predefined classic stories like Romeo and Juliet from `data/source_stories.yaml`.

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
uv run main.py \
  --custom-story "Your story text here..." \
  --target-world "Description of target world" \
  --maintain "element1" "element2" \
  --constraints "no magic" "realistic tech" \
  --output my_transformation.txt
```

#### OMDb Movie Reimagining
Search OMDb by title, confirm a selection (GPT-suggested index), choose a genre from a curated list, then automatically reimagine the selected movie using its full plot as the source.

```bash
# Pick a movie by title, then describe the target world interactively
uv run main.py --movie-title "Sholay"

# Or provide the target world up-front and an output file
uv run main.py --movie-title "Sholay" \
   --target-world "Neo-Noir Mumbai in 2040 with AI-enhanced policing and syndicates" \
   --output sholay_neo_noir.md
```

Requirements:
- Ensure `OMDB_API_KEY` is set in `.env`.
- The tool queries `http://www.omdbapi.com/?apikey=[yourkey]&...` (title search `s`, details `i` with `plot=full`).
- The movie's full plot becomes the `source_story` for the same multi-agent pipeline used for predefined stories.
- You will be prompted to select a genre (Action, Adventure, Comedy, Drama, Horror, Romance, Science Fiction, Fantasy, Thriller, Western, Musical, Mystery, Crime, Animation, Sports). The pipeline uses this to guide tone and conventions.

#### GPT-Based Movie Reimagining (Alternate)
Use GPT-4o-mini to disambiguate a title and generate a deep plot summary when OMDb lacks data or as an alternate path.

```bash
# Interactive: candidates suggested, pick one, choose genre, describe world
uv run main.py --movie-title-gpt "Sholay"

# Provide world and output explicitly
uv run main.py --movie-title-gpt "Sholay" \
   --target-world "Neo-Noir Mumbai in 2040 with AI-enhanced policing and syndicates" \
   --output sholay_neo_noir_gpt.md
```

Notes:
- The LLM proposes candidate movies (title/year) for disambiguation; you select the best match.
- It then produces an in-depth plot summary used as `source_story` for the same pipeline.
- Genre selection is applied to `creative_constraints`.

#### Web Search Movie Reimagining (GPT-4o-mini with Web Search)
Use GPT-4o-mini with web search capabilities to search for movies and get complete, up-to-date information from the web.

```bash
# Interactive: search movie, review results, choose genre, language, describe world
uv run main.py --movie-title-web "Dhurandhar"

# Provide world and output explicitly
uv run main.py --movie-title-web "Dhurandhar" \
   --target-world "Contemporary Mumbai under pervasive surveillance and gig-economy power brokers" \
   --output dhurandhar_contemporary_web.md
```

Notes:
- Uses `gpt-4o-mini-search-preview-2025-03-11` with `web_search_options={}` to gather recent movie information.
- Simple search query: `"search for movie - {title}"` returns comprehensive results including plot, cast, release info, streaming availability.
- Displays complete search results in markdown format for review.
- User confirms before proceeding with reimagining.
- Prompts for genre (15 options), language style (15 options), and output language (30 languages; defaults to English).
- Full search result used as `source_story` for transformation.
- All selections applied to `creative_constraints` to guide the transformation.

#### Getting Your OMDb API Key

The OMDb (Open Movie Database) API provides access to movie data. To use the `--movie-title` flow, obtain a key at http://www.omdbapi.com/apikey.aspx and add it to `.env`.

### Running with Predefined Classic Stories
The system includes predefined classic stories (Romeo and Juliet, Dracula, Odyssey, etc.) in `data/source_stories.yaml` that can be reimagined into different worlds.

```bash
# List stories
uv run main.py --list-stories

# Transform a predefined story
uv run main.py \
   --story-name ROMEO_AND_JULIET \
   --target-world "Silicon Valley AI labs rivalry in 2024" \
   --maintain "star-crossed love" "tragic miscommunication" \
   --constraints "grounded tech" \
   --output romeo_juliet_ai_labs.md

# Preview a story summary without transformation
uv run main.py --preview ROMEO_AND_JULIET
```

### Preview Saved Outputs
Render a previously saved file in the console.

```bash
uv run main.py --preview-file output/romeo_juliet_ai_labs.md
```

## Ancient India Target Worlds

Reimagine movies or predefined classic stories into richly detailed Ancient India-inspired settings. Each example world offers unique cultural, technological, and social dynamics perfect for narrative transformation.

### Example Worlds

1. **Vedic Era** - Bronze Age Saraswati valley with ritual specialists and nomadic tribes
2. **Mauryan Empire** - Imperial administration, Buddhist monasteries, Arthashastra politics
3. **Gupta Golden Age** - Scientific academies, university towns, artistic renaissance
4. **Chola Naval Empire** - Maritime trade, temple-states, bronze craftsmen
5. **Vijayanagara Kingdom** - Fortified cities, bazaar economy, warrior culture
6. **Sangam Tamil Nadu** - Bardic traditions, three crowned kings, literary assemblies
7. **Indus Valley Civilization** - Urban planning, trade networks, undeciphered script
8. **Magadha Republic** - Philosophical debates, merchant guilds, early democracy
9. **Kashmir Shaivism** - Mountain monasteries, tantric philosophy, scholar-ascetics
10. **Ajanta-Ellora Era** - Cave monasteries, trade caravans, rock-cut architecture
11. **Pallava Dynasty** - Shore temples, Dravidian architecture, Sanskrit revival
12. **Harsha's Empire** - Buddhist councils, diplomatic missions, cultural synthesis
13. **Rashtrakuta Dynasty** - Multilingual courts, Jain merchants, agrarian prosperity
14. **Chalukya Kingdoms** - Temple patronage, irrigation systems, feudal administration
15. **Ancient Kerala** - Spice trade, Ayurvedic medicine, matrilineal society

### Example Transformations

#### OMDb Flow (Recent Indian & English Films)
```bash
# Transform "Jawan" (2023, India) into Gupta Golden Age
uv run main.py --movie-title "Jawan" \
   --target-world "Gupta Golden Age scientific academies and civic reforms, moral dilemmas framed by dharma and statecraft" \
   --output jawan_gupta.md

# Transform "Oppenheimer" (2023, English) into Kashmir Shaivism
uv run main.py --movie-title "Oppenheimer" \
   --target-world "Kashmir Shaivism era with scholar-ascetics debating creation and destruction within cosmic consciousness" \
   --output oppenheimer_kashmir.md
```

#### GPT Flow (Alternate)
```bash
# Transform "Pathaan" (2023, India) into Chola Naval Empire
uv run main.py --movie-title-gpt "Pathaan" \
   --target-world "Chola Naval Empire with maritime espionage, temple-state alliances, and guild politics" \
   --output pathaan_chola.md

# Transform "Dune: Part Two" (2024, English) into Indus Valley Civilization
uv run main.py --movie-title-gpt "Dune: Part Two" \
   --target-world "Indus Valley Civilization trade networks, resource conflicts, and prophecy interpreted through undeciphered scripts" \
   --output dune2_indus.md
```

#### Web Search Flow with Ancient India Worlds
```bash
# Transform recent Indian film into Sangam Tamil Nadu
uv run main.py --movie-title-web "KGF" \
   --target-world "Sangam Tamil Nadu with bardic traditions, three crowned kings competing for dominance, literary assemblies judging warrior deeds" \
   --output kgf_sangam.md

# Transform "Interstellar" into Mauryan Empire
uv run main.py --movie-title-web "Interstellar" \
   --target-world "Mauryan Empire Buddhist monasteries preserving knowledge during famine, Arthashastra politics determining resource allocation, father-daughter bond across imperial distances" \
   --output interstellar_mauryan.md
```

#### Predefined Stories with Ancient India Worlds
```bash
# Transform Romeo & Juliet into Pallava Dynasty
uv run main.py \
   --story-name ROMEO_AND_JULIET \
   --target-world "Pallava Dynasty with feuding temple architect families, star-crossed lovers from rival Dravidian architecture schools, Sanskrit revival dividing communities" \
   --output romeo_juliet_pallava.md

# Transform Dracula into Ancient Kerala
uv run main.py \
   --story-name DRACULA \
   --target-world "Ancient Kerala spice trade networks concealing a merchant who drains rivals' wealth through Ayurvedic poisons, matrilineal society protecting ancient secrets" \
   --output dracula_kerala.md
```

<!-- Tips section removed for a more concise professional README -->

<!-- Changelog removed to keep README focused on usage and API -->

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

<!-- Subtitles rationale removed for brevity -->

<!-- Evaluation criteria and ownership & innovation removed for a professional, focused README -->

<!-- Challenges & mitigations removed -->

<!-- Future improvements removed -->

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

This project is licensed under the Apache License. See the `LICENSE` file for details.

## Contact

For questions about this system's design or implementation, see the code and documentation.
