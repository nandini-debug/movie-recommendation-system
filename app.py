import streamlit as st
import pandas as pd
import requests
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

API_KEY = "f26db22f"

st.set_page_config(page_title="Netflix AI Movie Recommender", layout="wide")

# -------- NETFLIX DARK UI --------

st.markdown("""
<style>

body{
background-color:#000;
color:white;
}

.title{
text-align:center;
color:#E50914;
font-size:50px;
font-weight:bold;
}

.card{
background:#141414;
padding:10px;
border-radius:15px;
text-align:center;
transition:0.3s;
}

.card:hover{
transform:scale(1.05);
box-shadow:0 0 15px red;
}

</style>
""", unsafe_allow_html=True)

st.markdown("<div class='title'>🎬 Netflix AI Movie Recommender</div>", unsafe_allow_html=True)

# -------- DATASET --------

movies = pd.read_csv("movie.csv")

# -------- AI MODEL --------

vectorizer = CountVectorizer()
vectors = vectorizer.fit_transform(movies["title"])
similarity = cosine_similarity(vectors)

# -------- OMDB API --------

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

    movie_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    rec_movies = []

    for i in movie_list:
        rec_movies.append(movies.iloc[i[0]].title)

    return rec_movies


# -------- TRAILER LINKS --------

trailers = {}

trailers = {

"Inception":"https://www.youtube.com/watch?v=zp_YGmAoht0",
"Avatar":"https://www.youtube.com/watch?v=_V1lLSS9lCc",
"Interstellar":"https://www.youtube.com/watch?v=zSWdZVtXT7E",
"The Dark Knight":"https://www.youtube.com/watch?v=EXeTwQWrcwY",
"Titanic":"https://www.youtube.com/watch?v=2e-eXJ6HgkQ",
"The Matrix":"https://www.youtube.com/watch?v=vKQi3bBA1y8",
"Fight Club":"https://www.youtube.com/watch?v=SUXWAEX2jlg",
"Forrest Gump":"https://www.youtube.com/watch?v=bLvqoHBptjg"

}



# -------- TRENDING MOVIES SECTION --------

st.subheader("🔥 Trending Movies")

trending_movies = [
"Inception",
"Avatar",
"Interstellar",
"The Dark Knight",
"Titanic"
]

cols = st.columns(5)

for i, m in enumerate(trending_movies):

    data = movie_info(m)

    with cols[i]:

        st.markdown("<div class='card'>", unsafe_allow_html=True)

        if data and data.get("Poster") != "N/A":
            st.image(data["Poster"])

        st.write(m)

        st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")

# -------- MOVIE SELECT --------

movie_list = movies["title"].values

selected_movie = st.selectbox("🎥 Select Movie", movie_list)

# -------- USER RATING --------

rating = st.slider("⭐ Your Rating", 1, 10, 5)

st.write("Your Rating:", rating)

# -------- BUTTON --------

if st.button("Recommend Movies 🤖"):

    movie = movie_info(selected_movie)

    if movie and movie["Response"] == "True":

        col1, col2 = st.columns(2)

        with col1:

            if movie.get("Poster") != "N/A":
                st.image(movie["Poster"])

        with col2:

            st.subheader(movie.get("Title"))

            st.write("⭐ IMDb:", movie.get("imdbRating"))

            st.write("🎭 Genre:", movie.get("Genre"))

            st.write("📅 Year:", movie.get("Year"))

            st.write("📝 Plot:", movie.get("Plot"))

        # -------- TRAILER --------

        st.subheader("🎞 Watch Trailer")

        if selected_movie in trailers:
            st.video(trailers[selected_movie])
        else:
            st.write("Trailer not available")

        # -------- SIMILAR MOVIES --------

        st.subheader("🔥 Similar Movies")

        recommendations = recommend(selected_movie)

        cols = st.columns(5)

        for i, m in enumerate(recommendations):

            data = movie_info(m)

            with cols[i]:

                st.markdown("<div class='card'>", unsafe_allow_html=True)

                if data and data.get("Poster") != "N/A":
                    st.image(data["Poster"])

                st.write(data.get("Title"))

                st.write("⭐", data.get("imdbRating"))

                st.markdown("</div>", unsafe_allow_html=True)

    else:

        st.error("Movie not found ❌")