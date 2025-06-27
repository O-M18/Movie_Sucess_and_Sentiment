import joblib
import nltk
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from bs4 import BeautifulSoup

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

model = joblib.load("best_model.pkl")
vectorizer = joblib.load("vectorizer.pkl")
encoder = joblib.load("encoder.pkl")
# Clean function from notebook
def clean_text(text):
    text = BeautifulSoup(text, "html.parser").get_text()
    text = text.lower()
    text = re.sub('\[[^]]*\]', '', text)
    text = re.sub(r'[^a-z\s]', '', text)
    words = nltk.word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word not in stop_words]
    lemmatizer = WordNetLemmatizer()
    words = [lemmatizer.lemmatize(word) for word in words]
    return " ".join(words)

# Predict function
def predict_sentiment(text):

    cleaned = clean_text(text)
    vec = vectorizer.transform([cleaned])
    pred = model.predict(vec)
    label = encoder.inverse_transform([pred[0]])[0]
    return label