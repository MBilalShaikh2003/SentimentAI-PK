import csv
import torch
from pathlib import Path
from collections import Counter
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
)

from transformers import AutoTokenizer, AutoModelForSequenceClassification

DATA_PATH = Path("data/sentiment_dataset.csv")
MODEL_NAME = "cardiffnlp/twitter-xlm-roberta-base-sentiment-multilingual"
LABELS = ["negative", "neutral", "positive"]

with DATA_PATH.open("r", encoding="utf-8-sig", newline="") as file:
    rows = list(csv.DictReader(file))

texts = [row["text"].strip() for row in rows]
targets = [row["sentiment"].strip().lower() for row in rows]

if not texts or set(targets) != set(LABELS):
    raise ValueError("Dataset empty hai ya sentiment labels expected format mein nahi hain.")

train_texts, test_texts, train_labels, test_labels = train_test_split(
    texts,
    targets,
    test_size=0.30,
    random_state=42,
    stratify=targets,
)

print("Total comments:", len(texts))
print("Test comments:", len(test_texts))
print("Test label distribution:", dict(Counter(test_labels)))
print("\nLoading multilingual model...")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
model.eval()

predictions = []

for index, text in enumerate(test_texts, start=1):
    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        max_length=128,
    )

    with torch.no_grad():
        logits = model(**inputs).logits
        predicted_id = int(logits.argmax(dim=-1).item())

    predictions.append(model.config.id2label[predicted_id])

    if index % 10 == 0 or index == len(test_texts):
        print(f"Evaluated {index}/{len(test_texts)} comments")

print("\nAccuracy:", f"{accuracy_score(test_labels, predictions):.2%}")
print("\nClassification report:")
print(classification_report(
    test_labels,
    predictions,
    labels=LABELS,
    zero_division=0,
    digits=3,
))

print("Confusion matrix (rows=actual, columns=predicted):")
print("Label order:", LABELS)
print(confusion_matrix(test_labels, predictions, labels=LABELS))

output_path = Path("data/multilingual_baseline_results.csv")
with output_path.open("w", encoding="utf-8-sig", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["text", "actual_sentiment", "predicted_sentiment"])
    writer.writerows(zip(test_texts, test_labels, predictions))

print("\nSaved predictions to:", output_path)
