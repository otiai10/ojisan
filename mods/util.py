import json

# this module must be called as static
def jsonstr2dict(jsn_str):
  return json.loads(jsn_str)

def dict2jsonstr(dictionary):
  return json.dumps(dictionary)
