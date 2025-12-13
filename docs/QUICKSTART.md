# Quick Start Guide

## 5-Minute Setup

### 1. Install
```bash
cd Reimagine-movies
uv init
uv venv
source .venv/bin/activate
uv sync
```

### 2. Configure
```bash
touch .env
```

Edit `.env` and add your required API keys:
```
OPENAI_API_KEY=sk-your-actual-key-here
OMDB_API_KEY=your-omdb-api-key
```

OMDb (Open Movie Database) API is used for the `--movie-title` flow to fetch official movie plots.

How to get OMDb API key:
- Visit http://www.omdbapi.com/apikey.aspx
- Choose the free tier (up to 1,000 requests/day)
- Verify your email, then paste the key into `.env` as `OMDB_API_KEY`

### 3. Run Example
```bash
uv run main.py --example or uv run main.py --example
```

This transforms Romeo and Juliet into a Silicon Valley AI rivalry story.

## Basic Usage
### OMDb Movie Reimagining (official plots)
```bash
uv run main.py --movie-title "Sholay"
```
- Searches OMDb by title and lets you choose the correct match
- Fetches the full official plot as the source story
- Prompts you to select a genre to guide tone and conventions

Optional:
```bash
uv run main.py --movie-title "Sholay" \
  --target-world "Neo-Noir Mumbai in 2040 with AI-enhanced policing and syndicates" \
  --output sholay_neo_noir.md
```
Requires: `OMDB_API_KEY` in `.env`

### GPT-Based Movie Reimagining (when OMDb is insufficient)
```bash
uv run main.py --movie-title-gpt "Sholay"
```
- Uses GPT to suggest disambiguation and produce a deep, structured plot summary
- Same transformation pipeline; useful for recent/regional titles missing in OMDb

### Web Search Movie Reimagining (current web data)
```bash
uv run main.py --movie-title-web "Dhurandhar"
```
- Uses GPT with web search to assemble comprehensive, up-to-date details
- You confirm the result before transformation

### List Available Stories
```bash
uv run main.py --list-stories
```

Output:
```
Available Stories:
  ROMEO_AND_JULIET
  DRACULA
  ODYSSEY
  FRANKENSTEIN
  HAMLET
  CINDERELLA
```

### Transform a Story
```bash
uv run main.py \
  --story-name DRACULA \
  --target-world "Modern Silicon Valley where a mysterious investor drains startups" \
  --output dracula_vc.txt
```

### Custom Story
```bash
uv run main.py \
  --custom-story "Once upon a time, in a kingdom far away..." \
  --target-world "A cyberpunk megacity in 2099" \
  --maintain "underdog victory" "good vs evil" \
  --constraints "realistic technology" \
  --output custom_story.txt
```

## API Usage

### Start Server
```bash
uv run main.py --api
```

Server runs at: `http://localhost:8000`

### API Documentation
Visit: `http://localhost:8000/docs`

### Transform via API
```bash
curl -X POST http://localhost:8000/transform \
  -H "Content-Type: application/json" \
  -d '{
    "source_story": "Story text here...",
    "target_world_description": "A space station in 2247",
    "maintain_elements": ["theme", "character arcs"],
    "creative_constraints": ["hard science fiction"]
  }'
```

Tip: If you're transforming a movie via CLI first, the output is saved in `output/`. You can preview it with:
```bash
uv run main.py --preview-file output/reimagined_<title>.md
```

### Get Example Transformations
```bash
curl http://localhost:8000/knowledge-base/examples
```

## Common Commands

### Get Help
```bash
uv run main.py --help
```

### View Story Details
```bash
curl http://localhost:8000/source-stories/ROMEO_AND_JULIET
```

### Check System Health
```bash
curl http://localhost:8000/
```

## Troubleshooting

### "ModuleNotFoundError: No module named 'openai'"
```bash
uv sync
```

### "openai.APIError: Invalid API key"
Check your `.env` file has correct `OPENAI_API_KEY=sk-...`

### "OMDb error" or "No results found"
- Ensure `OMDB_API_KEY` is set in `.env`
- Try a more precise title or include the year
- Use `--movie-title-gpt` or `--movie-title-web` for alternate sources

### "FileNotFoundError: data/source_stories.yaml"
Run from project root directory:
```bash
cd /path/to/Reimagine-movies
uv run main.py --list-stories
```

### Output files not found
They're saved to `output/` directory:
```bash
ls output/
cat output/romeo_juliet_ai_labs.txt
```

## Understanding Output

The system generates:
1. **Transformed Story** - The main narrative (2-3 pages)
2. **Analysis Data** - Original story structure
3. **Transformation Notes** - How adaptation was done
4. **Quality Scores** - Consistency and fidelity metrics

Example output structure:
```
================================================================================
TRANSFORMATION RESULT
================================================================================

Original: Romeo and Juliet
New World: Silicon Valley Tech Ecosystem
Consistency Score: 88.0%

================================================================================
TRANSFORMED STORY
================================================================================

[Full narrative here...]

================================================================================
TRANSFORMATION ANALYSIS
================================================================================

Original Theme: The destructive nature of hatred
Moral Lesson: Unchecked rivalry destroys innocent lives

World Details:
  Era: Contemporary (2024)
  Technology: AI/ML research, quantum computing
  Social Structure: Tech oligarchy controlled by VCs

Character Mappings:
  Romeo → Rohan: Senior ML Engineer at Montague AI
  Juliet → Julia: Lead Researcher at Capulet Labs
  ...

Transformation Notes:
  Best Adaptation: Corporate rivalry mirrors family feud
  Most Creative: Poison → malicious code transformation
  Needs Work: Could deepen Julia's internal conflict
```

## Next Steps

1. **Try different worlds**: Transform Hamlet into a corporate thriller
2. **Use the API**: Build a web interface
3. **Customize agents**: Modify `src/agents/` for different styles
4. **Add stories**: Edit `data/source_stories.yaml`
5. **Share results**: Output files are in `output/` directory

## Resources

- Full Documentation: `README.md`
- System Design: `docs/SOLUTION.md`
- Example Transformation: `docs/EXAMPLE_TRANSFORMATION.md`
- API Docs: `http://localhost:8000/docs` (when server running)

## Cost Estimates

Approximate OpenAI API costs per transformation:
- Story Analysis: ~$0.05
- World Building: ~$0.03
- Character Mapping: ~$0.04
- Plot Transformation: ~$0.06
- Story Writing: ~$0.12
- Quality Assurance: ~$0.04

**Total per transformation: ~$0.30-0.40**

Using GPT-4o-mini (much cheaper than GPT-4 while maintaining quality)

## Performance

Typical transformation time:
- Story Analysis: 8-12 seconds
- World Building: 6-10 seconds
- Character Mapping: 10-15 seconds
- Plot Transformation: 12-18 seconds
- Story Writing: 20-30 seconds
- Quality Assurance: 8-12 seconds

**Total: 90-120 seconds per transformation**

Can be parallelized for batch processing.
