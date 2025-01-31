#!/bin/bash

# Start serving ollama in the background

ollama serve &
echo("Serving ollama...")

# Need this sleep to start ollama in the background
sleep 10

ollama pull llama 3.2

streamlit run ui.py --server.port=8501 --server.adress=0.0.0.0
