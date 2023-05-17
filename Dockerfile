FROM python:slim-buster

WORKDIR /app

# Install dependencies
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# Copy all files
COPY . .

# Expose port
EXPOSE 8501

# Run streamlit app
ENTRYPOINT ["streamlit", "run", "src/homepage.py", "--server.port=8501", "--server.address=0.0.0.0"]