#!/bin/env python3

import requests
from bs4 import BeautifulSoup
import json
import datetime
from dateutil.rrule import rrule, DAILY

EMAIL = "YOUR_EMAIL_HERE"
PASS = "YOUR_PASSOWRD_HERE"
PROP = "OBJEKTAS_AKA_PROPERTY_ID"

# uncomment to fix SSLError(SSLError(1, '[SSL: DH_KEY_TOO_SMALL] dh key too small
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'

login = {"login_type":"1", "name":EMAIL, "pass":PASS, "form_id":"user_login_form"}

ses = requests.session()
res = ses.post("https://mano.eso.lt/", data=login, verify=True)
res = ses.get("https://mano.eso.lt/consumption", verify=True)

soup = BeautifulSoup(res.text, "html.parser")
csrf = soup.find('input', {'name':'form_token'})['value']

sd = datetime.date(2023, 1, 1)
ed = datetime.date.today()

# iterate through days in drupal
for dt in rrule(DAILY, dtstart=sd, until=ed):

	stamp  = dt.strftime("%Y-%m-%d")
	stamp2 = (dt + datetime.timedelta(days=1)).strftime("%Y-%m-%d")

	# POST body
	export = {"objects[]" : PROP,
			  "display_type" : "hourly",
			  "period" : "day",
			  "energy_type" : "general",
			  "active_date_value" : stamp +  " 00:00",
			  "next_button_value" : stamp2 + " 00:00",
			  "form_token" : csrf,
			  "form_id" : "eso_consumption_history_form",
			  "_triggering_element_name" : "op"}

	res = ses.post("https://mano.eso.lt/consumption?ajax_form=1&_wrapper_format=drupal_ajax", data=export, verify=False, proxies=proxies)

	# hackish way of parsing drupal's JSON response
	stats = {}
	data = json.loads(res.text)
	for d in data:
		if d["command"] == "settings":
			if "eso_consumption_history_form" in d["settings"]:
				for s in d["settings"]["eso_consumption_history_form"]["graphics_data"]["datasets"]:
					if s["key"] == "P+":
						stats = s["record"]
						break
		if stats != {}:
			break

	for stat in stats:
		print(stat["date"], ",", stat["value"])
