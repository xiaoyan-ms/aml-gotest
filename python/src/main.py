

from contextlib import contextmanager
from io import StringIO
import json
import os
import sys
import traceback
from flask import Flask, jsonify, request
from azure.identity import ManagedIdentityCredential
from azure.eventhub import EventHubProducerClient, EventData, EventDataBatch
from pyraisdk import rlog

#rlog.initialize(eh_structured='struct', eh_unstructured='unstruct', eh_hostname='xiaoyan-eh.servicebus.windows.net', client_id='9fd61a68-1faa-4bca-9a4e-8611b254d342')
app = Flask(__name__)


@app.route("/liveness")
def liveness():
    return "ok"

@app.route("/readiness")
def readiness():
    return "ok"

@app.route("/execute", methods=['POST'])
def execute():
    code = request.data
    return execute_python_code(code)


@contextmanager
def RedirectIO(stream):
    stdout, sys.stdout = sys.stdout, stream
    stderr, sys.stderr = sys.stderr, stream
    try:
        yield
    finally:
        sys.stdout = stdout
        sys.stderr = stderr
        

def execute_python_code(code: str) -> str:
    buff = StringIO()
    with RedirectIO(buff):
        try:
            exec(code)
        except:
            traceback.print_exc()
    return buff.getvalue()
