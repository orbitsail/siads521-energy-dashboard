# Is the world's electricity getting cleaner?

An interactive dashboard that explores how the electricity mix of 160 countries changed between 2000 and 2023, and whether a rising "low-carbon share" really means a country is decarbonizing. Built with Streamlit and Plotly for SIADS 521 (Visual Exploration of Data), University of Michigan MADS, Assignment 3.

- **Live dashboard:** _link coming after deployment_
- **Video walkthrough:** _link coming_

## Data

Our World in Data, [Energy dataset](https://github.com/owid/energy-data), licensed CC BY 4.0. Underlying third-party sources (Energy Institute, Ember, EIA) are listed in OWID's codebook.

`data/energy_clean.csv` is produced from the raw file by `prep_data.py`:

```bash
pip install -r requirements-prep.txt
curl -L -o owid-energy-data.csv https://nyc3.digitaloceanspaces.com/owid-public/data/energy/owid-energy-data.csv
python prep_data.py owid-energy-data.csv
```

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```
