Pavan-Putra Invoice Generator
An enterprise-grade billing and international trade automation engine built using a localized Agentic Harness architecture. This project replaces fragile, cloud-sandbox autonomous setups with a highly controlled local environment that perfectly bridges messy human natural language intent with deterministic financial validation logic.

System Architecture and Features
The Cognitive Engine: Powered by gemini-2.0-flash to execute intent parsing, parameter extraction, and structural entity mapping.

The Local Harness: Built with a FastAPI backend framework and a Tailwind CSS frontend dashboard.

Multi-Tool Orchestration: Integrated with a live currency data pipeline (fetch_live_exchange_rates) to query and scale global indices automatically.

Data Ingestion: Supports manual entry grid arrays, custom AI copilot text strings, and automated Excel/CSV line-item sheet parsing.

Local Deployment Setup Guide
Follow these steps to deploy and execute the Pavan-Putra Command Center on your local machine:

1. Environment Initialization
Clone this repository to your directory, navigate inside, and initialize a clean virtual sandbox by running the following commands in your terminal:

python -m venv venv

.\venv\Scripts\activate

2. Dependency Ingestion
Install all required web, multi-format parsing, and PDF report compilation binaries by entering this command:

pip install -r requirements.txt

3. Configure Your Credentials
Create a file named .env in the root directory and mount your secure access key exactly like this, replacing the placeholder with your actual key:

GEMINI_API_KEY=your_actual_api_key_here

4. Boot Up the Engine
Launch the Uvicorn web deployment server natively on Windows using this explicit path command:

.\venv\Scripts\python.exe app.py

Once executed, open your web browser and point it to http://127.0.0.1:5000 to access the live dashboard workspace.