import os
import io
import tempfile
import base64
import streamlit as st
import openmm as openmm

from openmm.app import *
from openmm import *
from openmm.unit import *
from simtk import unit
from pdbfixer import PDBFixer

from PIL import Image  

icon = Image.open('icon.png')

# Streamlit title & icon 
st.set_page_config(
    page_title='ProteinForger',
    page_icon='icon.png', 
    layout= 'centered'
    )

# Convert the image to base64
image_stream = io.BytesIO()
icon.save(image_stream, format='PNG')
encoded_image = base64.b64encode(image_stream.getvalue()).decode()

# Use HTML and CSS to create a horizontal layout
st.markdown(
    f"""
    <div style="display: flex; align-items: center;">
        <img src="data:image/png;base64,{encoded_image}"
        style="width:80px; height:80px; margin-right:10px;">
        <h1>ProteinForger</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# Input and output directory paths
with st.expander('Input and Output Directorires'):
    file_selection = st.radio("Select a file option:", ["Single File", "Multiple Files"]) # Select between single file and multiple files
    
    # Based on the selection, display the appropriate input elements
    if file_selection == "Single File":
        uploaded_file = st.file_uploader(label='Upload a single PDB file',
                                        type=['pdb'], 
                                        accept_multiple_files= False)
        output_dir = st.text_input("Project Title:")
    elif file_selection == "Multiple Files":
        input_dir = st.text_input ("Path of Input Directory",
                                help="For multiple proteins: give complete address of directory !")
        output_dir = st.text_input("Project Title",
                                help="Project title will be used as output directory !")


# Create an option for the force field
with st.expander('Force Field & Water Model'):
    force_field_choice = st.radio("Select Force Field",
                                ["CHARMM36", "AMBER-14"],
                                help="Recommended force field: CHARMM36")
    if force_field_choice == "CHARMM36":
        water_model_choice = st.radio("Water Model",
                                    ["CHARMM/water"])
        water_model_xml = 'charmm36/water.xml' # Path to the XML file
    elif force_field_choice == "AMBER-14":
        water_model_choice = st.radio("Water Model",
                                    ["TIP3P-FB"])
        water_model_xml = 'amber14/tip3pfb.xml'

# Define the corresponding XML files
forcefield_xml = None
if force_field_choice == 'AMBER-14':
    forcefield_xml = 'amber14/protein.ff14SB.xml'
elif force_field_choice == 'CHARMM36':
    forcefield_xml = 'charmm36.xml'

# Select Platform name
with st.expander('Platform'):
    platform_selection = st.radio("Select a Platform", 
                                ("CPU", "CUDA"),
                                help="Select CPU / GPU (CUDA)")

# Create a temporary directory to save uploaded files
temp_dir = tempfile.TemporaryDirectory()

# Define Number of Steps
steps = st.number_input("Number of Steps for Minimization:",
                        min_value = 1,
                        value= 100,
                        help="Recommended: 100 steps")

if st.button("Minimize"):
    os.makedirs(output_dir, exist_ok=True)  # Create the output directory
    pdb_files = []
    
    if file_selection == "Single File" and uploaded_file is not None:
        uploaded_file_path = os.path.join(temp_dir.name, uploaded_file.name)    # Save the uploaded file to the temporary directory
        with open(uploaded_file_path, "wb") as f:
            f.write(uploaded_file.read())
        pdb_files = [uploaded_file_path] 
    elif file_selection == "Multiple Files" and input_dir:
        pdb_files.extend([os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.endswith(".pdb")]) # List all PDB files in the input directory
    else:
        st.error("Please provide input files.", icon="⚠️")
        st.stop()

    if not any(file.endswith(".pdb") for file in pdb_files):    # Check if pdb_files contains any .pdb files
        st.error("No PDB files found in the selected input.", icon="⚠️")
        st.stop()
    
    print("Force Field XML:", forcefield_xml)
    print("Water Model XML:", water_model_xml)
    st.info("Minimization started...", icon="🚨")
    st.toast("Script Initiated", icon="🚨")
    
    # Load the force field
    forcefield = ForceField(forcefield_xml, water_model_xml)
    for pdb_file_path in pdb_files:
        # Load PDB file
        print(f'Loading {pdb_file_path}')
        st.write(f'Loading {os.path.basename(pdb_file_path)}')
        pdb = PDBFile(pdb_file_path)
        
        # Use PDBFixer to check and add missing heavy atoms and hydrogens
        fixer = PDBFixer(filename=pdb_file_path)
        
        # Find and add missing heavy atoms
        fixer.findMissingResidues()
        fixer.findMissingAtoms()
        fixer.addMissingAtoms()
        
        # Add missing hydrogens
        st.write('Adding Hydrogens')
        fixer.addMissingHydrogens(7.0)
        
        # Create a modeller based on the fixed structure
        modeller = Modeller(fixer.topology, fixer.positions)
        
        # Add solvent
        print('Adding Solvent')
        st.write('Adding Solvent')
        modeller.addSolvent(forcefield, model='tip3p', padding=1 * unit.nanometer)
        
        # Create a system
        print('Creating a System')
        st.write('Creating a System')
        system = forcefield.createSystem(modeller.topology, nonbondedMethod=app.PME)
        
        # Create an integrator
        integrator = LangevinIntegrator(300 * unit.kelvin, 1 / unit.picosecond, 0.002 * unit.picoseconds)
        
        # Create a simulation
        simulation = Simulation(modeller.topology, system, integrator, Platform.getPlatformByName(platform_selection))
        
        # Set the initial positions
        simulation.context.setPositions(modeller.positions)
        
        # Minimize energy
        print('Minimizing ...')
        st.write('Minimizing ...')
        simulation.minimizeEnergy(maxIterations=steps)
        
        st.write(f'Minimization of {os.path.basename(pdb_file_path)} completed :)')
        
        # Get the minimized positions
        positions = simulation.context.getState(getPositions=True).getPositions()
        
        # Create subdirectory based on the basename of the file
        basename = os.path.splitext(os.path.basename(pdb_file_path))[0]
        subdirectory = os.path.join(output_dir, os.path.splitext(os.path.basename(pdb_file_path))[0])
        os.makedirs(subdirectory, exist_ok=True)
        
        # Save the minimized_raw structure (contains water & ions) in the subdirectory
        raw_pdb_path = os.path.join(subdirectory, f'{basename}_minimized_raw.pdb')
        with open(raw_pdb_path, 'w') as raw_pdb_file:
            PDBFile.writeFile(simulation.topology, positions, raw_pdb_file)
        print(f"Processed: {os.path.basename(pdb_file_path)}")
        
        # Remove Heterogens (water + ions)
        fixer = PDBFixer(filename=raw_pdb_path)
        fixer.removeHeterogens(keepWater=False)
        
        # Save both cleaned & minimized structures in the subdirectory
        clean_pdb_path = os.path.join(subdirectory, f'{basename}_minimized_clean.pdb')
        with open(clean_pdb_path, 'w') as clean_pdb_file:
            PDBFile.writeFile(fixer.topology, fixer.positions, clean_pdb_file)
        
        print('Heterogens Removed')
        st.write('Heterogens Removed')
        
    # Clean up the temporary directory
    temp_dir.cleanup()
    print('All files have been processed !')
    st.success('All files have been processed !')
    st.info('Minimized protein structures generated in respective subdirectory(ies) !')
