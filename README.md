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