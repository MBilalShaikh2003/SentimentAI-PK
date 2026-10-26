
const form = document.getElementById("sentiment-form");
const commentInput = document.getElementById("comment-input");
const analyzeButton = document.getElementById("analyze-button");
const buttonText = document.getElementById("button-text");
const characterCount = document.getElementById("character-count");
const errorMessage = document.getElementById("error-message");
const resultSection = document.getElementById("result-section");

const sentimentResult = document.getElementById("sentiment-result");
const sentimentIcon = document.getElementById("sentiment-icon");

const scoreElements = {
    positive: {
        text: document.getElementById("positive-score"),
        bar: document.getElementById("positive-bar"),
    },
    neutral: {
        text: document.getElementById("neutral-score"),
        bar: document.getElementById("neutral-bar"),
    },
    negative: {
        text: document.getElementById("negative-score"),
        bar: document.getElementById("negative-bar"),
    },
};


// Character counter update karo
commentInput.addEventListener("input", () => {
    characterCount.textContent = `${commentInput.value.length} / 2000`;
});


// Sentiment result display karne ka function
function displayResult(data) {
    const sentiment = data.predicted_sentiment.toLowerCase();

    sentimentResult.textContent =
        sentiment.charAt(0).toUpperCase() + sentiment.slice(1);

    sentimentResult.className = sentiment;

    const icons = {
        positive: "☺",
        neutral: "😐",
        negative: "☹",
    };

    sentimentIcon.textContent = icons[sentiment] || "✳";

    for (const label of ["positive", "neutral", "negative"]) {
        const probability = Number(data.confidence_scores[label] ?? 0);
        const percentage = probability * 100;

        scoreElements[label].text.textContent = `${percentage.toFixed(2)}%`;
        scoreElements[label].bar.style.width =
            `${Math.max(0, Math.min(100, percentage))}%`;
    }

    resultSection.hidden = false;
}


// Form submit hone par API call karo
form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const text = commentInput.value.trim();

    errorMessage.hidden = true;
    errorMessage.textContent = "";

    if (!text) {
        errorMessage.textContent = "Please pehle koi comment enter karein.";
        errorMessage.hidden = false;
        return;
    }

    analyzeButton.disabled = true;
    buttonText.textContent = "Analyzing...";
    resultSection.hidden = true;

    try {
        const response = await fetch("/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            body: JSON.stringify({ text }),
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                data.detail || "Prediction nahi ho saki. Dobara try karein."
            );
        }

        displayResult(data);

    } catch (error) {
        errorMessage.textContent =
            error.message ||
            "API se connection nahi ho saka. Check karein ke backend chal raha hai.";
        errorMessage.hidden = false;

    } finally {
        analyzeButton.disabled = false;
        buttonText.textContent = "Analyze Sentiment";
    }
});
