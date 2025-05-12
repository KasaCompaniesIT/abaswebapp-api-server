from flask import Flask, request, send_file
import os
import csv
from datetime import datetime

app = Flask(__name__)

# Define the directory for saving CSV files
CSV_DIRECTORY = '/u/abas/kesdemo/win/LABOR_IMPORT/'

@app.route('/jobtime_entry', methods=['POST'])
def jobtime_entry():
    data = request.json
    if not data or 'EmpID' not in data or 'WorkDate' not in data or 'WSNumber' not in data:
        return {"error": "Invalid input. Please provide 'EmpID', 'WorkDate', and 'WSNumber'."}, 400

    # Extract entry details
    abas_id = data['EmpID']
    selected_date = data['WorkDate']
    work_slip_id = data['WSNumber']
    hours_worked = data['HoursWorked']

    # Generate a unique file name using a timestamp
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')  # Format: YYYYMMDDHHMMSS
    unique_file_name = f"jobtime_{abas_id}_{timestamp}.csv"

    # Define the network location for the CSV file
    csv_file_path = os.path.join(CSV_DIRECTORY, unique_file_name)

    # Write the entry to the CSV file
    try:
        with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)
            # Write the header
            csv_writer.writerow(['AbasID', 'Date', 'WorkSlipID', 'HoursWorked'])
            # Write the entry
            csv_writer.writerow([abas_id, selected_date, work_slip_id, hours_worked])
    except Exception as e:
        return {"error": f"Failed to write CSV file: {str(e)}"}, 500

    # Return the file as a downloadable attachment
    return send_file(csv_file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)