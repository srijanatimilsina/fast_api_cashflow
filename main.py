from fastapi import FastAPI, HTTPException, Query
import csv
from datetime import datetime, timedelta

app = FastAPI()

# Load CSV files
def load_csv(filename):
    data = []
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)
    return data

pnl_data = load_csv("data/pnl.csv")
working_capital_data = load_csv("data/working_capital.csv")


# Calculate cash flow from operations
def calculate_cash_flow(start_date, analysis_type):
    try:
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")

    operating_cash_flow = 0

    if analysis_type == "monthly":
        end_date = start_date.replace(day=1)
        end_date = end_date.replace(month=end_date.month + 1) - timedelta(days=1)
    elif analysis_type == "quarterly":
        quarter = (start_date.month - 1) // 3
        quarter_start_month = quarter * 3 + 1
        end_date = start_date.replace(month=quarter_start_month, day=1)
        end_date = end_date.replace(month=end_date.month + 3) - timedelta(days=1)
    elif analysis_type == "yearly":
        end_date = start_date.replace(month=1, day=1)
        end_date = end_date.replace(year=end_date.year + 1) - timedelta(days=1)

    for pnl_row in pnl_data:
        pnl_date = datetime.strptime(pnl_row["Date"], "%Y-%m-%d")
        if start_date <= pnl_date <= end_date:
            pnl_net_income = float(pnl_row["Net_Income"])
            pnl_depreciation = float(pnl_row["Depreciation"])
            working_capital_row = next((wc_row for wc_row in working_capital_data if wc_row["Date"] == pnl_row["Date"]), None)
            if working_capital_row:
                inventory = float(working_capital_row["Inventory"])
                accounts_receivable = float(working_capital_row["Accounts_Receivable"])
                accounts_payable = float(working_capital_row["Accounts_Payable"])
                operating_cash_flow += pnl_net_income - pnl_depreciation + (inventory - accounts_payable + accounts_receivable)
                
    return {
        "operating_cash_flow": operating_cash_flow
    }


# Endpoint for cash flow analysis
@app.get("/cash-flow/")
async def cash_flow_analysis(start_date: str = Query(..., description="Start date for analysis (YYYY-MM-DD)"),
                             analysis_type: str = Query(..., description="Analysis type: 'monthly', 'quarterly', or 'yearly'")):
    if analysis_type not in ["monthly", "quarterly", "yearly"]:
        raise HTTPException(status_code=400, detail="Invalid analysis type. Choose 'monthly', 'quarterly', or 'yearly'.")

    cash_flow = calculate_cash_flow(start_date, analysis_type)
    return {"cash_flow": cash_flow}
