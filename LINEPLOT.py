import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from itertools import cycle

class LinePlot:
    def __init__(self, data, saved_plots):
        self.data = data
        self.saved_plots = saved_plots
        self.numeric_columns = self.data.select_dtypes(include=["int", "float"]).columns.tolist()
        self.categorical_columns = self.data.select_dtypes(exclude=["int", "float"]).columns.tolist()
        self.columns = self.data.columns.tolist()

    def display(self):
        tab1, tab2 = st.tabs(["Plots", "Documents"])

        with tab1:
            st.header("LinePlot Generator")
            st.subheader("Core Data and Axes Parameters")
            st.info("The data is already loaded.")
            with st.expander("Data Frame is here"):
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
                    hue_norm_input = st.text_input("Enter a range to normalize values (e.g., (1, 2))")
                    self.hue_norm = eval(hue_norm_input) if hue_norm_input else None
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
                    size_range_input = st.text_input("Define size range (e.g., (10, 30))")
                    self.sizes = eval(size_range_input) if size_range_input else None
                else:
                    self.size_order = st.multiselect("Order of categories for size", self.data[self.size].unique().tolist())

            # Style Parameters
            st.subheader("Style Parameters")
            self.style = st.selectbox("Select style column", [None] + self.columns, index=0)
            self.style_order = None
            self.dashes = False
            self.markers = False
            if self.style:
                self.style_order = st.multiselect("Order of categories for style", self.data[self.style].unique().tolist())
                self.dashes = st.checkbox("Enable dashes")
                self.markers = st.checkbox("Enable markers")

            # Additional Parameters
            self.legend = st.selectbox("Select the value for legend", [False, "full", "brief", "auto"])
            self.units = st.selectbox("Select the column for Units", [None] + self.columns, index=0)
            self.weights = st.selectbox("Select the column for Weights", [None] + self.columns, index=0)
            self.estimator = st.text_input(
                "Method for aggregating across multiple observations of the y variable at the same x level.",
                value=None
            )
            errorbar_input = st.text_input(
                "Name of errorbar method (e.g., ('ci', 95))",
                value="('ci', 95)"
            )
            self.errorbar = eval(errorbar_input) if errorbar_input else None
            self.nboot = int(st.number_input("Number of bootstraps to use for computing the confidence interval.", value=1000))
            self.seed = st.number_input("Seed or random number generator for reproducible bootstrapping.", value=0)
            self.seed = int(self.seed) if self.seed else None
            self.orient = st.selectbox(
                "Dimension along which the data are sorted/aggregated.",
                ["x", "y"]
            )
            self.sort = st.checkbox(
                "Sort data by x and y variables",
                value=True
            )
            self.err_style = st.selectbox(
                "Draw confidence intervals as translucent error bands or discrete error bars.",
                ["band", "bars"]
            )

            # Generate Plot
            if st.button("Generate Line Plot"):
                try:
                    st.header("Current Plot")
                    plt.figure(figsize=(10, 6))
                    plt.title(f"{self.x} vs {self.y}")
                    plt.xlabel(self.x)
                    plt.ylabel(self.y)

                    fig = sns.lineplot(
                        data=self.data, x=self.x, y=self.y, hue=self.hue, hue_norm=self.hue_norm,
                        hue_order=self.hue_order, size=self.size, sizes=self.sizes, size_order=self.size_order,
                        style=self.style, style_order=self.style_order, dashes=self.dashes, markers=self.markers,
                        palette=self.palette, units=self.units, weights=self.weights, estimator=self.estimator,
                        errorbar=self.errorbar, n_boot=self.nboot, seed=self.seed, orient=self.orient,
                        sort=self.sort, err_style=self.err_style, legend=self.legend
                    )
                    st.pyplot(plt)
                    self.saved_plots.append(plt.gcf())
                except Exception as e:
                    st.error(f"Error generating plot: {e}")

        with tab2:
            st.header("Saved Plots")
            if self.saved_plots:
                col1, col2 = st.columns(2)
                cols = cycle([col1, col2])

                for saved_plot in self.saved_plots:
                    with next(cols):
                        st.pyplot(saved_plot)
            else:
                st.info("No plots saved yet.")
