# Protein-Forger

This GitHub repository contains all the dependencies (in yml file) & the necessary files for Proteinforger.
You just need to create a conda environment using the yml file.

[![run with conda](http://img.shields.io/badge/run%20with-conda-3EB049?labelColor=000000&logo=anaconda)](https://docs.conda.io/en/latest/)
[![run with docker](https://img.shields.io/badge/run%20with-docker-0db7ed?labelColor=000000&logo=docker)](https://www.docker.com/)
[![Platform](https://img.shields.io/badge/platform-linux-blue)](https://github.com/muneebdev7/proteinforger)

![Lisence MIT](https://anaconda.org/bioconda/nf-core/badges/license.svg)

## Create Conda Environment

 1. Go to directory where attached openmm.yml is downloaded.
 2. Open the terminal & type the following command:

    ```shell
    conda env create -f openmm.yml
    ```

 3. It would automatically make a conda environment naming **openmm**
 4. Verify the env creation by following command:

    ```shell
    conda env list
    ```

## Build and Run a Docker Image

If you prefer to run the app in a docker image instead of a conda environment. Then build the Docker image by following these steps:

1. Open a terminal and navigate to the directory containing the `Dockerfile`.
2. Build the Docker image using the following command:

    ```sh
    docker build -t proteinforger:latest .
    ```

3. Once the image is built, you can run the Docker container using the following command:

    ```sh
    docker run -p 8501:8501 proteinforger:latest
    ```

This will start the Streamlit app, and you can access it by navigating to `http://localhost:8501` in your web browser.

### Stopping the Docker Container

To stop the Docker container running the app, follow these steps:

1. List the running Docker containers to find the container ID:

   ```sh
   docker ps
   ```

2. Stop the Docker container using the container ID:

   ```sh
   docker stop <container_id>
   ```

Replace `<container_id>` with the actual container ID from the previous command.  >

## User Manual for Proteinforger

 1. Clone the repository & then go to the downloaded directory.
 2. Open the **terminal** in the directory and write the following command:

    ```shell
    conda activate openmm
    ```

 3. Then **run python script** through streamlit using following command:

    ```shell
    streamlit run proteinforger.py
    ```

    * OR simply **run bash script** in the terminal:

    ```bash
    ./proteinforger.sh
    ```

 4. This will start the Streamlit app, and you can access it by navigating to `http://localhost:8501` in your web browser.
 5. Select the necessary options & do not forget to specify the Project Title.
 6. By Default CPU will be used for minimization but if you have multiple proteins, **GPU/CUDA** option can be selected.
 7. Hit the **Minimize** button.

> [!NOTE]
   >
   >* Default Force Field will be **CHARMM36**
   >* Default Platform will be **CPU**
   >* Default # of Minimization steps would be 100. (for small proteins)
   >* Refer to the excel file [`ERRAT.xlsx`](benchmark/ERRAT.xlsx) regarding suggested Number of Minimization Steps, for reference.
   >
> Author's note:  For further assistance email me at <muneebgojra@gmail.com>
   >
   > *This app was originally built at BioCode.ltd*
