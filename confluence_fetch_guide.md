# Confluence Data Fetch Automation Guide

This guide explains how to automatically fetch and convert Confluence pages to Markdown files using a Python script. It is designed for beginners and covers every step from setup to execution.

---

## What Is This?

This project provides a Python script to:

- Connect to your Atlassian Confluence workspace using the REST API
- Download all pages from a specified Confluence space
- Convert the content to Markdown
- Save the results in a local folder for further use (e.g., training AI models)

---

## Why Use This?

- **No more manual copy-pasting**: Automate the process of exporting Confluence content.
- **Keep your docs up-to-date**: Easily re-run the script to fetch the latest changes.
- **Markdown output**: Use the exported files for documentation, training data, or backups.

---

## Prerequisites

- Python 3 installed (use `python3` on macOS)
- Access to your Confluence workspace
- Your Atlassian account email
- A Confluence API token

---

## 1. Get Your Confluence API Access

### a. Find Your Confluence Base URL

- Example: `https://yourcompany.atlassian.net/wiki`
- For LF Technology: `https://lftechnology.atlassian.net/wiki`

### b. Get Your Email

- Use the email you use to log in to Confluence (e.g., `purnashrestha@lftechnology.com`)

### c. Generate an API Token

1. Go to [Atlassian API tokens](https://id.atlassian.com/manage-profile/security/api-tokens)
2. Click **Create API token**
3. Give it a name and copy the token

---

## 2. Find Your Confluence Space Key

- Go to the space in your Confluence site
- Look at the URL: `https://lftechnology.atlassian.net/wiki/spaces/HR/pages/123456789/Some-Page-Title`
- The part after `/spaces/` (e.g., `HR`) is your **space key**

---

## 3. Set Up Your Environment

### a. Clone or Download This Project

### b. Edit the `.env` File

Add the following lines (replace with your actual values):

```
CONFLUENCE_BASE_URL="https://lftechnology.atlassian.net/wiki"
CONFLUENCE_EMAIL="your-email@example.com"
CONFLUENCE_API_TOKEN=your-api-token-here
CONFLUENCE_SPACE_KEY=YOURSPACEKEY
```

### c. Install Python Dependencies

Run this command in your terminal:

```
python3 -m pip install -r requirements.txt
```

---

## 4. How to Run the Script

In your terminal, run:

```
python3 confluence_fetch.py
```

- If all values are set in `.env`, the script will run without prompts.
- If `CONFLUENCE_SPACE_KEY` is not set, you will be prompted to enter it.
- The script will fetch all pages from the specified space and save them as markdown files in the `docs-confluence/` folder.

---

## 5. Troubleshooting

- **pip not found**: Use `python3 -m pip` instead of `pip`.
- **Authentication errors**: Double-check your email and API token in `.env`.
- **Permission errors**: Make sure your account has access to the Confluence space.
- **Dependencies missing**: Ensure you ran the install command above.

---

## 6. Updating or Re-running

- To fetch the latest content, just run the script again.
- To change the space, update `CONFLUENCE_SPACE_KEY` in `.env` or leave it blank to be prompted.

---

## 7. Security Note

- **Never share your API token publicly.**
- Keep your `.env` file private and out of version control (add `.env` to `.gitignore`).

---

## 8. Useful Links

- [Atlassian API tokens](https://id.atlassian.com/manage-profile/security/api-tokens)
- [Confluence REST API docs](https://developer.atlassian.com/cloud/confluence/rest/)

---

## 9. Example `.env` File

```
CONFLUENCE_BASE_URL="https://lftechnology.atlassian.net/wiki"
CONFLUENCE_EMAIL="purnashrestha@lftechnology.com"
CONFLUENCE_API_TOKEN=your-api-token-here
CONFLUENCE_SPACE_KEY=HR
```

---

## 10. Example Output

- After running the script, you will find markdown files for each Confluence page in the `docs-confluence/` folder.

---

## 11. Support

If you have issues, contact your admin or ask for help in your team’s support channel.
