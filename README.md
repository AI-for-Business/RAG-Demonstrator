# A simple RAG - Demonstrator

RAG, or retrieval augmented generation, is a method of supplementing generative AI models with specific knowledge. This simple streamlit prototype shows off the capabilities of RAG.

# Quick Setup

Install [Docker](https://docs.docker.com/desktop/setup/install/windows-install/) and start the Docker daemon by starting the Docker Desktop app.

Create and run the image: `docker compose up --build`. Ollama and Streamlit will run in seperate containers.

You can now reach the ui locally at http://127.0.0.1:8501/

# Advanced Setup without Docker

Please install a wsl distro of your choice or run on Linux. This assumes that you use a distro based on apt, if not, use the package manager that comes with your distro. 

## Ollama

First, install ollama locally
`curl -fsSL https://ollama.ai/install.sh | sh`

Then, run it via `ollama serve`. In a new Terminal, install the latest model suitable for your machine. As of time of writing, this is llama3.2. `ollama pull "llama3.2"`. Additionally, install nomic-embed-text via `ollama pull "nomic-embed-text"` 

## Python

Install python3 `sudo apt install python3`. 

If necessary, install pip and venv seperately `sudo apt install python3-pip` `python3 -m pip install virtualenv`.

Create a virtual environment: `python3 -m venv venv`

Activate the virtual environment: `source venv/bin/activate`. 

Inside the venv, install the required packages: `pip install -r requirements.txt`

Finally, copy the .env.example file to a normal .env file and paste a valid openai key. Do not commit this key, ever. 

## Running the Demonstrator locally

Run ollama via `ollama serve`. In a seperate window, start the model of your choice `ollama run <model>`. 

Activate the virtual environment as before `source venv/bin/activate`. 

Then, start the streamlit app `streamlit run ui.py`






