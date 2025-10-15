# Use the official Pathway image
FROM pathwaycom/pathway:latest

# Set the working directory
WORKDIR /app 

# Copy the requirements file and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install jupyter nbconvert notebook

# Copy the rest of the application code
COPY . .

# Make the entrypoint script executable
RUN chmod +x entrypoint.sh

# Expose the port for the Jupyter server
EXPOSE 8888

# Set the command to run when the container starts
ENTRYPOINT ["./entrypoint.sh"]