import requests
import pandas as pd
import time

languages = {
    "English": "en",
    "Hindi": "hi",
    "Marathi": "mr",
    "Sanskrit": "sa"
}

queries = {
    "English": [
        "fiction",
        "novel",
        "fantasy",
        "history",
        "science"
    ],
    "Hindi": [
        "हिंदी",
        "प्रेम",
        "कहानी",
        "उपन्यास"
    ],
    "Marathi": [
        "मराठी",
        "कथा",
        "कादंबरी",
        "साहित्य"
    ],
    "Sanskrit": [
        "संस्कृत",
        "रामायण",
        "महाभारत",
        "वेद"
    ]
}

all_books = []


for language_name, language_code in languages.items():

    print()
    print(f"========== {language_name} ==========")

    titles = set()

    for query in queries[language_name]:

        if len(titles) >= 100:
            break

        print(f"Searching: {query}")

        for start in range(0, 200, 40):

            if len(titles) >= 100:
                break

            try:

                response = requests.get(
                    "https://www.googleapis.com/books/v1/volumes",
                    params={
                        "q": query,
                        "langRestrict": language_code,
                        "startIndex": start,
                        "maxResults": 40,
                        "printType": "books"
                    },
                    timeout=30
                )

                response.raise_for_status()

                data = response.json()

                for item in data.get("items", []):

                    info = item.get(
                        "volumeInfo", {}
                    )

                    title = info.get(
                        "title", ""
                    ).strip()

                    if not title:
                        continue

                    language = info.get(
                        "language", ""
                    ).lower()

                    if language != language_code:
                        continue

                    title_key = title.lower()

                    if title_key in titles:
                        continue

                    authors = ", ".join(
                        info.get(
                            "authors", []
                        )
                    )

                    categories = info.get(
                        "categories", []
                    )

                    genre = ", ".join(
                        categories
                    )

                    year = info.get(
                        "publishedDate", ""
                    )

                    year = str(year)[:4]

                    image_links = info.get(
                        "imageLinks", {}
                    )

                    cover_url = (
                        image_links.get(
                            "thumbnail",
                            ""
                        )
                    )

                    all_books.append({
                        "title": title,
                        "author": authors,
                        "language": language_name,
                        "genre": genre,
                        "year": year,
                        "cover_url": cover_url
                    })

                    titles.add(title_key)

                    if len(titles) >= 100:
                        break

                time.sleep(0.5)

            except Exception as e:

                print(
                    f"Error: {e}"
                )
                break

        print(
            f"Valid books: {len(titles)}"
        )

    print(
        f"Final {language_name}: "
        f"{len(titles)} books"
    )


books = pd.DataFrame(
    all_books,
    columns=[
        "title",
        "author",
        "language",
        "genre",
        "year",
        "cover_url"
    ]
)

books = books.drop_duplicates(
    subset=[
        "title",
        "author",
        "language"
    ]
)

books.to_csv(
    "books.csv",
    index=False,
    encoding="utf-8-sig"
)

print()
print("=" * 40)
print("DATASET CREATED")
print("=" * 40)
print()
print("Total books:", len(books))
print()
print("Books by language:")
print(
    books["language"].value_counts()
)