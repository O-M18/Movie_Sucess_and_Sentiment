# Movie Success Prediction and Sentiment Analysis Web App

This project is an end-to-end Streamlit-based web application that predicts whether a movie will be a **Hit**, **Flop**, or **Average**, and also performs sentiment analysis on user reviews. The app utilizes machine learning models, external APIs, and a local SQLite database to provide real-time analysis and interaction.

---

## Features

- Search for any movie using OMDb and TMDb APIs
- View movie details: poster, release date, rating, overview, director, budget, and revenue
- Submit your own comment and receive a sentiment classification (positive/negative)
- Predict the commercial success of a movie using a trained machine learning model
- Store and update movie metadata and sentiment scores in a local SQLite database
- View top movies by positive or negative sentiment

---

## Demo
contain a demo video of the full streamlit app in repo

---

## Tech Stack

| Component            | Technology           |
|----------------------|----------------------|
| Frontend             | Streamlit            |
| Backend              | Python               |
| ML Models            | Random Forest (Pickle Format), Logistic regression (Pickle Format) |
| Data Source          | OMDb API, TMDb API   |
| Database             | SQLite               |
| NLP                  | TextBlob or custom sentiment model |
| Data Handling        | Pandas, NumPy        |
| Model Persistence    | joblib               |

---

## Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/movie-prediction-app.git
   cd movie-prediction-app
   ```
2. **Install  Dependencies**
    ```bash
    pip install -r requirements.txt
    ```
3. **Set Environment Variable**
    API_KEY=your_tmdb_api_key
    OMBD_API=your_omdb_api_key
4.  **Run the Streamlit App**
    ```bash
    Streamlit run app.py
    ```

## How It Works
  -  The user searches for a movie title.
  -   Movie metadata is pulled from APIs and displayed.
  -  Users can submit a review — sentiment is predicted and stored.
  -  The ML model takes features like budget, revenue, and outputs a prediction (hit/flop/average).
  -  All data is persisted in a SQLite database.


