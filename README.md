# OpenLibrary-App

OpenLibrary-App is a Streamlit application that lets users search OpenLibrary for books from a simple web interface.

## Features

- Enter an app access key directly in the app UI
- Optional strict key validation with `APP_ACCESS_KEY` in Streamlit secrets
- Search books by title
- Display title, author, and first publish year
- Built-in GitHub Repository and GitHub Sponsors buttons

## How it works

1. The user enters an app access key in the Streamlit frontend.
2. The app validates the key before allowing searches (if `APP_ACCESS_KEY` is configured, the key must match exactly; otherwise, it must meet strong format requirements).
3. The app sends the search request to OpenLibrary and displays the results.

## Setup and run

### 1) Clone the repository

```bash
git clone https://github.com/gituserc1140/OpenLibrary-App.git
cd OpenLibrary-App
```

### 2) Install dependencies

```bash
pip install streamlit requests
```

### 3) Run the app

```bash
streamlit run app.py
```

### Optional: configure a required access key

Create `.streamlit/secrets.toml` and add:

```toml
APP_ACCESS_KEY = "your-expected-key"
```

## Usage

1. Open the Streamlit URL shown in your terminal.
2. Enter your app access key (must match `APP_ACCESS_KEY` if configured).
   - If `APP_ACCESS_KEY` is not configured, enter a key with 8+ characters that includes uppercase, lowercase, a number, and a special character.
3. Enter a book title.
4. Click **Search** to view results.
5. Use the GitHub and GitHub Sponsors buttons at the top of the app to visit project/support pages.

## Reference

This app concept is similar to: https://github.com/gituserc1140/TranscriptionApp
