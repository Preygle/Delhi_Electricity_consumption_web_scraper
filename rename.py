import requests
import os
from datetime import datetime, timedelta


def generate_urls():
    # Start and end dates
    start_date = datetime(2024, 9, 1)
    end_date = datetime(2024, 9, 7)

    # List to store URLs
    url_list = []

    # Generate URLs for each date from start_date to end_date
    current_date = start_date
    while current_date <= end_date:
        # Format the date in 'dd.mm.yy'
        dd_mm_yy = current_date.strftime('%d.%m.%y')
        # Extract the month name without the year (2024 was removed)
        month_yyyy = current_date.strftime('%B')

        # Create the URL
        url = f"https://report.grid-india.in/ReportData/Daily%20Report/PSP%20Report/2024-2025/{month_yyyy}%202024/{dd_mm_yy}_NLDC_PSP.pdf"
        url_list.append(url)

        # Check if the day is the 23rd

        # Move to the next date
        current_date += timedelta(days=1)

    return url_list


# Generate the URLs
urls = generate_urls()

# Print the URLs
for url in urls:
    print(url)

output_dir = "sep"

if not os.path.exists(output_dir):  # Create the output directory if it doesn't exist
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
