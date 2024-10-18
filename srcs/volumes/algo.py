import logging
from flask import Flask, request, jsonify
logging.basicConfig(level=logging.DEBUG, format='%(message)s')

def get_and_parse_load(data):
    # Recover the data from the request
    load = data['load']
    try:
        load = int(load)
        if load <= 0:
            return jsonify({"error": "Invalid load value"}), 400
    except (ValueError, TypeError):
        return jsonify({"error": "Load must be an integer"}), 400
    return load

def get_and_parse_fuels(data):
    # Recover the data from the request
    fuels = data['fuels']
    if not fuels:
        return jsonify({"error": "No fuels provided"}), 400
    gas = fuels['gas(euro/MWh)']
    try:
        gas = int(gas)
        if gas <= 0:
            return jsonify({"error": "Invalid gas value"}), 400
    except (ValueError, TypeError):
        return jsonify({"error": "Fuels must be integers"}), 400
    kerosine = fuels['kerosine(euro/MWh)']
    try:
        kerosine = int(kerosine)
        if kerosine <= 0:
            return jsonify({"error": "Invalid kerosine value"}), 400
    except (ValueError, TypeError):
        return jsonify({"error": "Fuels must be integers"}), 400
    wind = fuels['wind(%)']
    try:
        wind = int(wind)
        if wind < 0:
            return jsonify({"error": "Invalid wind value"}), 400
    except (ValueError, TypeError):
        return jsonify({"error": "Fuels must be integers"}), 400
    return fuels

def get_and_parse_powerplants(data):
    # Recover the data from the request
    powerplants = data['powerplants']
    if not powerplants:
        return jsonify({"error": "No powerplants provided"}), 400
    
    for powerplant in powerplants:
        name = powerplant['name']
        if not name:
            return jsonify({"error": "No powerplant name provided"}), 400
        type = powerplant['type']
        if not type or type not in ["windturbine", "gasfired", "turbojet"]:
            return jsonify({"error": "No powerplant type provided"}), 400
        efficiency = powerplant['efficiency']
        try :
          efficiency = int(efficiency)
          if efficiency < 0 or efficiency > 1:
              return jsonify({"error": "Invalid efficiency value"}), 400
        except (ValueError, TypeError):
            return jsonify({"error": "Efficiency must be an integer"}), 400
        pmin = powerplant['pmin']
        try :
          pmin = int(pmin)
          if pmin < 0 :
              return jsonify({"error": "Invalid pmin value"}), 400
        except (ValueError, TypeError):
            return jsonify({"error": "Pmin must be an integer"}), 400
        pmax = powerplant['pmax']
        try :
          pmax = int(pmax)
          if pmax <= 0 :
              return jsonify({"error": "Invalid pmax value"}), 400
        except (ValueError, TypeError):
            return jsonify({"error": "Pmax must be an integer"}), 400
    return powerplants

def get_cost_per_efficiency(powerplant, fuels):
    gas_price = fuels['gas(euro/MWh)']
    kerosine_price = fuels['kerosine(euro/MWh)']
    co2_price = fuels['co2(euro/ton)']
    wind_percentage = fuels['wind(%)']
    efficiency = powerplant['efficiency']
    cost_per_mwh = 0

    type = powerplant['type']
    if type == "windturbine":
        cost_per_mwh = 0
    elif type == "turbojet":
        cost_per_mwh = kerosine_price / efficiency
    elif type == "gasfired":
        cost_per_mwh = gas_price / efficiency

    return cost_per_mwh
    
def order_powerplants_by_cost(powerplants, fuels):

    powerplants_ordered_by_cost = []

    for powerplant in powerplants:
          # Get the powerplant's name
          name = powerplant['name']
          logging.debug(f"Processing powerplant: {name}")

          # Get the powerplant's type
          type = powerplant['type']
          logging.debug(f"Powerplant type: {type}")

          # Get the powerplant's efficiency
          efficiency = powerplant['efficiency']
          logging.debug(f"Powerplant efficiency: {efficiency}")

          # Get the powerplant's pmin
          pmin = powerplant['pmin']
          logging.debug(f"Powerplant pmin: {pmin}")

          # Get the powerplant's pmax
          pmax = powerplant['pmax']
          logging.debug(f"Powerplant pmax: {pmax}")

          # Get the powerplant's cost
          cost = get_cost_per_efficiency(powerplant, fuels)

          powerplants_ordered_by_cost.append({"name": name, "cost": cost, "pmax": pmax, "pmin":pmin})

    # Sort the powerplants by cost
    powerplants_ordered_by_cost.sort(key=lambda x: x['cost'])
    logging.debug(f"Powerplants ordered by cost: {powerplants_ordered_by_cost}")
    
    return powerplants

def pick_powerplants(powerplants_ordered_by_cost, load):
    powerplants_selected = []
    remaining_load = load
    for powerplant in powerplants_ordered_by_cost:
        pmax = powerplant['pmax']
        pmin = powerplant['pmin']
        name = powerplant['name']
        if remaining_load >= pmax:
            powerplants_selected.append({"name": name, "p": pmax})
            remaining_load -= pmax
        elif remaining_load >= pmin:
            # Here we could implement a logic to minimize the waste
            powerplants_selected.append({"name": name, "p": remaining_load})
            remaining_load = 0
        if remaining_load == 0:
            break
    logging.debug(f"Powerplants selected: {powerplants_selected}")
    return powerplants_selected

def prduction_plan(data):
    # Recover the data from the request
    logging.debug(f"Received data: {data}")
    load = get_and_parse_load(data)
    logging.debug(f"Received load: {load}")
    fuels = get_and_parse_fuels(data)
    logging.debug(f"Received fuels: {fuels}")
    powerplants = get_and_parse_powerplants(data)
    logging.debug(f"Received powerplants: {powerplants}")

    # Loop through each powerplant
    powerplants_ordered_by_cost = order_powerplants_by_cost(powerplants, fuels)
    logging.debug(f"Response: {powerplants_ordered_by_cost}")

    # Attribute the powerplants to use
    powerplants_selected = pick_powerplants(powerplants_ordered_by_cost, load)
    




    
    
