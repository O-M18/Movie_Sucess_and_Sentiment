import streamlit as st
from Data_Collection import fetch_movie_titles, get_movie_details
from Review_proecss import predict_sentiment
from Update import Insert_value, update_score


st.set_page_config(
    page_title="🎬 Movie  App",    
    page_icon="🍿",                        
    layout="centered")


st.title("🎬 Movie Search App")

# 1. User inputs movie name
query = st.text_input("Search for a movie")

# 2. Fetch movie options
if query:
    movie_list = fetch_movie_titles(query)
    if not movie_list:
        st.warning("No movies found.")
    else:
        # 3. User selects one from dropdown
        options = {movie["title"]: movie["id"] for movie in movie_list}
        selected_title = st.selectbox("Select the movie", options.keys())

        if selected_title:
            movie_id = options[selected_title]

            # 4. Fetch and display selected movie details
            movie = get_movie_details(movie_id,selected_title)

            st.header(movie["title"])
            if movie["poster_url"]:
                st.image(movie["poster_url"], width=300)
            else:
                st.warning("No poster image available.")
    
            st.markdown(f"**Release Date:** {movie['release_date']}")
            # st.markdown(f"**Director:** {movie['Director']}")
            st.markdown(f"**Rating:** {movie['rating']} ⭐")
            st.markdown(f"**Popularity:** {movie['popularity']}")
            st.markdown(f"**Overview:** {movie['overview']}")
            st.markdown(f"**Top Review:**\n\n{movie['top_review']}")
            st.title('make a comment on the movie')
            comment=st.text_area(" write anything")
            if "submitted_movies" not in st.session_state:
                st.session_state["submitted_movies"] = set()
            if st.button("Submit"):
                if comment.strip() != "":
                    result = predict_sentiment(comment)
                    emoji = {"positive": "😊", "negative": "😞"}
                    st.success(f"**{result.upper()}** {emoji.get(result.lower(), '')}")

                    # Insert or update DB
                    Insert_value(
                        ID=movie.get('id'),
                        Title=movie.get('title'),
                        Year=movie.get('release_date'),
                        Poster=movie.get('poster_url'),
                        Genre=movie.get('genre'),  # can be list or string
                        Director=movie.get('director', 'N/A'),
                        Rating=float(movie.get('rating') or 0),
                        Awards=movie.get('Awards', 'N/A'),
                        Budget=int(movie.get('Budget') or 0),
                        Revenue=int(movie.get('revenue') or 0),
                        Popularity=float(movie.get('popularity')or 0)
                        
                    )

                    update_score(movie_id, result)  # update scores

                else:
                    st.warning("Please write something before submitting.")
                
                    
        
    
        
