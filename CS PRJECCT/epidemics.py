import json 

epidemics = {
    'COVID-19': {
        'population_size': 1000,
        'initial_infected': 10,
        'infection_rate': 0.03,
        'recovery_rate': 0.01,
        'death_rate': 0.002,
        'vaccination_rate': 0.005,                              
        'incubation_period': 5,
        'quarantine_effectiveness': 0.7,
        'quarantine_start_day': 30,
        'quarantine_duration': 50,
        'simulation_duration': 100
    },
    'Black Plague': {
        'population_size': 1000,
        'initial_infected': 10,
        'infection_rate': 0.2,
        'recovery_rate': 0.005,
        'death_rate': 0.1,
        'vaccination_rate': 0.0,  
        'incubation_period': 3,
        'quarantine_effectiveness': 0.2,
        'quarantine_start_day': 20,
        'quarantine_duration': 80,
        'simulation_duration': 100
    },

}

def get_custom_parameters():
    global custom_params
    print("Enter custom epidemic parameters:")
    custom_params = {}
    custom_params['population_size'] = int(input("Population size: "))
    custom_params['initial_infected'] = int(input("Initial infected: "))
    custom_params['infection_rate'] = float(input("Infection rate (e.g., 0.05 for 5%): "))
    custom_params['recovery_rate'] = float(input("Recovery rate (e.g., 0.01 for 1%): "))
    custom_params['death_rate'] = float(input("Death rate (e.g., 0.005 for 0.5%): "))
    custom_params['vaccination_rate'] = float(input("Vaccination rate (e.g., 0.002 for 0.2%): "))
    custom_params['incubation_period'] = int(input("Incubation period (days): "))
    custom_params['quarantine_effectiveness'] = float(input("Quarantine effectiveness (e.g., 0.5 for 50%): "))
    custom_params['quarantine_start_day'] = int(input("Quarantine start day: "))
    custom_params['quarantine_duration'] = int(input("Quarantine duration (days): "))
    custom_params['simulation_duration'] = int(input("Simulation duration (days): "))
    return custom_params

get_custom_parameters()

print(custom_params)


with open("epidemics.json", 'a') as f:
    json.dump(custom_params, f)

