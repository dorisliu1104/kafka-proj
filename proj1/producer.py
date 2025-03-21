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
import pandas as pd
import numpy as np
import logging

from confluent_kafka import Producer
from employee import Employee
import pandas as pd
from confluent_kafka.serialization import StringSerializer

logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("kafka-producer")

employee_topic_name = "bf_employee_salary"
csv_file = 'Employee_Salaries.csv'

#Can use the confluent_kafka.Producer class directly
class salaryProducer(Producer):
    #if connect without using a docker: host = localhost and port = 29092
    #if connect within a docker container, host = 'kafka' or whatever name used for the kafka container, port = 9092
    def __init__(self, host="localhost", port="29092"):
        self.host = host
        self.port = port
        producerConfig = {'bootstrap.servers':f"{self.host}:{self.port}",
                          'acks' : 'all'}
        super().__init__(producerConfig)
     

class DataHandler:
    '''
    Your data handling logic goes here. 
    You can also implement the same logic elsewhere. Your call
    '''
    def __init__(self, filePath):
        self.filePath = filePath
        
    def readData(self):
        df = pd.read_csv(self.filePath)
        df['hireDate'] = pd.to_datetime(df["Initial Hire Date"], format='%d-%b-%Y')
        wantedDepartments = ['ECC','CIT','EMS']
        df = df.query('Department in @wantedDepartments and hireDate >= "2010-01-01"')
        df['Salary'].fillna(0, inplace = True)
        df['Salary'] = np.floor(df['Salary']).astype(int)
    
        return df.to_numpy()


if __name__ == '__main__':
    encoder = StringSerializer('utf-8')
    reader = DataHandler(csv_file)
    producer = salaryProducer()
    '''
    # implement other instances as needed
    # you can let producer process line by line, and stop after all lines are processed, or you can keep the producer running.
    # finish code with your own logic and reasoning

    for line in lines:
        emp = Employee.from_csv_line(line)
        producer.produce(employee_topic_name, key=encoder(emp.emp_dept), value=encoder(emp.to_json()))
        producer.poll(1)
    '''
    data = reader.readData()
    logger.info("Producer started")
    for line in data:
        emp = Employee.from_csv_line(line)
        producer.produce(employee_topic_name, key=encoder(emp.emp_dept), value=encoder(emp.to_json()))
        logger.info(f"Producer produces line {line}")
        producer.poll(1)
    
    logger.info("Producer completed")


    
    