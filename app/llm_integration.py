from openai import OpenAI
from os import getenv
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Access the API key
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

def generate_feedback(total_prices, sales_dates):
    # Concatenate total prices and sales dates into a single input string
    sales_dates_str = [date.strftime('%Y-%m-%d %H:%M:%S') for date in sales_dates]
    input_text = "Total prices: {}\nSales dates: {}".format(", ".join(map(str, total_prices)), ", ".join(sales_dates_str))
    
    # Construct a prompt with the input text and desired context
    prompt = """
    Provide performance feedback based on the following sales data:

    Total prices: {}
    Sales dates: {}

    Feedback:
    """.format(", ".join(map(str, total_prices)), ", ".join(sales_dates_str))
    
    # Request feedback from GPT-3
    response = client.chat.completions.create(
        model="gpt-4",  # Specify the model to use (e.g., gpt-4)
        messages=[
            {"role": "system", "content": "User: " + prompt}
        ],
        max_tokens=200  # Maximum number of tokens for the response
    )
    
    return response.choices[0].message.content
def generate_insights_prompt(team_performance):
    # Define the prompt
    prompt = f"Team Performance Insights:\n\nTotal sales volume: {team_performance['total_sales_volume']}\nAverage sale price: {team_performance['average_sale_price']}\nSales trends over time: {team_performance['sales_trends']}\nAvailable units count: {team_performance['available_units_count']}\nAverage unit price: {team_performance['average_unit_price']}\n\nGenerate insights based on the team performance metrics provided above."

    # Request insights from GPT-4
    response = client.chat.completions.create(
        model="gpt-4",  # Specify the model to use (e.g., gpt-4)
        messages=[
            {"role": "system", "content": "User: " + prompt}
        ],
        max_tokens=200  # Maximum number of tokens for the response
    )

    # Extract the generated insights from the response
    return response.choices[0].message.content
