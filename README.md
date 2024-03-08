## Setup

1. Clone the repository:

   git clone https://github.com/srijanatimilsina/fast_api_cashflow.git

2. Navigate to the project directory:
   cd fast_api_cashflow

3. Create and activate a virtual environment
   python -m venv venv
   source venv/bin/activate
4. Install dependencies:
   pip install -r requirements.txt
5. Run the FastAPI application:
   uvicorn main:app --reload
   The API will be available at http://127.0.0.1:8000.

Cash Flow Analysis

- Endpoint: /cash-flow/
- Parameters:
  start_date (str): Start date for analysis in the format YYYY-MM-DD.
  analysis_type (str): Analysis type, choose from 'monthly', 'quarterly', or 'yearly'.
- Example Usage:
  /cash-flow/?start_date=2022-01-01&analysis_type=monthly

Run tests with:
pytest test_main.py
