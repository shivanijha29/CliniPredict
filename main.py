from flask import Flask, jsonify,render_template,request
import pandas as pd
import os
import json 
# from google import genai
import datetime
import random
# import agent

app = Flask(__name__)

UPLOAD_FOLDER=r"I:\My Drive\Medico\static\uploadedFeedbacks" 
previous_length = None  # Initialize a variable to store the previous length


@app.route('/api/data')
def get_data():
    current_time = datetime.datetime.now()
    i=current_time.second
      
   
    data =   [
            {
                "Group": "Card",
                "Header": "Total Feedbacks",
                "ChartData": [
                    {
                        "Title": "Doctor",
                        "ChartType": "NumberCard",
                        "Data":[500 + i]
                    },
                    {
                        "Title": "Patient",
                        "ChartType": "NumberCard",
                        "Data": [253 + i * 2]
                    },

                ]
            }
            ,
            {
                "Group": "Patient",
                "DataSource": "PatientChurn.csv",
                "Header": "Patient Insights",
                "ChartData": [
                    {
                        "Title": "Satisfaction",
                        "ChartType": "Column",
                        "Data": [  {"country": "Low", "value": random.randint(200, 250)},
                    {"country": "Medium", "value": random.randint(170, 200)},
                    {"country": "High", "value": random.randint(180, 210)}
                    ]
                    },
                    {
                        "Title": "Communication",
                        "ChartType": "clockgauge",
                        "Data": [(70+i)%100]
                    },
                    {
                        "Title": "Satisfaction(%)",
                        "ChartType": "clockgauge",
                        "Data": [(60+i)%100]
                    }
                ]
            },
            {
                "Group": "Doctor",
                "DataSource": "Doctorchurn.csv",
                "Header": "Doctor Insights",
                "ChartData": [
                    {
                        "Title": "Sanitation",
                        "ChartType": "Column",
                        "Data": [  {"country": "Low", "value": random.randint(200, 250)},
                    {"country": "Medium", "value": random.randint(170, 200)},
                    {"country": "High", "value": random.randint(180, 210)}]
                    },
                    {
                        "Title": "Compensation",
                        "ChartType": "pie",
                        "Data": [{
                            "country": "Satisfied",
                            "value": 509 + i
                        }, {
                            "country": "Not Satisfied",
                            "value": 301 + i
                        }]
                    }
                ]
            }

        ]

    return (data)

@app.route('/dashboard')
def analysis():
   return render_template('dashboard.html')


@app.route('/feedback')
def feedback():
   return render_template('feedback-grid.html')

@app.route('/')
def landing():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)