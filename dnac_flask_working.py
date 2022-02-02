import requests
from flask import Flask, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
#from flask_marshmallow import Marshmallow
from datetime import datetime
# Init app
app = Flask(__name__)

def get_token():
    token_path = "https://sandboxdnac.cisco.com/dna" #URL
    auth = ("devnetuser","Cisco123!") #Login credentials
    headers = {"Content-Type": "application/json"} #Header type

    auth_resp = requests.post( #request library POST
    f"{token_path}/system/api/v1/auth/token", auth=auth, headers=headers
    )

    auth_resp.raise_for_status() #Prints error if auth failure 
    token = auth_resp.json()["Token"] #Retrieve the token
    # print("Token Retrieved: {}".format(token))
    return token #Creates a return statement for later use
    


def devlist():
    token = get_token() 
    api_path = "https://sandboxdnac.cisco.com/dna" 
    headers = {"Content-Type": "application/json", "X-Auth-Token": token} 

    #Note the different URL from our last program. This is going to network-device
    get_resp = requests.get(
    f"{api_path}/intent/api/v1/network-device", headers=headers 
    )

    # This is to print out the same large JSON dump as our curl command
    # import json; print(json.dumps(get_resp.json(), indent=2))

    #This is a loop on just printing the device ID and IP address
    if get_resp.ok:
        # for device in get_resp.json()["response"]:
        #     print(f" ID: {device['id']} IP: {device['managementIpAddress']}")
        return get_resp.json()["response"]
    else:
        print(f"Device collection failed with code {get_resp.status_code}")
        print(f"Failure body: {get_resp.text}")

# devices = devlist()
# for device in devices:
#     print ("##############")
#     print (device['id'])
#     print (device['managementIpAddress'])

#App Routes
#The first route is the index route which is required. Best practive is to limit methods to those supported.
# Typical function show with a post method for form, otherise a default listing of all db entries
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

#This route links to the first python action, things to populate your DB or manipulate it's fields
@app.route('/action', methods=['POST'])
def action():
    devices = devlist()
    table_data = []
    for device in devices:
        table_row = { "id": device['id'], "ip": device['managementIpAddress']}
        table_data.append(table_row)
    return render_template('action.html', data=table_data) 

@app.route('/ip_filter_action', methods=['POST'])
def ip_action():
    device = request.form['device']
    devices = devlist()
    table_data = []
    for d in devices:
        table_row = { "id": d['id'], "ip": d['managementIpAddress']}
        if table_row['ip'] == device:
            table_data.append(table_row)
    return render_template('action.html', data=table_data) 

@app.route('/name_filter_action', methods=['POST'])
def name_action():
    device = str(request.form['device'])
    devices = devlist()
    table_data = []
    for d in devices:
        table_row = { "id": d['id'], "ip": d['managementIpAddress']}
        if device in str(table_row['id']):
            table_data.append(table_row)
    return render_template('action.html', data=table_data) 

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000)