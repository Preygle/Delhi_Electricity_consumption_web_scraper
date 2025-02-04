# code to extract a particular data (Here Delhi's max demand met and energy met) and store it in excel for ML purpose

import os
import pdfplumber
import pandas as pd

city = 'Delhi'

def extract_delhi_values(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[1] # Required value is in page 2 of the PDF
        text = page.extract_text()
        lines = text.split('\n')
        for line in lines:
            if city in line: # Search city data
                words = line.split()
                max_demand_met = words[1] # max demand is in column 2 on the row containing city
                energy_met = words[3]  # energy met is in column 4 on the row containing city
                # words[1] = Max Demand
                # words[2] = Shortage during max demand
                # words[3] = Energy Met
                # words[4] = Drawn Schedule
                # words[5] = OD(+) / UD(-)
                # words[6] = Max OD
                # words[7] = Energy Shortage
                
                return max_demand_met, energy_met

    return None, None # If not found

output_dir = r"Your_DIR" # Dir containing the pdfs of extracted data
data = []

for file_name in os.listdir(output_dir): # Iterate through each PDF in the directory
    if file_name.endswith(".pdf"): # make sure no other pdfs are present in the directory
        pdf_path = os.path.join(output_dir, file_name)
        max_demand_met, energy_met = extract_delhi_values(pdf_path)
        if max_demand_met and energy_met: # If not null
            date_str = file_name.split('_')[0]  # Extracting 'dd.mm.yy' part which is unique to each pdf
            date = pd.to_datetime(date_str, format='%d.%m.%y')
            data.append([date, max_demand_met, energy_met]) # Apeending date and values to data list
            print(date)

columns = ['Date', 'Max Demand Met (MW)', 'Energy Met (MU)']
df = pd.DataFrame(data, columns=columns) # Convert the data list into a DataFrame
df = df.sort_values(by='Date') # Sorting dataframe by date
output_excel = r"Output_DIR" 
df.to_excel(output_excel, index=False)  # Saving to excel
print(f"Data has been saved to {output_excel}")
