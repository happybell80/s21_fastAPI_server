"""
Benchmark Rate Calculator Module

This module provides functions for calculating personalized benchmark rates
based on age, income, capital, and other financial parameters.
"""

def calculate_benchmark_rate(age, income, investment, capital, leverage, interate, age_fired, cashflow):
    """
    Calculate the benchmark rate (ROI) and asset return rate (ROA) based on input parameters.
    
    Args:
        age (int): The current age
        income (float): Annual income in 10,000 KRW
        investment (float): Annual investment amount in 10,000 KRW
        capital (float): Total capital in 100,000,000 KRW
        leverage (float): Acceptable leverage ratio as percentage
        interate (float): Interest rate based on credit as percentage
        age_fired (int): Target retirement age
        cashflow (float): Target monthly cash flow at retirement in 10,000 KRW
        
    Returns:
        dict: A dictionary containing calculation results
    """
    # Convert values to appropriate types to ensure calculation works
    age = int(age)
    income = float(income)
    investment = float(investment)
    capital = float(capital)
    leverage = float(leverage)
    interate = float(interate)
    age_fired = int(age_fired)
    cashflow = float(cashflow)
    
    # Constants
    duration = age_fired - age
    cost_of_carry = 0.005  # 0.5% holding cost
    income_tax_rate = 0.2  # 20% income tax
    inflation = 0.025      # 2.5% annual inflation
    
    # Iteratively find the required rate of return
    myinterate = None
    for i in range(1, 1000):
        # Initial values
        net_cash_flow = investment
        net_investment = capital * 10000 + net_cash_flow
        purchased_asset = net_investment / (1 - leverage/100)
        leverage_amount = purchased_asset - net_investment
        sum_asset = purchased_asset
        sum_leverage = leverage_amount
        monthly_cash_flow = 0
        
        # Simulate for each year until retirement
        for j in range(1, duration + 1):
            income_j = income * ((1 + inflation) ** j)
            investment_j = investment * ((1 + inflation) ** j)
            
            # Calculate income and costs
            asset_income = sum_asset * i / 1000
            leverage_cost = sum_leverage * interate / 100
            holding_cost = sum_asset * cost_of_carry
            income_tax = (asset_income - leverage_cost - holding_cost) * income_tax_rate
            
            # Account for inflation
            asset_growth = sum_asset * inflation
            leverage_growth = sum_leverage * inflation
            
            # Calculate cash flows
            asset_cash_flow = asset_income - leverage_cost - holding_cost - income_tax + leverage_growth
            monthly_cash_flow = asset_cash_flow / 12
            net_cash_flow = asset_cash_flow + investment_j
            
            # Update for next year
            net_investment = net_cash_flow
            purchased_asset = net_investment / (1 - leverage/100)
            leverage_amount = purchased_asset - net_investment
            
            sum_asset += asset_growth + purchased_asset
            sum_leverage += leverage_growth + leverage_amount
        
        # Check if we've met the target
        if monthly_cash_flow > cashflow:
            myinterate = i
            break
    
    # Calculate ROA and ROI
    ROA = myinterate / 10 if myinterate is not None else 0
    ROI = round((ROA - (leverage/100) * (interate/100)) / (1 - leverage/100) * 10) / 10
    
    # Return results
    return {
        "benchmark_rate": ROI,
        "asset_return_rate": ROA,
        "age": age,
        "income": income,
        "investment": investment,
        "capital": capital,
        "leverage": leverage,
        "interate": interate,
        "age_fired": age_fired,
        "cashflow": cashflow,
        "years_to_retirement": duration,
        "holding_cost": cost_of_carry * 100,
        "income_tax_rate": income_tax_rate * 100,
        "inflation_rate": inflation * 100,
        "monthly_cash_flow": monthly_cash_flow
    } 