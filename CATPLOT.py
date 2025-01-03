import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from itertools import cycle

class Catplot:
    def __init__(self, data, saved_plots):
        self.data = data
        self.saved_plots = saved_plots
        self.numeric_columns = self.data.select_dtypes(include=["int", "float"]).columns.tolist()
        self.categorical_columns = self.data.select_dtypes(exclude=["int", "float"]).columns.tolist()
        self.columns = self.data.columns.tolist()

    def display(self):
        tab1, tab2 = st.tabs(["Plots", "Documents"])

        with tab1:
            st.header("Catplot Generator")
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

            # Kind of Plot
            st.subheader("Kind of Plot")
            self.kind = st.selectbox("Select plot type", ["strip", "swarm", "box", "violin", "boxen", "point", "bar", "count"])

            # Error Bar
            self.errorbar = st.selectbox("Select error bar method", [None, "ci", "pi", "se", "sd"])

            # Statistical Estimation
            self.estimator = st.selectbox("Select estimator", ["mean", "median", "std"])

            # Facet Parameters
            st.subheader("Facet Parameters")
            self.row = st.selectbox("Facet by rows", [None] + self.columns, index=0)
            if self.row:
                self.row_order = self.data[self.row].unique().tolist() if self.row else None
            self.col = st.selectbox("Facet by columns", [None] + self.columns, index=0)
            if self.col:
                self.col_order = self.data[self.col].unique().tolist() if self.col else None
                self.col_wrap = st.number_input(
                    "Wrap columns at specified width", min_value=1, max_value=5, value=3
                ) if self.col else None

            # Plot Aesthetics
            st.subheader("Plot Aesthetics")
            self.height = st.number_input("Set height of facets (in inches)", min_value=1, value=5)
            self.aspect = st.number_input("Set aspect ratio of facets", min_value=1, value=1)

            # Additional Parameters
            self.log_scale = st.checkbox("Log scale")
            self.native_scale = st.checkbox("Native scale")
            self.legend = st.selectbox("Select legend", ["auto", "brief", "full", False])
            self.legend_out = st.checkbox("Place legend outside")

            # Extra Parameters for Catplot
            st.subheader("Additional Parameters")
            self.n_boot = st.number_input("Number of bootstraps", min_value=100, value=1000)
            self.seed = st.number_input("Random seed", value=None)
            self.units = st.selectbox("Units", [None] + self.columns, index=0)
            self.weights = st.selectbox("Weights", [None] + self.columns, index=0)
            self.order = st.multiselect("Order of categories", self.data[self.x].unique().tolist()) if self.x else None
            self.orient = st.selectbox("Orientation", ["v", "h"])
            self.color = st.selectbox("Color", [None] + self.columns, index=0)
            self.shareX=st.checkbox("Share X")
            self.shareY=st.checkbox("Share Y")
            self.marginTitles=st.checkbox("Margin titles")

            # Generate Plot
            if st.button("Generate Plot"):
                try:
                    fig = sns.catplot(
                        data=self.data, x=self.x, y=self.y, hue=self.hue, hue_order=self.hue_order,
                        palette=self.palette, kind=self.kind, estimator=self.estimator, errorbar=self.errorbar,
                        n_boot=self.n_boot, seed=self.seed, units=self.units, weights=self.weights,
                        order=self.order, hue_norm=self.hue_norm, row=self.row, col=self.col,
                        row_order=self.row_order, col_order=self.col_order, col_wrap=self.col_wrap,
                        height=self.height, aspect=self.aspect, log_scale=self.log_scale,
                        native_scale=self.native_scale, formatter=None, orient=self.orient, color=self.color,
                        legend=self.legend, legend_out=self.legend_out, sharex=self.shareX, sharey=self.shareY,
                        margin_titles=self.marginTitles, facet_kws=None
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
