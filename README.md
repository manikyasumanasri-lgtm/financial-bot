# Personal Finance Advisor Bot

A full-stack AI-powered web application using Python Flask for the backend and a modern responsive frontend using HTML, CSS, JavaScript, and Tailwind CSS. The application helps users manage personal finances, analyze spending habits, generate AI-powered budget plans, and provide saving recommendations.

## Features
- **User Authentication:** Secure signup and login system.
- **Dashboard:** Overview of income, expenses, balance, and saving goals with charts.
- **Income & Expense Management:** Add, edit, delete, and categorize financial records.
- **AI Budget Planner:** AI-generated personalized monthly budgets and savings targets using Gemini.
- **Spending Analysis:** Detects overspending categories and provides smart insights.
- **Integrations:** Future-ready integrations with Google Sheets and Notion.

## Prerequisites
- Python 3.8+

## Setup Instructions

1. **Clone or Download the Repository**
2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
3. **Configuration**
   Copy the `.env.example` file to `.env` and fill in your API keys.
   ```bash
   cp .env.example .env
   ```
4. **Run the Application**
   ```bash
   python app.py
   ```
5. **Access the App**
   Open your browser and navigate to `http://localhost:5000`

## Environment Variables
- `SECRET_KEY`: Flask secret key for sessions.
- `DATABASE_URL`: Database URI (defaults to `sqlite:///finance.db`).
- `GEMINI_API_KEY`: API key for Google Gemini (required for AI features).
- `NOTION_API_KEY`: API key for Notion integration.
- `GOOGLE_SHEETS_CREDENTIALS`: Credentials for Google Sheets integration.
