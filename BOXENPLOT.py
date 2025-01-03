import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
from itertools import cycle

class BoxenplotVisualizer:
    def __init__(self, data, saved_plots):
        self.data = data
        self.saved_plots = saved_plots
        self.columns = self.data.columns.tolist()

    def display(self):
        self.tab1, self.tab2 = st.tabs(["Plots", "Documents"])

        with self.tab1:
            st.header("Boxenplot Generator")
            st.subheader("Core Data and Axes Parameters")
            st.info("The data is already loaded.")
            st.dataframe(self.data)

            # Select columns for x and y axes
            self.x = st.selectbox("Select the column for x-axis", [None] + self.columns, index=0)
            self.y = st.selectbox("Select the column for y-axis", [None] + self.columns, index=0)

            # Hue Parameters
            self.hue = st.selectbox("Select the column for hue", [None] + self.columns, index=0)
            self.hue_norm = None
            self.hue_order = None
            if self.hue:
                if self.hue in self.data.select_dtypes(include=["int", "float"]).columns.tolist():
                    self.hue_norm = st.text_input("Enter a range to normalize values (e.g., (1, 2))")
                    self.hue_norm = eval(self.hue_norm) if self.hue_norm else None
                else:
                    self.hue_order = st.multiselect("Select the hue order", self.data[self.hue].unique().tolist())

            # Color and Palette selection
            self.color = st.color_picker("Pick a single color for the plot", "#000000")
            self.palette = st.selectbox(
                "Select a color palette",
                ["deep", "muted", "pastel", "dark", "colorblind", "viridis", "coolwarm"]
            )

            # Saturation and fill
            self.saturation = st.slider("Saturation", min_value=0.0, max_value=1.0, value=0.75, step=0.05)
            self.fill = st.checkbox("Fill plot area?", value=True)

            # Dodge and Width settings
            self.dodge = st.selectbox("Dodge", ["auto", True, False])
            self.width = st.slider("Width", min_value=0.0, max_value=2.0, value=0.8, step=0.05)
            self.gap = st.slider("Gap", min_value=0.0, max_value=2.0, value=0, step=0.05)

            # Line and Width
            self.linewidth = st.slider("Line Width", min_value=0.1, max_value=5.0, value=1.0, step=0.1)
            self.linecolor = st.color_picker("Line Color", "#000000")

            # Boxenplot width method and k_depth
            self.width_method = st.selectbox("Boxenplot Width Method", ["exponential", "linear", "area"])
            self.k_depth = st.selectbox("Number of Tails", ["tukey", "proportion", "trustworthy", "full"])

            # Outlier Parameters
            self.outlier_prop = st.slider("Outlier Proportion", min_value=0.0, max_value=1.0, value=0.007, step=0.001)
            self.trust_alpha = st.slider("Trust Alpha", min_value=0.0, max_value=1.0, value=0.05, step=0.01)
            self.showfliers = st.checkbox("Show Outliers?", value=True)

            # Log Scale and Formatter
            self.log_scale = st.checkbox("Apply Log Scale?", value=False)
            self.native_scale=st.checkbox("Native Scale")
            self.formatter = st.text_input("Enter Formatter Function (Optional)")
            self.orient=st.selectbox("Choose Orient",["v","h"])

            # Legend settings
            self.legend = st.selectbox("Legend", ["auto", "brief", "full", False])

            # Generate and plot
            if st.button("Generate Plot"):
                self.generate_plot()

    def generate_plot(self):
        fig, ax = plt.subplots(figsize=(10, 6))

        sns.boxenplot(
            data=self.data,
            x=self.x,
            y=self.y,
            hue=self.hue,
            order=self.hue_order,
            color=self.color,
            palette=self.palette,
            saturation=self.saturation,
            fill=self.fill,
            dodge=self.dodge,
            width=self.width,
            gap=self.gap,
            linewidth=self.linewidth,
            linecolor=self.linecolor,
            width_method=self.width_method,
            k_depth=self.k_depth,
            outlier_prop=self.outlier_prop,
            trust_alpha=self.trust_alpha,
            showfliers=self.showfliers,
            hue_norm=self.hue_norm,
            log_scale=self.log_scale,
            formatter=self.formatter,
            legend=self.legend,
            orient=self.orient,
            native_scale=self.native_scale
        )
        if st.button("PLot the graph",use_container_width=True):
            st.pyplot(fig)
            self.saved_plots.append(fig)

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
  
