import tkinter as tk
from tkinter import messagebox, ttk
import json, os

# ================= File Handling Helpers =================

def load_data(filename):
    if not os.path.exists(filename):
        return []
    with open(filename, "r") as f:
        return json.load(f)

def save_data(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

patients_file = "patients.json"
doctors_file = "doctors.json"
appointments_file = "appointments.json"

patients = load_data(patients_file)
doctors = load_data(doctors_file)
appointments = load_data(appointments_file)

# ================= Tkinter App =================

root = tk.Tk()
root.title("Hospital Management System")
root.geometry("950x650")
root.configure(bg="#0d1b2a")  # Dark blue background

style = ttk.Style()
style.theme_use("clam")
style.configure("TNotebook", background="#0d1b2a")
style.configure("TFrame", background="#0d1b2a")
style.configure("TLabel", background="#0d1b2a", foreground="white")
style.configure("TButton", background="#1b263b", foreground="white")
style.configure("TEntry", fieldbackground="#1b263b", foreground="white")

# Notebook for tabs
notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True, padx=10, pady=10)

# Frames for tabs
patients_frame = ttk.Frame(notebook)
doctors_frame = ttk.Frame(notebook)
appointments_frame = ttk.Frame(notebook)
manage_frame = ttk.Frame(notebook)

notebook.add(patients_frame, text="Patients")
notebook.add(doctors_frame, text="Doctors")
notebook.add(appointments_frame, text="Appointments")
notebook.add(manage_frame, text="Manage Records")

# Helper to get next id (handles deletions)
def next_id(items, key='id'):
    if not items:
        return 1
    return max(item.get(key, 0) for item in items) + 1

# ================= Patients Tab =================

def add_patient():
    name = name_entry.get().strip()
    age = age_entry.get().strip()
    gender = gender_var.get()
    disease = disease_entry.get().strip()
    phone = phone_entry.get().strip()

    if not name or not age:
        messagebox.showerror("Error", "Name and Age are required")
        return
    try:
        age_i = int(age)
    except ValueError:
        messagebox.showerror("Error", "Age must be a number")
        return

    patient = {
        "id": next_id(patients),
        "name": name,
        "age": age_i,
        "gender": gender,
        "disease": disease,
        "phone": phone
    }
    patients.append(patient)
    save_data(patients_file, patients)
    messagebox.showinfo("Success", "Patient added successfully!")
    refresh_patients()
    # clear
    name_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    disease_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)

# Patient Form (left side)
left_p = ttk.Frame(patients_frame)
left_p.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

name_label = ttk.Label(left_p, text="Name:")
name_label.pack(anchor=tk.W)
name_entry = ttk.Entry(left_p, width=30)
name_entry.pack()

age_label = ttk.Label(left_p, text="Age:")
age_label.pack(anchor=tk.W, pady=(8,0))
age_entry = ttk.Entry(left_p, width=30)
age_entry.pack()

gender_label = ttk.Label(left_p, text="Gender:")
gender_label.pack(anchor=tk.W, pady=(8,0))
gender_var = tk.StringVar()
gender_dropdown = ttk.Combobox(left_p, textvariable=gender_var, values=["Male", "Female", "Other"], state='readonly', width=28)
gender_dropdown.current(0)
gender_dropdown.pack()

disease_label = ttk.Label(left_p, text="Disease:")
disease_label.pack(anchor=tk.W, pady=(8,0))
disease_entry = ttk.Entry(left_p, width=30)
disease_entry.pack()

phone_label = ttk.Label(left_p, text="Phone:")
phone_label.pack(anchor=tk.W, pady=(8,0))
phone_entry = ttk.Entry(left_p, width=30)
phone_entry.pack()

add_btn = ttk.Button(left_p, text="Add Patient", command=add_patient)
add_btn.pack(pady=12)

# Patient List (right side)
right_p = ttk.Frame(patients_frame)
right_p.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

patients_list = tk.Listbox(right_p, width=80, bg="#1b263b", fg="white", activestyle='dotbox')
patients_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

patients_scroll = ttk.Scrollbar(right_p, orient=tk.VERTICAL, command=patients_list.yview)
patients_scroll.pack(side=tk.RIGHT, fill=tk.Y)
patients_list.config(yscrollcommand=patients_scroll.set)

def refresh_patients():
    patients_list.delete(0, tk.END)
    for p in patients:
        patients_list.insert(tk.END, f"{p['id']}. {p['name']} ({p['age']} yrs, {p['gender']}) | Disease: {p['disease']} | Phone: {p['phone']}")

refresh_patients()

# ================= Doctors Tab =================

def add_doctor():
    name = dname_entry.get().strip()
    spec = spec_entry.get().strip()
    phone = dphone_entry.get().strip()
    if not name:
        messagebox.showerror("Error", "Doctor name is required")
        return
    doctor = {
        "id": next_id(doctors),
        "name": name,
        "specialization": spec,
        "phone": phone
    }
    doctors.append(doctor)
    save_data(doctors_file, doctors)
    messagebox.showinfo("Success", "Doctor added successfully!")
    refresh_doctors()
    dname_entry.delete(0, tk.END)
    spec_entry.delete(0, tk.END)
    dphone_entry.delete(0, tk.END)

# Doctor Form (left)
left_d = ttk.Frame(doctors_frame)
left_d.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

dname_label = ttk.Label(left_d, text="Doctor Name:")
dname_label.pack(anchor=tk.W)
dname_entry = ttk.Entry(left_d, width=30)
dname_entry.pack()

spec_label = ttk.Label(left_d, text="Specialization:")
spec_label.pack(anchor=tk.W, pady=(8,0))
spec_entry = ttk.Entry(left_d, width=30)
spec_entry.pack()

dphone_label = ttk.Label(left_d, text="Phone:")
dphone_label.pack(anchor=tk.W, pady=(8,0))
dphone_entry = ttk.Entry(left_d, width=30)
dphone_entry.pack()

add_doc_btn = ttk.Button(left_d, text="Add Doctor", command=add_doctor)
add_doc_btn.pack(pady=12)

# Doctor List (right)
right_d = ttk.Frame(doctors_frame)
right_d.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

doctors_list = tk.Listbox(right_d, width=80, bg="#1b263b", fg="white", activestyle='dotbox')
doctors_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

doctors_scroll = ttk.Scrollbar(right_d, orient=tk.VERTICAL, command=doctors_list.yview)
doctors_scroll.pack(side=tk.RIGHT, fill=tk.Y)
doctors_list.config(yscrollcommand=doctors_scroll.set)

def refresh_doctors():
    doctors_list.delete(0, tk.END)
    for d in doctors:
        doctors_list.insert(tk.END, f"{d['id']}. {d['name']} - {d['specialization']} | Phone: {d['phone']}")

refresh_doctors()

# ================= Appointments Tab =================

def book_appointment():
    try:
        pid = int(pid_entry.get())
        did = int(did_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Patient ID and Doctor ID must be numbers")
        return
    date_val = date_entry.get().strip()
    time_val = time_entry.get().strip()
    # basic validation
    if not any(p['id'] == pid for p in patients):
        messagebox.showerror("Error", "Patient ID not found")
        return
    if not any(d['id'] == did for d in doctors):
        messagebox.showerror("Error", "Doctor ID not found")
        return

    appt = {
        "appointment_id": next_id(appointments, 'appointment_id'),
        "patient_id": pid,
        "doctor_id": did,
        "date": date_val,
        "time": time_val
    }
    # prevent exact double-booking for same doctor
    for a in appointments:
        if a['doctor_id'] == did and a['date'] == date_val and a['time'] == time_val:
            messagebox.showerror("Error", "This doctor already has an appointment at that time")
            return

    appointments.append(appt)
    save_data(appointments_file, appointments)
    messagebox.showinfo("Success", "Appointment booked successfully!")
    refresh_appointments()
    pid_entry.delete(0, tk.END)
    did_entry.delete(0, tk.END)
    date_entry.delete(0, tk.END)
    time_entry.delete(0, tk.END)

# Appointment Form (left)
left_a = ttk.Frame(appointments_frame)
left_a.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

pid_label = ttk.Label(left_a, text="Patient ID:")
pid_label.pack(anchor=tk.W)
pid_entry = ttk.Entry(left_a, width=30)
pid_entry.pack()

did_label = ttk.Label(left_a, text="Doctor ID:")
did_label.pack(anchor=tk.W, pady=(8,0))
did_entry = ttk.Entry(left_a, width=30)
did_entry.pack()

date_label = ttk.Label(left_a, text="Date (YYYY-MM-DD):")
date_label.pack(anchor=tk.W, pady=(8,0))
date_entry = ttk.Entry(left_a, width=30)
date_entry.pack()

time_label = ttk.Label(left_a, text="Time:")
time_label.pack(anchor=tk.W, pady=(8,0))
time_entry = ttk.Entry(left_a, width=30)
time_entry.pack()

add_appt_btn = ttk.Button(left_a, text="Book Appointment", command=book_appointment)
add_appt_btn.pack(pady=12)

# Appointment List (right)
right_a = ttk.Frame(appointments_frame)
right_a.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

appointments_list = tk.Listbox(right_a, width=90, bg="#1b263b", fg="white", activestyle='dotbox')
appointments_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

appointments_scroll = ttk.Scrollbar(right_a, orient=tk.VERTICAL, command=appointments_list.yview)
appointments_scroll.pack(side=tk.RIGHT, fill=tk.Y)
appointments_list.config(yscrollcommand=appointments_scroll.set)

def refresh_appointments():
    appointments_list.delete(0, tk.END)
    for a in appointments:
        appointments_list.insert(tk.END, f"Appt {a['appointment_id']}: Patient {a['patient_id']} with Doctor {a['doctor_id']} on {a['date']} at {a['time']}")

refresh_appointments()

# ================= Manage Records Tab =================

def update_disease():
    try:
        pid = int(up_pid_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Patient ID must be a number")
        return
    new_disease = up_disease_entry.get().strip()
    for p in patients:
        if p['id'] == pid:
            p['disease'] = new_disease
            save_data(patients_file, patients)
            messagebox.showinfo("Success", f"Disease updated for Patient {pid}")
            refresh_patients()
            return
    messagebox.showerror("Error", "Patient not found")


def remove_patient():
    try:
        pid = int(rm_pid_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Patient ID must be a number")
        return
    global patients, appointments
    patients = [p for p in patients if p['id'] != pid]
    # Also remove appointments for this patient
    appointments = [a for a in appointments if a['patient_id'] != pid]

    save_data(patients_file, patients)
    save_data(appointments_file, appointments)
    messagebox.showinfo("Success", f"Patient {pid} removed")
    refresh_patients()
    refresh_appointments()


def remove_doctor():
    try:
        did = int(rm_did_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Doctor ID must be a number")
        return
    global doctors, appointments
    doctors = [d for d in doctors if d['id'] != did]
    # Remove appointments for this doctor
    appointments = [a for a in appointments if a['doctor_id'] != did]

    save_data(doctors_file, doctors)
    save_data(appointments_file, appointments)
    messagebox.showinfo("Success", f"Doctor {did} removed")
    refresh_doctors()
    refresh_appointments()

# Manage UI
manage_top = ttk.Frame(manage_frame)
manage_top.pack(fill=tk.X, padx=10, pady=10)

up_pid_label = ttk.Label(manage_top, text="Patient ID:")
up_pid_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=3)
up_pid_entry = ttk.Entry(manage_top, width=15)
up_pid_entry.grid(row=0, column=1, padx=5, pady=3)

up_disease_label = ttk.Label(manage_top, text="New Disease:")
up_disease_label.grid(row=0, column=2, sticky=tk.W, padx=5, pady=3)
up_disease_entry = ttk.Entry(manage_top, width=25)
up_disease_entry.grid(row=0, column=3, padx=5, pady=3)

up_btn = ttk.Button(manage_top, text="Update Disease", command=update_disease)
up_btn.grid(row=0, column=4, padx=5, pady=3)

rm_pid_label = ttk.Label(manage_top, text="Patient ID to Remove:")
rm_pid_label.grid(row=1, column=0, sticky=tk.W, padx=5, pady=3)
rm_pid_entry = ttk.Entry(manage_top, width=15)
rm_pid_entry.grid(row=1, column=1, padx=5, pady=3)

rm_p_btn = ttk.Button(manage_top, text="Remove Patient", command=remove_patient)
rm_p_btn.grid(row=1, column=2, padx=5, pady=3)

rm_did_label = ttk.Label(manage_top, text="Doctor ID to Remove:")
rm_did_label.grid(row=1, column=3, sticky=tk.W, padx=5, pady=3)
rm_did_entry = ttk.Entry(manage_top, width=15)
rm_did_entry.grid(row=1, column=4, padx=5, pady=3)

rm_d_btn = ttk.Button(manage_top, text="Remove Doctor", command=remove_doctor)
rm_d_btn.grid(row=1, column=5, padx=5, pady=3)

# ================= Run App =================
root.mainloop()
