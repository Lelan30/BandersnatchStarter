from altair import Chart, Tooltip
from pandas import DataFrame


def chart(df: DataFrame, x: str, y: str, target: str) -> Chart:
    graph = Chart(
        df,
        title=f"{y} by {x} for {target}",
    ).mark_circle(size=100).encode(
        x=x,
        y=y,
        color=target,
        tooltip=Tooltip(df.columns.to_list())
    ).properties(
        width=1200,
        height=400,
        background="#8888c6",
        padding=40
    ).configure(
        axis={
            "titlePadding": 20,
            "labelColor": "#cca76e",
            "titleColor": "#cca76e",
        },
        title={
            "color": "#204203",
            "fontSize": 30
        }
    )
    return graph
