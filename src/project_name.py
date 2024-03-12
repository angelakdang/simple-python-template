# This is where the bulk of your functions will go
import json


def load_data():
    f = open("data/example.json")
    data = json.load(f)
    print(f"Data loaded: {data}")


def transform_data():
    print("Data transformed.")


def generate_chart():
    print("Here's a chart.")
