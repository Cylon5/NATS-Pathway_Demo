# Use the official Pathway image
FROM pathwaycom/pathway:latest

# Set the working directory
WORKDIR /app 

# Copy the requirements file and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Command to run the Pathway script
CMD ["python", "./app.py"]