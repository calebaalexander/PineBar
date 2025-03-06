import pandas as pd
import numpy as np

def generate_data(option):
    """
    Generate synthetic data for Pine Bar analytics
    
    Parameters:
    option (str): Data period option, one of "2023 Full Year", "2024 Full Year", or "2025 (up to March 5)"
    
    Returns:
    pandas.DataFrame: Generated data
    """
    # Categories and items
    categories = {
        "BEER": ["Hemlock", "CURRENT CAN", "GANSETT", "N/A BEER", "Return Beer", "SIX POINT", "Vermonter Cider"],
        "COCKTAILS": ["BEAD & FEATHER", "BLACK MANHATTAN", "CARPETBAGGER", "COCKTAIL OF THE DAY", 
                     "COCKTAIL SHAKEN", "COCKTAIL STIRRED", "Daiquiri", "Gershwin", "Gimlet", 
                     "Gin & Sin", "HAITIAN DIVORCE", "HOT DRINX", "Manhattan", "Margarita", 
                     "Martini Gin", "Martini Vodka", "Negroni", "Old Fashioned", "Open Cocktail", 
                     "Paper Plane", "Penicillin", "Pineapple Daiq", "pineapple daiquiri", 
                     "POP-UP COCKTAIL", "Rainy Day Dark And Stormy", "SAZERAC COCKTAIL", 
                     "SHOOTER", "Soda", "SPRITZ", "TITOS MARTINI", "TONE POLICE"],
        "FOOD": ["BABA GHANO0USH", "BEEF TARTARE", "BITTER SALAD", "BOQUERONES", "BROWNIE", 
                "Burger", "CARROTS", "CAVIAR DOG", "CHARRED BEETS", "CHICKEM KEBAB", 
                "CHX SANDWICH", "CROQUETTES", "Doggie", "DUCK RILLETTES", "EXTRA FOCACCIA", 
                "Extra Patty", "FALAFEL", "FOCACCIA", "FRENCH FRIES", "Fries", "HANDER STEAK", 
                "HUMMUS", "LAMB KABAB", "LEEK TOAST", "MEZE PLATTER", "MEZE PLATTY", "PLATTY", 
                "MOUSSE", "MOZZ STICKS", "MUHAMMARA", "NYE TACOS", "OLIVES AND PICKELS", 
                "Open Food", "Order note", "Pimento Cheese", "Salad", "SAUSAGE", "SEA TROUT", 
                "Smash - Vegan Patty", "STEAK FRITES", "SUNCHOKES", "TOSTADA", "TZATZIKI", "VCC"],
        "SPIRITS": ["AMARGO VALLET", "Amaro", "Balvenie", "Bourbon", "BW WHEAT", "CAMPARI", 
                   "CASCUIN TAHONA", "CURRENT CASSIS", "CYNAR", "EL DORADO 12", "ESPOLON", 
                   "Fernet", "Gin", "Hendricks", "Juice", "Macallan 18", "Makers", "Mezcal", 
                   "Michters", "MONTENEGRO", "NONINO", "OLD FORESTER 100", "Open Spirit", 
                   "Rare Breed", "RITTENHOUSE", "Rum", "SAZERAC", "Scotch", "SHOT 4$", 
                   "SHOT 5$", "SHOT 6$", "SHOT 7$", "SHOT 8$", "SHOT 9$", "Spirit", 
                   "SUZE", "Talisker", "Tequila", "TEREMANA REPOSADO", "Tesoro", "Titos", 
                   "Toki", "TULLY", "Vodka", "Wathen's", "ZACAPA"],
        "WINE": ["BTL Fizzy", "GLS Fizzy", "GLS Red", "GLS Rose", "GLS White", "OPEN WINE"],
        "N/A": ["Ginger Beer", "Mock Turtleneck", "POP-UP MOCKTAIL"],
        "Merch": ["Candle 2 oz", "Candle 9oz", "Misc", "GIFT CERTIFICATE"]
    }
    
    # Set random seed based on option for consistent results
    if option == "2023 Full Year":
        np.random.seed(2023)
        n_samples = 150
        year = "2023"
    elif option == "2024 Full Year":
        np.random.seed(2024)
        n_samples = 180
        year = "2024"
    else:  # 2025 data
        np.random.seed(2025)
        n_samples = 70
        year = "2025"
    
    # Create empty dataframe
    data = []
    
    # Generate synthetic data for each category
    for category, items in categories.items():
        for item in items:
            # Only include some items to match the number of samples
            if np.random.random() > 0.3:
                # Generate realistic metrics
                total_amount = np.random.randint(500, 25000)
                total_quantity = np.random.randint(10, int(total_amount / 10) + 1)
                transaction_count = np.random.randint(5, min(500, total_quantity + 1))
                
                # Calculate other metrics based on total
                zero_priced = np.random.randint(0, int(total_quantity * 0.05) + 1)
                disc_amount = -np.random.randint(0, int(total_amount * 0.15) + 1) if np.random.random() > 0.3 else 0
                disc_quantity = np.random.randint(0, int(total_quantity * 0.15) + 1) if disc_amount < 0 else 0
                disc_transactions = np.random.randint(0, min(50, disc_quantity + 1)) if disc_quantity > 0 else 0
                
                offered_amount = np.random.randint(0, int(total_amount * 0.1) + 1) if np.random.random() > 0.7 else 0
                offered_quantity = np.random.randint(0, int(total_quantity * 0.05) + 1) if offered_amount > 0 else 0
                offered_transactions = np.random.randint(0, min(20, offered_quantity + 1)) if offered_quantity > 0 else 0
                
                loss_amount = -np.random.randint(0, int(total_amount * 0.1) + 1) if np.random.random() > 0.8 else 0
                loss_quantity = np.random.randint(0, int(total_quantity * 0.05) + 1) if loss_amount < 0 else 0
                loss_transactions = np.random.randint(0, min(10, loss_quantity + 1)) if loss_quantity > 0 else 0
                
                returned_amount = -np.random.randint(0, int(total_amount * 0.05) + 1) if np.random.random() > 0.85 else 0
                returned_quantity = np.random.randint(0, int(total_quantity * 0.03) + 1) if returned_amount < 0 else 0
                returned_transactions = np.random.randint(0, min(5, returned_quantity + 1)) if returned_quantity > 0 else 0
                
                # Calculate final transaction values
                transaction_amount = total_amount + disc_amount + offered_amount + loss_amount + returned_amount
                transaction_quantity = total_quantity - zero_priced - disc_quantity - offered_quantity - loss_quantity - returned_quantity
                if transaction_quantity < 0: transaction_quantity = 0
                
                # Cost and profit
                cost_factor = {
                    "BEER": 0.35 + np.random.random() * 0.1,      # 35-45%
                    "COCKTAILS": 0.25 + np.random.random() * 0.1, # 25-35%
                    "FOOD": 0.4 + np.random.random() * 0.15,      # 40-55%
                    "SPIRITS": 0.3 + np.random.random() * 0.1,    # 30-40%
                    "WINE": 0.45 + np.random.random() * 0.1,      # 45-55%
                    "N/A": 0.15 + np.random.random() * 0.1,       # 15-25%
                    "Merch": 0.5 + np.random.random() * 0.2,      # 50-70%
                }
                
                cost = total_amount * cost_factor[category]
                profit = transaction_amount - cost
                profit_margin = (profit / transaction_amount * 100) if transaction_amount > 0 else 0
                
                data.append({
                    "SKU": item, 
                    "Category": category, 
                    "Total Amount": total_amount, 
                    "Total Quantity": total_quantity, 
                    "Total Transaction Count": transaction_count,
                    "Zero Priced Count": zero_priced, 
                    "Discounted Amount": disc_amount, 
                    "Discounted Quantity": disc_quantity, 
                    "Discounted Transaction Count": disc_transactions,
                    "Offered Amount": offered_amount, 
                    "Offered Quantity": offered_quantity, 
                    "Offered Transaction Count": offered_transactions,
                    "Loss Amount": loss_amount, 
                    "Loss Quantity": loss_quantity, 
                    "Loss Transaction Count": loss_transactions,
                    "Returned Amount": returned_amount, 
                    "Returned Quantity": returned_quantity, 
                    "Returned Transaction Count": returned_transactions,
                    "Transaction Amount": transaction_amount, 
                    "Transaction Quantity": transaction_quantity, 
                    "Transaction Count": transaction_count,
                    "Cost": cost, 
                    "Profit": profit,
                    "Profit Margin": profit_margin,
                    "Year": year
                })
    
    df = pd.DataFrame(data)
    return df
