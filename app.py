import streamlit as st
import requests

def fetch_book_data(api_key, book_title):
    url = f"https://openlibrary.org/search.json?title={book_title}"
    headers = {
        "Authorization": f"Token {api_key}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error fetching data: {response.status_code}")
        return None

def main():
    st.title("OpenLibrary Book Search")
    api_key = st.text_input("Enter your OpenLibrary API Key", type="password")
    book_title = st.text_input("Enter the book title to search")

    if st.button("Search") and api_key and book_title:
        data = fetch_book_data(api_key, book_title)
        if data:
            st.write("Search Results:")
            for book in data.get('docs', []):
                st.write(f"Title: {book.get('title', 'N/A')}")
                st.write(f"Author: {', '.join(book.get('author_name', ['N/A']))}")
                st.write(f"First Publish Year: {book.get('first_publish_year', 'N/A')}")
                st.write("---")

if __name__ == "__main__":
    main()