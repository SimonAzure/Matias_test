from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import secrets
import json
import os
import requests
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import date

from builder import build_json, validate_inputs

app = Flask(__name__)
secret_key = secrets.token_hex(24)
app.secret_key = secret_key

executor = ThreadPoolExecutor(max_workers=1)

@app.route('/', methods=['GET'])
def index():
    current_date = date.today().strftime('%Y-%m-%d')
    return render_template('index.html', current_date=current_date)

@app.route('/build-report', methods=['POST'])
def build_report():
    report_type = request.form.get('report_type')
    columns = request.form.getlist('columns')
    timezone = request.form.get('timezone')
    format = request.form.get('format')
    report_interval = request.form.get('report_interval')	
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')

    # Validate inputs
    if validate_inputs(report_type, columns, timezone, format, report_interval, start_date, end_date):
        # Build the JSON
        report_json = build_json(report_type, columns, timezone, format, report_interval, start_date, end_date)

        return render_template('result.html', report_json=report_json)
    else:
        error_message = "Invalid inputs. Please check your inputs and try again."
        return render_template('error.html', error_message=error_message)

@app.route('/get-report', methods=['GET'])
def get_report():
    report_type = request.args.get('report_type')

    user = os.environ['API_USER']
    password = os.environ['API_PASS']

    payload = '{"auth": {"username" : "%s","password" : "%s"}}' % (user, password)
    response = requests.post("https://api.appnexus.com/auth", data=payload)

    authcookies = response.cookies

    api_url = 'https://api.appnexus.com/report?meta=' + report_type
    report_fields = requests.request("GET", api_url, cookies=authcookies)
    report_formatted = json.dumps(report_fields.json(), indent=2)

    if response.status_code != 200:
        raise Exception(response.reason)

    return render_template('report.html', report_response=report_formatted)

@app.route('/post-report', methods=['POST'])
def post_report():
    try:
        # Get the JSON data from the POST request
        # json_data = request.data.decode('utf-8')  # Correctly call request.get_json to parse JSON
        json_data = request.form.get('json_data')
        member_id = request.form.get('member_id')

        # Make the POST request to create the report
        user = os.environ['API_USER']
        password = os.environ['API_PASS']

        authentication = '{"auth": {"username" : "%s", "password" : "%s"}}' % (user, password)
        response_auth = requests.post("https://api.appnexus.com/auth", data=authentication)

        authcookies = response_auth.cookies

        payload = json_data
        headers = {'Content-Type': 'text/plain'}  # Set the request headers

        response = requests.post("https://api.appnexus.com/report?member_id=" + member_id, data=payload, headers=headers, cookies=authcookies)
        response_json = response.json()
        report_id = response_json.get('response', {}).get('report_id')
        #Hacer ciclo while con llamada a report?id=
        #time.sleep
        # execution_status = response_json.get('response', {}).get('execution_status')

        if response.status_code == 200:
            #storing the report_id value
            session['report_id'] = report_id
            print('Report ID in session is: ', report_id)
            # session['execution_status'] = execution_status
            # print(execution_status)
            # Report was successfully created, parse the response JSON
            fetch_report(report_id)
            return render_template('loading.html',  report_id=report_id)
        else:
            return jsonify({'error': f"Failed to create report. Error: {response.text}"}), 500  # Return an error response as JSON
        
    except Exception as e:
        return jsonify({'error': f"An error occurred: {str(e)}"}), 500  # Handle any exceptions and return an error response

def fetch_report(report_id):
    print('Fetching report with ID: ', report_id)
    try:
        #get the report_id from the session
        user = os.environ['API_USER']
        password = os.environ['API_PASS']

        payload = '{"auth": {"username" : "%s","password" : "%s"}}' % (user, password)
        response = requests.post("https://api.appnexus.com/auth", data=payload)

        authcookies = response.cookies

        report_download_url = "https://api.appnexus.com/report-download?id=" + report_id
        print(report_download_url)
        report_response = requests.request("GET", report_download_url, cookies=authcookies)

        if report_response.status_code == 200:
            session['report_data'] = report_response.text
        else:
            session['report_data'] = 'Failed to fetch the report'
    except Exception as e:
        session['report_data'] = 'Failed to fetch the report'
    
@app.route('/get-report-data', methods=['GET'])
def get_report_data():
    report_data = session.get('report_data')
    return jsonify({'report_data': report_data})

@app.route('/show-report', methods=['GET'])
def show_report():
    report_data = session.get('report_data')
    return render_template('report_created.html', report_response=report_data)
	
if __name__ == '__main__':
	app.run()
