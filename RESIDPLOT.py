import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
from itertools import cycle

class ResidplotVisualizer:
    def __init__(self, data, saved_plots):
        self.data = data
        self.saved_plots = saved_plots
        self.columns = self.data.columns.tolist()

    def display(self):
        self.tab1, self.tab2 = st.tabs(["Plots", "Documents"])

        with self.tab1:
            st.header("ResidPlot Generator")
            st.subheader("Core Data and Axes Parameters")
            st.info("The data is already loaded.")
            st.dataframe(self.data)

            # Select columns for x and y axes
            self.x = st.selectbox("Select the column for x-axis", [None] + self.columns, index=0)
            self.y = st.selectbox("Select the column for y-axis", [None] + self.columns, index=0)

            # Regression Parameters
            self.lowess = st.checkbox("Fit Lowess Smoother?", value=False)
            self.order = st.slider("Order of Polynomial for Residuals", min_value=1, max_value=5, value=1)
            self.robust = st.checkbox("Fit Robust Regression?", value=False)
            self.dropna = st.checkbox("Drop NA values?", value=True)

            # Plot Appearance
            self.color = st.color_picker("Pick a color for the plot", "#000000")
            self.scatter = st.checkbox("Show Scatter Plot?", value=True)

            # Generate Plot Button
            if st.button("Generate Plot"):
                self.generate_plot()

        with self.tab2:
            st.header("Documents Section")
            st.subheader("Saved Plots")

            if self.saved_plots:
                col1, col2 = st.columns(2)
                cols = cycle([col1, col2])

                for fig in self.saved_plots:
                    with next(cols):
                        st.pyplot(fig)
            else:
                st.info("No plots saved yet.")

    def generate_plot(self):
        # Prepare the arguments for residplot
        plot_args = {
            'data': self.data,
            'x': self.x,
            'y': self.y,
            'lowess': self.lowess,
            'order': self.order,
            'robust': self.robust,
            'dropna': self.dropna,
            'scatter': self.scatter,
            'color': self.color
        }

        fig = sns.residplot(**plot_args)
        
        if st.button("Plot the graph", use_container_width=True):
            st.pyplot(fig)
            self.saved_plots.append(fig)
