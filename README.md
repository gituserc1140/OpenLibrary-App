# OpenLibrary-App

OpenLibrary-App is a Streamlit application that lets users search OpenLibrary for books from a simple web interface.

## Features

- Search books by title
- Display title, author, and first publish year
- Built-in app-side rate limiting (5 searches per 60 seconds per browser session)
- Built-in GitHub Repository and GitHub Sponsors buttons

## How it works

1. The user enters a book title in the Streamlit frontend.
2. The app enforces a per-session rate limit of 5 searches per 60 seconds.
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

## Usage

1. Open the Streamlit URL shown in your terminal.
2. Enter a book title.
3. Click **Search** to view results.
4. If you exceed 5 searches within 60 seconds in the same browser session, wait for the cooldown message and retry.
5. Use the GitHub and GitHub Sponsors buttons at the top of the app to visit project/support pages.

## Reference

This app concept is similar to: https://github.com/gituserc1140/TranscriptionApp  
Both apps are Streamlit-based tools that collect user-provided input in the frontend and then process results from an external API workflow.
