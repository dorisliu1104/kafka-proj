"""
Copyright (C) 2024 BeaconFire Staffing Solutions
Author: Ray Wang

This file is part of Oct DE Batch Kafka Project 1 Assignment.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

import csv
import json
import os
from confluent_kafka import Producer
from employee import Employee
import confluent_kafka
import logging
import pandas as pd
from confluent_kafka.serialization import StringSerializer
import psycopg2

logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("kafka-producer")


employee_topic_name = "bf_employee_cdc"

class cdcProducer(Producer):
    #if running outside Docker (i.e. producer is NOT in the docer-compose file): host = localhost and port = 29092
    #if running inside Docker (i.e. producer IS IN the docer-compose file), host = 'kafka' or whatever name used for the kafka container, port = 9092
    def __init__(self, host="localhost", port="29092"):
        self.host = host
        self.port = port
        producerConfig = {'bootstrap.servers':f"{self.host}:{self.port}",
                          'acks' : 'all'}
        super().__init__(producerConfig)
        self.running = True
    
    def cleanupCdc(self):
        try:
            conn = psycopg2.connect(
                host="localhost",
                database="postgres",
                user="postgres",
                port = '5432',
                password="postgres")
            conn.autocommit = True
            cur = conn.cursor()
            #your logic should go here

            cur.execute("DELETE FROM employeeCdc;")
            cur.close()
            conn.close()
        except Exception as err:
            print(f"Error fetching CDC: {err}")

    def fetchCdc(self):
        try:
            conn = psycopg2.connect(
                host="localhost",
                database="postgres",
                user="postgres",
                port = '5432',
                password="postgres")
            conn.autocommit = True
            cur = conn.cursor()
            #your logic should go here

            cur.execute("SELECT * FROM employeeCdc;")
            rows = cur.fetchall()
            cur.close()
            conn.close()
            return rows
        except Exception as err:
            raise Exception(f"Error fetching CDC: {err}")


if __name__ == '__main__':
    encoder = StringSerializer('utf-8')
    producer = cdcProducer()
    
    while producer.running:
        updateRows = producer.fetchCdc()
        if updateRows:
            logger.info(f'Sending records {updateRows} to Kafka')
        for row in updateRows:
            emp = Employee.from_line(row)
            producer.produce(employee_topic_name, key=encoder(str(emp.emp_id)), value=encoder(emp.to_json()))
        
        if updateRows:
            producer.cleanupCdc()

