from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
import logging

from src.schemas.schemas import TextQuery
from src.model.llm_chain import LLMChain

logger = logging.getLogger(__name__)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

llm_chain = LLMChain()


@app.post("/query/")
async def query_lang_chain(request: TextQuery = Body(...)):
    try:
        request_payload = request
        logger.info(request_payload)
        print(f"request_payload: {request_payload}")
        return llm_chain.send_query(query=request)

    except Exception as e:
        print("error : {e}")
        logger.error("error: ", e)
