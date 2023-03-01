# UPDATE 2023-03-01

Due to the bug in ESO API, ZIP cannot be exported for those who replace smart electric meter recently.
In that case the export will only show old numbers prior to the change.
I have contacted ESO and they said everything is broken and they cannot fix it at the moment.
Because of that the script has been updated to use a hackish way of exporting through the Drupal JSON.

# ESO

ESO is a Lithuanian grid operator. It offers a web self service to view and export energy usage stats: https://mano.eso.lt/consumption/history. However, it does not provide an API to export and use the data in third party tools.

# Usage

You may need to install Python dependencies:

* bs4
* requests

Open the script and update it with your email, password and the property ID (objektas). The property ID can be found on the web export page: view html source and search for `option value="`

# Adjust

You can adjust the start date of the export directly in the script, default is 2023-01-01.

