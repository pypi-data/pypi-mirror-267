import pandas as pd
import panel as pn

from rrcgeoviz.arguments import Arguments


class ParentGeovizFeature:
    def __init__(self, args: Arguments) -> None:
        self.df = args.getData()
        self.time_column_name = args.getColumns()["time_column"]
        self.latitude_column_name = args.getColumns()["latitude_column"]
        self.longitude_column_name = args.getColumns()["longitude_column"]
        self.featureCustomizations = args.getFeatureCustomizations()
        self.df[self.time_column_name] = pd.to_datetime(self.df[self.time_column_name])
        self.df["Month"] = self.df[self.time_column_name].dt.month
        self.df["Year"] = self.df[self.time_column_name].dt.year
        self.df["Day"] = self.df[self.time_column_name].dt.day
        self.generated_data = args.generated_data

    def getOptionName(self):
        raise NotImplementedError(
            "Feature subclasses need to return the name of the feature to be put in the options file."
        )

    def getRequiredColumns(self):
        raise NotImplementedError(
            "Feature subclasses need to return an array of required data columns"
        )

    def getHeaderText(self):
        raise NotImplementedError(
            "Feature subclasses need to return text to be put in the header above the feature."
        )

    def generateFeature(self):
        header_text = pn.widgets.StaticText(
            name="Static Text", value=self.getHeaderText(), height=12
        )
        feature = pn.Column(
            pn.Card(
                self._generateComponent().servable(),
                header=pn.panel(header_text, height=12),
                sizing_mode="stretch_width",
                collapsed=False,
            ),
            sizing_mode="stretch_width",
        ).servable()

        return feature

    def _generateComponent(self):
        raise NotImplementedError(
            "Add the code to create the actual feature here. Wrap it in a Panel.Column"
        )
