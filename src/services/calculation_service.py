from datetime import datetime
from src.repositories.calculation_repository import get_monthly_data
from src.entities.calculation_entity import calculate_rates

def perform_calculations(data, mongo): 
    results = {}
    current_month = datetime.now().month
    current_year = datetime.now().year
    
    for well in data['wells']:
        separator_type = well.get("separator_type")
        if not separator_type:
            continue

        db_results = get_monthly_data(mongo, separator_type, current_year, current_month) 
        
        if db_results:
            results[well['well_id']] = calculate_rates(db_results, well)
    
    return results
