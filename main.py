# app.py

from flask import Flask, render_template, request
import plotly.express as px
import pandas as pd
import numpy as np
import plotly
import json
import os 
import io

app = Flask(__name__)

@app.route("/")
def home():

    df = pd.read_csv("Output Data.csv", index_col=0)

    # 
    daus = []
    added_daus = []
    for index, row in df.iterrows():
        dau = "DAU " + str(row["DAU"])
        gmus = "(" + str(row["GMUs"]) + ")"
        if dau not in added_daus:
            daus.append(
                {
                    "dau": dau,
                    "dauNum":str(row["DAU"]),
                    "gmus":gmus
                }
            )
            added_daus.append(dau)

    print(len(request.args))
    print(request.args)
    if len(request.args) > 0:

        dau_filter = [key for key in request.args.keys()]

        # Filter the data (I want to eventually use Flask as in interface)
        # dau_list = ["8","9","10"]
        dau_filter = str(dau_filter).lstrip("[").rstrip("]")
        df = df.query(f"DAU in ({dau_filter})")
        print(f"DAU in ({dau_filter})")

        # Plot the data
        fig = px.line(df, x="year", y="Post Hunt Estimate", color='DAU')
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


        return render_template("index.html", params = daus, graphJSON=graphJSON)

    else:

        return render_template("index.html", params = daus)

if __name__ == "__main__":

    app.run(debug=True)





# # Helpful in figuring things out
# #   -> https://github.com/chezou/tabula-py/issues/126
# #   -> https://github.com/chezou/tabula-py/blob/5c22254a03862c4d8ab1cd319a090e3c464ea6df/tabula/io.py#L97
# #   -> https://stackoverflow.com/questions/45457054/tabula-extract-tables-by-area-coordinates

# # Write a Flask app where you choose a DAU and then see the population over time

# # Do we try the parrelel web requests? - for now, get the app
# running while reding data from csv