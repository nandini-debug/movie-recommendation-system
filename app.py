import streamlit as st
import pandas as pd
import requests
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

API_KEY = "f26db22f"

st.set_page_config(page_title="Netflix Movie Recommender", layout="wide")

# -------- NETFLIX DARK UI + STYLING --------
st.markdown("""
<style>
html, body, [class*="css"] {
    background-color:#0b0b0b;
    color:white;
}
[data-testid="stAppViewContainer"]{
    background-color:#0b0b0b;
}
[data-testid="stSidebar"]{
    background-color:#111111;
}
.title{
    text-align:center;
    color:#E50914;
    font-size:55px;
    font-weight:bold;
}
.card{
    background:#141414;
    padding:15px;
    border-radius:15px;
    text-align:center;
    transition:0.3s;
}
.card:hover{
    transform:scale(1.05);
    box-shadow:0px 8px 25px rgba(229,9,20,0.6);
}
h2, .stSubheader {
    color:#FF6F61;  /* lighter headings */
    font-weight:600;
}
.rating, .genre, .year, .plot {
    color:#E0E0E0;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='title'>🎬 Netflix Movie Recommender</div>", unsafe_allow_html=True)

# -------- DATASET --------
movies = pd.read_csv("movie.csv")

# -------- AI MODEL --------
vectorizer = CountVectorizer()
vectors = vectorizer.fit_transform(movies["title"])
similarity = cosine_similarity(vectors)

# -------- OMDB API FUNCTION --------
def movie_info(title):
    url = f"http://www.omdbapi.com/?t={title}&apikey={API_KEY}"
    try:
        data = requests.get(url).json()
        return data
    except:
        return None

# -------- RECOMMEND FUNCTION --------
def recommend(movie):
    index = movies[movies["title"] == movie].index[0]
    distances = similarity[index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    rec_movies = [movies.iloc[i[0]].title for i in movie_list]
    return rec_movies

# -------- TRAILER LINKS --------
trailers = {
    "Inception":"https://www.youtube.com/watch?v=YoHD9XEInc0",
    "Avatar":"https://www.youtube.com/watch?v=5PSNL1qE6VY",
    "Interstellar":"https://www.youtube.com/watch?v=zSWdZVtXT7E",
    "The Dark Knight":"https://www.youtube.com/watch?v=EXeTwQWrcwY",
    "Avengers: Infinity War":"https://www.youtube.com/watch?v=6ZfuNTqbHE8",
    "The Matrix":"https://www.youtube.com/watch?v=vKQi3bBA1y8",
    "Titanic":"https://www.youtube.com/watch?v=2e-eXJ6HgkQ",
    "Forrest Gump":"https://www.youtube.com/watch?v=bLvqoHBptjg",
    "Fight Club":"https://www.youtube.com/watch?v=SUXWAEX2jlg",
    "The Empire Strikes Back":"https://www.youtube.com/watch?v=JNwNXF9Y6kY"
}

# -------- TRENDING MOVIES --------
st.subheader("🔥 Trending Movies 🎥")
trending_movies = ["Inception", "Avatar", "Interstellar", "The Dark Knight", "Titanic"]
cols = st.columns(5)
for i, m in enumerate(trending_movies):
    data = movie_info(m)
    with cols[i]:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        if data and data.get("Poster") != "N/A":
            st.image(data["Poster"])
        st.write(f"🎬 {m}")
        st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")

# -------- MOVIE SELECT & USER RATING --------
movie_list = movies["title"].values
selected_movie = st.selectbox("🎬 Select Your Movie:", movie_list)
rating = st.slider("⭐ Your Rating", 1, 10, 5)
st.write(f"Your Rating: {rating} ⭐")

# -------- RECOMMENDATION BUTTON --------
if st.button("Recommend Movies 🤖✨"):
    movie = movie_info(selected_movie)
    if movie and movie["Response"] == "True":
        col1, col2 = st.columns([1,2])
        with col1:
            if movie.get("Poster") != "N/A":
                st.image(movie["Poster"])
        with col2:
            st.markdown(f"<h2>🎬 {movie.get('Title')}</h2>", unsafe_allow_html=True)
            st.markdown(f"<div class='rating'>⭐ IMDb Rating: {movie.get('imdbRating')}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='genre'>🎭 Genre: {movie.get('Genre')}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='year'>📅 Year: {movie.get('Year')}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='plot'>📝 {movie.get('Plot')}</div>", unsafe_allow_html=True)

        # -------- TRAILER --------
        st.subheader("🎞 Watch Trailer ▶️")
        if selected_movie in trailers:
            st.video(trailers[selected_movie])
        else:
            st.write("Trailer not available ❌")

        # -------- SIMILAR MOVIES --------
        st.subheader("✨ Similar Movies You May Like 🍿")
        recommendations = recommend(selected_movie)
        cols = st.columns(5)
        for i, m in enumerate(recommendations):
            data = movie_info(m)
            with cols[i]:
                st.markdown("<div class='card'>", unsafe_allow_html=True)
                if data and data.get("Poster") != "N/A":
                    st.image(data["Poster"])
                st.write(f"🎬 {data.get('Title')}")
                st.markdown(f"<div class='rating'>⭐ {data.get('imdbRating')}</div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.error("Movie not found ❌")
