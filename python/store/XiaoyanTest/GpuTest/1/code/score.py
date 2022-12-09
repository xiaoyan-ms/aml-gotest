
from contextlib import contextmanager
from io import StringIO
import sys
import traceback


def init():
    pass

def run(data):
    return execute_python_code(data)
    

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
