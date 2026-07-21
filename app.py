import streamlit as st
import requests
import re

DEFAULT_GITHUB_REPO_URL = "https://github.com/gituserc1140/OpenLibrary-App"
DEFAULT_GITHUB_SPONSORS_URL = "https://github.com/sponsors/gituserc1140"
APP_USER_AGENT = "OpenLibrary-App/1.0 (https://github.com/gituserc1140/OpenLibrary-App)"

def get_expected_access_key():
    raw_key = st.secrets.get("APP_ACCESS_KEY")
    if raw_key is None:
        return ""
    if isinstance(raw_key, str):
        return raw_key.strip()

    st.warning("APP_ACCESS_KEY is configured but not a string. Using fallback key validation instead.")
    return ""

def has_required_character_types(provided_key):
    return (
        len(provided_key) >= 8
        and re.search(r"[a-z]", provided_key)
        and re.search(r"[A-Z]", provided_key)
        and re.search(r"\d", provided_key)
        and re.search(r"[^\w\s]", provided_key)
    )

def validate_access_key(access_key):
    provided_key = access_key.strip()
    if not provided_key:
        return False, "Access key is required."

    expected_key = get_expected_access_key()
    if expected_key:
        if provided_key == expected_key:
            return True, None
        return False, "Access key is invalid."

    if not has_required_character_types(provided_key):
        return False, "Access key must be 8+ chars and include upper/lowercase, a number, and a special character."

    return True, None

def fetch_book_data(book_title):
    url = "https://openlibrary.org/search.json"
    headers = {
        "User-Agent": APP_USER_AGENT
    }

    try:
        response = requests.get(url, headers=headers, params={"title": book_title}, timeout=10)
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
    repo_url = str(st.secrets.get("GITHUB_REPO_URL", DEFAULT_GITHUB_REPO_URL))
    sponsors_url = str(st.secrets.get("GITHUB_SPONSORS_URL", DEFAULT_GITHUB_SPONSORS_URL))

    st.subheader("Project Links")
    col1, col2 = st.columns(2)
    with col1:
        st.link_button("GitHub Repository", repo_url, use_container_width=True)
    with col2:
        st.link_button("GitHub Sponsors", sponsors_url, use_container_width=True)

def display_search_results(data):
    results = data.get("docs", [])
    if not results:
        st.info("No books found for this title.")
        return

    st.write("Search Results:")
    for book in results:
        st.write(f"Title: {book.get('title', 'N/A')}")
        st.write(f"Author: {', '.join(book.get('author_name', ['N/A']))}")
        st.write(f"First Publish Year: {book.get('first_publish_year', 'N/A')}")
        st.write("---")

def main():
    st.set_page_config(page_title="OpenLibrary Book Search", page_icon="📚")
    st.title("OpenLibrary Book Search App")
    st.caption(
        "Search public OpenLibrary books. The access key is an app-level gate configured by this app owner, not OpenLibrary."
    )

    render_support_links()

    if not get_expected_access_key():
        st.info(
            "APP_ACCESS_KEY is not configured, so the fallback key must include upper/lowercase, a number, and a special character."
        )

    access_key = st.text_input("Enter your app access key", type="password")
    book_title = st.text_input("Enter the book title to search")

    if st.button("Search", type="primary"):
        is_valid, error_message = validate_access_key(access_key)
        if not is_valid:
            st.error(error_message)
            return
        if not book_title:
            st.error("Please enter a book title.")
            return

        data = fetch_book_data(book_title)
        if data:
            display_search_results(data)

if __name__ == "__main__":
    main()