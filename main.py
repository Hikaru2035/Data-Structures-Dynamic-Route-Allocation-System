import random
import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import os
import itertools

class Parcel:
    def __init__(self, parcel_id, parcel_weight, parcel_destination, parcel_customer_name):
        self.parcel_id = parcel_id
        self.parcel_weight= parcel_weight
        self.parcel_destination= parcel_destination
        self.customer_name= parcel_customer_name

    def __str__(self) -> str:
        return f"Parcel({self.parcel_id}, {self.parcel_weight}kg, {self.parcel_destination}, {self.customer_name})"

class Trucks: 
    def __init__(self, truck_max_capacity):
        self.truck_max_capacity = truck_max_capacity
        self.remaining_capacity = truck_max_capacity
        self.parcels = []
        self.destinations = set()

    def truck_accomodation(self, parcel):
        return self.remaining_capacity >= parcel.parcel_weight

    def add_parcel(self, parcel):
        self.parcels.append(parcel)
        self.parcels = sorted(self.parcels, key=lambda pkg: destination_distances.get(pkg.parcel_destination,0), reverse=True)
        self.remaining_capacity -= parcel.parcel_weight
        self.destinations.add(parcel.parcel_destination)

    
    def __str__(self) -> str:
        return (f"Truck(Capacity: {self.truck_max_capacity}kg, Remaining: {self.remaining_capacity}kg, "
                f"Stops: {', '.join(self.destinations)}, parcels: {len(self.parcels)})")

class BinPackingSystem:
    def __init__(self, truck_capacity):
        self.truck_capacity = truck_capacity
        self.trucks = []
        
    #Apply BFD in packing parcels
    def packing_parcels(self, parcels):
        #Sort parcels received at Hanoi in decreasing order
        parcels = sorted(parcels, key = lambda parcel:parcel.parcel_weight, reverse = True)

        #Scan each parcels to find best fitted truck
        for each_parcel in parcels:
            #Try to load recent parcels into an existing truck
            loading_truck = None
            best_fitting_truck_capacity = self.truck_capacity + 1
            
            #Scan each truck to find ideal remaining capacity available
            for each_truck in self.trucks:
                if each_truck.truck_accomodation(each_parcel):
                    remaining_capacity_after = each_truck.remaining_capacity - each_parcel.parcel_weight
                    if remaining_capacity_after < best_fitting_truck_capacity:
                        best_fitting_truck_capacity = remaining_capacity_after
                        loading_truck = each_truck

            #Loading parcel onto best fitted truck or create new truck
            if loading_truck:
                loading_truck.add_parcel(each_parcel)
            else:
                new_truck = Trucks(self.truck_capacity)
                new_truck.add_parcel(each_parcel)   
                self.trucks.append(new_truck)

        return self.trucks


destination_distances = {
        "Dalat": 250,
        "HCMC": 300,
        "Da Nang": 150,
        "Hai Phong": 100,
        "Nha Trang": 200
    }

#Generate default customer dataset         
def get_default_parcels_from_excel(file_path):
    """
    Reads parcel data from an Excel file and creates Parcel objects.
    
    :param file_path: Path to the Excel file containing parcel data.
    :return: List of Parcel objects.
    """
    # Load data from the Excel file
    df = pd.read_excel(file_path)

    # Ensure the required columns are present
    required_columns = ["parcel_id", "weight", "destination", "customer_name"]
    for column in required_columns:
        if column not in df.columns:
            raise ValueError(f"Missing required column in Excel file: {column}")

    # Create Parcel objects from the data
    default_parcels = []
    for _, row in df.iterrows():
        parcel_id = row["parcel_id"]
        weight = row["weight"]
        destination = row["destination"]
        customer_name = row["customer_name"]

        # Create Parcel object and add to the list
        default_parcels.append(Parcel(parcel_id, weight, destination, customer_name))

    return default_parcels

class BinPackingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bin Packing System")
        self.root.geometry("1000x800")

        # Parcel Table
        self.parcels = get_default_parcels_from_excel("packages.xlsx")
        self.parcel_table = ttk.Treeview(root, columns=("Number","ID", "Weight", "Destination", "Customer"), show="headings")
        self.parcel_table.heading("Number", text="No.")
        self.parcel_table.heading("ID", text="Parcel ID")
        self.parcel_table.heading("Weight", text="Weight (kg)")
        self.parcel_table.heading("Destination", text="Destination")
        self.parcel_table.heading("Customer", text="Customer Name")
        self.parcel_table.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.load_parcels()

        # Buttons
        self.button_frame = tk.Frame(root)
        self.button_frame.pack(fill=tk.X, padx=10, pady=10)

        self.pack_button = tk.Button(self.button_frame, text="Pack Parcels", command=self.pack_parcels)
        self.pack_button.pack(side=tk.LEFT, padx=5)

        self.clear_button = tk.Button(self.button_frame, text="Clear", command=self.clear_trucks)
        self.clear_button.pack(side=tk.LEFT, padx=5)

        self.add_button = tk.Button(self.button_frame, text="Add Parcel", command=self.add_parcel)
        self.add_button.pack(side=tk.LEFT, padx=5)

        # Truck Details
        self.truck_list = tk.Text(root, state="disabled", height=15)
        self.truck_list.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.system = BinPackingSystem(truck_capacity=500)

    def load_parcels(self):
        for parcel in self.parcels:
            self.parcel_table.insert("", tk.END, values=(self.parcels.index(parcel),parcel.parcel_id, parcel.parcel_weight, parcel.parcel_destination, parcel.customer_name))

    def add_parcel(self):
        add_window = tk.Toplevel(self.root)
        add_window.title("Add parcel")

        # Input fields
        tk.Label(add_window, text="Weight (kg):").grid(row=1, column=0, padx=5, pady=5)
        weight_entry = tk.Entry(add_window)
        weight_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(add_window, text="Destination:").grid(row=2, column=0, padx=5, pady=5)
        destination_var = tk.StringVar(value="HCMC")  # Default value
        destination_menu = tk.OptionMenu(add_window, destination_var, "HCMC", "Da Nang", "Nha Trang", "Dalat", "Hai Phong")
        destination_menu.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(add_window, text="Customer Name:").grid(row=3, column=0, padx=5, pady=5)
        customer_name_entry = tk.Entry(add_window)
        customer_name_entry.grid(row=3, column=1, padx=5, pady=5)

        # Submit button
        def submit():
            parcel_id = f"P{random.randint(1, 999999):06d}"
            weight = weight_entry.get()
            destination = destination_var.get()
            customer_name = customer_name_entry.get()

            if not (parcel_id and weight and destination and customer_name):
                messagebox.showerror("Input Error", "All fields must be filled!")
                return

            try:
                weight = float(weight)
            except ValueError:
                messagebox.showerror("Input Error", "Weight must be a number!")
                return

            # Add parcel to the list and table
            parcel = Parcel(parcel_id, weight, destination, customer_name)
            self.parcels.append(parcel)
            self.parcel_table.insert("", tk.END, values=(self.parcels.index(parcel),parcel_id, weight, destination, customer_name))
            
            # Save to Excel file
            save_to_excel(parcel)
            
            messagebox.showinfo("Success", f"Package {parcel_id} added successfully!")
            add_window.destroy()

        def save_to_excel(parcel):
            file_name = "packages.xlsx"
            package_data = {
                        "parcel_id": [parcel.parcel_id],
                        "weight": [parcel.parcel_weight],
                        "destination": [parcel.parcel_destination],
                        "customer_name": [parcel.customer_name]
                    }
            new_data = pd.DataFrame(package_data)

            try:
                if os.path.exists(file_name):
                    # If file exists, append the data
                    existing_data = pd.read_excel(file_name)
                    updated_data = pd.concat([existing_data, new_data], ignore_index=True)
                else:
                    # If file doesn't exist, create it
                    updated_data = new_data

                # Save to Excel
                updated_data.to_excel(file_name, index=False)
                print(f"Package details successfully saved to {file_name}")
            except Exception as e:
                print(f"Failed to save package details: {str(e)}")

        submit_button = tk.Button(add_window, text="Submit", command=submit)
        submit_button.grid(row=4, column=0, columnspan=2, pady=10)

    def pack_parcels(self):
        self.system.packing_parcels(self.parcels)

        # Display truck details
        self.truck_list.config(state="normal")
        self.truck_list.delete(1.0, tk.END)

        for idx, truck in enumerate(self.system.trucks, 1):
            self.truck_list.insert(tk.END, f"Truck {idx}: {truck}\n")
            for parcel in truck.parcels:
                self.truck_list.insert(tk.END, f"  {parcel}\n")
            self.truck_list.insert(tk.END, "\n")

        self.truck_list.config(state="disabled")

        def save_invoices_to_separate_files(parcels, base_folder="Invoices"):
        # Create the base folder if it doesn't exist
            if not os.path.exists(base_folder):
                os.makedirs(base_folder)

            for parcel in parcels:
                distance = destination_distances.get(parcel.parcel_destination, 0)
                cost = parcel.parcel_weight * 2 + distance * 0.01 * 5

                # Prepare invoice data
                invoice_data = {
                    "Parcel ID": [parcel.parcel_id],
                    "Destination": [parcel.parcel_destination],
                    "Weight (kg)": [parcel.parcel_weight],
                    "Distance (km)": [distance],
                    "Cost ($)": [cost],
                    "Customer Name": [parcel.customer_name]
                }

                # Create a DataFrame
                df = pd.DataFrame(invoice_data)

                # Define the file name
                file_path = os.path.join(base_folder, f"{parcel.parcel_id}_{parcel.customer_name}.xlsx")

                # Save the DataFrame to an Excel file
                df.to_excel(file_path, index=False)
                print(f"Invoice saved to {file_path}")
        
        save_invoices_to_separate_files(self.parcels)

    def clear_trucks(self):
        self.truck_list.config(state="normal")
        self.truck_list.delete(1.0, tk.END)
        self.truck_list.config(state="disabled")
        self.system.trucks = []

if __name__ == "__main__":
    root = tk.Tk()
    app = BinPackingApp(root)
    root.mainloop()