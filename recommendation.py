import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

books = pd.read_csv("books.csv")

books = books.fillna("")

books["combined_features"] = (
    books["title"] + " " +
    books["author"] + " " +
    books["genre"] + " " +
    books["language"]
)

tfidf = TfidfVectorizer(
    stop_words="english"
)

tfidf_matrix = tfidf.fit_transform(
    books["combined_features"]
)

similarity = cosine_similarity(
    tfidf_matrix
)

indices = pd.Series(
    books.index,
    index=books["title"]
).drop_duplicates()


def recommend_similar(title, number=8):

    if title not in indices:
        return pd.DataFrame()

    idx = indices[title]

    scores = list(
        enumerate(similarity[idx])
    )

    scores = sorted(
        scores,
        key=lambda x: x[1],
        reverse=True
    )

    book_indices = [
        x[0]
        for x in scores[1:number + 1]
    ]

    return books.iloc[book_indices]


def recommend_genre(genre, number=8):

    result = books[
        books["genre"].str.contains(
            genre,
            case=False,
            na=False
        )
    ]

    return result.head(number)


def recommend_author(author, number=8):

    result = books[
        books["author"].str.contains(
            author,
            case=False,
            na=False
        )
    ]

    return result.head(number)


def recommend_language(language, number=8):

    result = books[
        books["language"].str.lower()
        == language.lower()
    ]

    return result.head(number)