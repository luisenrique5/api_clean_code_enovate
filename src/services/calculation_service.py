from datetime import datetime

def perform_calculations(data, mongo):
    results = {}
    current_month = datetime.now().month
    current_year = datetime.now().year
    
    for well in data['wells']:
        separator_type = well.get("separator_type")
        if not separator_type:
            continue

        db_results = mongo.db.tracker_volume.find({
            "separator_type": separator_type,
            "date": {
                "$gte": f"{current_year}-{current_month:02d}-01",
                "$lte": f"{current_year}-{current_month:02d}-{datetime.now().day:02d}"
            }
        })
        
        total_liquid_avg = 0
        total_gas_avg = 0
        count = 0
        
        for result in db_results:
            total_liquid_avg += result['liquid_avg']
            total_gas_avg += result['gas_avg']
            count += 1
        
        if count > 0:
            monthly_liquid_avg = total_liquid_avg / count
            monthly_gas_avg = total_gas_avg / count
            
            oil_rate = monthly_liquid_avg * well['fcat'] * (1 - well['water_cut'])
            gas_rate = monthly_gas_avg * well['fcat'] * well['water_cut']
            results[well['well_id']] = {
                'oil_rate': oil_rate,
                'gas_rate': gas_rate
            }
    
    return results
