from __future__ import annotations

from IPython.display import HTML, display
import pandas as pd
import tabulate

def show_df(context):
    """
    Display a dataframe or array as HTML.

    Expected context keys:
        df, columns
    """

    df = context["df"]
    columns = context["columns"]

    if type(df) != type(pd.DataFrame()):
        df = pd.DataFrame(df)

    display(HTML(tabulate.tabulate(df[columns],
                                   headers = columns,
                                   tablefmt = "html")))
