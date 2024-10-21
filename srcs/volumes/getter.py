import logging
from flask import Flask, request, jsonify, abort
logging.basicConfig(level=logging.DEBUG, format='%(message)s')

# Recover the load data from the request
def get_and_parse_load(data):
    load = data['load']
    try:
        load = int(load)
        if load <= 0:
            abort(400, description="Invalid load value")
    except (ValueError, TypeError):
        abort(400, description="Load must be an integer")
    return load

# Recover the fuels data from the request
def get_and_parse_fuels(data):
    fuels = data['fuels']
    if not fuels:
        abort(400, description="No fuels provided")
    gas = fuels['gas(euro/MWh)']
    try:
        gas = int(gas)
        if gas <= 0:
            abort(400, description="Invalid gas value")
    except (ValueError, TypeError):
        abort(400, description="Fuels must be integers")
    kerosine = fuels['kerosine(euro/MWh)']
    try:
        kerosine = int(kerosine)
        if kerosine <= 0:
            abort(400, description="Invalid kerosine value")
    except (ValueError, TypeError):
        abort(400, description="Fuels must be integers")
    wind = fuels['wind(%)']
    try:
        wind = int(wind)
        if wind < 0:
            abort(400, description="Invalid wind value")
    except (ValueError, TypeError):
        abort(400, description="Fuels must be integers")
    return fuels

# Recover the data from the request
def get_and_parse_powerplants(data):
    powerplants = data['powerplants']
    if not powerplants:
        abort(400, description="No powerplants provided")
    
    for powerplant in powerplants:
        name = powerplant['name']
        if not name:
            abort(400, description="No powerplant name provided")
        type = powerplant['type']
        if not type or type not in ["windturbine", "gasfired", "turbojet"]:
            abort(400, description="Invalid powerplant type")
        efficiency = powerplant['efficiency']
        try :
          efficiency = int(efficiency)
          if efficiency < 0 or efficiency > 1:
              abort(400, description="Invalid efficiency value")
        except (ValueError, TypeError):
            abort(400, description="Efficiency must be an integer")
        pmin = powerplant['pmin']
        try :
          pmin = int(pmin)
          if pmin < 0 :
              abort(400, description="Invalid pmin value")
        except (ValueError, TypeError):
            abort(400, description="Pmin must be an integer")
        pmax = powerplant['pmax']
        try :
          pmax = int(pmax)
          if pmax <= 0 :
              abort(400, description="Invalid pmax value")
        except (ValueError, TypeError):
            abort(400, description="Pmax must be an integer")
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