import logging

from fastapi import FastAPI
from langchain.messages import HumanMessage

from app.logging_config import configure_logging
from app.graph.shopping_graph import build_graph
from app.models.shopping import ShoppingRequest

configure_logging()

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Autonomous Shopping Agent",
    version="0.1.0"
)

shopping_graph = build_graph()


@app.get("/health")
async def health():

    return {
        "status": "UP"
    }



@app.post("/agent/shopping")
async def shopping(request: ShoppingRequest):

    try:
        logger.info(
            "REQUEST_RECEIVED trace=%s request=%s",
            request.session_id,
            request.request
        )

        result = await shopping_graph.ainvoke({
            "session_id": request.session_id,
            "user_request": request.request,
            "messages": [
                HumanMessage(content=request.request)
            ]
        })

        logger.info(
                "REQUEST_COMPLETED trace=%s",
                request.session_id
        )

        return {
            "session_id": request.session_id,
            "messages": [
                message.model_dump()
                for message in result["messages"]
            ]
        }

    except Exception:
        logger.exception(
            "REQUEST_FAILED trace=%s",
            request.session_id
        )
        raise