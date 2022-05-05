# Python Standard Library Modules
from os import path
import pickle
# 3rd-party installed modules
from flask import Flask, render_template, request
# Custom Project Modules (*.py files)
import model.stock_project as mod

# Load pre-fitted preprocessors, models, transformers
APP_DIR = path.dirname(path.abspath(__file__))

# repeat for each pickle file
with open(f"stock_project/implementation/model/stock_ssx.pickle", "r") as file:
    ssx = pickle.load(file)
with open(f"stock_project/implementation/model/stock_ssy.pickle", "r") as file:
    ssy = pickle.load(file)
with open(f"stock_project/implementation/model/stock_model.pickle", "r") as file:
    model = pickle.load(file)
# Define Flask app
app = Flask(__name__)

# Landing Page
@app.route("/")
def index():
    return render_template("index.html")

# Predict Page
@app.route("/predict", methods=["GET"]
def predict_form():
    return render_template("predict.html")
# Result Page
@app.route("/result", methods=["POST"])
def result_page():
    form_data = list(request.form.items())
    open, close, volume, low, high = form_data[0][1], form_data[1][1], form_data[2][1], form_data[3][1], form_data[4][1]        
    # Prep form data for model
    df = mod.use_data(open, close, high, low, volume)
    # Generate, transform, and format predictions
    df = mod.feature_engineer(df)
    x,y = mod.use_scale(df, ssx, ssy)
    pred = model_predict(model, x, ssy)
    # Render prediction
    return render_template("result.html", prediction=pred)

# About Page
@app.route("/about")
def about_page():
    return render_template("about.html")
    )
