import httpx
import os

ML_MODEL_URL = os.getenv("ML_MODEL_URL")


async def analyse_sentiment(text: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{ML_MODEL_URL}/analyse", json={"text": text})
        response.raise_for_status()
        return response.json()
