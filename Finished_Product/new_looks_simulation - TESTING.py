# ---------- LIBRARIES ----------

import json
import random
import customtkinter as ctk
from tkinter import messagebox, simpledialog
import matplotlib.pyplot as plt
from PIL import Image, ImageTk

# ---------- CUSTOMTKINTER  ----------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# ---------- CONSTANTS ----------
BACKGROUND_IMAGE_PATH = "EPIDEMIC_red_white_one-750x422.jpeg"
ALLOWED_PASSWORDS = ["admin", "WHO", "abdur"]

# Load epidemic data
with open(r"C:\Users\Abdur Rahmaan\OneDrive\Desktop\CS PRJECCT\finish_nea_ACC\epidemics.json", "r") as f:
    epidemic_data = json.load(f)
    epidemics = epidemic_data[0]

country_parameters = {
    "USA": {"population_size": 1000, "recovery_rate": 0.005, "death_rate": 0.1, "vaccination_rate": 0.0, "quarantine_effectiveness": 0.2},
    "Ghana": {"population_size": 1000, "recovery_rate": 0.0025, "death_rate": 0.09, "vaccination_rate": 0.0, "quarantine_effectiveness": 0.1},
    "Chad": {"population_size": 1000, "recovery_rate": 0.0025, "death_rate": 0.09, "vaccination_rate": 0.0, "quarantine_effectiveness": 0.1},
}

#---------- FUNCTIONS ----------

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
#---------- SIMULATION LOOP ----------
def simulationOfTheloop(params, population):
    data = initializeThedata()
    for day in range(params['simulation_duration']):
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
                if random.random() < params['recovery_rate']:
                    person['status'] = 'recovered'
                elif random.random() < params['death_rate']:
                    person['status'] = 'deceased'
            elif person['status'] == 'susceptible' and random.random() < params['vaccination_rate']:
                person['status'] = 'recovered'

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

#---------- FOR CREATING CUSTOM EPIDEMIC ----------

def create_custom_epidemic():
    custom_params = {}
    custom_params['name'] = simpledialog.askstring("Custom Epidemic", "Enter epidemic name:")
    custom_params['population_size'] = int(simpledialog.askstring("Population Size", "Enter population size:"))
    custom_params['initial_infected'] = int(simpledialog.askstring("Initial Infected", "Enter initial infected count:"))
    custom_params['infection_rate'] = float(simpledialog.askstring("Infection Rate", "Enter infection rate (e.g. 0.05):"))
    custom_params['recovery_rate'] = float(simpledialog.askstring("Recovery Rate", "Enter recovery rate (e.g. 0.01):"))
    custom_params['death_rate'] = float(simpledialog.askstring("Death Rate", "Enter death rate (e.g. 0.005):"))
    custom_params['vaccination_rate'] = float(simpledialog.askstring("Vaccination Rate", "Enter vaccination rate (e.g. 0.002):"))
    custom_params['incubation_period'] = int(simpledialog.askstring("Incubation Period", "Enter incubation period in days:"))
    custom_params['quarantine_effectiveness'] = float(simpledialog.askstring("Quarantine Effectiveness", "Enter quarantine effectiveness (e.g. 0.5):"))
    custom_params['quarantine_start_day'] = int(simpledialog.askstring("Quarantine Start Day", "Enter start day:"))
    custom_params['quarantine_duration'] = int(simpledialog.askstring("Quarantine Duration", "Enter duration in days:"))
    custom_params['simulation_duration'] = int(simpledialog.askstring("Simulation Duration", "Enter duration in days:"))

    epidemics[custom_params['name']] = custom_params
    saveToJson()
    update_epidemic_choices()
    messagebox.showinfo("Success", f"{custom_params['name']} added to the list.")

def update_epidemic_choices():
    epidemic_choice.configure(values=list(epidemics.keys()))
    epidemic_choice1.configure(values=list(epidemics.keys()))
    epidemic_choice2.configure(values=list(epidemics.keys()))

def show_main_menu():
    login_frame.pack_forget()
    menu_frame.pack(expand=True)

def login():
    user = username_entry.get()
    pwd = password_entry.get()
    if pwd in ALLOWED_PASSWORDS:
        show_main_menu()
    else:
        messagebox.showerror("Login Failed", "Incorrect username or password")

# ---------- GUI Setup ----------
app = ctk.CTk()
app.title("Epidemic Simulation")
app.geometry("800x500")

# Background image
bg_img = Image.open(BACKGROUND_IMAGE_PATH)
bg_photo = ImageTk.PhotoImage(bg_img)
bg_label = ctk.CTkLabel(master=app, image=bg_photo, text="")
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Login Frame
login_frame = ctk.CTkFrame(master=app, fg_color=("#222222", "#222222"), corner_radius=15)
login_frame.pack(expand=True)
ctk.CTkLabel(login_frame, text="Login", font=("Arial", 24)).pack(pady=10)
username_entry = ctk.CTkEntry(login_frame, placeholder_text="Username")
username_entry.pack(pady=5)
password_entry = ctk.CTkEntry(login_frame, placeholder_text="Password", show="*")
password_entry.pack(pady=5)
ctk.CTkButton(login_frame, text="Login", command=login).pack(pady=10)

# Main Menu Frame
menu_frame = ctk.CTkFrame(master=app, fg_color=("#222222", "#222222"), corner_radius=15)

ctk.CTkLabel(menu_frame, text="Main Menu", font=("Arial", 24)).pack(pady=10)
ctk.CTkButton(menu_frame, text="Create Custom Epidemic", command=create_custom_epidemic).pack(pady=5)
ctk.CTkButton(menu_frame, text="Simulate One Epidemic", command=lambda: [menu_frame.pack_forget(), simulation_frame.pack(expand=True)]).pack(pady=5)
ctk.CTkButton(menu_frame, text="Compare Two Epidemics", command=lambda: [menu_frame.pack_forget(), comparison_frame.pack(expand=True)]).pack(pady=5)

# Simulation Frame
simulation_frame = ctk.CTkFrame(master=app, fg_color=("#222222", "#222222"), corner_radius=15)
ctk.CTkLabel(simulation_frame, text="Simulate Epidemic", font=("Arial", 24)).pack(pady=10)
country_choice = ctk.CTkComboBox(master=simulation_frame, values=list(country_parameters.keys()))
country_choice.pack(pady=5)
epidemic_choice = ctk.CTkComboBox(master=simulation_frame, values=list(epidemics.keys()))
epidemic_choice.pack(pady=5)
ctk.CTkButton(master=simulation_frame, text="Run Simulation", command=lambda: start_simulation(True)).pack(pady=10)
ctk.CTkButton(simulation_frame, text="Back to Menu", command=lambda: [simulation_frame.pack_forget(), menu_frame.pack(expand=True)]).pack(pady=5)

# Comparison Frame
comparison_frame = ctk.CTkFrame(master=app, fg_color=("#222222", "#222222"), corner_radius=15)
ctk.CTkLabel(comparison_frame, text="Compare Epidemics", font=("Arial", 24)).pack(pady=10)
epidemic_choice1 = ctk.CTkComboBox(master=comparison_frame, values=list(epidemics.keys()))
epidemic_choice1.pack(pady=5)
epidemic_choice2 = ctk.CTkComboBox(master=comparison_frame, values=list(epidemics.keys()))
epidemic_choice2.pack(pady=5)
country_choice = ctk.CTkComboBox(master=comparison_frame, values=list(country_parameters.keys()))
country_choice.pack(pady=5)
ctk.CTkButton(master=comparison_frame, text="Compare", command=lambda: start_simulation(False)).pack(pady=10)
ctk.CTkButton(comparison_frame, text="Back to Menu", command=lambda: [comparison_frame.pack_forget(), menu_frame.pack(expand=True)]).pack(pady=5)

update_epidemic_choices()
app.mainloop()
