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

# Hosting on Azure


# Getting Started

First off, due to weird azure quirks, you have to replace all instances of ollama:11434 with localhost 11434. Custom domains do not work in azure, and docker compose does not work with localhost.  

Install the Azure package:

```Powershell
Update-Module -Name Az -Force
```

Next, login to Azure

``` Powershell
az login
az acr login --name <Name_of_container_Registry>
```

Then, tag the image that you want to push

``` Powershell
docker images
docker tag rag-demonstrator-rag-demonstrator <name-of-login-server (e.g: ragprototyp.azurecr.io)>/ui
docker tag ollama/ollama <name-of-login-server (e.g: ragprototyp.azurecr.io)>/ollama
```

Push the images to the registry via the tags:

``` PowerShell
docker push <name-of-loginserver>/ui
docker push <name-of-login-server>/ollama
```

Next, we create the Web-App in Azure. Navigate to portal.azure.com and create the Webapp Service. Select a plan with at least 8gb RAM. Under container, make sure to enable sidecar support. Select the ui container and specify the port (8501). Once the container is spun up, go to the tab Deployment Center and add a custom container. Here, add your previously pushed ollama image and specify the port (11434). Wait until the ollama container is running, now you should be able to use the webapp in Azure.

Make sure to stop the container when you are not using it anymore. The 8GB server is very expensive.

# Copyright / License
This work is licensed under a Creative Commons Attribution 4.0 International License (CC BY-NC-SA 4.0).

![](CC-BY-NC-SA.jpg)
 
As such:

### You are free to:
* Share — copy and redistribute the material in any medium or format
* Adapt — remix, transform, and build upon the material
* The licensor cannot revoke these freedoms as long as you follow the license terms.

### Under the following terms:
* Attribution — You must give appropriate credit , provide a link to the license, and indicate if changes were made . You may do so in any reasonable manner, but not in any way that suggests the licensor endorses you or your use.
* NonCommercial — You may not use the material for commercial purposes .
* ShareAlike — If you remix, transform, or build upon the material, you must distribute your contributions under the same license as the original.

# Contact / About us
* You can find all of our repositories [here](https://github.com/orgs/AI-for-Business/repositories).
* You can find the homepage of the project ABBA: **A**I for **B**usiness | **B**usiness for **A**I
[here](https://abba-project.de/).
* You can contact the authors by sending us an [email](mailto:abba-services@fim-rc.de).
