import os
import pdfplumber
import pandas as pd


def extract_delhi_values(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[1] # Required value is is page 2 of PDF
        text = page.extract_text()
        lines = text.split('\n')
        for line in lines:
            if "Delhi" in line: # Search Delhi data
                words = line.split()
                max_demand_met = words[1] # Required data is in coulumn 2 and 4 on the row containing Delhi
                energy_met = words[3]
                return max_demand_met, energy_met

    return None, None # If not found

output_dir = r"C:\Users\moham\Documents\PROGRAMMING\sep"
data = []

for file_name in os.listdir(output_dir):# Iterate through each PDF in the directory
    if file_name.endswith(".pdf"):
        pdf_path = os.path.join(output_dir, file_name)
        max_demand_met, energy_met = extract_delhi_values(pdf_path)
        if max_demand_met and energy_met: # If not null
            date_str = file_name.split('_')[0]  # Extracting 'dd.mm.yy' part
            date = pd.to_datetime(date_str, format='%d.%m.%y')
            data.append([date, max_demand_met, energy_met]) # Apeending date and values to data list
            print(date)

columns = ['Date', 'Max Demand Met (MW)', 'Energy Met (MU)']
df = pd.DataFrame(data, columns=columns) # Convert the data list into a DataFrame
df = df.sort_values(by='Date') # Sorting dataframe by date
output_excel = r"C:\Users\moham\Documents\PROGRAMMING\september.xlsx" 
df.to_excel(output_excel, index=False)  # Saving to excel
print(f"Data has been saved to {output_excel}")
