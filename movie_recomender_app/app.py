import gzip
import pickle
import pandas as pd
import requests
import streamlit as st

# 0. FUNGSI FETCH POSTER DARI API TMDB
def fetch_poster(movie_id):
    # Masukin API Key TMDB:
    api_key = "be15199e0432eb194e280b104f9997f1"
    
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
    
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            poster_path = data.get('poster_path')
            if poster_path:
                return f"https://image.tmdb.org/t/p/w500{poster_path}"
    except Exception:
        pass
        
    # Gambar placeholder kalau ada satu dua film yang apes gak ada posternya
    return "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?q=80&w=500&auto=format&fit=crop"

# 1. FUNGSI UNTUK MENGAMBIL REKOMENDASI
def recommend(movie_title):
    # Mengambil indeks film yang dipilih
    movie_index = movies[movies['title'] == movie_title].index[0]
    distances = similarity[movie_index]
    
    # Urutkan berdasarkan kemiripan tertinggi (ambil top 5)
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    recommended_movies = []
    recommended_movie_posters = []
    
    for i in movies_list:
        # Ambil judul film
        recommended_movies.append(movies.iloc[i[0]].title)
        
        # Ambil movie_id asli bawaan TMDB 5000
        movie_id = movies.iloc[i[0]].movie_id
        
        # Cetak log debug ke terminal VS Code biar kelihatan prosesnya
        print(f"Mengambil poster untuk: {movies.iloc[i[0]].title} (ID: {movie_id})")
        
        # Tembak API buat ambil link poster
        recommended_movie_posters.append(fetch_poster(movie_id))
        
    return recommended_movies, recommended_movie_posters

# 2. LOAD DATA BARU (TMDB 5000)
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

with gzip.open('similarity.pkl.gz', 'rb') as f:
    similarity = pickle.load(f)

# 3. LAYOUT UI STREAMLIT (TAMPILAN WEB)
st.set_page_config(page_title="Movie Recommender", layout="wide")

st.title("🎬 Movie Recommender System")
st.write("Cari film mainstream favorit kamu secara instan menggunakan AI + Real-time TMDB API!")

# Dropdown menu berisi list film populer dari TMDB 5000
movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Ketik atau pilih film terakhir yang kamu tonton:",
    movie_list
)

if st.button("Cari Rekomendasi 🚀"):
    with st.spinner("AI lagi mencari film dan poster HD dari server TMDB..."):
        names, posters = recommend(selected_movie)
        
        st.success(f"Karena kamu suka film **{selected_movie}**, nih 5 rekomendasi teratas buat kamu:")
        
        # Bikin 5 kolom horizontal estetik ala Netflix
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.image(posters[0], use_container_width=True)
            st.caption(f"**{names[0]}**")
        with col2:
            st.image(posters[1], use_container_width=True)
            st.caption(f"**{names[1]}**")
        with col3:
            st.image(posters[2], use_container_width=True)
            st.caption(f"**{names[2]}**")
        with col4:
            st.image(posters[3], use_container_width=True)
            st.caption(f"**{names[3]}**")
        with col5:
            st.image(posters[4], use_container_width=True)
            st.caption(f"**{names[4]}**")
