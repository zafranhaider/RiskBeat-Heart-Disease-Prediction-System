import pickle
import pandas as pd

def read_pickle_file(file_path):
    try:
        with open(file_path, "rb") as file:
            data = pickle.load(file)
        
        if isinstance(data, pd.DataFrame):
            print("Data is a DataFrame:")
            print(data)
        elif isinstance(data, dict):
            print("Data is a dictionary:")
            df = pd.DataFrame(list(data.items()), columns=["Key", "Value"])
            print(df)
        else:
            print("Data is of type:", type(data))
            print(data)
    except Exception as e:
        print("Error reading pickle file:", e)

if __name__ == "__main__":
    file_path = "lifestyle.pkl"  # Change this to your actual file path
    read_pickle_file(file_path)