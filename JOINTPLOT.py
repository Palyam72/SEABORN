import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
from itertools import cycle

class JointPlotVisualizer:
    def __init__(self, data, saved_plots):
        self.data = data
        self.saved_plots = saved_plots
        self.columns = self.data.columns.tolist()

    def display(self):
        self.tab1, self.tab2 = st.tabs(["Plots", "Documents"])

        with self.tab1:
            st.header("JointPlot Generator")
            st.subheader("Core Data and Axes Parameters")
            st.info("The data is already loaded.")
            st.dataframe(self.data)

            # Select variables for the joint plot
            self.x = st.selectbox("Select X variable", self.columns)
            self.y = st.selectbox("Select Y variable", self.columns)
            self.hue = st.selectbox("Select Hue Variable", [None] + self.columns)
            self.kind = st.selectbox("Select Plot Kind", ["scatter", "kde", "hist", "hex", "reg", "resid"])
            self.height = st.slider("Height of the Plot", min_value=4, max_value=10, value=6)
            self.ratio = st.slider("Ratio of Joint to Marginal Axes", min_value=1, max_value=10, value=5)
            self.space = st.slider("Space Between Joint and Marginal Axes", min_value=0.1, max_value=1.0, value=0.2)
            self.dropna = st.checkbox("Drop Missing Values?", value=False)
            self.xlim = st.text_input("X-axis Limits (comma-separated)", "")
            self.ylim = st.text_input("Y-axis Limits (comma-separated)", "")
            self.color = st.text_input("Single Color for Plot", "")
            self.palette = st.text_input("Color Palette", "deep")
            self.hue_order = st.text_input("Hue Order (comma-separated)", "")
            self.hue_norm = st.text_input("Hue Normalization", "")
            self.marginal_ticks = st.checkbox("Show Marginal Ticks?", value=False)

            # Generate Plot Button
            if st.button("Generate JointPlot"):
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
        # Prepare the arguments for JointPlot
        plot_args = {
            'data': self.data,
            'x': self.x,
            'y': self.y,
            'hue': self.hue,
            'kind': self.kind,
            'height': self.height,
            'ratio': self.ratio,
            'space': self.space,
            'dropna': self.dropna,
            'xlim': eval(self.xlim) if self.xlim else None,
            'ylim': eval(self.ylim) if self.ylim else None,
            'color': self.color,
            'palette': self.palette,
            'hue_order': eval(self.hue_order) if self.hue_order else None,
            'hue_norm': eval(self.hue_norm) if self.hue_norm else None,
            'marginal_ticks': self.marginal_ticks
        }

        # Generate the JointPlot
        g = sns.jointplot(**plot_args)

        if st.button("Plot the graph", use_container_width=True):
            st.pyplot(g)
            self.saved_plots.append(g.fig)