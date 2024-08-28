import json
import os
import random
import matplotlib.pyplot as plt

# Load epidemic data from JSON file
if os.path.exists("epidemics.json"):
    with open("epidemics.json", "r") as f:
        try:
            epidemic_data = json.load(f)
            epidemics = epidemic_data[0]  # Access the dictionary within the list
        except (json.JSONDecodeError, IndexError):
            epidemics = {}
else:
    epidemics = {}

def making_population(params):
    global population
    population = [{'status': 'susceptible', 'days_infected': 0} for _ in range(params['population_size'] - params['initial_infected'])] + \
                 [{'status': 'infected', 'days_infected': 0} for _ in range(params['initial_infected'])]
    random.shuffle(population)

# Data collection
def initialize_data():
    global susceptible_count, infected_count, recovered_count, deceased_count
    susceptible_count = []
    infected_count = []
    recovered_count = []
    deceased_count = []

def simulation_loop(params):
    for day in range(params['simulation_duration']):
        new_infected = 0
        new_recovered = 0
        new_deceased = 0
        
        for person in population:
            if person['status'] == 'infected':
                person['days_infected'] += 1
                # Transmission
                if person['days_infected'] > params['incubation_period']:
                    effective_infection_rate = params['infection_rate']
                    if params['quarantine_start_day'] <= day < params['quarantine_start_day'] + params['quarantine_duration']:
                        effective_infection_rate *= params['quarantine_effectiveness']
                    
                    for other in population:
                        if other['status'] == 'susceptible' and random.random() < effective_infection_rate:
                            other['status'] = 'infected'
                            other['days_infected'] = 0
                            new_infected += 1
                
                # Recovery or Death
                if random.random() < params['recovery_rate']:
                    person['status'] = 'recovered'
                    new_recovered += 1
                elif random.random() < params['death_rate']:
                    person['status'] = 'deceased'
                    new_deceased += 1
                    
            elif person['status'] == 'susceptible':
                # Vaccination
                if random.random() < params['vaccination_rate']:
                    person['status'] = 'recovered'
                    new_recovered += 1

        # Update counts
        susceptible_count.append(sum(1 for p in population if p['status'] == 'susceptible'))
        infected_count.append(sum(1 for p in population if p['status'] == 'infected'))
        recovered_count.append(sum(1 for p in population if p['status'] == 'recovered'))
        deceased_count.append(sum(1 for p in population if p['status'] == 'deceased'))

def plotting(params): 
    plt.figure(figsize=(10, 6))
    plt.plot(range(params['simulation_duration']), susceptible_count, label='Susceptible', color='blue')
    plt.plot(range(params['simulation_duration']), infected_count, label='Infected', color='red')
    plt.plot(range(params['simulation_duration']), recovered_count, label='Recovered', color='green')
    plt.plot(range(params['simulation_duration']), deceased_count, label='Deceased', color='black')
    plt.xlabel('Days')
    plt.ylabel('Population')
    plt.title(f'Epidemic Spread Simulation - {chosen_epidemic}')
    plt.legend()
    plt.show()

def get_custom_parameters():
    print("Enter custom epidemic parameters:")
    disease_name = input("Name of the disease: ")
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

    # Append custom epidemic to the dictionary
    epidemics[disease_name] = custom_params
    save_to_json(epidemics)  # Save the updated dictionary to JSON
    
    return custom_params

def save_to_json(updated_epidemics):
    # Save the entire dictionary as a single element in the list
    with open("epidemics.json", 'w') as f:
        json.dump([updated_epidemics], f, indent=4)

    print(f"Custom epidemic data has been saved to epidemics.json")

# Menu
print("Choose an epidemic:")
for i, epidemic in enumerate(epidemics.keys()):
    print(f"{i + 1}. {epidemic}")
print(f"{len(epidemics) + 1}. Create your own epidemic")

choice = int(input("Enter the number of your choice: ")) - 1
if choice < len(epidemics):
    chosen_epidemic = list(epidemics.keys())[choice]
    params = epidemics[chosen_epidemic]
else:
    chosen_epidemic = 'Custom Epidemic'
    params = get_custom_parameters()

initialize_data()
making_population(params)
simulation_loop(params)
plotting(params)
