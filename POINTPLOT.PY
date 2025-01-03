import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
from itertools import cycle

class PointplotVisualizer:
    def __init__(self, data, saved_plots):
        self.data = data
        self.saved_plots = saved_plots
        self.columns = self.data.columns.tolist()

    def display(self):
        self.tab1, self.tab2 = st.tabs(["Plots", "Documents"])

        with self.tab1:
            st.header("Pointplot Generator")
            st.subheader("Core Data and Axes Parameters")
            st.info("The data is already loaded.")
            st.dataframe(self.data)

            # Select columns for x and y axes
            self.x = st.selectbox("Select the column for x-axis", [None] + self.columns, index=0)
            self.y = st.selectbox("Select the column for y-axis", [None] + self.columns, index=0)

            # Hue Parameters
            self.hue = st.selectbox("Select the column for hue", [None] + self.columns, index=0)
            self.hue_order = None
            if self.hue:
                self.hue_order = st.multiselect("Select the hue order", self.data[self.hue].unique().tolist())

            # Estimator
            self.estimator = st.selectbox("Select Estimator", ["mean", "median", "std"])

            # Errorbar and Bootstrap Settings
            self.errorbar = st.selectbox("Errorbar", ["ci", "pi", "se", "sd"])
            self.n_boot = st.slider("Number of Bootstrap Samples", min_value=100, max_value=10000, value=1000, step=100)
            self.seed = st.number_input("Seed", min_value=0, value=42)

            # Color and Palette selection
            self.color = st.color_picker("Pick a single color for the plot", "#000000")
            self.palette = st.selectbox(
                "Select a color palette",
                ["deep", "muted", "pastel", "dark", "colorblind", "viridis", "coolwarm"]
            )

            # Log Scale
            self.log_scale = st.checkbox("Apply Log Scale?", value=False)

            # Marker and Line Settings
            self.markers = st.text_input("Enter Markers", "o")
            self.linestyles = st.text_input("Enter Line Styles", "-")

            # Dodge
            self.dodge = st.selectbox("Dodge", [True, False])

            # Plot options
            self.orientation = st.selectbox("Choose Plot Orientation", ["v", "h"])
            self.legend = st.selectbox("Legend", ["auto", "brief", "full", False])

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
        fig, ax = plt.subplots(figsize=(10, 6))

        sns.pointplot(
            data=self.data,
            x=self.x,
            y=self.y,
            hue=self.hue,
            hue_order=self.hue_order,
            estimator=self.estimator,
            errorbar=self.errorbar,
            n_boot=self.n_boot,
            seed=self.seed,
            color=self.color,
            palette=self.palette,
            markers=self.markers,
            linestyles=self.linestyles,
            dodge=self.dodge,
            log_scale=self.log_scale,
            orient=self.orientation,
            legend=self.legend
        )

        if st.button("Plot the graph", use_container_width=True):
            st.pyplot(fig)
            self.saved_plots.append(fig)
