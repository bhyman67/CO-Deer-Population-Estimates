# app.py

from flask import Flask, render_template, request, session
import pandas as pd
import json
import os 
import io

app = Flask(__name__)
app.secret_key = os.urandom(28)

@app.route("/")
def home():

    if "data" not in session.keys():

        data = {'Name':['Tom', 'nick', 'krish', 'jack'],
                'Age':[20, 21, 19, 18]}
        df = pd.DataFrame(data)

        session["data"] = df.to_json()

        return render_template("index.html", output = "New data") 

    else:

        df = pd.read_json(session.get("data"))
        return render_template("index.html", output = "Same data")

if __name__ == "__main__":

    app.run(debug=True)







# # Helpful in figuring things out
# #   -> https://github.com/chezou/tabula-py/issues/126
# #   -> https://github.com/chezou/tabula-py/blob/5c22254a03862c4d8ab1cd319a090e3c464ea6df/tabula/io.py#L97
# #   -> https://stackoverflow.com/questions/45457054/tabula-extract-tables-by-area-coordinates

# # Write a Flask app where you choose a DAU and then see the population over time

# # Do we try the parrelel web requests? 

# import plotly.express as px
# import pandas as pd
# import numpy as np
# import tabula

# pull_from_web = False

# if pull_from_web:

#     years = ["2010","2011","2012","2013","2014","2015","2016","2017","2018","2019"]

#     df_list = []
#     cpw_base_url = "https://cpw.state.co.us"
#     for year in years:

#         # The url changed a little bit for reports after 2013
#         if int(year) <= 2014:

#             url = f"{cpw_base_url}/Documents/Hunting/BigGame/Statistics/Deer/{year}DeerPopulationEstimate.pdf"

#         else:

#             url = f"{cpw_base_url}/Documents/Hunting/BigGame/Statistics/Deer/{year}DeerPopulationEstimates.pdf"

#         print(url)
#         # Refresh the Flask app right here

#         # Grab the data. The 2019 report was tricky to parse.. 
#         if year != "2019":
#             df = tabula.read_pdf(url)[0]
#         else:
#             # wow, this was a pain... 
#             df = tabula.read_pdf(url, guess = False, area = [92.88,120.24,489.6,675], pages = 1)[0]

#         # Drop the first row and rename rows
#         if year != "2010":
#             df.drop(0,0,inplace = True)
#         df.rename( 
#             columns = {
#                 df.columns[0]:"DAU",
#                 df.columns[1]: "GMUs",
#                 df.columns[2]:"Post Hunt Estimate",
#                 df.columns[3]:"Buck/Doe ratio (per 100)"
#             },
#             inplace = True
#         )

#         # Create a year column
#         df["year"] = year

#         # Add current df to the df list 
#         df_list.append(df)

#     # Combine all the dfs in the df list to one df
#     df = pd.concat(df_list)

# else:

#     df = pd.read_excel("Output Data.xlsx", index_col=0)

# # Format data types among some of the cols... 
# df["Post Hunt Estimate"].replace(",","",regex = True, inplace = True)
# df["Post Hunt Estimate"] = pd.to_numeric(df["Post Hunt Estimate"])
# df["DAU"] = df["DAU"].astype(str)
# df["year"] = df["year"].astype(str)
# df["DAU"] = df["DAU"].str.strip("**")
# df["DAU"] = pd.to_numeric(df["DAU"])

# # Filter the data (I want to eventually use Flask as in interface)
# dau_list = ["8","9","10"]
# dau_list_str = str(dau_list).lstrip("[").rstrip("]")
# df = df.query(f"DAU in ({dau_list_str})")

# # Plot the data
# fig = px.line(df, x="year", y="Post Hunt Estimate", color='DAU')
# fig.show()

# # ...
# # df.to_excel("Output Data.xlsx")
# print("done")