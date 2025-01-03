import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from itertools import cycle


class RugPlot:
    def __init__(self, data, saved_plots):
        self.data = data
        self.saved_plots = saved_plots
        self.columns = self.data.columns.tolist()

    def display(self):
        # Set up tabs for plot generation and saved plots
        tab1, tab2 = st.tabs(["Plots", "Documents"])

        # Plot Generation Tab
        with tab1:
            st.header("Rug Plot Generator")
            st.subheader("Core Data and Axes Parameters")
            st.info("The data is already loaded.")
            with st.expander("View Data Frame"):
                st.dataframe(self.data)

            # Select columns for x and y axes
            self.x = st.selectbox("Select the column for x-axis", [None] + self.columns)
            self.y = st.selectbox("Select the column for y-axis (optional)", [None] + self.columns)

            if not self.x:
                st.warning("Please select an x-axis for the plot.")
                return

            # Determine if the plot is bivariate
            is_bivariate = bool(self.y)

            # Hue Parameters
            st.subheader("Hue Parameters")
            self.hue = st.selectbox("Select the column for hue (optional)", [None] + self.columns)
            self.hue_order = None
            if self.hue:
                self.hue_order = st.multiselect("Select the hue order", self.data[self.hue].unique().tolist())
                self.hue_norm = st.text_input("Enter normalization min and max range (e.g., (10, 20))")
                if self.hue_norm:
                    try:
                        self.hue_norm = eval(self.hue_norm)  # Convert input to tuple
                    except:
                        st.warning("Invalid range format. Please enter a tuple like (10, 20).")
                        self.hue_norm = (10, 20)
                else:
                    self.hue_norm = (10, 20)

            # Palette selection
            self.palette = st.selectbox(
                "Select a color palette",
                ["deep", "muted", "pastel", "dark", "colorblind", "viridis", "coolwarm"]
            )

            # Other Parameters
            self.height = st.number_input("Height of the rug", value=0.025, step=0.001)
            self.expand_margins = st.checkbox("Expand Margins", value=True)
            self.legend = st.checkbox("Show Legend", value=True)

            # Generate Plot Button
            if st.button("Generate Rug Plot"):
                try:
                    # Create the plot
                    st.header("Current Plot")
                    plt.figure(figsize=(10, 6))
                    plt.title(f"Rug Plot of {self.x} vs {self.y if is_bivariate else ''}")
                    plt.xlabel(self.x)
                    if is_bivariate:
                        plt.ylabel(self.y)

                    # Generate the rug plot
                    if is_bivariate:
                        sns.rugplot(
                            data=self.data, x=self.x, y=self.y, hue=self.hue,
                            height=self.height, expand_margins=self.expand_margins,
                            palette=self.palette, hue_order=self.hue_order,hue_norm=self.hue_norm,
                            legend=self.legend
                        )
                    else:
                        sns.rugplot(
                            data=self.data, x=self.x, hue=self.hue,
                            height=self.height, expand_margins=self.expand_margins,
                            palette=self.palette, hue_order=self.hue_order,
                            hue_norm=self.hue_norm, legend=self.legend
                        )

                    # Display the plot
                    st.pyplot(plt.gcf())

                    # Save the plot
                    self.saved_plots.append(plt.gcf())

                except Exception as e:
                    st.error(f"Error generating plot: {e}")

        # Saved Plots Tab
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
