from flask import Flask, request, send_file
import pandas as pd
import os

app = Flask(__name__)

@app.route('/create_csv', methods=['POST'])
def create_csv():
    data = request.json
    if not data or 'filename' not in data or 'content' not in data:
        return {"error": "Invalid input. Please provide 'filename' and 'content'."}, 400

    filename = data['filename']
    content = data['content']

    # Create a DataFrame from the content
    df = pd.DataFrame(content)

    # Save the DataFrame to a CSV file
    csv_file_path = os.path.join('static', filename)
    df.to_csv(csv_file_path, index=False)

    return send_file(csv_file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)