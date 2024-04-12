from matplotlib import pyplot as plt
import panel as pn
import seaborn as sns
from rrcgeoviz.features.ParentGeovizFeature import ParentGeovizFeature


class FeatureAllMonths(ParentGeovizFeature):
    def getOptionName(self):
        return "all_months"

    def getRequiredColumns(self):
        return ["time_column"]

    def getHeaderText(self):
        return "Month-to-Month Frequency"

    def _generateComponent(self):
        fig, ax = plt.subplots(figsize=(8, 4))
        plt.close(fig)  # close any previous plots generated from other features
        fig, ax = plt.subplots(figsize=(5.5, 4.5))
        plt.title("All Incidents by Month", fontsize=12)
        sns.countplot(data=self.df, x="Month", palette="colorblind")
        plt.xlabel("Month")
        plt.ylabel("Frequency")
        # Add text annotations
        for p in ax.patches:
            ax.text(
                p.get_x() + p.get_width() / 2.0,
                p.get_height(),
                "%d" % int(p.get_height()),
                fontsize=10,
                ha="center",
                va="bottom",
            )

        months_app = pn.Column(pn.pane.Matplotlib(plt.gcf()), align="center")

        # Show the Panel app
        return months_app
