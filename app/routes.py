from flask import Blueprint, request, jsonify
import pandas as pd
from .llm_integration import generate_insights_prompt, generate_feedback
from datetime import datetime
main = Blueprint('main', __name__)


all_sheets = pd.read_excel("dataa.xlsx", sheet_name=None)

# Access each sheet from the dictionary
building_table = all_sheets['building_table']
history_table = all_sheets['unit_table']
unit_table = all_sheets['history_table']




def read_data(filepath, format):
    if format == 'csv':
        return pd.read_csv(filepath)
    elif format == 'json':
        return pd.read_json(filepath)
    else:
        raise ValueError("Unsupported file format")

@main.route("/api/sales_rep_feedback", methods=["POST"])
def sales_rep_feedback():
    # Get parameters from the request
    data = request.json
    sales_rep_id = data.get("sales_rep_id")
    
    # Filter sales data for the specified sales representative
    sales_rep_sales = unit_table[unit_table["unit_id"] == sales_rep_id]
    
    # Extract total prices, sales, and dates
    total_prices = sales_rep_sales["price"].tolist()
    sales_dates = sales_rep_sales["created_on"].tolist()
    total_sales = len(total_prices)
    
    # Generate feedback message
    feedback = {
        "sales_rep_id": sales_rep_id,
        "total_sales": total_sales,
        "total_prices": total_prices,
        "sales_dates": sales_dates
    }
    feedback1 = generate_feedback(total_prices, sales_dates)
    
    return jsonify({"feedback": feedback1})
    
    # return jsonify(feedback)


@main.route('/api/team_performance', methods=['GET'])

def assess_team_performance():
    # Load Sales Data Sheet
    
    sales_data = unit_table[['unit_id', 'price', 'created_on']]
    
    # Load Unit Information Sheet
   
    unit_info = history_table[['building_id', 'price', 'available date']]
    
    # Calculate total sales volume
    total_sales_volume = len(sales_data)
    
    # Calculate average sale price
    average_sale_price = sales_data['price'].mean()
    
    # Identify sales trends over time
    sales_data['created_on'] = pd.to_datetime(sales_data['created_on'])
    sales_data['month_year'] = sales_data['created_on'].dt.to_period('M')
    sales_trends = sales_data.groupby('month_year').size().reset_index(name='sales_count')
    sales_trends['month_year'] = sales_trends['month_year'].astype(str)  # Convert Period to string
    
    
    # Assess unit availability and pricing
     # Clean up available_date column
    unit_info['available date'] = unit_info['available date'].apply(lambda x: x if isinstance(x, datetime) else pd.NaT)
    available_units_count = len(unit_info[unit_info['available date'].notnull()])
    average_unit_price = unit_info['price'].mean()
    
    # Generate insights
    insights = {
        "total_sales_volume": total_sales_volume,
        "average_sale_price": average_sale_price,
        "sales_trends": sales_trends.to_dict(orient='records'),
        "available_units_count": available_units_count,
        "average_unit_price": average_unit_price
    }
    feedback2=generate_insights_prompt(insights)
    return jsonify({"feedback": feedback2})
    # return jsonify(insights)

# @main.route('/api/trends_forecasting', methods=['GET'])
# def trends_forecasting():
#     data = read_data('path/to/historical_data.csv', 'csv')
#     prompt = "Forecast the sales performance trends based on this data."
#     insight = ask_gpt(prompt)
#     return jsonify({"insight": insight})
