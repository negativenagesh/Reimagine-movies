from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import yaml
from src.models.domain import TransformationRequest, TransformationResult
from src.orchestrator import TransformationOrchestrator

app = FastAPI(
    title="Story Transformation API",
    description="Microservice API for transforming narratives across contexts using multi-agent AI",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

orchestrator = TransformationOrchestrator()


class TransformRequest(BaseModel):
    source_story: str
    target_world_description: str
    maintain_elements: list[str] = []
    creative_constraints: list[str] = []


class HealthResponse(BaseModel):
    status: str
    agents_available: list[str]


@app.get("/", response_model=HealthResponse)
async def health_check():
    return HealthResponse(
        status="healthy",
        agents_available=[
            "StoryAnalysisAgent",
            "WorldBuilderAgent",
            "CharacterMappingAgent",
            "PlotTransformationAgent",
            "StoryWriterAgent",
            "QualityAssuranceAgent"
        ]
    )


@app.get("/source-stories")
async def list_source_stories():
    try:
        with open("data/source_stories.yaml", "r") as f:
            stories = yaml.safe_load(f)
        return {"stories": list(stories.keys())}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/source-stories/{story_name}")
async def get_source_story(story_name: str):
    try:
        with open("data/source_stories.yaml", "r") as f:
            stories = yaml.safe_load(f)
        
        if story_name not in stories:
            raise HTTPException(status_code=404, detail="Story not found")
        
        return {"name": story_name, "content": stories[story_name]}
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Stories database not found")


@app.post("/transform", response_model=TransformationResult)
async def transform_story(request: TransformRequest):
    try:
        transformation_request = TransformationRequest(
            source_story=request.source_story,
            target_world_description=request.target_world_description,
            maintain_elements=request.maintain_elements,
            creative_constraints=request.creative_constraints
        )
        
        result = await orchestrator.transform_story(transformation_request)
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transformation failed: {str(e)}")


@app.get("/knowledge-base/archetypes")
async def get_character_archetypes():
    try:
        with open("data/knowledge_base.yaml", "r") as f:
            kb = yaml.safe_load(f)
        return kb["character_archetypes"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/knowledge-base/narrative-patterns")
async def get_narrative_patterns():
    try:
        with open("data/knowledge_base.yaml", "r") as f:
            kb = yaml.safe_load(f)
        return kb["narrative_patterns"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/knowledge-base/examples")
async def get_transformation_examples():
    try:
        with open("data/knowledge_base.yaml", "r") as f:
            kb = yaml.safe_load(f)
        return kb["transformation_examples"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
