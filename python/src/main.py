

import json
from flask import Flask, jsonify, request
from azure.identity import ManagedIdentityCredential
from azure.eventhub import EventHubProducerClient, EventData, EventDataBatch

app = Flask(__name__)


@app.route("/liveness")
def liveness():
    return "ok"

@app.route("/readiness")
def readiness():
    return "ok"

@app.route("/send", methods=["POST"])
def send():
    if request.json is None:
        raise Exception('no json body')
    send_to_eventhub('xiaoyan-eh.servicebus.windows.net', "9fd61a68-1faa-4bca-9a4e-8611b254d342", 'aml-py-test', request.json)
    return jsonify(request.json)

def send_to_eventhub(hostname, client_id, ehname, msg):
    credential = ManagedIdentityCredential(client_id=client_id)
    client = EventHubProducerClient(hostname, ehname, credential)
    batch = client.create_batch()
    batch.add(EventData(json.dumps(msg)))
    client.send_batch(batch)


