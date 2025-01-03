import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
from itertools import cycle

class CountplotVisualizer:
    def __init__(self, data, saved_plots):
        self.data = data
        self.saved_plots = saved_plots
        self.columns = self.data.columns.tolist()

    def display(self):
        self.tab1, self.tab2 = st.tabs(["Plots", "Documents"])

        with self.tab1:
            st.header("Countplot Generator")
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

            # Statistic Type
            self.stat = st.selectbox("Statistic to compute", ['count', 'percent', 'proportion', 'probability'])

            # Color and Palette selection
            self.color = st.color_picker("Pick a single color for the plot", "#000000")
            self.palette = st.selectbox(
                "Select a color palette",
                ["deep", "muted", "pastel", "dark", "colorblind", "viridis", "coolwarm"]
            )

            # Log Scale
            self.log_scale = st.checkbox("Apply Log Scale?", value=False)

            # Width and Dodge Settings
            self.width = st.slider("Width of bars", min_value=0.1, max_value=2.0, value=0.8, step=0.1)
            self.dodge = st.selectbox("Dodge", [True, False, "auto"])

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

        sns.countplot(
            data=self.data,
            x=self.x,
            y=self.y,
            hue=self.hue,
            hue_order=self.hue_order,
            stat=self.stat,
            color=self.color,
            palette=self.palette,
            width=self.width,
            dodge=self.dodge,
            log_scale=self.log_scale,
            orient=self.orientation,
            legend=self.legend
        )

        if st.button("Plot the graph", use_container_width=True):
            st.pyplot(fig)
            self.saved_plots.append(fig)
