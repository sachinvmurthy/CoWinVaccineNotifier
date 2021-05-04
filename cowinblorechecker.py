import time
import requests
import datetime
import json
import smtplib


s = smtplib.SMTP('smtp.gmail.com', 587)
s.starttls()
s.login("sender_email", "pass")
#Karnataka
#Please see distric_id in reademe 
DIST_ID = 16
age = 18
# Print details flag
print_flag = 'Y'
numdays = 3
base = datetime.datetime.today()
date_list = [base + datetime.timedelta(days=x) for x in range(numdays)]
date_str = [x.strftime("%d-%m-%Y") for x in date_list]
while (True):
    print("TIME : ", datetime.datetime.now())
    for INP_DATE in date_str:
        URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={}&date={}".format(
            DIST_ID, INP_DATE)
        response = requests.get(URL)
        if response.ok:
            resp_json = response.json()
            # print(json.dumps(resp_json, indent = 1))
            flag = False
            if resp_json["centers"]:
                if (print_flag == 'y' or print_flag == 'Y'):
                    for center in resp_json["centers"]:
                        for session in center["sessions"]:
                            if session["min_age_limit"] <= age and session["available_capacity"] > 0:
                                print("Available on: {}".format(INP_DATE))
                                print("\t", center["name"])
                                print("\t", center["block_name"])
                                print("\t Price: ", center["fee_type"])
                                print("\t Available Capacity: ", session["available_capacity"])
                                message = "Center " + center["name"] + " Block Name " + center[
                                    "block_name"] + " Fees: " + center["fee_type"] + " Slots Available: " + session[
                                              "available_capacity"]
                                s.sendmail("sender_email", "to_email", message)
                                if (session["vaccine"] != ''):
                                    print("\t Vaccine: ", session["vaccine"])
                                print("\n\n")
                            else:
                                print("No available slots on {}".format(INP_DATE))
                                break
            else:
                print("No available slots on {}".format(INP_DATE))
    time.sleep(1800)
