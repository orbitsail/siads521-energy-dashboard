"""Clean the OWID energy dataset for the dashboard.
Usage: python prep_data.py [raw_csv_path]   (default /tmp/energy.csv)
"""
import sys
from pathlib import Path
import pandas as pd
import country_converter as coco

raw = sys.argv[1] if len(sys.argv) > 1 else "/tmp/energy.csv"
df = pd.read_csv(raw)
print(f"Raw: {df.shape[0]} rows x {df.shape[1]} cols")

# 1. Keep only real countries: OWID aggregates (World, Africa, ...) have no iso_code or an OWID_ code.
df = df[df["iso_code"].notna() & ~df["iso_code"].astype(str).str.startswith("OWID")]
print(f"After dropping aggregates: {df['country'].nunique()} countries")

# 2. Keep 2000-2023. 2024 is about half-missing (reporting lag), so it is excluded.
df = df[df["year"].between(2000, 2023)].copy()

# 3. Add continent from ISO3 via country_converter. Kosovo (OWID_KOS) is already gone with the OWID filter.
cc = coco.CountryConverter()
iso = df["iso_code"].drop_duplicates()
mapping = dict(zip(iso, cc.convert(iso.tolist(), src="ISO3", to="continent")))
df["continent"] = df["iso_code"].map(mapping)
# Split 'America' into North / South America (country_converter has no 7-continent scheme).
SOUTH = {"ARG","BOL","BRA","CHL","COL","ECU","GUY","PRY","PER","SUR","URY","VEN","FLK","GUF"}
df.loc[df["continent"] == "America", "continent"] = df["iso_code"].apply(
    lambda c: "South America" if c in SOUTH else "North America")
bad = df[df["continent"].isna() | (df["continent"] == "not found")]
print("Dropped (continent not mapped):", sorted(bad["country"].unique()))
df = df.drop(bad.index)

# 4. Keep countries with population >= 1,000,000 in 2023 (micro-states make slope/bar charts noisy).
pop23 = df[df["year"] == 2023].set_index("country")["population"]
keep = pop23[pop23 >= 1_000_000].index
df = df[df["country"].isin(keep)]
print(f"Countries kept (pop >= 1M in 2023): {len(keep)}")

# 5. Column selection. Note OWID naming mismatch: other_renewable_electricity (singular)
#    but other_renewables_share_elec (plural). Normalize everything to other_renewable_*.
df = df.rename(columns={"other_renewables_share_elec": "other_renewable_share_elec"})
srcs = ["coal","gas","oil","nuclear","hydro","wind","solar","biofuel","other_renewable"]
cols = ["country","iso_code","continent","year","population","energy_per_capita",
        "carbon_intensity_elec","electricity_generation"]
cols += [f"{s}_electricity" for s in srcs] + [f"{s}_share_elec" for s in srcs]
print("Columns used:", cols)

# low-carbon / fossil shares: use OWID's if present, else compute from the source shares
low = ["nuclear","hydro","wind","solar","biofuel","other_renewable"]
if "low_carbon_share_elec" not in df:
    df["low_carbon_share_elec"] = df[[f"{s}_share_elec" for s in low]].sum(axis=1, min_count=len(low))
if "fossil_share_elec" not in df:
    df["fossil_share_elec"] = df[[f"{s}_share_elec" for s in ["coal","gas","oil"]]].sum(axis=1, min_count=3)
cols += ["low_carbon_share_elec", "fossil_share_elec"]
df = df[cols].sort_values(["country","year"]).reset_index(drop=True)

Path("data").mkdir(exist_ok=True)
df.to_csv("data/energy_clean.csv", index=False)
print(f"Wrote data/energy_clean.csv: {df.shape}")

# 6. Missing-value summary
miss = df.isna().sum()
print("\nMissing values (kept columns):")
print(pd.DataFrame({"missing": miss, "pct": (miss / len(df) * 100).round(1)})[miss > 0].to_string())
print("\nContinent counts:", df.groupby("continent")["country"].nunique().to_dict())
