import streamlit as st
import requests

GITHUB_REPO_URL = "https://github.com/gituserc1140/OpenLibrary-App"
GITHUB_SPONSORS_URL = "https://github.com/sponsors/gituserc1140"

def is_valid_access_key(access_key):
    return len(access_key.strip()) >= 8

def fetch_book_data(book_title):
    url = f"https://openlibrary.org/search.json?title={book_title}"
    headers = {
        "User-Agent": "OpenLibrary-App"
    }

    try:
        response = requests.get(url, headers=headers, timeout=15)
    except requests.RequestException as exc:
        st.error(f"Network error while fetching data: {exc}")
        return None

    if response.status_code in (401, 403):
        st.error("Request was denied by the service. Please try again later.")
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
    st.caption("Search public OpenLibrary books. This app requires an access key to run searches.")

    render_support_links()

    access_key = st.text_input("Enter your app access key", type="password")
    book_title = st.text_input("Enter the book title to search")

    if not access_key:
        st.warning("Enter an access key to enable search.")

    if st.button("Search", type="primary"):
        if not access_key:
            st.error("Access key is required.")
            return
        if not is_valid_access_key(access_key):
            st.error("Access key must be at least 8 characters.")
            return
        if not book_title:
            st.error("Please enter a book title.")
            return

        data = fetch_book_data(book_title)
        if data:
            display_search_results(data)

if __name__ == "__main__":
    main()