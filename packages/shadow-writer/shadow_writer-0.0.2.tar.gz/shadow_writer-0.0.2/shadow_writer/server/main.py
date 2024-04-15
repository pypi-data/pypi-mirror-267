import os
import uvicorn
from fastapi import FastAPI, HTTPException, Depends, Body
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from models.api import (
    ReseachRequest,
    ResearchResponse,
    WritingRequest,
    WritingResponse,
    EditingRequest,
    EditingResponse,
)
from rag.tidb import TiDBCorpusClient
from llm.gemini import Gemini_client
from llm.openai import OAI_client
from agents.researcher import Researcher
from agents.writer import Writer
from agents.editor import Editor


app = FastAPI()
# app.mount("/.well-known", StaticFiles(directory=".well-known"), name="static")

bearer_scheme = HTTPBearer()
BEARER_TOKEN = os.environ.get("BEARER_TOKEN")
assert BEARER_TOKEN is not None, "BEARER_TOKEN environment variable must be set"

# data serving configuration on TiDB Cloud
TiDB_CONNECTION_URL = os.environ.get("TiDB_CONNECTION_URL")
assert (
    TiDB_CONNECTION_URL is not None
), "TiDB_CONNECTION_URL environment variable must be set"

GOOGLE_AI_API_KEY = os.environ.get("GOOGLE_AI_API_KEY")
assert (
    GOOGLE_AI_API_KEY is not None
), "GOOGLE_AI_API_KEY environment variable must be set"

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
assert OPENAI_API_KEY is not None, "OPENAI_API_KEY environment variable must be set"

tidb_corpus = TiDBCorpusClient(TiDB_CONNECTION_URL)
gemini_client = Gemini_client(api_key=GOOGLE_AI_API_KEY)
oai_client = OAI_client(OPENAI_API_KEY)

# initial the agents
researcher = Researcher(oai_client, tidb_corpus)
writer = Writer(gemini_client)
editor = Editor(oai_client)


def validate_token(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    """Validate the token provided in the request."""
    if credentials.scheme != "Bearer" or credentials.credentials != BEARER_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid or missing token")
    return credentials


@app.post(
    "/research",
    response_model=ResearchResponse,
)
async def do_research(
    request: ReseachRequest = Body(...),
    token: HTTPAuthorizationCredentials = Depends(validate_token),
):
    try:
        result = researcher.search(
            request.article_spec,
            request.seo_keywords,
            request.max_tokens,
        )
        return ResearchResponse(data=result.to_json(orient="records"))
    except Exception as e:
        print("Error:", e)
        raise HTTPException(status_code=500, detail="Internal Service Error")


@app.post(
    "/write",
    response_model=WritingResponse,
    description="ask the agent to write an article based on the spec and materials.",
)
async def do_write(
    request: WritingRequest = Body(...),
    token: HTTPAuthorizationCredentials = Depends(validate_token),
):
    try:
        background_materials = ""
        if request.background_materials is None:
            materials = researcher.search(
                request.article_spec,
                request.seo_keywords,
            )
            for index, row in materials.iterrows():
                background_materials = (
                    background_materials
                    + "\n"
                    + (
                        f"source title: {row['source_name']}\n"
                        f"source url: {row['source_uri']}\n"
                        f"paragraph: ... {row['text']} ..\n"
                    )
                )
        else:
            background_materials = request.background_materials

        result = writer.write(
            article_spec=request.article_spec,
            background_materials=background_materials,
            seo_keywords=request.seo_keywords,
        )
        return WritingResponse(article_content=result)
    except Exception as e:
        print("Error:", e)
        raise HTTPException(status_code=500, detail="Internal Service Error")


@app.post(
    "/edit",
    response_model=EditingResponse,
    # NOTE: We are describing the shape of the API endpoint input due to a current limitation in parsing arrays of objects from OpenAPI schemas. This will not be necessary in the future.
    description="ask the agent to edit an article based on the opinion.",
)
async def do_edit(
    request: EditingRequest = Body(...),
    token: HTTPAuthorizationCredentials = Depends(validate_token),
):
    try:
        result = editor.edit(request.opinion, request.article_content)
        return EditingResponse(edited_article=result)
    except Exception as e:
        print("Error:", e)
        raise HTTPException(status_code=500, detail="Internal Service Error")


def start():
    uvicorn.run("server.main:app", host="0.0.0.0", port=8000, reload=True)
