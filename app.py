import streamlit as st
import pandas as pd

from recommendation import (
    books,
    recommend_similar,
    recommend_genre,
    recommend_author,
    recommend_language
)

st.set_page_config(
    page_title="Book Recommendation System",
    page_icon="📚",
    layout="wide"
)

st.markdown("""
<style>
.main {
    background-color: #f7f9fc;
}

.hero {
    padding: 25px;
    border-radius: 15px;
    background: linear-gradient(135deg, #4f46e5, #7c3aed);
    color: white;
    margin-bottom: 25px;
}

.hero h1 {
    font-size: 40px;
    margin-bottom: 5px;
}

.hero p {
    font-size: 18px;
}

.book-card {
    padding: 18px;
    border-radius: 14px;
    background-color: white;
    border: 1px solid #e5e7eb;
    margin-bottom: 15px;
}

.book-title {
    font-size: 22px;
    font-weight: 700;
}

.book-info {
    color: #555;
    font-size: 15px;
}

.rating {
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)


# ---------- HEADER ----------

st.markdown("""
<div class="hero">
    <h1>📚 Book Recommendation System</h1>
    <p>Discover your next favorite book using intelligent recommendations.</p>
</div>
""", unsafe_allow_html=True)


# ---------- SIDEBAR ----------

st.sidebar.title("📚 Navigation")

option = st.sidebar.radio(
    "Recommendation Type",
    [
        "🔍 Similar Book",
        "📖 By Genre",
        "✍️ By Author",
        "🌐 By Language"
    ]
)

st.sidebar.divider()

st.sidebar.info(
    "This system uses content-based filtering "
    "with TF-IDF and cosine similarity."
)


# ---------- STATISTICS ----------

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "📚 Books",
        f"{len(books):,}"
    )

with col2:
    st.metric(
        "✍️ Authors",
        f"{books['authors_clean'].nunique():,}"
    )

with col3:
    st.metric(
        "⭐ Avg Rating",
        f"{books['average_rating'].mean():.2f}"
    )

with col4:
    st.metric(
        "🌐 Languages",
        f"{books['language_code'].nunique():,}"
    )

st.divider()


# ---------- BOOK CARD ----------

def display_books(results):

    if results.empty:
        st.warning("No books found.")
        return

    for _, book in results.iterrows():

        col1, col2 = st.columns([1, 4])

        with col1:
            image = book["image_url"]

            if pd.notna(image) and image:
                st.image(
                    image,
                    width=140
                )
            else:
                st.write("📚")

        with col2:

            st.markdown(
                f'<div class="book-title">{book["title"]}</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                f'<div class="book-info">'
                f'✍️ <b>Author:</b> {book["authors_clean"]}'
                f'</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                f'<div class="book-info">'
                f'🏷️ <b>Genre:</b> {book["genres_clean"]}'
                f'</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                f'<div class="rating">'
                f'⭐ {book["average_rating"]}/5'
                f'</div>',
                unsafe_allow_html=True
            )

            if pd.notna(book["original_publication_year"]):
                st.write(
                    f"📅 Published: "
                    f"{int(book['original_publication_year'])}"
                )

        st.divider()


# ---------- SIMILAR BOOK ----------

if option == "🔍 Similar Book":

    st.header("🔍 Find Similar Books")

    st.write(
        "Select a book and discover books with similar content."
    )

    titles = sorted(
        books["title"].dropna().unique()
    )

    selected_book = st.selectbox(
        "Select your favorite book",
        titles
    )

    if st.button(
        "✨ Recommend Similar Books",
        use_container_width=True
    ):

        results = recommend_similar(
            selected_book,
            8
        )

        st.subheader(
            f"Books similar to {selected_book}"
        )

        display_books(results)


# ---------- GENRE ----------

elif option == "📖 By Genre":

    st.header("📖 Discover Books by Genre")

    genres = sorted(
        set(
            genre.strip()
            for value in books["genres_clean"]
            for genre in value.split(",")
            if genre.strip()
        )
    )

    selected_genre = st.selectbox(
        "Select a genre",
        genres
    )

    if st.button(
        "✨ Find Books",
        use_container_width=True
    ):

        results = recommend_genre(
            selected_genre,
            8
        )

        st.subheader(
            f"Top {selected_genre} Books"
        )

        display_books(results)


# ---------- AUTHOR ----------

elif option == "✍️ By Author":

    st.header("✍️ Discover Books by Author")

    authors = sorted(
        set(
            author.strip()
            for value in books["authors_clean"]
            for author in value.split(",")
            if author.strip()
        )
    )

    selected_author = st.selectbox(
        "Select an author",
        authors
    )

    if st.button(
        "✨ Find Books",
        use_container_width=True
    ):

        results = recommend_author(
            selected_author,
            8
        )

        st.subheader(
            f"Books by {selected_author}"
        )

        display_books(results)


# ---------- LANGUAGE ----------

else:

    st.header("🌐 Discover Books by Language")

    languages = sorted(
        books["language_code"]
        .dropna()
        .unique()
    )

    selected_language = st.selectbox(
        "Select a language",
        languages
    )

    if st.button(
        "✨ Find Books",
        use_container_width=True
    ):

        results = recommend_language(
            selected_language,
            8
        )

        st.subheader(
            f"Books in {selected_language}"
        )

        display_books(results)


# ---------- FOOTER ----------

st.divider()

st.caption(
    "📚 Book Recommendation System • "
    "Built with Python, Pandas, Scikit-learn & Streamlit"
)