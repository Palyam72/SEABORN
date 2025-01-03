import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from itertools import cycle

class Swarmplot:
    def __init__(self, data, saved_plots):
        self.data = data
        self.saved_plots = saved_plots
        self.numeric_columns = self.data.select_dtypes(include=["int", "float"]).columns.tolist()
        self.categorical_columns = self.data.select_dtypes(exclude=["int", "float"]).columns.tolist()
        self.columns = self.data.columns.tolist()

    def display(self):
        tab1, tab2 = st.tabs(["Plots", "Documents"])

        with tab1:
            st.header("Swarmplot Generator")
            st.subheader("Core Data and Axes Parameters")
            st.info("The data is already loaded.")
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
 
            # Additional Parameters
            self.log_scale = st.checkbox("Log scale")
            self.native_scale = st.checkbox("Native scale")
            self.legend = st.selectbox("Select legend", ["auto", "brief", "full", False])

            # Extra Parameters for Swarmplot
            st.subheader("Additional Parameters")
            self.order = st.multiselect("Order of categories", self.data[self.x].unique().tolist()) if self.x else None
            self.color = st.selectbox("Color", [None] + self.columns, index=0)
            self.dodge = st.checkbox("Dodge hue levels")
            self.warn_thresh = st.number_input("Warn Threshold", min_value=0.0, max_value=1.0, value=0.05)

            # Generate Plot
            if st.button("Generate Plot"):
                try:
                    fig = sns.swarmplot(
                        data=self.data, x=self.x, y=self.y, hue=self.hue, hue_order=self.hue_order,
                        palette=self.palette, dodge=self.dodge,
                        order=self.order, hue_norm=self.hue_norm, log_scale=self.log_scale,
                        native_scale=self.native_scale, formatter=None, orient=self.orient, color=self.color,
                        legend=self.legend, warn_thresh=self.warn_thresh
                    )
                    st.pyplot(fig)
                    self.saved_plots.append(fig)
                except Exception as e:
                    st.error(f"Error generating plot: {e}")

        with tab2:
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
