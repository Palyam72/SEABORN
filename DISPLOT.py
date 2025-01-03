import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from itertools import cycle

class DisPlot:
    def __init__(self, data, saved_plots):
        self.data = data
        self.saved_plots = saved_plots
        self.numeric_columns = self.data.select_dtypes(include=["int", "float"]).columns.tolist()
        self.categorical_columns = self.data.select_dtypes(exclude=["int", "float"]).columns.tolist()
        self.columns = self.data.columns.tolist()

    def display(self):
        tab1, tab2 = st.tabs(["Plots", "Documents"])

        with tab1:
            st.header("DisPlot Generator")
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

            # Additional Parameters
            self.legend = st.selectbox("Select the value for legend", [False, "full", "brief", "auto"])
            self.weights = st.selectbox("Select the column for Weights", [None] + self.columns, index=0)
            self.row = st.selectbox("Select the column for row", [None] + self.columns, index=0)
            if self.row:
                self.row_order = st.multiselect("Select the row order", self.data[self.row].unique())
                if not self.row_order:
                    self.row_order = None
            else:
                self.row_order = None

            self.col = st.selectbox("Select the column for col", [None] + self.columns, index=0)
            if self.col:
                self.col_order = st.multiselect("Select the col order", self.data[self.col].unique())
                if not self.col_order:
                    self.col_order = None
                self.col_wrap = int(st.number_input("Please Enter the number of columns that should present in a row ", 0))
                if self.col_wrap == 0:
                    self.col_wrap = None
            else:
                self.col_order = None
                self.col_wrap = None
            self.rug = st.checkbox("Rug : If True, show each observation with marginal ticks (as in rugplot()).")
            self.log_scale = st.checkbox("Log Scale")
            self.colors = [
                'red', 'green', 'blue', 'yellow', 'orange', 'purple', 'pink', 'brown', 'gray', 'black', 'white',
                'cyan', 'magenta', 'lime', 'indigo', 'violet', 'teal', 'navy', 'maroon', 'olive', 'beige'
            ]
            self.color = st.selectbox("Single color specification for when hue mapping is not used. Otherwise, the plot will try to hook into the matplotlib property cycle.", self.colors)
            self.height = int(st.number_input("Height : ", 5.0))
            self.aspect = int(st.number_input("Aspect : ", 1.0))
            self.kind = st.selectbox("Please select the type of distribution plot", ["hist", "kde", "ecdf"])

            # Generate Plot
            if st.button("Generate Distribution Plot"):
                try:
                    st.header("Current Plot")
                    plt.figure(figsize=(10, 6))
                    plt.title(f"{self.x} vs {self.y}")
                    plt.xlabel(self.x)
                    plt.ylabel(self.y)

                    fig = sns.displot(
                        data=self.data, x=self.x, y=self.y, hue=self.hue, hue_norm=self.hue_norm,
                        hue_order=self.hue_order, row=self.row, col=self.col, col_wrap=self.col_wrap,
                        palette=self.palette, legend=self.legend, weights=self.weights, rug=self.rug,
                        log_scale=self.log_scale, height=self.height, aspect=self.aspect, kind=self.kind,
                        color=self.color, row_order=self.row_order, col_order=self.col_order
                    )
                    st.pyplot(fig)
                    self.saved_plots.append(fig)
                except Exception as e:
                    st.error(f"Error generating plot: {e}")

        with tab2:
            st.header("Saved Plots", divider='blue')
            if self.saved_plots:
                col1, col2 = st.columns(2)
                cols = cycle([col1, col2])

                for saved_plot in self.saved_plots:
                    with next(cols):
                        st.pyplot(saved_plot)
            else:
                st.info("No plots saved yet.")
