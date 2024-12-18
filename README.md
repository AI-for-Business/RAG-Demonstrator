# Getting started

Please install a wsl distro of your choice or run on Linux. I will assume that you use a distro based on apt, if not, use the package manager that comes with your distro. 

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


