FROM continuumio/miniconda3

# Set the working directory in the container
WORKDIR /app

# Copy the Conda environment file from the parent directory
COPY openmm.yml .

# Create the Conda environment and clean up to reduce image size
RUN conda env create -f ./openmm.yml && conda clean -afy

# Set PATH to use the Conda environment
ENV PATH=/opt/conda/envs/openmm/bin:$PATH

# Copy the app files
COPY . .

# Copy Streamlit configuration (To avoid the security warnings)
# Because this app is configured to run on local machine
COPY /docker/config.toml /root/docker/config.toml

# Ensure correct permissions
RUN chmod -R 755 /app

# Expose the port for Streamlit
EXPOSE 8501

# Run the Streamlit app
CMD ["streamlit", "run", "proteinforger.py"]
