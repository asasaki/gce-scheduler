import logging
import os

from flask import Flask
from google.appengine.api import app_identity
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials

project = os.environ['PROJECT']
label_key = os.environ['LABEL_KEY']
label_value = os.environ['LABEL_VALUE']

credentials = GoogleCredentials.get_application_default()
compute = discovery.build(
    'compute', 'v1',
    credentials=credentials,
    cache_discovery=False
)

app = Flask(__name__)

def get_instances():
    instances = []

    result = compute.instances().aggregatedList(
        project=project,
        filter='labels.{key} eq {value}'.format(
            key=label_key,
            value=label_value
        )
    ).execute()

    for zone in result.get('items', {}).values():
        for instance in zone.get('instances', []):
            instances.append(
                {
                    "project": project,
                    "zone": instance['zone'].rsplit('/', 1)[-1],
                    "name": instance['name']
                }
            )
    return instances

@app.route('/start_instances')
def start_instances():
    for instance in get_instances():
        response = compute.instances().start(
            project=instance['project'],
            zone=instance['zone'],
            instance=instance['name']
        ).execute()
        logging.info(response)
    return ''

@app.route('/stop_instances')
def stop_instances():
    for instance in get_instances():
        response = compute.instances().stop(
            project=instance['project'],
            zone=instance['zone'],
            instance=instance['name']
        ).execute()
        logging.info(response)
    return ''
