import pickle

def save_data(bank_system, filename="bank_data.pkl"):
    with open(filename, 'wb') as f:
        pickle.dump(bank_system, f)
    print("Data saved successfully.")

def load_data(filename="bank_data.pkl"):
    try:
        with open(filename, 'rb') as f:
            bank_system = pickle.load(f)
        print("Data loaded successfully.")
        return bank_system
    except FileNotFoundError:
        print("No saved data found.")
        return None
