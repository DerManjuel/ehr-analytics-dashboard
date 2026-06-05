import pandas as pd

# load datasets
patients = pd.read_csv("data/output/csv/patients.csv")
encounters = pd.read_csv("data/output/csv/encounters.csv")
conditions = pd.read_csv("data/output/csv/conditions.csv")

# Display basic information about the datasets
print("patients.columns:")
print(patients.columns)
print("encounters.columns:")
print(encounters.columns)
print("conditions.columns:")
print(conditions.columns)

# calculate encounters per patient
encounters_per_patient = encounters.groupby("PATIENT").size()

print("Encounters per patient:")
print(encounters_per_patient.head())
print("Maximum encounters per patient:")
print(encounters_per_patient.max())

# convert to DataFrame for better visualization
encounters_per_patient = encounters_per_patient.reset_index()

encounters_per_patient.columns = [
    "patient_id",
    "encounter_count"
]

# how many patients need frequent care?
import plotly.express as px

fig = px.histogram(
    encounters_per_patient,
    x="encounter_count",
    nbins=20,
    title="Healthcare Encounters Per Patient"
)

fig.write_html("docs/encounters_per_patient.html")

# conditions exploration
print("Conditions Description:")
print(conditions["DESCRIPTION"].unique())
print(
    conditions["DESCRIPTION"]
    .value_counts()
    .head(100)
)

# top conditions
top_conditions = (
    conditions["DESCRIPTION"]
    .value_counts()
    .head(10)
)

fig = px.bar(
    x=top_conditions.values,
    y=top_conditions.index,
    orientation="h",
    title="Top Conditions"
)

fig.write_html("docs/top_conditions.html")


conditions["category"] = conditions["DESCRIPTION"].str.extract(r"\(([^)]+)\)", expand=False).fillna("unknown")
categories = sorted(conditions["category"].dropna().unique())
print("Condition categories:")
print(categories)
print(conditions["category"].value_counts())


category_counts = conditions["category"].value_counts()


def plot_top_category(df, category, n=10, title=None):
    subset = df[df["category"] == category]
    top = subset["DESCRIPTION"].value_counts().head(n)

    fig = px.bar(
        x=top.values,
        y=top.index,
        orientation="h",
        title=title or f"Top {n} {category}s"
    )

    file_path = f"docs/top_{category}.html"

    fig.write_html(file_path)

    print(f"Saved: {file_path}")

    return fig


cat_counts = conditions["category"].value_counts()

fig = px.bar(
    x=cat_counts.values,
    y=cat_counts.index,
    orientation="h",
    title="Condition Categories"
)

fig.write_html("docs/condition_categories.html")


plot_top_category(conditions, "disorder", title="Top Disorders")
plot_top_category(conditions, "finding", title="Top Findings")
plot_top_category(conditions, "situation", title="Top Situations")





"""disorders = conditions[conditions["category"] == "disorder"]
top10_disorders = disorders["DESCRIPTION"].value_counts().head(10)

fig = px.bar(
    x=top10_disorders.values,
    y=top10_disorders.index,
    orientation="h",
    title="Top Disorders"
)

fig.write_html("docs/top_disorders.html")



finding = conditions[conditions["category"] == "finding"]
top10_findings = finding["DESCRIPTION"].value_counts().head(10)

fig = px.bar(
    x=top10_findings.values,
    y=top10_findings.index,
    orientation="h",
    title="Top Findings"
)

fig.write_html("docs/top_findings.html")



situation = conditions[conditions["category"] == "situation"]
top10_situations = situation["DESCRIPTION"].value_counts().head(10)

fig = px.bar(
    x=top10_situations.values,
    y=top10_situations.index,
    orientation="h",
    title="Top Situations"
)

fig.write_html("docs/top_situations.html")

"""