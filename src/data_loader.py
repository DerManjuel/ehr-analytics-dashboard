import pandas as pd

def load_data(file_path):
    """
    Load data from a CSV file.

    Parameters:
    file_path (str): The path to the CSV file.

    Returns:
    pd.DataFrame: A DataFrame containing the loaded data.
    """
    try:
        data = pd.read_csv(file_path)
        return data
    except Exception as e:
        print(f"An error occurred while loading the data: {e}")
        return None
    
if __name__ == "__main__":
    # Example usage
    #data = load_data("data/patients.csv")
    #if data is not None:
    #    print(data.head())

    patients = pd.read_csv("data/output/csv/patients.csv")

    print(patients.head())
    print(patients.columns)