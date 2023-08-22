# ------------------------------------------------------------------------
# Filename:    text_analysis.py
# Copyright (C) 2023 Romain DODET
# Author:      Romain DODET
# ------------------------------------------------------------------------


from ..core.exceptions import (ModelInferenceError, TextTooLongError,
                               TextTooShortError)
from ..core.config import MAX_TEXT_LENGTH, MIN_TEXT_LENGTH, logger
from transformers import BartForConditionalGeneration, BartTokenizer, pipeline
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter
import re
import nltk

nltk.download('stopwords')
nltk.download('punkt')


# Initialize models
summarizer = BartForConditionalGeneration.from_pretrained(
    'facebook/bart-large-cnn')
summarizer_tokenizer = BartTokenizer.from_pretrained('facebook/bart-large-cnn')
sentiment_analyzer = pipeline("sentiment-analysis")


def keyword_extractor(text: str, num_keywords: int = 5) -> list:
    text = text.lower()
    # Remove special characters (hashtags, accents, etc.)
    text = re.sub(r'[^\w\s]', '', text)

    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(text)

    # Remove stopwords and punctuations
    filtered_tokens = [
        w for w in word_tokens if w not in stop_words and w.isalnum()]

    # Count frequency of each word
    word_freq = Counter(filtered_tokens)

    # Get the most common words
    keywords = word_freq.most_common(num_keywords)

    # Extract only the keywords, not their frequency counts
    keywords_only = [item[0] for item in keywords]

    return keywords_only


def analyze_text(text: str, options: dict):
    logger.info("Starting the text analysis...")
    text_length = len(text)

    if text_length > MAX_TEXT_LENGTH:
        raise TextTooLongError(text_length, MAX_TEXT_LENGTH)

    if text_length < MIN_TEXT_LENGTH:
        raise TextTooShortError(text_length, MIN_TEXT_LENGTH)

    result = {}

    if options.summary:
        try:
            # Text Summarization
            inputs = summarizer_tokenizer(
                [text], max_length=1024, return_tensors='pt', truncation=True)
            summary_ids = summarizer.generate(
                inputs['input_ids'], num_beams=4, min_length=30, max_length=250, early_stopping=True)
            summary = summarizer_tokenizer.decode(
                summary_ids[0], skip_special_tokens=True)
            result["summary"] = summary
        except Exception as e:
            raise ModelInferenceError("BART Summarizer") from e

    if options.sentiment:
        try:
            # Sentiment Analysis
            sentiment_result = sentiment_analyzer(text)
            sentiment = sentiment_result[0]['label']
            score = sentiment_result[0]['score']
            result["sentiment"] = sentiment
            result["score"] = score
        except Exception as e:
            raise ModelInferenceError("Sentiment Analysis Model") from e

    if options.keyword_extraction:
        try:
            # Keyword extraction
            keywords = keyword_extractor(text)
            result["keywords"] = keywords
        except Exception as e:
            raise ModelInferenceError("Keyword Extraction Model") from e

    logger.info("Text analysis models processed the input successfully.")

    return result
