## AI-Powered News Aggregator & Digest Agent

This project is a multi-agent system that automatically tracks developments in the world of artificial intelligence, analyzes them, prepares a digest of news personalized to the user's interests, and sends it to the user by e-mail.

---

## Key Features

* **Automatic Data Collection:** Automatically scans the latest news and videos from OpenAI, Anthropic and selected YouTube channels.
* **Data Analysis:** The collected data is analyzed with **Groq (Llama 3.3)**, summaries are prepared and items are grouped into categories by topic.
* **Personalized Ranking (Curator Agent):** News items are ranked by the "Curator Agent" according to the user's profile and area of interest.
* **News Digest via E-mail:** The main news and videos matching the user's interests are composed in HTML format and sent via Gmail.

---

## Technologies Used:

| Technology | Purpose |
| :--- | :--- |
| **Python 3.14+** | Main programming language |
| **Groq API** | Fast LLM processing with the Llama-3.3-70b model |
| **Supabase (PostgreSQL)** | Data storage (Repository pattern) |
| **Pydantic** | Data validation and structuring |
| **uv** | Modern Python package and dependency management |
| **SMTP / SSL** | Secure e-mail delivery |

---

## Folder Structure

```
ai-news-aggregator/
├── app/
│   ├── agent/          # LLM Agents (Curator, Digest, Email)
│   ├── database/       # Supabase connection and Repository pattern
│   ├── scrapers/       # YouTube, OpenAI and Anthropic scrapers
│   ├── services/       # Business logic and e-mail service
│   └── config.py       # System settings
├── main.py             # Main entry point of the application
├── daily_runner.py     # Script that manages the entire pipeline
└── pyproject.toml      # Project dependencies
```
---

## How Does It Work?

The system is built on a pipeline consisting of 5 main stages:

*  **Scraping:** Data is collected from the sources (RSS, YouTube API, Markdown).
*  **Processing:** Video transcripts and articles are cleaned and written to the database.
*  **Digesting:** The AI reads each item and prepares a summary.
*  **Ranking:** The 10 most important news items are selected according to the user's area of interest.
*  **Emailing:** The selected news items are placed into an HTML template and sent to the user.

---

## Setup and Usage

1. **Clone the repository:**
   git clone https://github.com/azizmirz/ai-news-aggregator.git

2. **Install the dependencies:**
   uv sync

3. **Prepare the environment (.env) file:**
   ```
   GROQ_API_KEY=your_groq_key
   MY_EMAIL=your_gmail_address
   APP_PASSWORD=google_app_password
   DATABASE_URL=supabase_repository_url

4. **Start the system:**
   Run the **main.py** file to launch the entire pipeline


* **Note:** Optionally, you can adjust the number of hours and the number of news items: **python main.py 48 20**
