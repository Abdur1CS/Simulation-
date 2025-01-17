import json
import random
import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk
import matplotlib.pyplot as plt

# Load epidemic data from JSON file
with open("epidemics.json", "r") as f:
    epidemic_data = json.load(f)
    epidemics = epidemic_data[0]

# Functions for epidemic simulation and plotting
def makingThepopulation(params):
    return [{'status': 'susceptible', 'days_infected': 0} for _ in range(params['population_size'] - params['initial_infected'])] + \
           [{'status': 'infected', 'days_infected': 0} for _ in range(params['initial_infected'])]

def initializeThedata():
    return {
        'susceptible_count': [],
        'infected_count': [],
        'recovered_count': [],
        'deceased_count': []
    }
        
def simulationOfTheloop(params, population):
    data = initializeThedata()
    for day in range(params['simulation_duration']):
        new_infected = new_recovered = new_deceased = 0
        for person in population:
            if person['status'] == 'infected':
                person['days_infected'] += 1
                if person['days_infected'] > params['incubation_period']:
                    effective_infection_rate = params['infection_rate']
                    if params['quarantine_start_day'] <= day < params['quarantine_start_day'] + params['quarantine_duration']:
                        effective_infection_rate *= params['quarantine_effectiveness']
                    for other in population:
                        if other['status'] == 'susceptible' and random.random() < effective_infection_rate:
                            other['status'] = 'infected'
                            other['days_infected'] = 0
                            new_infected += 1
                if random.random() < params['recovery_rate']:
                    person['status'] = 'recovered'
                    new_recovered += 1
                elif random.random() < params['death_rate']:
                    person['status'] = 'deceased'
                    new_deceased += 1
            elif person['status'] == 'susceptible' and random.random() < params['vaccination_rate']:
                person['status'] = 'recovered'
                new_recovered += 1
        data['susceptible_count'].append(sum(1 for p in population if p['status'] == 'susceptible'))
        data['infected_count'].append(sum(1 for p in population if p['status'] == 'infected'))
        data['recovered_count'].append(sum(1 for p in population if p['status'] == 'recovered'))
        data['deceased_count'].append(sum(1 for p in population if p['status'] == 'deceased'))
    return data

def plotting(comparisonData, params_list): 
    plt.figure(figsize=(10, 6))
    for data, params in zip(comparisonData, params_list):
        label = params['name']
        plt.plot(data['susceptible_count'], label=f'Susceptible ({label})', linestyle='--')
        plt.plot(data['infected_count'], label=f'Infected ({label})', linestyle='-')
        plt.plot(data['recovered_count'], label=f'Recovered ({label})', linestyle=':')
        plt.plot(data['deceased_count'], label=f'Deceased ({label})', linestyle='-.')
    plt.xlabel('Days')
    plt.ylabel('Population')
    plt.title('Epidemic Spread Comparison' if len(params_list) > 1 else f'Epidemic Spread - {params_list[0]["name"]}')
    plt.legend()
    plt.show()

def saveToJson():
    with open("epidemics.json", 'w') as f:
        json.dump([epidemics], f, indent=4)

def get_params(epidemic_name):
    params = epidemics[epidemic_name].copy()
    params['name'] = epidemic_name
    return params

def start_simulation(single_epidemic=True):
    comparisonData = []
    params_list = []
    
    if single_epidemic:
        epidemic_name = epidemic_choice.get()
        if epidemic_name not in epidemics:
            messagebox.showerror("Error", "Please select a valid epidemic")
            return
        params = get_params(epidemic_name)
        population = makingThepopulation(params)
        data = simulationOfTheloop(params, population)
        comparisonData.append(data)
        params_list.append(params)
    else:
        epidemic_name1 = epidemic_choice1.get()
        epidemic_name2 = epidemic_choice2.get()
        
        if epidemic_name1 == epidemic_name2:
            messagebox.showerror("Error", "Choose two different epidemics for comparison")
            return
        
        for epidemic_name in [epidemic_name1, epidemic_name2]:
            params = get_params(epidemic_name)
            population = makingThepopulation(params)
            data = simulationOfTheloop(params, population)
            comparisonData.append(data)
            params_list.append(params)

    plotting(comparisonData, params_list)

def create_custom_epidemic():
    custom_params = {}
    
    # Dialog box for each parameter
    custom_params['name'] = simpledialog.askstring("Custom Epidemic", "Enter the name of the epidemic:")
    custom_params['population_size'] = int(simpledialog.askstring("Population Size", "Enter population size:"))
    custom_params['initial_infected'] = int(simpledialog.askstring("Initial Infected", "Enter initial infected count:"))
    custom_params['infection_rate'] = float(simpledialog.askstring("Infection Rate", "Enter infection rate (e.g., 0.05 for 5%):"))
    custom_params['recovery_rate'] = float(simpledialog.askstring("Recovery Rate", "Enter recovery rate (e.g., 0.01 for 1%):"))
    custom_params['death_rate'] = float(simpledialog.askstring("Death Rate", "Enter death rate (e.g., 0.005 for 0.5%):"))
    custom_params['vaccination_rate'] = float(simpledialog.askstring("Vaccination Rate", "Enter vaccination rate (e.g., 0.002 for 0.2%):"))
    custom_params['incubation_period'] = int(simpledialog.askstring("Incubation Period", "Enter incubation period in days:"))
    custom_params['quarantine_effectiveness'] = float(simpledialog.askstring("Quarantine Effectiveness", "Enter quarantine effectiveness (e.g., 0.5 for 50%):"))
    custom_params['quarantine_start_day'] = int(simpledialog.askstring("Quarantine Start Day", "Enter quarantine start day:"))
    custom_params['quarantine_duration'] = int(simpledialog.askstring("Quarantine Duration", "Enter quarantine duration in days:"))
    custom_params['simulation_duration'] = int(simpledialog.askstring("Simulation Duration", "Enter simulation duration in days:"))
    
    # Add to epidemics dictionary and save to JSON
    epidemics[custom_params['name']] = custom_params
    saveToJson()
    update_epidemic_choices()
    messagebox.showinfo("Success", f"{custom_params['name']} has been added to the list of epidemics.")

def update_epidemic_choices():
    # Update dropdowns with the latest list of epidemics
    epidemic_choice['values'] = list(epidemics.keys())
    epidemic_choice1['values'] = list(epidemics.keys())
    epidemic_choice2['values'] = list(epidemics.keys())

# GUI setup
root = tk.Tk()
root.title("Epidemic Simulation")

root.geometry("1000x900")

frame = tk.Frame(root, bg='lightblue')
frame.place(relwidth=1, relheight=1)


# single simulation
ttk.Label(root, text="Select Epidemic for Single Simulation:").grid(column=0, row=0, padx=10, pady=5)
epidemic_choice = ttk.Combobox(root, values=list(epidemics.keys()))
epidemic_choice.grid(column=1, row=0, padx=10, pady=5)
ttk.Button(root, text="Simulate", command=lambda: start_simulation(True)).grid(column=2, row=0, padx=10, pady=5)

#  comparison
ttk.Label(root, text="Compare Epidemics:").grid(column=0, row=1, padx=10, pady=5)
epidemic_choice1 = ttk.Combobox(root, values=list(epidemics.keys()))
epidemic_choice1.grid(column=1, row=1, padx=10, pady=5)
epidemic_choice2 = ttk.Combobox(root, values=list(epidemics.keys()))
epidemic_choice2.grid(column=2, row=1, padx=10, pady=5)
ttk.Button(root, text="Compare", command=lambda: start_simulation(False)).grid(column=3, row=1, padx=10, pady=5)

# custom epidemic
ttk.Button(root, text="Create Custom Epidemic", command=create_custom_epidemic).grid(column=0, row=2, padx=10, pady=10)

root.mainloop()
