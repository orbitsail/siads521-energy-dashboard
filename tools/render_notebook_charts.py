"""Render the chart PNGs used in the notebook (run from repo root)."""
import os
import plotly.io as pio
from streamlit.testing.v1 import AppTest
APP = os.path.abspath("app.py")
OUT = "screens/notebook"

def grab(region, focus, yrs, wanted, prefix):
    at = AppTest.from_file(APP).run(timeout=60)
    at.selectbox[0].set_value(region).run(timeout=60)
    at.selectbox[1].set_value(focus).run(timeout=60)
    at.slider[0].set_value(yrs).run(timeout=60)
    assert not at.exception, at.exception
    print(at.title[0].value)
    for el in at.get("plotly_chart"):
        fig = pio.from_json(el.proto.spec)
        n = fig.layout.title.text[:1]
        if n in wanted:
            fig.write_image(f"{OUT}/{prefix}_{n}.png", width=900, height=450, scale=1.5)

os.makedirs(OUT, exist_ok=True)
grab("Asia", "India", (2010, 2023), "ABCDE", "chart")
grab("Asia", "Lebanon", (2010, 2023), "ABE", "lebanon")
grab("All", "Germany", (2000, 2023), "AD", "germany")
grab("Asia", "Laos", (2010, 2023), "A", "laos")
grab("All", "Germany", (2000, 2023), "A", "stage1")
os.replace(f"{OUT}/stage1_A.png", f"{OUT}/stage1_single_chart.png")
