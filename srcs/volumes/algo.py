import logging
from flask import Flask, request, jsonify
from getter import get_and_parse_load, get_and_parse_fuels, get_and_parse_powerplants, get_cost_per_efficiency
logging.basicConfig(level=logging.DEBUG, format='%(message)s')

# Function to order the powerplants by cost per efficiency
def order_powerplants_by_cost(powerplants, fuels):

    powerplants_ordered_by_cost = []

    for powerplant in powerplants:
          # Get the powerplant's name
          name = powerplant['name']

          # Get the powerplant's type
          type = powerplant['type']

          # Get the powerplant's efficiency
          efficiency = powerplant['efficiency']

          # Get the powerplant's pmin
          pmin = powerplant['pmin']
          if (type == "windturbine"):
              pmin = powerplant['pmin'] * (fuels['wind(%)'] / 100)

          # Get the powerplant's pmax
          pmax = powerplant['pmax']
          if (type == "windturbine"):
              pmax = powerplant['pmax'] * (fuels['wind(%)'] / 100)

          # Get the powerplant's cost
          cost = get_cost_per_efficiency(powerplant, fuels)

          powerplants_ordered_by_cost.append({"name": name, "cost": cost, "pmax": pmax, "pmin":pmin})

    # Sort the powerplants by cost
    powerplants_ordered_by_cost.sort(key=lambda x: x['cost'])
    
    return powerplants_ordered_by_cost

# Function to optimize the cost of the powerplants taking into consideration pmin waste
def optimize_last_powerplants(powerplants_ordered_by_cost, remaining_load, powerplants_response):
    # temporary list to store the powerplants that can be used to cover the remaining load
    powerplants_temp = []

    for powerplant in powerplants_ordered_by_cost:
        # if the powerplant is not already in the response
        if powerplant['name'] not in [p['name'] for p in powerplants_response]:
          total_cost = 0
          contribution = 0
          # Waste of pmin - remaining_load
          if powerplant['pmin'] > remaining_load:
              total_cost = powerplant['pmin'] * powerplant['cost']
              contribution = remaining_load
          else:
              total_cost = remaining_load * powerplant['cost']
              # Check if the powerplant can cover the remaining load
              if powerplant['pmax'] > remaining_load:
                  contribution = remaining_load
              else:
                contribution = powerplant['pmax']
          powerplants_temp.append({"name": powerplant['name'], "total_cost": total_cost, "contribution": contribution})

    # Sort the powerplants by total cost
    powerplants_temp.sort(key=lambda x: x['total_cost'])

    # Add the powerplant with the lowest cost to the response
    powerplants_response.append({"name": powerplants_temp[0]['name'], "p": round(powerplants_temp[0]['contribution'], 1)})
    remaining_load -= powerplants_temp[0]['contribution']

    return remaining_load

# Function to attribute the powerplants to use
def pick_powerplants(powerplants_ordered_by_cost, load):
    powerplants_response = []
    remaining_load = load

    for powerplant in powerplants_ordered_by_cost:
        pmax = powerplant['pmax']
        pmin = powerplant['pmin']
        name = powerplant['name']
        if remaining_load >= pmax:
            powerplants_response.append({"name": name, "p": round(pmax, 1)})
            remaining_load -= pmax
        elif remaining_load >= pmin:
            powerplants_response.append({"name": name, "p": round(remaining_load, 1)})
            remaining_load = 0          
        elif remaining_load < pmin and remaining_load > 0:
            # Optimize the cost of the powerplants taking into consideration pmin waste
            remaining_load = optimize_last_powerplants(powerplants_ordered_by_cost, remaining_load, powerplants_response)        
        if remaining_load <= 0 and powerplant not in powerplants_response:
          powerplants_response.append({"name": name, "p": round(remaining_load, 1)})

    return powerplants_response

def prduction_plan(data):
    # Get all data
    load = get_and_parse_load(data)
    fuels = get_and_parse_fuels(data)
    powerplants = get_and_parse_powerplants(data)

    # Loop through each powerplant
    powerplants_ordered_by_cost = order_powerplants_by_cost(powerplants, fuels)

    # Attribute the powerplants to use
    powerplants_response = pick_powerplants(powerplants_ordered_by_cost, load)

    return powerplants_response