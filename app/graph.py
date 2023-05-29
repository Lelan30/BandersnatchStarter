from altair import Chart
from pandas import DataFrame

def chart(df: DataFrame, x: str, y:str, target: str) -> Chart:
    """
    Function: Create a chart object from the dataframe.
    """
    data = df[[x, y, target]]
    title = f"y by {x} for {target}"
    chart_objc = Chart(data).mark_circle(size=100).encode(
        x=x,
        y=y,
        color=target,
        tooltip=[x, y, target]
    ).properties(
        width=450,
        height=450,
        background='black',
        padding=20,
    ).configure_axis(
        titleFontSize=20,
        labelFontSize=15,
    ).configure_title(
        fontSize=23,
    ).configure_legend(
        gradientLength=400,
        gradientThickness=20,
        titleFontSize=20,
        labelFontSize=15,
    )
    return chart_objc


