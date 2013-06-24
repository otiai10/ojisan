import json, datetime
from mods.handler import Handler
from mods.usher import Usher

class Message:

  def __init__(self, to_member):
    self.to_member = to_member

  def build(self, params):
    is_me = False
    if params['sender'] is not None:
      if params['sender']['key'] == self.to_member['key']:
        is_me = True
    response = {
      'content' : params['content'],
      'sender'  : {
        'nickname' : params['sender']['nickname'],
        'is_me'    : is_me
      },
      'timestamp' : str(datetime.datetime.now()),
      'request'   : params['request'],
    }
    #return json.dumps(response, ensure_ascii=False)
    return json.dumps(response)

  @classmethod
  def handle(self, msg, key=None):
    msg = msg.encode('utf-8')
    _orig = json.loads(msg)
    if key is not None:
      _orig['socket_key'] = key
    result = Handler(_orig).execute()
    return result

