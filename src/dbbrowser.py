from flask import Flask, render_template, jsonify
import sqlite3


app = Flask(__name__)

@app.route("/")
def main1Page(): return render_template('home.html')

@app.route("/old")
def oldMain1Page(): return render_template('home_new.html')

@app.route("/api/list/country")
def listCountries():
    conn = sqlite3.connect('..\\db\\data.db')
    cur = conn.cursor()
    cur.execute('SELECT distinct country, country_code from data order by country')
    res = cur.fetchall()
    toret = []
    for u in res:
        toret.append({"isocode":u[1], "label":u[0]})
    return jsonify(toret)

@app.route("/api/list/state")
def listStates():
    conn = sqlite3.connect('..\\db\\data.db')
    cur = conn.cursor()
    cur.execute('SELECT distinct state from data order by state')
    return jsonify(cur.fetchall())

@app.route("/api/list/admin2")
def listAdmin2():
    conn = sqlite3.connect('..\\db\\data.db')
    cur = conn.cursor()
    cur.execute('SELECT distinct admin2 from data order by admin2')
    return jsonify(cur.fetchall())

@app.route("/api/list/<string:country>/state")
def listStateInCountry(country):
    conn = sqlite3.connect('..\\db\\data.db')
    cur = conn.cursor()
    cur.execute('SELECT distinct state from data where country = \"' + country + '\" order by state')
    return jsonify(cur.fetchall())


@app.route("/api/list/<string:country>/<string:state>/admin2")
def listAdmin2InState(country, state):
    conn = sqlite3.connect('..\\db\\data.db')
    cur = conn.cursor()
    cur.execute('SELECT distinct admin2 from data where country = \"' + country + '\" and state = \"' + state + '\" order by admin2')
    return jsonify(cur.fetchall())

@app.route("/api/table/data/country")
def countryDataTable():
    conn = sqlite3.connect('..\\db\\data.db')
    cur = conn.cursor()
    cur.execute('select country, SUM(confirmed), SUM(deaths), SUM(recovered), sum(active) from data where date = (select MAX(date) from data)  group by country order by country')
    return jsonify(cur.fetchall())

@app.route("/api/table/data/<string:country>")
def stateDataTable(country):
    conn = sqlite3.connect('..\\db\\data.db')
    cur = conn.cursor()
    cur.execute('select state, SUM(confirmed), SUM(deaths), SUM(recovered), sum(active) from data where country = "'+country+'" and date = (select MAX(date) from data)  group by state order by state')
    return jsonify(cur.fetchall())

@app.route("/api/table/data/<string:country>/<string:state>")
def admin2DataTable(country, state):
    conn = sqlite3.connect('..\\db\\data.db')
    cur = conn.cursor()
    cur.execute('select admin2, SUM(confirmed), SUM(deaths), SUM(recovered), sum(active) from data where country = "'+country+'" and state = "'+ state+'" and date = (select MAX(date) from data)  group by admin2 order by admin2')
    return jsonify(cur.fetchall())

@app.route("/api/table/history/world")
def WorldHistoryData():
    conn = sqlite3.connect('..\\db\\data.db')
    cur = conn.cursor()
    cur.execute('select date, SUM(confirmed), SUM(deaths), SUM(recovered), SUM(active) from data group by date order by date')
    return jsonify(cur.fetchall())

@app.route("/api/table/history/<string:country>")
def CountryHistoryData(country):
    conn = sqlite3.connect('..\\db\\data.db')
    cur = conn.cursor()
    cur.execute('select date, SUM(confirmed), SUM(deaths), SUM(recovered), SUM(active) from data where country = "'+country+'" group by date order by date')
    return jsonify(cur.fetchall())

@app.route("/api/table/history/<string:country>/<string:state>")
def StateHistoryData(country, state):
    conn = sqlite3.connect('..\\db\\data.db')
    cur = conn.cursor()
    cur.execute('select date, SUM(confirmed), SUM(deaths), SUM(recovered), SUM(active) from data where country = "' + country + '" and state = "' + state + '" group by date order by date')
    return jsonify(cur.fetchall())

@app.route("/api/table/history/<string:country>/<string:state>/<string:admin2>")
def Admin2HistoryData(country, state, admin2):
    conn = sqlite3.connect('..\\db\\data.db')
    cur = conn.cursor()
    cur.execute('select date, SUM(confirmed), SUM(deaths), SUM(recovered), SUM(active) from data where country = "' + country + '" and state = "' + state + '" and admin2 = "' + admin2 + '" group by date order by date')
    return jsonify(cur.fetchall())


app.run(debug=True, port=8080)