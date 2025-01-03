import chardet
import streamlit as st
import pandas as pd  # Missing import added
import matplotlib.pyplot as plt
import seaborn as sns

# Importing all the entities from different python files
from ECDF import *
from HISTPLOT import *
from KDEPLOT import *
from RUGPLOT import *
from DISPLOT import *
from LINEPLOT import *
from RELPLOT import *
from SCATTERPLOT import *
from CATPLOT import *         
from STRIPPLOT import *       
from SWARMPLOT import *    
from BOXPLOT import *      
from VIOLINPLOT import *     
from BOXENPLOT import *      
from POINTPLOT import *       
from BARPLOT import *         
from COUNTPLOT import *      
from LMPLOT import *        
from REGPLOT import *         
from RESIDPLOT import *      
from HEATMAP import *         
from CLUSTERMAP import *      
from FACETGRID import *       
from PAIRPLOT import *        
from PAIRGRID import *        
from JOINTPLOT import *       
from JOINTGRID import *      
from fpdf import FPDF

def download_pdf(selected_graph_plots):
    if selected_graph_plots:
        pdf = FPDF()
        for img in selected_graph_plots:
            pdf.add_page()
            pdf.image(img, x=0, y=0, w=210)
        pdf_output = "plots_output.pdf"
        pdf.output(pdf_output)
        with open(pdf_output, "rb") as file:
            st.download_button(
                label="Download PDF",
                data=file,
                file_name=pdf_output,
                mime="application/pdf"
            )
    else:
        st.error("No images to download.")

def readCSV(uploaded_file):
    raw_data = uploaded_file.getvalue()
    detected_encoding = chardet.detect(raw_data)
    encoding = detected_encoding['encoding']   
    try:
        df = pd.read_csv(uploaded_file, encoding=encoding)
        return df
    except UnicodeDecodeError:
        try:
            uploaded_file.seek(0)
            df = pd.read_csv(uploaded_file, encoding='utf-8')
            return df
        except UnicodeDecodeError:
            try:
                uploaded_file.seek(0)
                df = pd.read_csv(uploaded_file, encoding='ISO-8859-1')
                return df
            except Exception as e:
                print(f"Error reading the file: {e}")
                return None

listVariables = [
    "rugplot", "ecdf", "kdeplot", "histplot", "displot", "relplot", "scatterplot", 
    "lineplot", "catplot", "stripplot", "swarmplot", "boxplot", "violinplot", 
    "boxenplot", "pointplot", "barplot", "countplot", "lmplot", "regplot", 
    "residplot", "heatmap", "clustermap", "FacetGrid", "pairplot", "PairGrid", 
    "jointplot", "JointGrid"
]

for i in listVariables:
    if i not in st.session_state:
        st.session_state[i] = []

file = st.sidebar.file_uploader("Upload the CSV file", type=["csv"])
st.sidebar.divider()
selectedPlot = st.sidebar.radio("Select the plot", listVariables)

col1, col2 = st.columns([2, 1])
with col1:
    if file is not None:
        df = readCSV(file)
        if isinstance(df, pd.DataFrame):
            # Add your plot-specific logic here
            pass
        else:
            st.error("Failed to load the CSV file. Please upload a valid file.")
with col2:
    selectedGraph = st.selectbox("Select any graph to see the saved plots", st.session_state.keys())
    if selectedGraph:
        for i in st.session_state[selectedGraph]:
            st.image(i, caption=f"Plot {i}", width=400)  # Removed `height` argument
            if st.button("Download it into a PDF"):
                download_pdf(st.session_state[selectedGraph])
