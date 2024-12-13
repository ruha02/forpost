import uvicorn
from core.database import init_db
from core.logging import LOG_FORMAT
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from models import *
from routers import (
    AnswerRouter,
    AuthRouter,
    QuestionRouter,
    SourceRouter,
    SystemRouter,
    UserRouter,
)

app = FastAPI(
    title="ФОРПОСТ",
    version="1.0.0",
    description="Помощник для ИБ-инженеров, программистов и менеджеров в сфере ИБ",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_event():
    init_db()


@app.get("/healthcheck", tags=["Healthcheck"])
def healthcheck():
    return JSONResponse(status_code=200, content={"healthchek": True})


app.include_router(AuthRouter, tags=["Auth"], prefix="/auth")
app.include_router(SystemRouter)
app.include_router(UserRouter)
app.include_router(SourceRouter)
app.include_router(QuestionRouter)
app.include_router(AnswerRouter)

if __name__ == "__main__":
    log_config = uvicorn.config.LOGGING_CONFIG
    log_config["formatters"]["access"]["fmt"] = LOG_FORMAT
    log_config["formatters"]["default"]["fmt"] = LOG_FORMAT

    uvicorn.run(
        "main:app", host="0.0.0.0", port=9000, reload=True, log_config=log_config
    )
