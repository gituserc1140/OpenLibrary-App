import streamlit as st
import requests
import time

DEFAULT_GITHUB_REPO_URL = "https://github.com/gituserc1140/OpenLibrary-App"
DEFAULT_GITHUB_SPONSORS_URL = "https://github.com/sponsors/gituserc1140"
APP_USER_AGENT = "OpenLibrary-App/1.0 (https://github.com/gituserc1140/OpenLibrary-App)"
RATE_LIMIT_MAX_REQUESTS = 5
RATE_LIMIT_WINDOW_SECONDS = 60


def is_rate_limited():
    now = time.time()
    window_start = now - RATE_LIMIT_WINDOW_SECONDS
    request_times = st.session_state.get("request_times", [])
    request_times = [timestamp for timestamp in request_times if timestamp >= window_start]

    if len(request_times) >= RATE_LIMIT_MAX_REQUESTS:
        st.session_state["request_times"] = request_times
        retry_after_seconds = max(1, int(request_times[0] + RATE_LIMIT_WINDOW_SECONDS - now))
        return True, retry_after_seconds

    request_times.append(now)
    st.session_state["request_times"] = request_times
    return False, None

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
        "Search public OpenLibrary books. No API key is required for this endpoint."
    )

    render_support_links()

    book_title = st.text_input("Enter the book title to search")

    if st.button("Search", type="primary"):
        is_limited, retry_after_seconds = is_rate_limited()
        if is_limited:
            st.error(f"Rate limit reached. Please wait about {retry_after_seconds} seconds and try again.")
            return
        if not book_title:
            st.error("Please enter a book title.")
            return

        data = fetch_book_data(book_title)
        if data:
            display_search_results(data)

if __name__ == "__main__":
    main()