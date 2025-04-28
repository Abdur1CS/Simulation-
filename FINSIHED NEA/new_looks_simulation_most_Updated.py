import json
import random
import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk
import matplotlib.pyplot as plt
from PIL import Image, ImageTk

# ---------- Constants ----------
BACKGROUND_COLOR = "#ddefb0"
TEXT_COLOR = "#222"

# Load epidemic data from JSON file
with open(r"C:\Users\Abdur Rahmaan\OneDrive\Desktop\CS PRJECCT\finish_nea_ACC\epidemics.json", "r") as f:
    epidemic_data = json.load(f)
    epidemics = epidemic_data[0]

country_parameters = {
    "USA": {"population_size": 1000, "recovery_rate": 0.005, "death_rate": 0.1, "vaccination_rate": 0.0, "quarantine_effectiveness": 0.2},
    "Ghana": {"population_size": 1000, "recovery_rate": 0.005 * 0.5, "death_rate": 0.1 * 0.9, "vaccination_rate": 0.0, "quarantine_effectiveness": 0.1},
    "Chad": {"population_size": 1000, "recovery_rate": 0.005 * 0.5, "death_rate": 0.1 * 0.9, "vaccination_rate": 0.0, "quarantine_effectiveness": 0.1},
}

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

    final_values = f"Final Values:\nSusceptible: {data['susceptible_count'][-1]}\nInfected: {data['infected_count'][-1]}\nRecovered: {data['recovered_count'][-1]}\nDeceased: {data['deceased_count'][-1]}"
    plt.gca().text(0.5, 0.5, final_values, ha='center', va='center', transform=plt.gca().transAxes, fontsize=12, bbox=dict(boxstyle="round,pad=0.3", edgecolor='black', facecolor='lightgrey'))
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
        selected_country = country_choice.get()
        if epidemic_name not in epidemics:
            messagebox.showerror("Error", "Please select a valid epidemic")
            return
        params = get_params(epidemic_name)
        params['population_size'] += country_parameters[selected_country]['population_size']
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
            params['population_size'] += country_parameters[country_choice.get()]['population_size']
            population = makingThepopulation(params)
            data = simulationOfTheloop(params, population)
            comparisonData.append(data)
            params_list.append(params)
    
    plotting(comparisonData, params_list)

def create_custom_epidemic():
    custom_params = {}
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

    epidemics[custom_params['name']] = custom_params
    saveToJson()
    update_epidemic_choices()
    messagebox.showinfo("Success", f"{custom_params['name']} has been added to the list of epidemics.")

def update_epidemic_choices():
    epidemic_choice['values'] = list(epidemics.keys())
    epidemic_choice1['values'] = list(epidemics.keys())
    epidemic_choice2['values'] = list(epidemics.keys())

# ---------------- GUI Setup ----------------
root = tk.Tk()
root.title("Epidemic Simulation")
root.geometry("750x422")
root.configure(bg='#dde9ff')
root.wm_attributes('-transparentcolor', '#dde9ff')

bg_img = Image.open("EPIDEMIC_red_white_one-750x422.jpeg")
bg_photo = ImageTk.PhotoImage(bg_img)
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)
bg_label.image = bg_photo

frame = tk.Frame(root, bg='#ffffff', bd=0, highlightbackground="#ffffff", highlightthickness=0)
frame.place(relx=0.5, rely=0.5, anchor='center')
frame.configure(bg='#ffffff')
frame.pack_propagate(False)
frame.configure(width=650, height=350)

style = ttk.Style()
style.theme_use('clam')
style.configure("TCombobox",
                fieldbackground="#ffffff",
                background="#ffffff",
                foreground="#222",
                arrowcolor="#222")

# Title
title_label = tk.Label(frame, text="Epidemic Simulation", font=("Arial", 24), bg='#ffffff', fg=TEXT_COLOR)
title_label.pack(pady=20)

# Country selection
country_frame = tk.Frame(frame, bg='#ffffff')
country_frame.pack(pady=10)
tk.Label(country_frame, text="Select Country:", bg='#ffffff', fg=TEXT_COLOR).grid(column=0, row=0, padx=10)
country_choice = ttk.Combobox(country_frame, values=list(country_parameters.keys()))
country_choice.grid(column=1, row=0, padx=10)

# Single simulation
single_frame = tk.Frame(frame, bg='#ffffff')
single_frame.pack(pady=10)
tk.Label(single_frame, text="Select Epidemic for Single Simulation:", bg='#ffffff', fg=TEXT_COLOR).grid(column=0, row=0, padx=10)
epidemic_choice = ttk.Combobox(single_frame, values=list(epidemics.keys()))
epidemic_choice.grid(column=1, row=0, padx=10)
tk.Button(single_frame, text="Simulate", command=lambda: start_simulation(True), bg='#cccccc', fg=TEXT_COLOR, borderwidth=0).grid(column=2, row=0, padx=10)

# Comparison
comparison_frame = tk.Frame(frame, bg='#ffffff')
comparison_frame.pack(pady=10)
tk.Label(comparison_frame, text="Compare Epidemics:", bg='#ffffff', fg=TEXT_COLOR).grid(column=0, row=0, padx=10)
epidemic_choice1 = ttk.Combobox(comparison_frame, values=list(epidemics.keys()))
epidemic_choice1.grid(column=1, row=0, padx=10)
epidemic_choice2 = ttk.Combobox(comparison_frame, values=list(epidemics.keys()))
epidemic_choice2.grid(column=2, row=0, padx=10)
tk.Button(comparison_frame, text="Compare", command=lambda: start_simulation(False), bg='#cccccc', fg=TEXT_COLOR, borderwidth=0).grid(column=3, row=0, padx=10)

# Custom epidemic
custom_frame = tk.Frame(frame, bg='#ffffff')
custom_frame.pack(pady=10)
tk.Button(custom_frame, text="Create Custom Epidemic", command=create_custom_epidemic, bg='#cccccc', fg=TEXT_COLOR, borderwidth=0).grid(column=0, row=0, padx=10)

root.mainloop()