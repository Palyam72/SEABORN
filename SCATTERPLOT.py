import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from itertools import cycle

class ScatterPlot:
    def __init__(self, data, saved_plots):
        self.data = data
        self.saved_plots = saved_plots
        self.numeric_columns = self.data.select_dtypes(include=["int", "float"]).columns.tolist()
        self.categorical_columns = self.data.select_dtypes(exclude=["int", "float"]).columns.tolist()
        self.columns = self.data.columns.tolist()

    def display(self):
        tab1, tab2 = st.tabs(["Plots", "Documents"])

        with tab1:
            st.header("Scatter Plot Generator")
            st.subheader("Core Data and Axes Parameters")
            st.info("The data is already loaded.")
            with st.expander("Data Frame is inside"):
                st.dataframe(self.data)

            # Select columns for x and y axes
            self.x = st.selectbox("Select the column for x-axis", [None] + self.columns, index=0)
            self.y = st.selectbox("Select the column for y-axis", [None] + self.columns, index=0)

            # Hue Parameters
            st.subheader("Hue Parameters")
            self.hue = st.selectbox("Select the column for hue", [None] + self.columns, index=0)
            self.hue_norm = None
            self.hue_order = None
            if self.hue:
                if self.hue in self.numeric_columns:
                    self.hue_norm = st.text_input("Enter a range to normalize values (e.g., (1, 2))")
                    self.hue_norm = eval(self.hue_norm) if self.hue_norm else None
                else:
                    self.hue_order = st.multiselect("Select the hue order", self.data[self.hue].unique().tolist())

            # Palette selection
            self.palette = st.selectbox(
                "Select a color palette",
                ["deep", "muted", "pastel", "dark", "colorblind", "viridis", "coolwarm"]
            )

            # Size Parameters
            st.subheader("Size Parameters")
            self.size = st.selectbox("Select size column", [None] + self.columns, index=0)
            self.sizes = None
            self.size_order = None
            self.size_norm = None
            if self.size:
                if self.size in self.numeric_columns:
                    self.sizes = st.text_input("Define size range (e.g., (10, 30))")
                    self.sizes = eval(self.sizes) if self.sizes else None
                else:
                    self.size_order = st.multiselect("Order of categories for size", self.data[self.size].unique().tolist())

            # Style Parameters
            st.subheader("Style Parameters")
            self.style = st.selectbox("Select style column", [None] + self.columns, index=0)
            self.style_order = None
            self.markers = False
            if self.style:
                self.style_order = st.multiselect("Order of categories for style", self.data[self.style].unique().tolist())
                self.markers = st.checkbox("Enable markers")
            self.legend=st.selectbox("Plaese select a avalue for legend",[False,"full","brief","auto"])
            # Generate Plot
            if st.button("Generate Scatter Plot"):
                try:
                    plt.title(f"{self.x} VS {self.y}")
                    plt.xlabel(self.x)
                    plt.ylabel(self.y)
                    fig = sns.relplot(
                        data=self.data, x=self.x, y=self.y, hue=self.hue, hue_norm=self.hue_norm, hue_order=self.hue_order,
                        size=self.size, sizes=self.sizes, size_order=self.size_order, style=self.style,
                        style_order=self.style_order, markers=self.markers,palette=self.palette,legend=self.legend
                    )
                    st.pyplot(fig)
                    self.saved_plots.append(fig)
                except Exception as e:
                    st.error(f"Error generating plot: {e}")

        with tab1:
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
