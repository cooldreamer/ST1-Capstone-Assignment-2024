import tkinter as tk
import pandas as pd
import numpy as np
from tkinter import messagebox
from joblib import load

# Load model parameters
BMdf = pd.read_csv("BrandModelLU.csv")
NMLdf = pd.read_csv("normalparams.csv")
selected_row = NMLdf.iloc[0]
mean_year = selected_row['mean_year']
std_year = selected_row['std_year']
mean_km = selected_row['mean_km']
std_km = selected_row['std_km']

# Sort the DataFrame by 'Brand' and 'Model'
BMdf = BMdf.sort_values(by=['Brand', 'Model'])

# Load the trained Random Forests model
model_filename = "RF_CarPricing_trained_model.joblib"
loaded_model = load(model_filename)

# Create the Tkinter application
class CarPricePredictorApp:
    bmid = 0
    
    def __init__(self, root):
        self.root = root
        self.root.title("Car Price Predictor")

         # Create input fields
        self.brand_select = tk.Listbox(root, selectmode=tk.SINGLE, exportselection=False)
        
        # Populate the Listbox with Brand/Model pairs
        for index, row in BMdf.iterrows():
            brand_model = f"{row['Brand']} - {row['Model']}"
            self.brand_select.insert(tk.END, brand_model)

        # Bind the selection event
        self.brand_select.bind("<<ListboxSelect>>", self.on_brand_select)

        validate_num = root.register(self.validate_int)
        self.year_entry = tk.Entry(root, width=30, validate="key", validatecommand=(validate_num, "%P"))
        validate_fltnum = root.register(self.validate_float)
        self.km_entry = tk.Entry(root, width=30, validate="key", validatecommand=(validate_fltnum, "%P"))
        self.CylindersinEngine_entry = tk.Entry(root, width=30, validate="key", validatecommand=(validate_num, "%P"))
        self.EngineCap_entry = tk.Entry(root, width=30, validate="key", validatecommand=(validate_fltnum, "%P"))
        
        # Create variables to store the checkbox values
        self.NEW_checkbox_var = tk.IntVar()
        self.USED_checkbox_var = tk.IntVar()
        self.Unleaded_checkbox_var = tk.IntVar()

        # Create the checkboxs
        self.NEW_checkbox = tk.Checkbutton(root, text="New Car", variable=self.NEW_checkbox_var)
        self.USED_checkbox = tk.Checkbutton(root, text="Used Car", variable=self.USED_checkbox_var)
        self.Unleaded_checkbox = tk.Checkbutton(root, text="Unleaded", variable=self.Unleaded_checkbox_var)


        # Create a button to predict the price
        self.predict_button = tk.Button(root, text="Predict Price", command=self.predict_price)
        
        #Create labels and layout
        # Top row (centered label)
        self.top_label = tk.Label(root, text="Predict A Vehicle Price", font=("Helvetica", 12, "bold"))
        self.top_label.grid(row=0, column=0, columnspan=2, sticky="nsew")

        # Second row (right justified label and listbox)
        self.brand_label = tk.Label(root, text="Select Brand & Model")
        self.brand_label.grid(row=1, column=0, sticky="e")
        self.brand_select.grid(row=1, column=1, sticky="nsew")
      
        # Third row (right justified label and entrybox)
        self.year_label = tk.Label(root, text=f"What Year?")
        self.year_label.grid(row=2, column=0, sticky="e")
        self.year_entry.grid(row=2, column=1, sticky="nsew")

        # Fourth row (right justified label and entrybox)
        self.km_label = tk.Label(root, text=f"How many Kilometers?")
        self.km_label.grid(row=3, column=0, sticky="e")
        self.km_entry.grid(row=3, column=1, sticky="nsew")

        # Fifth row (right justified label and entrybox)
        self.CylindersinEngine_label = tk.Label(root, text=f"How many Cylinders?")
        self.CylindersinEngine_label.grid(row=4, column=0, sticky="e")
        self.CylindersinEngine_entry.grid(row=4, column=1, sticky="nsew")

        # Sixth row (right justified label and entrybox)
        self.EngineCap_label = tk.Label(root, text=f"Enter Engine Capacity in L")
        self.EngineCap_label.grid(row=5, column=0, sticky="e")
        self.EngineCap_entry.grid(row=5, column=1, sticky="nsew")

        # Seventh row (right justified label and entrybox)
        self.NEW_checkbox.grid(row=6, column=0, sticky="w")
        self.USED_checkbox.grid(row=6, column=1, sticky="w")
        
        # Last row (checkbox and button)
        self.Unleaded_checkbox.grid(row=8, column=0, sticky="w")
        self.predict_button.grid(row=8, column=1, sticky="se")

       
        # Set column weights to allow right column expansion
        root.columnconfigure(1, weight=1)

        # Set row weights to allow second row expansion
        root.rowconfigure(1, weight=1)

        # Set minimum window size
        root.update_idletasks()
        min_width = self.brand_select.winfo_reqwidth() + 20  
        min_height = root.winfo_reqheight()
        root.minsize(min_width, min_height)

    def on_brand_select(self, event):
        selected_index = self.brand_select.curselection()[0]
        selected_row = BMdf.iloc[selected_index]
        self.bmid = selected_row['BrandMdlID']
        #print(f"Selected BrandMdlID: {self.bmid}")

    def validate_float(self,P):
        # P is the proposed input value
        try:
            if not P:  # Empty string is considered valid (reverts to 0)
                return True
            float(P)  # Try converting to a float
            return True  # Valid input
        except ValueError:
            return False  # Invalid input (not a number)

    def validate_int(self,P):
        # P is the proposed input value
        try:
            if not P:  # Empty string is considered valid (reverts to 0)
                return True
            int(P)  # Try converting to an int
            return True  # Valid input
        except ValueError:
            return False  # Invalid input (not a number)


    def predict_price(self):
        try:
            # Get input values
            Brand = self.bmid #self.brand_select.get()
            Year = int(self.year_entry.get())
            Kilometres = float(self.km_entry.get())
            
            # Normalize the "Year" 
            Year = (Year - mean_year) / std_year
            
            
            # Normalise and log KM
            Kilometres = np.log(Kilometres+1)
            Kilometres = (Kilometres - mean_km) / std_km
 
            CylindersinEngine = int(self.CylindersinEngine_entry.get())
            EngineCap = float(self.EngineCap_entry.get())
 
            NewChk = self.NEW_checkbox_var.get()
            UsedChk = self.USED_checkbox_var.get()
            UnleadedChk = self.Unleaded_checkbox_var.get()

            # Create a feature vector 
            new_observation = {
                                'BrandMdlID': Brand,
                                'Nml_Year': Year,
                                'Log_Nml_Kilometres': Kilometres,
                                'CylindersinEngine': CylindersinEngine,
                                'EngineCap': EngineCap,
                                'NEW': NewChk,
                                'USED': UsedChk,
                                'Unleaded': UnleadedChk
                            }
            # Convert the dictionary to a pandas DataFrame
            # features = [brand, year, kilometres, CylindersinEngine, EngineCap, NewChk, UsedChk, UnleadedChk]
            features = pd.DataFrame([new_observation])

            # Make a prediction
            predicted_price = loaded_model.predict(features)[0]

            # Show the predicted price
            messagebox.showinfo("Prediction", f"Predicted Price: ${predicted_price:.2f}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CarPricePredictorApp(root)
    
    root.mainloop()