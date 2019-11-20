import base64

def encode(data):
    return str(base64.b64encode(data.encode()), 'utf-8')

def decode(data):
    return str(base64.b64decode(data), 'utf-8')