
import logging
import threading
from fastapi import FastAPI
from contextlib import asynccontextmanager
from adapter.pubsub_subscriber import run
import ssl

ssl._create_default_https_context = ssl._create_stdlib_context
logging.basicConfig(level=logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    consumer_thread = threading.Thread(target=run)
    consumer_thread.start()
    yield
    
app = FastAPI(lifespan=lifespan)

@app.get("/")
def read_root():
    return "OK"
