#code to download pdfs from a specific timeline for electricity consumption in India
#site used 'https://report.grid-india.in/psp_report.php'

import requests
import os
from datetime import datetime, timedelta


def generate_urls():
    # Start and end dates
    start_date = datetime(YYYY, MM, DD)
    end_date = datetime(YYYY, MM, DD)

    # List to store URLs
    url_list = []
    
    current_date = start_date
    while current_date <= end_date:
        dd_mm_yy = current_date.strftime('%d.%m.%y')
        # Extract the month name without the year for required pdf link expression
        month_yyyy = current_date.strftime('%B')

        # Create the URL RegEx
        url = f"https://report.grid-india.in/ReportData/Daily%20Report/PSP%20Report/2024-2025/{month_yyyy}%202024/{dd_mm_yy}_NLDC_PSP.pdf"
        url_list.append(url)
        #iterating days
        current_date += timedelta(days=1)

    return url_list


# Generate the URLs
urls = generate_urls()

# Print the URLs
for url in urls:
    print(url)

#directory to store all the pdfs
output_dir = "sep"

# Create the output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

for url in urls:
    response = requests.get(url)  # Send a GET request to the URL
    if response.status_code == 200:   # 200 is the HTTP status code for a successful request
        file_name = os.path.basename(url)
        with open(os.path.join(output_dir, file_name), "wb") as f:
            # Save the PDF file to the output directory
            f.write(response.content)
        print(f"Downloaded {file_name}")
    else:
        print(f"Failed to download {url}")
        break
