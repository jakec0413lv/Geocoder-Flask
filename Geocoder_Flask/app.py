from flask import Flask, render_template, request
import pandas
from geopy.geocoders import ArcGIS

app=Flask(__name__)

nom = ArcGIS()

@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        file = request.files['f']
        df = pandas.read_csv(file)
        if 'Address' not in df and 'address' not in df:
            message = "Please make sure you have an address column in your CSV file!"
            return render_template("index.html", message = message)
        lat = []
        lon = []
        for index, row in df.iterrows():
            location = nom.geocode(row['Address'])
            lat.append(location.latitude)
            lon.append(location.longitude)
        df['Latitude']  = lat
        df['Longtitude'] = lon
        print(df)
        return render_template("index.html", table = df.to_html(classes="data", header="true"))
    return render_template("index.html")

if __name__ == "__main__":
    app.debug=True
    app.run()