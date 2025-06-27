import streamlit as st
import pandas as pd
import sqlite3
import pickle
import ast
import joblib
# -------------------
# Config
# -------------------
st.set_page_config(page_title="🎯 Genre-wise Prediction", page_icon="🎬")
st.title("🎯 Predict Movie Success by Genre")

# -------------------
# Load Model + Preprocessing Function
# -------------------
@st.cache_resource
def load_model():
        return joblib.load("pages/rf_model.pkl")

model = load_model()
def Process_sample(df):
      # df['genre_list'] = df['genres'].apply(lambda x: [i['name'] for i in ast.literal_eval(x)])
      # df['genre_str']=df['genre_list'].apply(lambda x: ','.join(x))
      # genre_dummies = df['genre_str'].str.get_dummies(sep=',')
      df_2=df[['Budget','Revenue','popularity']]
      # df_2=pd.concat([df_2,genre_dummies],axis=1)
      # expected_col=['budget', 'revenue', 'popularity', 'Action', 'Adventure', 'Animation',
      #      'Comedy', 'Crime', 'Documentary', 'Drama', 'Family', 'Fantasy',
      #      'Foreign', 'History', 'Horror', 'Music', 'Mystery', 'Romance',
      #      'Science Fiction', 'TV Movie', 'Thriller', 'War', 'Western']
      # df_2=df_2.reindex(columns=expected_col,fill_value=0)
      df_2.columns = df_2.columns.str.lower()
      return df_2

def load_movies():
    with sqlite3.connect("Movie_detail.db") as conn:
        return pd.read_sql_query("SELECT * FROM Movie", conn)

df = load_movies()

# -------------------
# Genre Dropdown
# -------------------
df['genre_list'] = df['Genre'].apply(
    lambda x: [i['name'] for i in ast.literal_eval(x)] if isinstance(x, str) else []
)

all_genres = sorted(set(g for sub in df['genre_list'] for g in sub))
selected_genre = st.selectbox("🎞️ Select a Genre", all_genres)

filtered_df = df[df['genre_list'].apply(lambda x: selected_genre in x)]

# -------------------
# Predict & Display
# -------------------
st.dataframe(filtered_df)
if filtered_df.empty:
    st.warning("No movies found for selected genre.")
else:
    st.subheader(f"🎬 Movies in {selected_genre} Genre")

    try:
        # Step 1: Apply preprocessing function
        X = Process_sample(filtered_df)

        # Step 2: Predict
        y_pred = model.predict(X)

        # Step 3: Show results
        cols = st.columns(3)
        for idx, (i, row) in enumerate(filtered_df.iterrows()):
            with cols[idx % 3]:
                if row.get("Poster"):
                    st.image(row["Poster"], width=200)

                st.markdown(f"**🎬 {row['Title']} ({row['Year']})**")
                st.markdown(f"**🎬 Director:** {row.get('Director', 'N/A')}")
                pred = y_pred[idx]
                emoji = {"Hit": "🔥", "Flop": "💥", "Average": "⚖️"}
                st.success(f"{emoji.get(pred, '🎲')} **Prediction: {pred.upper()}**")

    except Exception as e:
        st.error(f"Prediction failed: {e}")
