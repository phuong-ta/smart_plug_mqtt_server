from fastapi import FastAPI
from typing import AsyncGenerator
import asyncio

# Define the lifespan event
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    print("Application is starting up...")
    
    # Set up resources here (e.g., connect to a database)
    await asyncio.sleep(1)  # Simulating some async setup task
    print("Resources are ready.")
    
    # Yield control back to FastAPI
    yield
    
    # Clean up resources when the app shuts down
    print("Application is shutting down...")
    await asyncio.sleep(1)  # Simulating async cleanup task
    print("Resources cleaned up.")

# Create the FastAPI app and pass the lifespan event
app = FastAPI(lifespan=lifespan)

@app.get("/")
async def read_root():
    return {"message": "Hello, Phuong"}
