# ABAS WebApp API Server

This project is a simple API server built using Flask that allows users to create and download CSV files.

## Project Structure

```
abaswebapp-api-server
├── app.py                # Main entry point of the Flask application
├── requirements.txt      # Lists the dependencies required for the project
├── static                # Directory for static files (CSS, JavaScript, images)
├── templates             # Directory for HTML templates
└── README.md             # Documentation for the project
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd abaswebapp-api-server
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Run the Flask application:
   ```
   python app.py

   or 

   gunicorn -w 4 -b 0.0.0.0:8000 app:app
   ```



2. The server will start on `http://127.0.0.1:5000/`.

3. To create a CSV file, send a POST request to the `/create-csv` endpoint with the necessary data.

## API Endpoints

- `POST /create-csv`: Generates a CSV file based on the provided data.

## License

This project is licensed under the MIT License.