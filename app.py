import streamlit as st
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

st.title("📚 Book Recommendation System")
st.write(
    "Discover books using similarity, genre, author, or language."
)

st.sidebar.header("Recommendation Type")

mode = st.sidebar.selectbox(
    "Choose an option",
    [
        "Similar Book",
        "By Genre",
        "By Author",
        "By Language"
    ]
)


def display_books(result):

    if result.empty:
        st.warning("No books found.")
        return

    cols = st.columns(4)

    for i, (_, book) in enumerate(result.iterrows()):

        with cols[i % 4]:

            if book["cover_url"]:
                st.image(
                    book["cover_url"],
                    use_container_width=True
                )
            else:
                st.markdown("### 📖")

            st.subheader(book["title"])

            st.write(
                f"**Author:** {book['author']}"
            )

            st.write(
                f"**Language:** {book['language']}"
            )

            st.write(
                f"**Genre:** {book['genre']}"
            )

            st.write(
                f"**Year:** {book['year']}"
            )


if mode == "Similar Book":

    st.header("Find Similar Books")

    title = st.selectbox(
        "Select a book",
        books["title"].tolist()
    )

    if st.button("Recommend Books"):

        result = recommend_similar(title)

        display_books(result)


elif mode == "By Genre":

    st.header("Find Books by Genre")

    genres = sorted(
        books["genre"].unique()
    )

    genre = st.selectbox(
        "Select genre",
        genres
    )

    if st.button("Find Books"):

        result = recommend_genre(genre)

        display_books(result)


elif mode == "By Author":

    st.header("Find Books by Author")

    authors = sorted(
        books["author"].unique()
    )

    author = st.selectbox(
        "Select author",
        authors
    )

    if st.button("Find Books"):

        result = recommend_author(author)

        display_books(result)


elif mode == "By Language":

    st.header("Find Books by Language")

    language = st.selectbox(
        "Select language",
        [
            "English",
            "Hindi",
            "Marathi",
            "Sanskrit"
        ]
    )

    if st.button("Find Books"):

        result = recommend_language(language)

        display_books(result)


st.divider()

st.caption(
    f"📚 {len(books)} books | "
    f"{books['language'].nunique()} languages"
)