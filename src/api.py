
import sys
from pathlib import Path

import torch
from transformers import pipeline
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field


BASE_DIR = Path(__file__).resolve().parent.parent
SRC_DIR = BASE_DIR / "src"
STATIC_DIR = BASE_DIR / "static"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))


MODEL_NAME = "cardiffnlp/twitter-xlm-roberta-base-sentiment-multilingual"

# CPU par multilingual sentiment model load karo
sentiment_pipeline = pipeline(
    task="text-classification",
    model=MODEL_NAME,
    device=-1,
)

app = FastAPI(
    title="SentimentAI PK API",
    description="Sentiment analysis for Roman Urdu, Urdu, English and mixed text",
    version="2.0.0",
)

app.mount(
    "/static",
    StaticFiles(directory=STATIC_DIR),
    name="static",
)


class PredictionRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=2000)


@app.get("/")
def home():
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "model_loaded": True,
        "model": MODEL_NAME,
    }




@app.post("/predict")
def predict_sentiment(request: PredictionRequest):
    text = request.text.strip()

    if not text:
        raise HTTPException(
            status_code=400,
            detail="Text cannot be empty.",
        )

    try:
        results = sentiment_pipeline(
            text,
            truncation=True,
            top_k=3,
        )

        # Transformers output ko normalize karo
        if results and isinstance(results[0], dict):
            results = results
        elif results and isinstance(results[0], list):
            results = results[0]

        label_map = {
            "LABEL_0": "negative",
            "LABEL_1": "neutral",
            "LABEL_2": "positive",
        }

        confidence_scores = {}

        for item in results:
            label = label_map.get(
                item["label"],
                item["label"].lower(),
            )
            confidence_scores[label] = round(
                float(item["score"]),
                4,
            )

        if not confidence_scores:
            raise ValueError("Model returned no sentiment scores.")

        predicted_label = max(
            confidence_scores,
            key=confidence_scores.get,
        )

        return {
            "text": text,
            "predicted_sentiment": predicted_label,
            "confidence": confidence_scores[predicted_label],
            "confidence_scores": confidence_scores,
            "model": MODEL_NAME,
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(error)}",
        ) from error
