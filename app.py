import streamlit as st
import requests

GITHUB_REPO_URL = "https://github.com/gituserc1140/OpenLibrary-App"
GITHUB_SPONSORS_URL = "https://github.com/sponsors/gituserc1140"

def fetch_book_data(api_key, book_title):
    url = f"https://openlibrary.org/search.json?title={book_title}"
    headers = {
        "Authorization": f"Token {api_key}",
        "X-API-Key": api_key,
        "User-Agent": "OpenLibrary-App"
    }

    try:
        response = requests.get(url, headers=headers, timeout=15)
    except requests.RequestException as exc:
        st.error(f"Network error while fetching data: {exc}")
        return None

    if response.status_code in (401, 403):
        st.error("The API key was rejected. Please check your key and try again.")
        return None

    if response.status_code == 200:
        try:
            return response.json()
        except ValueError:
            st.error("Received an invalid response from OpenLibrary.")
            return None

    st.error(f"Error fetching data: {response.status_code}")
    return None

def render_support_links():
    st.subheader("Project Links")
    col1, col2 = st.columns(2)
    with col1:
        st.link_button("GitHub Repository", GITHUB_REPO_URL, use_container_width=True)
    with col2:
        st.link_button("GitHub Sponsors", GITHUB_SPONSORS_URL, use_container_width=True)

def display_search_results(data):
    results = data.get("docs", [])
    if not results:
        st.info("No books found for this title.")
        return None

    st.write("Search Results:")
    for book in results:
        st.write(f"Title: {book.get('title', 'N/A')}")
        st.write(f"Author: {', '.join(book.get('author_name', ['N/A']))}")
        st.write(f"First Publish Year: {book.get('first_publish_year', 'N/A')}")
        st.write("---")

def main():
    st.set_page_config(page_title="OpenLibrary Book Search", page_icon="📚")
    st.title("OpenLibrary Book Search App")
    st.caption("Search books from OpenLibrary using your API key.")

    render_support_links()

    api_key = st.text_input("Enter your OpenLibrary API Key", type="password")
    book_title = st.text_input("Enter the book title to search")

    if not api_key:
        st.warning("Enter an API key to enable search.")

    if st.button("Search", type="primary"):
        if not api_key:
            st.error("API key is required.")
            return
        if not book_title:
            st.error("Please enter a book title.")
            return

        data = fetch_book_data(api_key, book_title)
        if data:
            display_search_results(data)

if __name__ == "__main__":
    main()