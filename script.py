"""Updates all Strava activities...for me."""
import certifi
import logging
import json
import urllib3

logging.basicConfig(level=logging.INFO)

ACCESS_TOKEN = 'THIS_IS_SECRET'
BASE_URL = 'https://www.strava.com/api/v3'


def get_activities(page, headers):
    """Return a page of up to 100 activities for the authenticated profile."""
    activities_resp = http.request(
        'GET',
        "{base}/athlete/activities?per_page=100&page={page}".format(base=BASE_URL, page=page),
        headers=headers
    )
    return json.loads(activities_resp.data.decode('utf-8'))


http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
headers = {'Authorization': 'Bearer ' + ACCESS_TOKEN}
page = 1
activities = get_activities(page=page, headers=headers)

while len(activities) > 0:
    logging.info("{n} activities in this page".format(n=len(activities)))
    for act in activities:
        if act['gear_id'] is not None:
            logging.debug("Activity {id} already has gear.".format(id=act['id']))
            continue

        if act['type'] == 'Run':
            gear_id = 'g3731534'  # Nike
        elif act['type'] == 'Ride':
            gear_id = 'b5289363'  # Schwinn
        else:
            continue

        resp = http.request(
            'PUT',
            "{base}/activities/{id}".format(id=act['id'], base=BASE_URL),
            headers=headers,
            fields={'gear_id': gear_id}
        )
        if resp.status == 200:
            logging.info("Updated {id}".format(id=act['id']))
        else:
            logging.warning("Error updating {id}".format(id=act['id']))

    page += 1
    logging.info("Starting page {page}".format(page=page))
    activities = get_activities(page=page, headers=headers)
