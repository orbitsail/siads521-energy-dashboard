import plotly.io as pio
from streamlit.testing.v1 import AppTest
at = AppTest.from_file("app.py").run(timeout=60)
at.selectbox[0].set_value("Asia").run(timeout=60)
at.selectbox[1].set_value("India").run(timeout=60)
at.slider[0].set_value((2010, 2023)).run(timeout=60)
for el in at.get("plotly_chart"):
    fig = pio.from_json(el.proto.spec)
    name = fig.layout.title.text[:1]
    fig.write_image(f"screens/{name}.png", width=900, height=450)
    print("wrote", name)
