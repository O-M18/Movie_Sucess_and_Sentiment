import streamlit as st
import sqlite3
import pandas as pd

# Function to fetch top movies by sentiment
def get_top_movies(order_by="Positive_score", top_n=6):
    with sqlite3.connect("Movie_detail.db") as conn:
        query = f"""
        SELECT M.ID, M.Title, M.Poster, S.Positive_score, S.Negative_score, S.Total_comment
        FROM Movie M
        JOIN Score S ON M.id = S.id
        ORDER BY S.{order_by} DESC
        LIMIT ?
        """
        return pd.read_sql_query(query, conn, params=(top_n,))
st.set_page_config(layout="wide", page_title="Top Movies", page_icon="🎬")
st.title("⭐ Top Movies by Sentiment")

# Sentiment toggle
sentiment = st.radio("Show by sentiment:", ["Positive", "Negative"], horizontal=True)
order_by = "Positive_score" if sentiment == "Positive" else "Negative_score"

# Fetch data
top_movies = get_top_movies(order_by=order_by)

if top_movies.empty:
    st.warning("No movie data found. Add some reviews first.")
else:
    # Layout in columns
    cols = st.columns(3)
    for idx, row in top_movies.iterrows():
        with cols[idx % 3]:
            if row["Poster"]:
                st.image(row["Poster"], width=200)
            st.markdown(f"### {row['Title']}")
            emoji = "👍" if sentiment == "Positive" else "👎"
            score=row[order_by]
            st.markdown(f"{emoji}:**{score}**")
            st.markdown(f"💬 **{row['Total_comment']}** comments")
