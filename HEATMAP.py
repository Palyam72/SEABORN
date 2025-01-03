import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
from itertools import cycle

class HeatmapVisualizer:
    def __init__(self, data, saved_plots):
        self.data = data
        self.saved_plots = saved_plots
        self.columns = self.data.columns.tolist()

    def display(self):
        self.tab1, self.tab2 = st.tabs(["Plots", "Documents"])

        with self.tab1:
            st.header("Heatmap Generator")
            st.subheader("Core Data and Axes Parameters")
            st.info("The data is already loaded.")
            st.dataframe(self.data)

            # Select columns for x and y axes
            self.columns_to_use = st.multiselect("Select columns for the heatmap", self.columns, default=self.columns)

            # Heatmap Parameters
            self.vmin = st.number_input("Min Value for Heatmap", min_value=float(self.data[self.columns_to_use].min().min()), value=float(self.data[self.columns_to_use].min().min()))
            self.vmax = st.number_input("Max Value for Heatmap", min_value=float(self.data[self.columns_to_use].max().max()), value=float(self.data[self.columns_to_use].max().max()))
            self.cmap = st.selectbox("Select Colormap", ['coolwarm', 'viridis', 'plasma', 'inferno', 'cividis', 'magma', 'twilight'])
            self.robust = st.checkbox("Use Robust Color Mapping?", value=False)
            self.annot = st.checkbox("Show Annotations?", value=True)
            self.fmt = st.text_input("Annotation Formatting", ".2g")
            self.annot_kws = {"size": st.slider("Annotation Font Size", 8, 16, 12)}  # Optional kwarg for annotation styling
            self.linewidths = st.slider("Cell Line Width", 0, 5, 1)
            self.linecolor = st.color_picker("Cell Line Color", "#FFFFFF")
            self.cbar = st.checkbox("Show Colorbar?", value=True)
            self.square = st.checkbox("Make Cells Square?", value=False)
            self.xticklabels = st.selectbox("X-Axis Labels", ['auto', 'True', 'False'])
            self.yticklabels = st.selectbox("Y-Axis Labels", ['auto', 'True', 'False'])

            # Generate Plot Button
            if st.button("Generate Heatmap"):
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
        # Prepare the arguments for heatmap
        plot_args = {
            'data': self.data[self.columns_to_use],
            'vmin': self.vmin,
            'vmax': self.vmax,
            'cmap': self.cmap,
            'robust': self.robust,
            'annot': self.annot,
            'fmt': self.fmt,
            'annot_kws': self.annot_kws,
            'linewidths': self.linewidths,
            'linecolor': self.linecolor,
            'cbar': self.cbar,
            'square': self.square,
            'xticklabels': self.xticklabels,
            'yticklabels': self.yticklabels
        }

        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(**plot_args, ax=ax)

        if st.button("Plot the graph", use_container_width=True):
            st.pyplot(fig)
            self.saved_plots.append(fig)
