# Quick Start Guide

## 5-Minute Setup

### 1. Install
```bash
cd Reimagine-movies
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

### 2. Configure
```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:
```
OPENAI_API_KEY=sk-your-actual-key-here
```

### 3. Run Example
```bash
python main.py --example
```

This transforms Romeo and Juliet into a Silicon Valley AI rivalry story.

## Basic Usage

### List Available Stories
```bash
python main.py --list-stories
```

Output:
```
Available Stories:
  • ROMEO_AND_JULIET
  • DRACULA
  • ODYSSEY
  • FRANKENSTEIN
  • HAMLET
  • CINDERELLA
```

### Transform a Story
```bash
python main.py \
  --story-name DRACULA \
  --target-world "Modern Silicon Valley where a mysterious investor drains startups" \
  --output dracula_vc.txt
```

### Custom Story
```bash
python main.py \
  --custom-story "Once upon a time, in a kingdom far away..." \
  --target-world "A cyberpunk megacity in 2099" \
  --maintain "underdog victory" "good vs evil" \
  --constraints "realistic technology" \
  --output custom_story.txt
```

## API Usage

### Start Server
```bash
python main.py --api
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
  }' \
  | jq '.full_story'
```

### Get Example Transformations
```bash
curl http://localhost:8000/knowledge-base/examples | jq
```

## Common Commands

### Get Help
```bash
python main.py --help
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
pip install -e .
```

### "openai.APIError: Invalid API key"
Check your `.env` file has correct `OPENAI_API_KEY=sk-...`

### "FileNotFoundError: data/source_stories.yaml"
Run from project root directory:
```bash
cd /path/to/Reimagine-movies
python main.py --list-stories
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
