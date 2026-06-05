###
# Explore the datasets to understand their structure and content.
###

import pandas as pd
import plotly.express as px
from datetime import datetime

###
# load datasets
###
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

##########################
# ENCOUNTERS EXPLORATION #
##########################
print("========================================================================================================================")
print("Encounters Columns:")
print(encounters.columns)
print("Encounters Descriptions:")
print(encounters["DESCRIPTION"].unique())

# calculate encounters per patient
encounters_per_patient = encounters.groupby("PATIENT").size()

print("Encounters per patient:")
print(encounters_per_patient.head())

# convert to DataFrame for better visualization
encounters_per_patient = encounters_per_patient.reset_index()

encounters_per_patient.columns = [
    "patient_id",
    "encounter_count"
]

# how many patients need frequent care?
fig = px.histogram(
    encounters_per_patient,
    x="encounter_count",
    nbins=20,
    title="Healthcare Encounters Per Patient"
)

fig.write_html("docs/encounters_per_patient.html")

##############################
### CONDITIONS EXPLORATION ###
##############################
print("========================================================================================================================")
print("Conditions Columns:")
print(conditions.columns)
print("Conditions Descriptions:")
print(conditions["DESCRIPTION"].unique())

print("Condition description counts:")
print(
    conditions["DESCRIPTION"]
    .value_counts()
    .head(100)
)

# top conditions extracted for plotting
top_conditions = (
    conditions["DESCRIPTION"]
    .value_counts()
    .head(10)
)

# plot top conditions
fig = px.bar(
    x=top_conditions.values,
    y=top_conditions.index,
    orientation="h",
    title="Top Conditions"
)

fig.write_html("docs/top_conditions.html")

# extract condition categories (usually in parentheses)
conditions["category"] = conditions["DESCRIPTION"].str.extract(r"\(([^)]+)\)", expand=False).fillna("unknown")
categories = sorted(conditions["category"].dropna().unique())
print("----------------------------------------------------------------------------------------------------------------------------")
print("Condition categories:")
print(categories)
print("Condition category counts:")
print(conditions["category"].value_counts())

# visualize category distribution
category_counts = conditions["category"].value_counts()

fig = px.bar(
    x=category_counts.values,
    y=category_counts.index,
    orientation="h",
    title="Condition Categories"
)

fig.write_html("docs/condition_categories.html")

# helper function to plot top conditions per category type
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

# plot top conditions for each category
plot_top_category(conditions, "disorder", title="Top Disorders")
plot_top_category(conditions, "finding", title="Top Findings")
plot_top_category(conditions, "situation", title="Top Situations")

##############################
### PATIENT EXPLORATION ###
##############################
print("========================================================================================================================")
print("Patient Columns:")
print(patients.columns)

patients["BIRTHDATE"] = pd.to_datetime(patients["BIRTHDATE"], errors="coerce")
patients["DEATHDATE"] = pd.to_datetime(patients["DEATHDATE"], errors="coerce")

today = pd.to_datetime("today")

patients["age"] = (
    (patients["DEATHDATE"].fillna(today) - patients["BIRTHDATE"])
    .dt.days / 365.25
)

avg_age = patients["age"].mean()
print(f"Average patient age: {avg_age:.2f} years "
      f"with max age of {patients['age'].max():.2f} years "
      f"and min age of {patients['age'].min():.2f} years"
    )

fig = px.histogram(
    patients,
    x="age",
    nbins=20,
    title="Overall Patient Age Distribution"
)

fig.write_html("docs/patient_ages.html")

# add status column based on DEATHDATE
patients["status"] = patients["DEATHDATE"].isna().map({
    True: "Alive",
    False: "Deceased"
})

# visualize age distribution by status
fig = px.histogram(
    patients,
    x="age",
    color="status",
    nbins=20,
    barmode="overlay",
    title="Age Distribution: Alive vs Deceased"
)

fig.write_html("docs/patient_age_by_status.html")

# create age groups for further analysis
patients["age_group"] = pd.cut(
    patients["age"],
    bins=[0, 18, 35, 50, 65, 120],
    labels=["0-18", "19-35", "36-50", "51-65", "65+"]
)

# merge conditions with patients to analyze age distribution for specific conditions
merged = conditions.merge(
    patients[["Id", "age_group"]],
    left_on="PATIENT",
    right_on="Id",
    how="left"
)

# filter only disorders for clearer analysis
disorders = merged[merged["category"] == "disorder"]

# top disorders by age group
top_by_age = (
    disorders
    .groupby(["age_group", "DESCRIPTION"])
    .size()
    .reset_index(name="count")
)

# extract top 5 conditions for each age group
top5_per_group = (
    top_by_age
    .sort_values(["age_group", "count"], ascending=[True, False])
    .groupby("age_group")
    .head(5)
)

# visualize top conditions by age group
fig = px.bar(
    top5_per_group,
    x="count",
    y="DESCRIPTION",
    color="age_group",
    orientation="h",
    title="Top Disorders by Age Group"
)

fig.write_html("docs/top_disorders_by_age_group.html")
