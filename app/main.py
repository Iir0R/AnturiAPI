from fastapi import FastAPI
from .routers import blocks, sensors, results, changes

app = FastAPI()

app.include_router(blocks.router)
app.include_router(sensors.router)
app.include_router(results.router)
app.include_router(changes.router)