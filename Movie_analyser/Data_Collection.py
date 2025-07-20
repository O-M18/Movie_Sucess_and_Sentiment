import requests
from bs4 import BeautifulSoup
import time
import random
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv() 

API_KEY=os.getenv("API_KEY")
URL= "https://api.themoviedb.org/3/search/movie?include_adult=false&language=en-US&page=1"
MOVIE_DETAIL="https://api.themoviedb.org/3/movie/"
MOVIE_IMG="https://image.tmdb.org/t/p/w500"
URL_REVIEWS = "https://api.themoviedb.org/3/movie/{}/reviews"
# URL_OMDB = f"http://www.omdbapi.com/?t={}&apikey={}
API_KEY_OMDB = os.getenv("OMBD_API")


def fetch_movie_titles(query):
    """Returns a list of matching movie titles with IDs"""
    response = requests.get(f"http://www.omdbapi.com/?s={query}&apikey={API_KEY_OMDB}")
    results = response.json().get("Search", [])
    movie_list = [
        {"title": f"{m.get('Title','N/A')} ({m.get('Year','N/A')})", "id": m.get("imdbID")}
        for m in results
    ]
    return movie_list


def get_movie_details(movie_id,movie_title):
    detail_url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    review_url = URL_REVIEWS.format(movie_id)

    # Fetch movie details
    movie_resp = requests.get(detail_url, params={"api_key": API_KEY})
    movie = movie_resp.json()
    URL_OMDB = f"http://www.omdbapi.com/?i={movie_id}&apikey={API_KEY_OMDB}"
    data=requests.get(URL_OMDB)
    data=data.json()
    # Fetch reviews
    review_resp = requests.get(review_url, params={"api_key": API_KEY})
    reviews = review_resp.json().get("results", [])
    top_review = reviews[0].get("content", "No review content.") if reviews else "No review available."

    poster_path = movie.get("poster_path")
    poster_url = f"{MOVIE_IMG}{poster_path}" if poster_path else None
    


    return {
        "id":movie_id,
        "title":movie_title,
        "overview": movie.get("overview"),
        "release_date": movie.get("release_date"),
        "popularity": movie.get("popularity"),
        "poster_url":poster_url,
        "top_review": top_review,
        "imdbVotes":data.get('imdbVotes'),
        "genre": movie.get('genres'),
        "Budget":movie.get('budget'),
        "revenue":movie.get('revenue','NA'),
        "rating":data.get('imdbRating'),
        "Awards":data.get('Awards'),
        "director":data.get('Director')
    }