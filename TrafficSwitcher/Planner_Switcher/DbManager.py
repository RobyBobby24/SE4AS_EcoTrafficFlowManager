import influxdb_client, os, time
import requests
from influxdb_client import InfluxDBClient, Point, WritePrecision
import re
from influxdb_client.client.write_api import SYNCHRONOUS
import json

host = "configuration_module2"
#host = "localhost"
url = f"http://{host}:5008/config/"


class DbManager:
    _token: str
    _org = "univaq"
    _host = "knowledge_module"  # "localhost"
    _url = "http://knowledge_module:8086"
    _analysis_time: int

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(DbManager, cls).__new__(cls)
            cls.instance._analysis_time = requests.get(url + "data/analysis_time").json()["data"]
            cls.instance._token = "seasinfluxdbtoken"
            cls.instance._client = influxdb_client.InfluxDBClient(url=cls.instance._url, token=cls.instance._token,
                                                                  org=cls.instance._org)
        return cls.instance

    def store_data_tag(self, measurement: str, field: str, value, tag_name_value=None):
        bucket = "seas"

        write_api = self._client.write_api(write_options=SYNCHRONOUS)
        data = Point(measurement)
        if tag_name_value != None:
            for tag_name, tag_value in tag_name_value.items():
                data = data.tag(tag_name, tag_value)

        point = (
            data.field(field, value)
        )
        write_api.write(bucket=bucket, org="univaq", record=point)



"""
    def store_data(self, measurement: str, field: str, value):
        bucket = "seas"

        write_api = self._client.write_api(write_options=SYNCHRONOUS)
        point = (
            Point(measurement)
            .field(field, value)
        )
        write_api.write(bucket=bucket, org="univaq", record=point)
"""

"""
    def query_last_time(self, bucket, start_time):
        query_api = self._client.query_api()

        query = ffrom(bucket: {bucket})
         |> range(start: {start_time})
        tables = query_api.query(query, org="univaq")
        return tables


    def query(self):
        query_api = self._client.query_api()

        query = f'from(bucket: "seas")'\
                f'|> range(start: -1000m)'
        tables = query_api.query(query, org="univaq")
        print(str(tables.to_json()))
        results = []
        for table in tables:
            for record in table.records:
                results.append(record)
"""
