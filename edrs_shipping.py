import requests
import json
import platform
import subprocess
import os
from fabric import Connection
from dotenv import load_dotenv
load_dotenv()

"""
* get data from Xi
* @params url
* return dict
"""
def get_xi_data(url):
    response = requests.get(url)
    data = json.loads(response.text)
    data = data[0]['fields']
    return data

"""
* sends SMS alerts
* @params url, params
* return dict
"""
def alert(url, params):
    headers = {'Content-type': 'application/json; charset=utf-8'}
    r = requests.post(url, json=params, headers=headers)
    return r

recipients = ["+265998006237", "+265991450316", "+265995246144", "+265992182669", "+265995532195", "+265884642428", "+265991852093"]

cluster = get_xi_data('http://10.44.0.52/sites/api/v1/get_single_cluster/29')

for site_id in cluster['site']:
    site = get_xi_data('http://10.44.0.52/sites/api/v1/get_single_site/' + str(site_id))

    # functionality for ping re-tries
    count = 0

    while (count < 3):

        # lets check if the site is available
        param = '-n' if platform.system().lower()=='windows' else '-c'

        if subprocess.call(['ping', param, '1', site['ip_address']]) == 0:

            # pushing edrs application
            push_edrs = "rsync " + "-r $WORKSPACE/edrs_facility " + site['username'] + "@" + site['ip_address'] + ":/var/www/"
            os.system(push_edrs)

            # Pushing edrs_setup script
            push_edrs_setup_script = "rsync " + "-r $WORKSPACE/edrs_setup.sh " + site['username'] + "@" + site['ip_address'] + ":/var/www/edrs_facility/"
            os.system(push_edrs_setup_script)

            # setting up edrs application
            run_edrs_setup_script = "ssh " + site['username'] + "@" + site['ip_address'] + " 'cd / && ./edrs_setup.sh'"
            os.system(run_edrs_setup_script)

            #result = Connection("" + site['username'] + "@" + site['ip_address'] + "").run('cd /var/www/BHT-EMR-API && git describe', hide=True)

            msg = "{0.stdout}"

            version = msg.format(result).strip()

            #api_version = "v4.11.11"

            #if api_version == version:
                #msgx = "Hi there,\n\nDeployment of API to " + version + " for " + site['name'] + " completed succesfully.\n\nThanks!\nEGPAF HIS."
            #else:
                #msgx = "Hi there,\n\nSomething went wrong while checking out to the latest API version. Current version is " + version + " for " + site['name'] + ".\n\nThanks!\nEGPAF HIS."

            # send sms alert
            for recipient in recipients:
                msg = "Hi there,\n\nDeployment of eDRS facility for " + site['name'] + " completed succesfully.\n\nThanks!\nEGPAF HIS."
                params = {
                    "api_key": os.getenv('API_KEY'),
                    "recipient": recipient,
                    "message": msgx
                }
                alert("http://sms-api.hismalawi.org/v1/sms/send", params)

            # close the while loop
            count = 3

        else:
            # increment the count
            count = count + 1

            # make sure we are sending the alert at the last pint attempt
            if count == 3:
                for recipient in recipients:

                    msg = "Hi there,\n\nDeployment of eDRS facility for " + site['name'] + " failed to complete after several connection attempts.\n\nThanks!\nEGPAF HIS."
                    params = {
                        "api_key": os.getenv('API_KEY'),
                        "recipient": recipient,
                        "message": msg
                    }
                    alert("http://sms-api.hismalawi.org/v1/sms/send", params)
