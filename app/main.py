import logging
from fastapi import FastAPI, Depends
from dotenv import load_dotenv
import qa, ping

log = logging.getLogger("uvicorn")

load_dotenv()

def create_application() -> FastAPI:
    """
    Create a FastAPI application instance.
    """ 

    application = FastAPI()

    # Add the routers
    application.include_router(
        qa.router, tags=["Question Answering"]
    )

    application.include_router(
        ping.router, tags=["Ping"]
    )

    return application

app = create_application()

@app.on_event("startup")
async def startup_event():
    log.info("Starting up...")

@app.on_event("shutdown")
async def shutdown_event():
    log.info("Shutting down...")
