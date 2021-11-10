#!/bin/env python3

import requests
from bs4 import BeautifulSoup
from zipfile import ZipFile
import io
import csv

EMAIL = "YOUR_EMAIL_HERE"
PASS = "YOUR_PASSOWRD_HERE"
PROP = "OBJEKTAS_AKA_PROPERTY_ID"

# uncomment to fix SSLError(SSLError(1, '[SSL: DH_KEY_TOO_SMALL] dh key too small
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'

login = {"login_type":"1", "name":EMAIL, "pass":PASS, "form_id":"user_login_form"}

ses = requests.session()
res = ses.post("https://mano.eso.lt/", data=login, verify=True)
res = ses.get("https://mano.eso.lt/consumption/history", verify=True)

soup = BeautifulSoup(res.text, "html.parser")
csrf = soup.find('input', {'name':'form_token'})['value']

download = {"period":"3", "display_type":"H", "objects_H":PROP, "objects_S":"", "form_token":csrf, "form_id":"eso_consumption_history_export_form"}
res = ses.post("https://mano.eso.lt/consumption/history", data=download, verify=True)

z = ZipFile(io.BytesIO(res.content))
for f in z.namelist():
	data = z.open(f, "r")
	lines = csv.reader(io.TextIOWrapper(data, "latin-1"), delimiter=';')
	for row in lines:
		# adjust this line to change fields order or format
		print(row[12].strip() + ";" + row[14].strip())

