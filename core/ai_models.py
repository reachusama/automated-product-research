from transformers import pipeline
from config.settings import WEBSITE_CATEGORY_FILTERS
from typing import Optional, List

# Initialize globally
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")


def classify_text(
    text: str,
    candidate_labels: List[str] = WEBSITE_CATEGORY_FILTERS,
    threshold: float = 0.5
) -> Optional[str]:
    """
    Classifies input text into one of the provided candidate labels.

    Args:
        text (str): Input text (e.g., homepage + SEO).
        candidate_labels (List[str]): List of labels to classify into.
        threshold (float): Minimum score required to accept a label.

    Returns:
        Optional[str]: Best-matching label or None if no label exceeds the threshold.
    """
    if not text or not candidate_labels:
        return None

    result = classifier(text, candidate_labels=candidate_labels, multi_label=False)

    top_label = result["labels"][0]
    top_score = result["scores"][0]

    if top_score >= threshold:
        return top_label
    return None
