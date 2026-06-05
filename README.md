# EHR Analytics Dashboard

Clinical analytics dashboard built with Streamlit and synthetic Synthea EHR data.

## General
- app.py	Streamlit entry point
- data_loader.py	load CSVs
- analytics.py	compute metrics
- visualizations.py	generate charts

## Generate Sample Data
This command generates a realistic dataset with 100 patients with csv export enabled:

'''java -jar synthea-with-dependencies.jar -p 100 --exporter.csv.export=true'''

While exploring the synthetic EHR data, I encountered socioeconomic and employment concepts mixed into the clinical condition dataset, which required semantic filtering and categorization.

## Data Exploration
condition.csv implements DESCRIPTION. These DESCRIPTIONs contain categories like "disorder" or "finding". Not all findings are of medical relevance. Condition is therefore split into the different categories. This enables easier data analysis, because the category is no longer embedded inside DESCRIPTION.

During the data exploration multiple plots are saved in docs to be quickly accessible later on. These plots contain condition-categories, top-conditions, top-disorders, top-findings and top-situations.

encounter.csv shows every encounter processed. This enables easy computing of the encounters-per-patient, which shows how often a patient needs medical care. This is also plottet as html in docs.

patients.csv offers other difficulties like the age distribution. Because we only have BIRTHDATE and DEATHDATE we firstly need to add a status field defining the patient as alive or deceased. After that we can calculate the age of living patients and the age at death of deceased patients. Now the histograms for patient age distributions can be plotted, even the distribution at what age patients die.

By merging patients with conditions, disorders per age group can be extracted. Also shown in top_disorders_per_age_group.html.