
import re


def preprocess_text(text: str) -> str:
    """Clean text while preserving sentiment-related words."""

    # Convert text to lowercase
    text = text.lower()

    # Remove URLs
    text = re.sub(r"https?://\S+|www\.\S+", " ", text)

    # Remove punctuation and symbols
    text = re.sub(r"[^\w\s]", " ", text)

    # Remove extra whitespace
    text = re.sub(r"\s+", " ", text).strip()

    return text


if __name__ == "__main__":
    examples = [
        "Yeh PRODUCT bohat acha hai!!!",
        "Mujhe yeh pasand nahi aya.",
        "Service achi nahi thi :(",
        "Amazing quality! Visit https://example.com",
    ]

    for example in examples:
        print("Original:  ", example)
        print("Processed: ", preprocess_text(example))
        print("-" * 40)
