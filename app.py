from flask import Flask, request, send_file, jsonify
import os
import csv
from datetime import datetime

app = Flask(__name__)

# Define the directory for saving CSV files
JOBTIME_CSV_DIR = '/u/abas/keserp/win/LABOR_IMPORT/'
PAYROLL_CSV_DIR = '/u/abas/keserp/win/PAYROLL_IMPORT/'

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
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S%f')  # Format: YYYYMMDDHHMMSS
    unique_file_name = f"jobtime_{abas_id}_{timestamp}.csv"

    # Define the network location for the CSV file
    csv_file_path = os.path.join(JOBTIME_CSV_DIR, unique_file_name)

    # Write the entry to the CSV file
    try:
        with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)
            # Write the header
            csv_writer.writerow(['AbasID', 'Date', 'WorkSlipID', 'HoursWorked'])
            # Write the entry
            csv_writer.writerow([
                abas_id,
                selected_date,
                work_slip_id,
                "0" if float(hours_worked) == 0 else f"{float(hours_worked):.2f}"
            ])
            
        # Return a success response
        return jsonify({'success': True, 'message': 'Data successfully imported.'}), 200
    except Exception as e:
        return {"error": f"Failed to write CSV file: {str(e)}"}, 500    


@app.route('/payroll_import', methods=['POST'])
def payroll_import():
    try:
        # Get the JSON data from the request
        data = request.get_json()

        # Extract abas_id, total_hours, and time_entries
        abas_id = data.get('abas_id')
        total_hours = data.get('total_hours')
        time_entries = data.get('time_entries')

        # Validate the data
        if not abas_id or not total_hours or not time_entries or not isinstance(time_entries, list):
            return jsonify({'success': False, 'error': 'Invalid data format.'}), 400

        # Generate a unique file name using a timestamp
        timestamp = datetime.now().strftime('%Y%m%d')  # Format: YYYYMMDDHHMMSS
    
        # Define the CSV file path
        csv_file_path = os.path.join(PAYROLL_CSV_DIR, f'payroll_{abas_id}_{timestamp}.csv')

        # Write the data to the CSV file
        with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file)

            # Write the header row
            csv_writer.writerow(['Abas ID', 'Date', 'Paychex Code', 'Hours', 'Comment'])

            # Write each row of data
            for entry in time_entries:
                csv_writer.writerow([
                    abas_id,
                    entry.get('date', ''),
                    entry.get('paychexCode', ''),
                    f"{float(entry.get('hours', 0)):.2f}",  # Limit to 2 decimal places
                    entry.get('comments', '')
                ])

        # Return a success response
        return jsonify({'success': True, 'message': 'Data successfully imported.'}), 200

    except Exception as e:
        # Handle any errors
        return jsonify({'success': False, 'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)


if __name__ == '__main__':
    app.run(debug=True)