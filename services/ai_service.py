import os
from google import genai
from utils.config import Config

def get_gemini_client():
    api_key = Config.GEMINI_API_KEY
    if not api_key or api_key == 'your_gemini_api_key_here':
        return None
    try:
        return genai.Client(api_key=api_key)
    except Exception as e:
        print(f"Error initializing Gemini client: {e}")
        return None

def generate_financial_advice(income_total, expenses_by_category, recent_expenses):
    client = get_gemini_client()
    
    if not client:
        return "⚠️ Gemini API key not found or invalid. Please check your .env file to enable AI insights."
    
    prompt = f"""
    You are an advanced AI Financial processor.
    Process the following financial data and output a highly structured, concise, metric-driven report.
    Do NOT write long paragraphs. Use sharp, smart, data-dense formatting.
    
    Data Input:
    - Total Monthly Income: ₹{income_total}
    - Expenses: {expenses_by_category}
    - Recent Logs: {recent_expenses}
    
    Structure the response EXACTLY as follows in Markdown:
    
    ## 🧠 Financial Score
    [Give a score out of 100 based on savings rate]
    
    ## 📊 Financial Overview
    [2-3 bullet points with crisp, data-backed insights on savings rate, largest expense, or income/expense ratio]
    
    ## ⚠️ Spending Alerts
    [If overspending or negative balance is detected, list as quick, sharp warnings with numbers. e.g., "**Food**: Exceeds threshold by 15%"]
    
    ## 💡 Smart Suggestions
    [2-3 short, actionable recommendations to maximize savings. Use bullet points.]
    
    ## 📈 Future Prediction
    [1 short sentence predicting next month's balance if habits continue]
    
    ## 🎯 Budget Plan
    [A concise suggested budget breakdown using a markdown table: Category | Suggested % | Suggested ₹]
    
    ## 🤖 AI Confidence
    [State your confidence level in these insights based on the amount of data provided (e.g., High, Medium, Low)]
    """
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        return response.text
    except Exception as e:
        print(f"Error generating content: {e}")
        return "Sorry, I couldn't generate the financial advice at this time. Please try again later."
