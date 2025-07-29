"""
Not Implemented / Used
"""

from typing import List, Optional

from transformers import pipeline

from config.settings import WEBSITE_CATEGORY_FILTERS

# Initialize globally
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")


def classify_text(
    text: str,
    candidate_labels: List[str] = WEBSITE_CATEGORY_FILTERS,
    threshold: float = 0.5,
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


def summarize_text(
    text: str, max_length: int = 50, min_length: int = 15
) -> Optional[str]:
    """
    Summarizes a long piece of text using facebook/bart-large-cnn.

    Args:
        text (str): The input text to summarize.
        max_length (int): Max tokens in the summary.
        min_length (int): Min tokens in the summary.

    Returns:
        Optional[str]: The summarized text or None if input is invalid.
    """
    if not text or len(text.strip()) < 20:
        return None

    try:
        summary = summarizer(
            text, max_length=max_length, min_length=min_length, do_sample=False
        )
        return summary[0]["summary_text"]
    except Exception as e:
        print(f"Summarization failed: {e}")
        return None
