from streamlit.testing.v1 import AppTest
at = AppTest.from_file("app.py").run(timeout=60)
assert not at.exception, at.exception
print("default ok; selectboxes:", [s.label for s in at.selectbox])
at.selectbox[0].set_value("Asia").run(timeout=60)
assert not at.exception, at.exception
at.selectbox[1].set_value("India").run(timeout=60)
at.slider[0].set_value((2010, 2023)).run(timeout=60)
assert not at.exception, at.exception
print("title:", at.title[0].value, "| infos:", len(at.info))
print("plotly charts:", len(at.get("plotly_chart")))
