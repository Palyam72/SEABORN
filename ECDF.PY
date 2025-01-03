import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from itertools import cycle

class ECDFPlot:
    def __init__(self, data, saved_plots):
        self.data = data
        self.saved_plots = saved_plots
        self.columns = self.data.columns.tolist()

    def display(self):
        tab1, tab2 = st.tabs(["Plots", "Documents"])

        with tab1:
            st.header("ECDF Plot Generator")
            st.subheader("Core Data and Axes Parameters")
            st.info("The data is already loaded.")
            with st.expander("Data Frame is here"):
                st.dataframe(self.data)

            # Select columns for x and y axes
            self.x = st.selectbox("Select the column for x-axis", [None] + self.columns, index=0)
            self.y = st.selectbox("Select the column for y-axis (optional)", [None] + self.columns, index=0)

            if not self.x:
                st.warning("Please select an x-axis for the plot.")
                return

            # If both x and y are selected, it will be bivariate
            is_bivariate = bool(self.y)

            # Hue Parameters
            st.subheader("Hue Parameters")
            self.hue = st.selectbox("Select the column for hue (optional)", [None] + self.columns, index=0)
            self.hue_order = None
            if self.hue:
                self.hue_order = st.multiselect("Select the hue order", self.data[self.hue].unique().tolist())

            # Palette selection
            self.palette = st.selectbox(
                "Select a color palette",
                ["deep", "muted", "pastel", "dark", "colorblind", "viridis", "coolwarm"]
            )

            # Statistical Parameters
            self.stat = st.selectbox("Select the statistic", ["proportion", "percent", "count"])
            self.complementary = st.checkbox("Complementary ECDF")
            self.log_scale = st.checkbox("Log Scale")

            # Generate Plot
            if st.button("Generate ECDF Plot"):
                try:
                    st.header("Current Plot")
                    plt.figure(figsize=(10, 6))
                    plt.title(f"ECDF of {self.x} vs {self.y if is_bivariate else ''}")
                    plt.xlabel(self.x)
                    if is_bivariate:
                        plt.ylabel(self.y)

                    # Generate ECDF plot using seaborn.ecdfplot
                    if is_bivariate:
                        fig = sns.ecdfplot(
                            data=self.data, x=self.x, y=self.y, hue=self.hue,
                            stat=self.stat, complementary=self.complementary,
                            palette=self.palette, hue_order=self.hue_order,
                            log_scale=self.log_scale
                        )
                    else:
                        fig = sns.ecdfplot(
                            data=self.data, x=self.x, hue=self.hue,
                            stat=self.stat, complementary=self.complementary,
                            palette=self.palette, hue_order=self.hue_order,
                            log_scale=self.log_scale
                        )

                    # Display the plot
                    st.pyplot(plt.gcf())

                    # Save the figure (save the actual matplotlib figure)
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
