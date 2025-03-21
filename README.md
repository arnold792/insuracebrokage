# Insurance Brokerage Management System

A comprehensive Flask-based web application for managing an insurance brokerage business. The system handles clients, policies, claims, payments, agents, underwriters, accidents, and beneficiaries.

## Features

- Client Management
- Policy Administration
- Claims Processing
- Payment Tracking
- Agent Management
- Underwriter Management
- Accident Reporting
- Beneficiary Management

## Tech Stack

- Python 3.x
- Flask
- MySQL
- SQLAlchemy
- Flask-Migrate
- TailwindCSS

## Prerequisites

- Python 3.x
- MySQL Server
- Node.js (for TailwindCSS)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd flaskdatabase
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Install Node.js dependencies:
```bash
npm install
```

4. Configure the database:
   - Create a MySQL database named 'insurance'
   - Update the database URI in `app.py` if needed

5. Initialize the database:
```bash
flask db upgrade
python init_db.py
```

6. (Optional) Add sample data:
```bash
python populate_db.py
```

## Running the Application

1. Build the CSS:
```bash
npm run build
```

2. Start the Flask server:
```bash
flask run
```

3. Visit `http://localhost:5000` in your browser

## Development

- Run TailwindCSS in watch mode:
```bash
npm run watch
```

- Run Flask in debug mode:
```bash
flask run --debug
```

## Project Structure
