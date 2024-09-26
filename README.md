

# Peppercorn AI

---<img width="1273" alt="main_page_wall" src="https://github.com/user-attachments/assets/07786197-fd8f-4444-8cf3-21dc0afb4ba2">



## Project Description

Peppercorn AI is an AI-powered email marketing tool designed to enhance drip campaign marketing by personalizing emails. The tool intelligently merges customer data with AI-generated email content, optimizing engagement and conversion rates for marketing campaigns.

## Features
- AI-powered email personalization
- Customizable email templates
- Drip campaign management
- Customer data integration

## Tech Stack
- **Backend:** Python, FastAPI
- **Database:** MongoDB
- **Frontend:** JavaScript, React
- **Other Tools:** Email handling API

## Project Structure

```bash
|-- backend/
|   |-- app/
|       |-- main.py  # FastAPI application
|       |-- models/  # MongoDB models
|       |-- routes/  # API routes for handling user login, registration, etc.
|       |-- services/  # Email and AI services
|
|-- frontend/
|   |-- src/
|       |-- components/  # React components for login, registration, etc.
|       |-- services/  # Services for making API calls
|       |-- App.js  # Main React app
|
|-- README.md  # This file
```

## Installation

### Backend

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/peppercorn-ai.git
   ```
2. Navigate to the `backend` directory:
   ```bash
   cd peppercorn-ai/backend
   ```
3. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # For Windows use `venv\Scripts\activate`
   ```
4. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Start the FastAPI server:
   ```bash
   uvicorn app.main:app --reload
   ```

### Frontend

1. Navigate to the `frontend` directory:
   ```bash
   cd ../frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Run the React application:
   ```bash
   npm start
   ```

