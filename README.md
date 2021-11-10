# ESO

ESO is a Lithuanian grid operator. It offers a web self service to view and export energy usage stats: https://mano.eso.lt/consumption/history. However, it does not provide an API to export and use the data in third party tools.

# Usage

You may need to install Pyhton dependencies:

* bs4
* requests

Open the script and update it with your email, password and the property ID (objektas). The property ID can be found on the web export page: view html source and search for `option value="`

# Adjust

You can adjust the CSV output and add more fields or fields' order by directly editting the script
