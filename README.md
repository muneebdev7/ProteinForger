# Protein-Forger

This GitHub repository have listed all the dependencies (in yml file) & the necessary files for Proteinforger.
You just need to create a conda environment using the yml file.

## Create an openmm environment (Only once)

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

## User Manual for Proteinforger

 1. Clone the repository & then go to the downloaded directory.
 2. Open the **terminal** in the directory and write the following command:

    ```shell
    conda activate openmm
    ```

 3. Then **run python script** through streamlit using following command:

    ```shell
    streamlit run proteinforger
    ```

    * OR simply **run bash script** in the terminal:

    ```bash
    ./proteinforger.sh
    ```

 4. A web-page will open.
 5. Select the necessary options & do not forget to specify the Project Title
 6. By default CPU will be used for minimization but if you have multiple proteins, **GPU/CUDA** option can be selected.
 7. Hit the **Minimize** button.

### Note

* Default Force Field will be CHARMM36
* Default Platform will be CPU
* Default # of Minimization steps would be 100. (for small proteins)
* Refer to the excel file (ERRAT.xlsx) regarding suggested Number of Minimization Steps, for reference.

Author's Note:  For further assistance email us at <muneebgojra@gmail.com>
This app was originally built at BioCode.ltd
