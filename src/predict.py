
import joblib
from pathlib import Path

from preprocessing import preprocess_text


BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "sentiment_model.joblib"

model = joblib.load(MODEL_PATH)

comments = [
    "Yeh service lajawab hai",
    "Mujhe bilkul acha nahi laga",
    "Delivery normal time par hui",
    "Product ki quality zabardast hai",
    "Customer support ne mera masla hal nahi kiya",
    "Parcel mein teen items hain",
]
for comment in comments:
    prediction = model.predict([comment])[0]
    probabilities = model.predict_proba([comment])[0]

    print(f"\nComment: {comment}")
    print(f"Predicted sentiment: {prediction}")

    print("Confidence scores:")

    for label, probability in zip(
        model.classes_, probabilities
    ):
        print(f"  {label}: {probability * 100:.2f}%")
