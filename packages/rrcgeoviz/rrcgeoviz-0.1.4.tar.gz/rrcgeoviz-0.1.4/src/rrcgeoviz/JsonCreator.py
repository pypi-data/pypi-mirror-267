from rrcgeoviz.JsonCreatorClasses.Sections.ColumnSetter import ColumnSetter
import panel as pn

from rrcgeoviz.JsonCreatorClasses.Sections.DownloadSection import DownloadSection

from rrcgeoviz.JsonCreatorClasses.Sections.FeatureSetter import FeatureSetter

from rrcgeoviz.JsonCreatorClasses.Sections.CacheSetter import CacheSetter

from rrcgeoviz.JsonCreatorClasses.Sections.FeatureCustomizationsSetter import (
    FeatureCustomizationsSetter,
)

from rrcgeoviz.JsonCreatorClasses.Sections.BaseSection import BaseSection


def main_javacreator():
    json_page = pn.Column()
    columnSetter = ColumnSetter()
    featureSetter = FeatureSetter()
    cacheSetter = CacheSetter()
    json_page.append(columnSetter.generate_section())
    json_page.append(featureSetter.generate_section(setGrid=True))
    json_page.append(cacheSetter.generate_section())
    json_page.append(
        DownloadSection([columnSetter, featureSetter, cacheSetter]).generate_section()
    )

    json_page.servable()
    pn.serve(json_page)
