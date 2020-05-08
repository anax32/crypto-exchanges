import json

import websocket

class WebSocketSubscriber:
  def __init__(self, name, uri, subscription_params, parse_fn=None):
    """ create the subscription
       name: identififer
       uri: websocket location
       subscription_params: dictionary to pass on subscribe
    """
    self.name = name
    self.uri = uri
    self.subscription_params = subscription_params
    self.conn = None

    if parse_fn is None:
      self.parse_fn = json.loads
    else:
      self.parse_fn = parse_fn


  def open(self):
    #print(json.dumps(subscribe))
    self.conn = websocket.create_connection(self.uri)
    subscription_string = json.dumps(self.subscription_params)
    self.conn.send(subscription_string)


  def close(self):
    if self.conn is not None:
      self.conn.close()
      self.conn = None


  def __call__(self):
    if self.conn is None:
      self.open()
      return {"exchange": self.name, "error": "create_connection()"}

    try:
      out = self.conn.recv()
    except ConnectionResetError:
      return {"exchange": self.name, "error": "ConnectionResetError"}
    except websocket.WebSocketConnectionClosedException:
      self.conn = None
      return {"exchange": self.name, "error": "websocket.WebSocketConnectionClosedException"}
    except BrokenPipeError:
      self.conn = None
      return {"exchange": self.name, "error": "BrokenPipeError"}

    try:
      D = self.parse_fn(out)
    except json.decoder.JSONDecodeError:
      return {"exchange": self.name, "error": "json.decoder.JSONDecodeError", "text": str(out)}

    D.update({"exchange": self.name})

    return D
