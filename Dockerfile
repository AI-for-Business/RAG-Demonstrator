FROM python:3.10-slim

WORKDIR /root

COPY . .
RUN apt update && apt install -y python3 python3-pip git
RUN pip install -r requirements.txt

EXPOSE 8501

CMD ["streamlit", "run", "ui.py", "--server.port=8501", "--server.address=0.0.0.0"]
