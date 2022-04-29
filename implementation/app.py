# Python Standard Library Modules
from os import path
import pickle
# 3rd-party installed modules
from flask import Flask, render_template, request
# Custom Project Modules (*.py files)


# Load pre-fitted preprocessors, models, transformers
APP_DIR = path.dirname(path.abspath(__file__))

# repeat for each pickle file
with open(f"{APP_DIR}/model/<FILENAME>", "r") as file:
    variable_name = pickle.load(file)

# Define Flask app
app = Flask(__name__)

# Landing Page
@app.route("/")
def index():
    return render_template("index.html")

# Predict Page
@app.route("/predict", methods=["GET"])
def predict_page():
    return render_template("predict.html")

    # Prep form data for model

    # Generate, transform, and format predictions

    # Render prediction
    return render_template("predict.html",
        date1=, price1=,date2=,price2=,date3=,price3=

# About Page
@app.route("/about")
def about_page():
    return render_template("about.html")
    )
