

import json
import os
from flask import Flask, jsonify, request
from azure.identity import ManagedIdentityCredential
from azure.eventhub import EventHubProducerClient, EventData, EventDataBatch
from pyraisdk import rlog

rlog.initialize(eh_structured='struct', eh_unstructured='unstruct', eh_hostname='xiaoyan-eh.servicebus.windows.net', client_id='9fd61a68-1faa-4bca-9a4e-8611b254d342')
app = Flask(__name__)


@app.route("/liveness")
def liveness():
    return "ok"

@app.route("/readiness")
def readiness():
    return "ok"

@app.route("/score")
def score():
    msg = request.args.get('msg')
    rlog.infof(msg)
    return msg

