# Vyaguta People Data Fetch & Store Automation Guide

This guide explains how to automatically fetch and store complete, up-to-date people data from the Vyaguta API as Markdown files using a Python script. It is designed for beginners and covers every step from setup to execution.

---

## What Is This?

This project provides a Python script to:

- Connect to the Vyaguta API using secure authentication
- Download all people data (with full details for each person)
- Save each person's data as a Markdown file in a local folder (`docs-api/people/`)
- Use the files for fast, reliable queries or as training data for AI models

---

## Why Use This?

- **No more incomplete results**: Always fetch all pages and all details for every person.
- **Fast local queries**: Use the Markdown files for instant answers without hitting the API.
- **Up-to-date data**: Easily re-run the script to refresh your local database.
- **Markdown output**: Use the exported files for documentation, training, or backups.

---

## Prerequisites

- Python 3 installed
- Access to the Vyaguta API (get your refresh token from your admin or Vyaguta account)

---

## 1. Get Your Vyaguta API Access

### a. Get Your Vyaguta Refresh Token

- Ask your admin or check your Vyaguta account settings for your `VYAGUTA_REFRESH_TOKEN`.

### b. Find Your API Base URL

- For Leapfrog: `https://vyaguta.lftechnology.com`

---

## 2. Set Up Your Environment

### a. Clone or Download This Project

### b. Edit the `.env` File

Add the following lines (replace with your actual values):

```
VYAGUTA_REFRESH_TOKEN=your-refresh-token-here
```

### c. Install Python Dependencies

Run this command in your terminal:

```
pip install -r requirements.txt
```

---

## 3. How to Run the Script

In your terminal, run:

```
python fetch_and_store_people_data.py
```

- If all values are set in `.env`, the script will run without prompts.
- The script will fetch all people from the Vyaguta API, fetch full details for each, and save them as markdown files in the `docs-api/people/` folder.

---

## 4. Troubleshooting

- **Authentication errors**: Double-check your refresh token in `.env`.
- **Permission errors**: Make sure your account has access to the Vyaguta API.
- **Dependencies missing**: Ensure you ran the install command above.
- **No files saved**: Check for error messages about missing tokens or API access.

---

## 5. Updating or Re-running

- To fetch the latest people data, just run the script again.
- To change the output folder, edit the script's `save_people_to_markdown` call.

---

## 6. Security Note

- **Never share your refresh token publicly.**
- Keep your `.env` file private and out of version control (add `.env` to `.gitignore`).

---

## 7. Example `.env` File

```
VYAGUTA_REFRESH_TOKEN=your-refresh-token-here
```

---

## 8. Example Output

- After running the script, you will find markdown files for each person in the `docs-api/people/` folder.
- Each file contains all available details for that person.

---

## 9. Support

If you have issues, contact your admin or ask for help in your team’s support channel.
