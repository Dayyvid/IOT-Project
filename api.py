from flask import Flask, request, json, jsonify
from flask_restful import Resource, Api
from flask_cors import CORS, cross_origin
from influxdb import InfluxDBClient
import datetime

dbClient = InfluxDBClient('0.0.0.0', 8086, 'root', 'root', 'mydb')

app = Flask(__name__)
api = Api(app)
CORS(app)

class Lightbulb(Resource):

    def get(self):
        searchQuery = 'SELECT * FROM "lightbulb"'
        result = dbClient.query(searchQuery)
        jsonData = list(result.get_points(measurement='lightbulb'))[0]
        return jsonData

    def post(self):
        # convert json data to python dict
        jsonData = request.get_data()
        jsonData = json.loads(jsonData)
        insertFields = {}
        insertFields['saturation'] = jsonData['saturation']
        insertFields['brightness'] = jsonData['brightness']
        insertFields['hue'] = jsonData['hue']
        insertFields['red'] = jsonData['red']
        insertFields['green'] = jsonData['green']
        insertFields['blue'] = jsonData['blue']
        insertFields['songName'] = jsonData['songName']
        
        # prep data to be inserted into influx
        receiveTime = datetime.datetime.utcnow()
        insertBody = [{
            "measurement": 'lightbulb',
            "time": receiveTime,
            "fields": insertFields
        }]

        # empty out influxdb
        deleteQuery = 'DELETE FROM "lightbulb"'
        dbClient.query(deleteQuery)

        #insert into influxdb
        dbClient.write_points(insertBody)

        searchQuery = 'SELECT * FROM "lightbulb"'
        result = dbClient.query(searchQuery)
        print(result)
api.add_resource(Lightbulb, '/lightbulb')
app.run(host='0.0.0.0', port=5000,debug=True)