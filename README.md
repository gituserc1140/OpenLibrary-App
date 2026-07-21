# OpenLibrary-App

OpenLibrary-App is a Streamlit application that lets users search OpenLibrary for books from a simple web interface.

## Features

- Enter an API key directly in the app UI
- Search books by title
- Display title, author, and first publish year
- Built-in GitHub Repository and GitHub Sponsors buttons

## How it works

1. The user enters an API key in the Streamlit frontend.
2. The app sends requests with the provided key.
3. The app behavior changes based on the key/request result (for example, missing key, rejected key, or successful response).

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

## Usage

1. Open the Streamlit URL shown in your terminal.
2. Enter your API key.
3. Enter a book title.
4. Click **Search** to view results.
5. Use the GitHub and GitHub Sponsors buttons at the top of the app to visit project/support pages.

## Reference

This app concept is similar to: https://github.com/gituserc1140/TranscriptionApp
