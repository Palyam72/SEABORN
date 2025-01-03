import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from itertools import cycle

class Stripplot:
    def __init__(self, data, saved_plots):
        self.data = data
        self.saved_plots = saved_plots
        self.numeric_columns = self.data.select_dtypes(include=["int", "float"]).columns.tolist()
        self.categorical_columns = self.data.select_dtypes(exclude=["int", "float"]).columns.tolist()
        self.columns = self.data.columns.tolist()

    def display(self):
        tab1, tab2 = st.tabs(["Plots", "Documents"])

        with tab1:
            st.header("Stripplot Generator")
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

            # Jitter
            st.subheader("Jitter Parameters")
            self.jitter = st.slider("Amount of jitter", 0.0, 1.0, 0.2)

            # Dodge
            self.dodge = st.checkbox("Dodge (separate the strips for different hue levels)")

            # Orientation
            self.orient = st.selectbox("Orientation", ["v", "h"])

            # Plot Aesthetics
            st.subheader("Plot Aesthetics")
            self.size = st.number_input("Size of markers", min_value=1, value=5)
            self.edgecolor = st.color_picker("Edge color", value="#000000")
            self.linewidth = st.number_input("Edge linewidth", min_value=0.0, value=0.0)

            # Additional Parameters
            self.log_scale = st.checkbox("Log scale")
            self.native_scale = st.checkbox("Native scale")
            self.legend = st.selectbox("Select legend", ["auto", "brief", "full", False])

            # Extra Parameters for Stripplot
            st.subheader("Additional Parameters")
            self.width = st.number_input("Width of the strips", min_value=0.0, value=0.8)
            self.color = st.selectbox("Color", [None] + self.columns, index=0)

            # Generate Plot
            if st.button("Generate Plot"):
                try:
                    fig = sns.stripplot(
                        data=self.data, x=self.x, y=self.y, hue=self.hue, hue_order=self.hue_order,
                        palette=self.palette, jitter=self.jitter, dodge=self.dodge, orient=self.orient,
                        size=self.size, edgecolor=self.edgecolor, linewidth=self.linewidth, 
                        log_scale=self.log_scale, native_scale=self.native_scale, legend=self.legend,
                        color=self.color, width=self.width
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
  
