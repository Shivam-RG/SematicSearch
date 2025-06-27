FROM python:3.13.5

# Set the working directory
WORKDIR /app

# Install curl and dependencies
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*


# Install the dependencies
RUN python -m pip install --no-cache-dir -r requirements.txt

# download retriever from github release
RUN mkdir -p artifacts && \
    curl -L "https://github.com/Shivam-RG/SematicSearch/releases/download/v.0.1/retriever.pkl" -o artifacts/retriever.pkl

# Copy your application code
COPY . .

# Expose the port FastAPI will run on
EXPOSE 5000

# Command to run the FastAPI app
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
