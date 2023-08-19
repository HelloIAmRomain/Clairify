# ------------------------------------------------------------------------
# Filename:    text_analysis.py
# Copyright (C) 2023 Romain DODET
# Author:      Romain DODET
# ------------------------------------------------------------------------


from transformers import BartTokenizer, BartForConditionalGeneration, pipeline
from ..core import config
from ..core.exceptions import TextTooLongError, ModelInferenceError
from ..core.config import MIN_TEXT_LENGTH, MAX_TEXT_LENGTH


# Initialize models
summarizer = BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn')
summarizer_tokenizer = BartTokenizer.from_pretrained('facebook/bart-large-cnn')
sentiment_analyzer = pipeline("sentiment-analysis")

def analyze_text(text: str):
    config.logger.info("Starting the text analysis...")
    if len(text) > MAX_TEXT_LENGTH:
        raise TextTooLongError(len(text), MAX_TEXT_LENGTH)

    try:
        # Text Summarization
        inputs = summarizer_tokenizer([text], max_length=1024, return_tensors='pt', truncation=True)
        summary_ids = summarizer.generate(inputs['input_ids'], num_beams=4, min_length=30, max_length=250, early_stopping=True)
        summary = summarizer_tokenizer.decode(summary_ids[0], skip_special_tokens=True)

        # Sentiment Analysis
        sentiment_result = sentiment_analyzer(text)
        sentiment = sentiment_result[0]['label']
        score = sentiment_result[0]['score']

        result = {
            "summary": summary,
            "sentiment": sentiment,
            "score": score
        }

        config.logger.info("Text analysis models processed the input successfully.")

        return result
    
    except Exception as e:
        raise ModelInferenceError("BART Summarizer") from e


if __name__ == "__main__":
    print(analyze_text("You are a very bad person. I hate you. I wish you were never born."))
    print(analyze_text("You are a very good person. I love you. I wish you were born earlier, so I could have met you sooner."))