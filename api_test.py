import requests
import json


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

def devdetail():
    token = get_token() 
    api_path = ("https://sandboxdnac.cisco.com/dna/intent/api/v1/network-device/")
    headers = {"Content-Type": "application/json", "X-Auth-Token": token}
    r = requests.get(api_path, headers=headers)
    rd = dict(r.json()["response"])
    # json_object = json.loads(r.text)
    # json_formatted_str = json.dumps(json_object, indent=2)
    # print(json_formatted_str)
    #print (r.json()["response"])
    #for line in r.json()["response"]:
    print (type(rd))
    for x in rd:
        print (x , ":", rd[x])
    #     print (key, value)
    return r.json()["response"]


devdetail("f0cb8464-1ce7-4afe-9c0d-a4b0cc5ee84c")
