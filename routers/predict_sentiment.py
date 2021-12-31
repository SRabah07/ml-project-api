import logging
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from joblib import load
import os

logger = logging.getLogger(__name__)

nltk.download('stopwords')
nltk.download('punkt')
STORED_SENTIMENT_MODELS_PATH = os.environ.get('STORED_MODELS_PATH', "./storage/models/sentiment")

STORED_STROKE_MODELS_PATH = os.environ.get('STORED_MODELS_PATH', "./storage/models/stroke")


def make_sentiment_prediction(key: str, text: str):
    logger.debug(f"Predict text: {text}, using model within key: {key}")
    if not text:
        raise Exception(f"Text is required!")

    # Load Vectorizer
    vectorizer = get_vectorizer(key)

    # Load Model
    model = get_model(key)

    # Cleand and Processed text
    cleaned_text = preprocess_text(text)
    logger.debug(f"""
        - Original text: "{text}"
        - Cleaned text: "{cleaned_text}"
        """)

    # Convert to numeric
    text_vectorized = vectorizer.transform([cleaned_text])

    # Prediction
    rating = model.predict(text_vectorized)

    return rating


def preprocess_text(text):
    stop_words = set(stopwords.words('english'))
    stop_words.update(["'ve", "", "'ll", "'s", ".", ",", "?", "!", "(", ")", "..", "'m", "n", "u"])
    text = text.lower()
    tokens = word_tokenize(text)
    tokens = [t for t in tokens if t not in stop_words]
    return ' '.join(tokens)


def get_vectorizer(key):
    path_to_model = f"{STORED_SENTIMENT_MODELS_PATH}/{key}.pkl"
    logger.debug(f"Load vectorizer from path:{path_to_model}")
    exist = os.path.exists(path_to_model)
    if not exist:
        raise Exception(f"Model for feature extraction within path={path} doesn't exist!")

    return load(path_to_model)


def get_model(key):
    path_to_model = f"{STORED_SENTIMENT_MODELS_PATH}/{key}.joblib"
    logger.debug(f"Load model from path:{path_to_model}")
    exist = os.path.exists(path_to_model)
    if not exist:
        raise Exception(f"Model within path={path_to_model} doesn't exist!")

    return load(path_to_model)
