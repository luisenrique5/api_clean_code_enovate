def calculate_rates(db_results, well):
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
        
        fcat = well['fcat'] / 100
        water_cut = well['water_cut'] / 100
        oil_rate = monthly_liquid_avg * fcat * (1 - water_cut)
        gas_rate = monthly_gas_avg * fcat 
        water_rate = monthly_liquid_avg * fcat * water_cut

        return {
            'oil_rate': oil_rate,
            'gas_rate': gas_rate,
            'water_rate': water_rate
        }
    else:
        return {}
