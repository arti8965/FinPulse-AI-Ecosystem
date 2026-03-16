import numpy as np

def predict_wealth(monthly_savings, years, interest_rate=7):
    # Monthly interest rate
    r = (interest_rate / 100) / 12
    # Total months
    n = years * 12
    # Future Value Formula
    future_value = monthly_savings * (((1 + r)**n - 1) / r)
    
    # Growth data for chart
    months = np.arange(1, n + 1)
    growth_data = [monthly_savings * (((1 + r)**i - 1) / r) for i in months]
    
    return round(future_value, 2), growth_data