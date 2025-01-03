import chardet
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from fpdf import FPDF

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

def download_pdf(selected_graph_plots):
    if selected_graph_plots:
        # Create instance of FPDF class
        pdf = FPDF()

        # Loop through all images and add them to the PDF
        for img in selected_graph_plots:
            pdf.add_page()

            # Save the matplotlib plot as an image
            img_path = f"temp_plot_{selected_graph_plots.index(img)}.png"
            img.savefig(img_path)
            pdf.image(img_path, x=0, y=0, w=210)

        # Save the PDF to a file
        pdf_output = "plots_output.pdf"
        pdf.output(pdf_output)

        # Provide the PDF for download in Streamlit
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
        if not raw_data.strip():  # Check if the file is empty
            st.error("The uploaded file is empty. Please upload a valid CSV file.")
            return None
        
        df = pd.read_csv(uploaded_file, encoding=encoding)
        return df
    except pd.errors.EmptyDataError:
        st.error("The uploaded file appears to be empty. Please check the file content.")
        return None
    except UnicodeDecodeError:
        try:
            st.warning(f"Encoding {encoding} failed. Retrying with 'utf-8'...")
            uploaded_file.seek(0)
            df = pd.read_csv(uploaded_file, encoding='utf-8')
            return df
        except UnicodeDecodeError:
            try:
                st.warning("Encoding 'utf-8' failed. Retrying with 'ISO-8859-1'...")
                uploaded_file.seek(0)
                df = pd.read_csv(uploaded_file, encoding='ISO-8859-1')
                return df
            except Exception as e:
                st.error(f"Error reading the file with fallback encodings: {e}")
                return None
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        return None


# Listing all the lists available in session states
listVariables = ["rugplot","ecdf","kdeplot","histplot","displot","relplot","scatterplot","lineplot","catplot", "stripplot", "swarmplot",
                 "boxplot", "violinplot", "boxenplot", "pointplot", "barplot", "countplot",
                 "lmplot", "regplot", "residplot", "heatmap",
                 "clustermap", "FacetGrid", "pairplot", "PairGrid", "jointplot", "JointGrid"]

# Assigning session states
for i in listVariables:
    if i not in st.session_state:
        st.session_state[i] = []

# Assigning streamlit main components to streamlit's sidebar
file = st.sidebar.file_uploader("Upload the CSV file", type=["csv"])
st.sidebar.divider()
selectedPlot = st.sidebar.radio("Select the plot", listVariables)

# Writing the logic for selecting and plotting based on the selected plot type
col1, col2 = st.columns([2, 1])
with col1:
    if file is not None:
        df = readCSV(file)

        # Check if df is a DataFrame and not None
        if isinstance(df, pd.DataFrame):
            if selectedPlot == "relplot":
                relplot = Relplot(df, st.session_state["relplot"])
                relplot.display()
            elif selectedPlot == "scatterplot":
                scatterplot = ScatterPlot(df, st.session_state["scatterplot"])
                scatterplot.display()
            elif selectedPlot == "lineplot":
                lineplot = LinePlot(df, st.session_state["lineplot"])
                lineplot.display()
            elif selectedPlot == "displot":
                displot = DisPlot(df, st.session_state["displot"])
                displot.display()
            elif selectedPlot == "histplot":
                histplot = HistPlot(df, st.session_state["histplot"])
                histplot.display()
            elif selectedPlot == "kdeplot":
                kdeplot = KDEPlot(df, st.session_state["kdeplot"])
                kdeplot.display()
            elif selectedPlot == "ecdf":
                ecdf = ECDFPlot(df, st.session_state["ecdf"])
                ecdf.display()
            elif selectedPlot == "rugplot":
                rugplot = RugPlot(df, st.session_state["rugplot"])
                rugplot.display()
            elif selectedPlot == "catplot":
                catplot = Catplot(df, st.session_state["catplot"])
                catplot.display()
            elif selectedPlot == "stripplot":
                stripplot = Stripplot(df, st.session_state["stripplot"])
                stripplot.display()
            elif selectedPlot == "swarmplot":
                swarmplot = Swarmplot(df, st.session_state["swarmplot"])
                swarmplot.display()
            elif selectedPlot == "boxplot":
                boxplot = Boxplot(df, st.session_state["boxplot"])
                boxplot.display()
            elif selectedPlot == "violinplot":
                violinplot = ViolinPlotVisualizer(df, st.session_state["violinplot"])
                violinplot.display()
            elif selectedPlot == "boxenplot":
                boxenplot = BoxenplotVisualizer(df, st.session_state["boxenplot"])
                boxenplot.display()
            elif selectedPlot == "pointplot":
                pointplot = PointplotVisualizer(df, st.session_state["pointplot"])
                pointplot.display()
            elif selectedPlot == "barplot":
                barplot = BarplotVisualizer(df, st.session_state["barplot"])
                barplot.display()
            elif selectedPlot == "countplot":
                countplot = CountplotVisualizer(df, st.session_state["countplot"])
                countplot.display()
            elif selectedPlot == "lmplot":
                lmplot = LmplotVisualizer(df, st.session_state["lmplot"])
                lmplot.display()
            elif selectedPlot == "regplot":
                regplot = RegplotVisualizer(df, st.session_state["regplot"])
                regplot.display()
            elif selectedPlot == "residplot":
                residplot = ResidplotVisualizer(df, st.session_state["residplot"])
                residplot.display()
            elif selectedPlot == "heatmap":
                heatmap = HeatmapVisualizer(df, st.session_state["heatmap"])
                heatmap.display()
            elif selectedPlot == "clustermap":
                clustermap = ClustermapVisualizer(df, st.session_state["clustermap"])
                clustermap.display()
            elif selectedPlot == "FacetGrid":
                facetgrid = FacetGridVisualizer(df, st.session_state["FacetGrid"])
                facetgrid.display()
            elif selectedPlot == "pairplot":
                pairplot = PairPlotVisualizer(df, st.session_state["pairplot"])
                pairplot.display()
            elif selectedPlot == "PairGrid":
                pairgrid = PairGridVisualizer(df, st.session_state["PairGrid"])
                pairgrid.display()
            elif selectedPlot == "jointplot":
                jointplot = JointPlotVisualizer(df, st.session_state["jointplot"])
                jointplot.display()
            elif selectedPlot == "JointGrid":
                jointgrid = JointGridVisualizer(df, st.session_state["JointGrid"])
                jointgrid.display()
            else:
                st.error("Invalid plot selection.")
        else:
            st.error("Failed to load the CSV file. Please upload a valid file.")
with col2:
    selectedGraph = st.selectbox("Select any graph to see the saved plots", list(st.session_state.keys()))
    if selectedGraph:
        for j, i in enumerate(st.session_state[selectedGraph]):
            st.pyplot(i, key=j)
        if st.button("Download it into a pdf"):
            download_pdf(st.session_state[selectedGraph])
