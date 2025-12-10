# System Flow Diagram

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACES                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────┐              ┌──────────────┐                │
│  │              │              │              │                │
│  │  CLI Runner  │              │  REST API    │                │
│  │  (main.py)   │              │  (api.py)    │                │
│  │              │              │              │                │
│  └──────┬───────┘              └──────┬───────┘                │
│         │                             │                         │
└─────────┼─────────────────────────────┼─────────────────────────┘
          │                             │
          └──────────────┬──────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                  TRANSFORMATION ORCHESTRATOR                     │
│                     (orchestrator.py)                            │
│                                                                   │
│  • Coordinates agent pipeline                                    │
│  • Manages data flow                                             │
│  • Tracks progress                                               │
│  • Handles errors                                                │
└─────────────────────────────────────────────────────────────────┘
                         │
                         │
        ┌────────────────┼────────────────┐
        │                │                │
        ▼                ▼                ▼
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│   AGENT 1   │  │   AGENT 2   │  │   AGENT 3   │
│   Story     │─▶│   World     │─▶│  Character  │
│  Analysis   │  │   Builder   │  │   Mapping   │
│             │  │             │  │             │
│  Temp: 0.3  │  │  Temp: 0.8  │  │  Temp: 0.6  │
└─────────────┘  └─────────────┘  └─────────────┘
        │                │                │
        └────────────────┼────────────────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
        ▼                ▼                ▼
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│   AGENT 4   │  │   AGENT 5   │  │   AGENT 6   │
│    Plot     │─▶│   Story     │─▶│   Quality   │
│Transform.   │  │   Writer    │  │  Assurance  │
│             │  │             │  │             │
│  Temp: 0.7  │  │  Temp: 0.85 │  │  Temp: 0.2  │
└─────────────┘  └─────────────┘  └─────────────┘
        │                │                │
        └────────────────┼────────────────┘
                         │
                         ▼
                ┌─────────────────┐
                │  FINAL RESULT   │
                │                 │
                │ • Story Text    │
                │ • Analysis Data │
                │ • QA Scores     │
                │ • Metadata      │
                └─────────────────┘
```

## Data Flow

```
┌──────────────┐
│ User Input   │
│              │
│ • Story text │
│ • Target     │
│   world desc │
└──────┬───────┘
       │
       ▼
┌──────────────────────────────────────────┐
│ STEP 1: Story Analysis                   │
├──────────────────────────────────────────┤
│ Input:  Raw story text                   │
│ Output: • Themes                         │
│         • Characters + archetypes        │
│         • Plot structure                 │
│         • Conflicts                      │
│         • Key symbols                    │
└──────┬───────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────┐
│ STEP 2: World Building                   │
├──────────────────────────────────────────┤
│ Input:  • Target description             │
│         • Original themes                │
│ Output: • Era & technology               │
│         • Social structure               │
│         • Rules & constraints            │
│         • Cultural norms                 │
│         • Power dynamics                 │
└──────┬───────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────┐
│ STEP 3: Character Mapping                │
├──────────────────────────────────────────┤
│ Input:  • Original characters            │
│         • New world context              │
│ Output: • Transformed names              │
│         • New roles/occupations          │
│         • Adapted motivations            │
│         • Preserved archetypes           │
└──────┬───────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────┐
│ STEP 4: Plot Transformation              │
├──────────────────────────────────────────┤
│ Input:  • Original plot points           │
│         • New world rules                │
│         • Transformed characters         │
│ Output: • Reimagined events              │
│         • Context-appropriate actions    │
│         • Maintained stakes              │
│         • Preserved structure            │
└──────┬───────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────┐
│ STEP 5: Story Writing                    │
├──────────────────────────────────────────┤
│ Input:  • All transformed elements       │
│         • Original emotional arc         │
│ Output: • Complete 2-3 page narrative    │
│         • Vivid prose                    │
│         • Atmosphere & detail            │
│         • Show don't tell                │
└──────┬───────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────┐
│ STEP 6: Quality Assurance                │
├──────────────────────────────────────────┤
│ Input:  • Original analysis              │
│         • All transformations            │
│         • Final story                    │
│ Output: • Thematic fidelity score        │
│         • Structural integrity score     │
│         • Character consistency score    │
│         • World coherence score          │
│         • Emotional authenticity score   │
│         • Creative reimagining score     │
│         • Overall score                  │
│         • Strengths & weaknesses         │
│         • Recommendations                │
└──────┬───────────────────────────────────┘
       │
       ▼
┌──────────────┐
│ Final Output │
│              │
│ • Story      │
│ • Analysis   │
│ • Scores     │
└──────────────┘
```

## Agent Communication Pattern

```
┌─────────────────────────────────────────────────────────────┐
│                    Message Passing Flow                      │
└─────────────────────────────────────────────────────────────┘

Orchestrator                Agent                    OpenAI API
     │                       │                           │
     │──process(input_data)─▶│                           │
     │                       │                           │
     │                       │──system_prompt + user────▶│
     │                       │                           │
     │                       │◀────JSON response─────────│
     │                       │                           │
     │                       │ (validate with Pydantic)  │
     │                       │                           │
     │◀─────return output────│                           │
     │                       │                           │
     │ (pass to next agent)  │                           │
     │                       │                           │
     ▼                       ▼                           ▼
```

## Knowledge Base Integration

```
┌─────────────────────────────────────┐
│      Knowledge Base (YAML)          │
├─────────────────────────────────────┤
│                                     │
│ • Source Stories (6 synopses)       │
│ • Transformation Examples           │
│ • Narrative Patterns                │
│   - Hero's Journey                  │
│   - Three-act structure             │
│ • Character Archetypes              │
│ • World-building Dimensions         │
│                                     │
└─────────────┬───────────────────────┘
              │
              │ (Referenced in prompts)
              │
              ▼
       ┌──────────────┐
       │    Agents    │
       │              │
       │ Use patterns │
       │ as few-shot  │
       │ examples     │
       └──────────────┘
```

## Error Handling Flow

```
┌─────────────┐
│ User Input  │
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│ Validation      │    ┌──────────────┐
│ • Check format  │───▶│ Invalid?     │───Yes──▶ Error Response
│ • Verify data   │    │ Return error │
└──────┬──────────┘    └──────────────┘
       │ Valid                ▲
       ▼                      │
┌─────────────────┐           │
│ Agent Pipeline  │           │
│                 │           │
│ Each agent:     │           │
│ • Try process   │           │
│ • Catch errors  │───Failed──┘
│ • Validate out  │
└──────┬──────────┘
       │ Success
       ▼
┌─────────────────┐
│ Return Result   │
└─────────────────┘
```

## Temperature Strategy

```
Analysis/Validation (Precise)
┌─────────────────────────────────┐
│ Story Analysis Agent:    0.3    │
│ QA Agent:                0.2    │
└─────────────────────────────────┘

Transformation (Balanced)
┌─────────────────────────────────┐
│ Character Mapping Agent: 0.6    │
│ Plot Transform Agent:    0.7    │
└─────────────────────────────────┘

Creative Generation (Imaginative)
┌─────────────────────────────────┐
│ World Builder Agent:     0.8    │
│ Story Writer Agent:      0.85   │
└─────────────────────────────────┘

Lower temperature = More deterministic
Higher temperature = More creative
```

## Deployment Options

```
Option 1: Monolithic
┌────────────────────────────┐
│   Single Server            │
│                            │
│  ┌──────────────────────┐  │
│  │  All agents          │  │
│  │  + Orchestrator      │  │
│  │  + API               │  │
│  └──────────────────────┘  │
│                            │
└────────────────────────────┘

Option 2: Microservices
┌──────────┐  ┌──────────┐  ┌──────────┐
│ Agent 1  │  │ Agent 2  │  │ Agent 3  │
│ Service  │  │ Service  │  │ Service  │
└────┬─────┘  └────┬─────┘  └────┬─────┘
     │             │             │
     └─────────────┼─────────────┘
                   │
           ┌───────▼───────┐
           │ Orchestrator  │
           │   Service     │
           └───────┬───────┘
                   │
           ┌───────▼───────┐
           │  API Gateway  │
           └───────────────┘

Option 3: Serverless
┌──────────────────────────────┐
│  Lambda/Cloud Functions      │
│                              │
│  • Each agent = Function     │
│  • Event-driven triggers     │
│  • Auto-scaling              │
│  • Pay per execution         │
└──────────────────────────────┘
```

## Performance Optimization

```
Sequential (Current)
Agent1 → Agent2 → Agent3 → Agent4 → Agent5 → Agent6
  10s     8s      12s      15s      25s      10s
Total: ~80-90 seconds

Parallel (Future)
          ┌─ Agent2 (8s)  ─┐
Agent1 ──▶│─ Agent3 (12s) ─├─▶ Agent4 → Agent5 → Agent6
  10s     └─ (parallel)  ──┘      15s      25s      10s
Total: ~60-70 seconds (25% faster)

Cached (Future)
Agent1 (cached) → Agent2 (cached) → Agent4 → Agent5 → Agent6
    instant         instant          15s      25s      10s
Total: ~50 seconds (40% faster)
```

## Key Design Principles

```
┌────────────────────────────────────────┐
│ 1. SEPARATION OF CONCERNS              │
│    Each agent has single responsibility│
└────────────────────────────────────────┘

┌────────────────────────────────────────┐
│ 2. COMPOSITION OVER MONOLITH           │
│    Small, focused agents combine       │
└────────────────────────────────────────┘

┌────────────────────────────────────────┐
│ 3. FAIL FAST WITH VALIDATION           │
│    Pydantic models catch errors early  │
└────────────────────────────────────────┘

┌────────────────────────────────────────┐
│ 4. OPTIMIZE PER TASK                   │
│    Different temperatures per agent    │
└────────────────────────────────────────┘

┌────────────────────────────────────────┐
│ 5. MEASURABLE QUALITY                  │
│    QA agent provides quantitative data │
└────────────────────────────────────────┘
```
