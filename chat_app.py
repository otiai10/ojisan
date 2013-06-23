# -*- coding: utf-8 -*-
import os, json, datetime, re
from geventwebsocket.handler import WebSocketHandler
from gevent import pywsgi, sleep

from mods.usher import Usher
from mods.asset import Asset
from mods.const import Const
from mods.message import Message

usher = Usher()
conf  = Const.get('conf')

def socket_by_socket(environ):
  key = environ['HTTP_SEC_WEBSOCKET_KEY']
  if usher.is_room_available():
    _nick_tmp = key[0:4]
    usher.add_member({'key':key,'socket':environ['wsgi.websocket'],'nickname':_nick_tmp})
  else:
    return False

  ws = usher.get_member_socket(key)
  print '>>>>>>>>>>> ENTER', usher.get_member_num()
  while 1:
    removed_list = set()
    msg = ws.receive()
    if msg is None:
      break
    for key, member in usher.find_all_members().iteritems():
      message = Message(member).handle(msg).generate()
      try:
        member['socket'].send(message)
      except Exception as e:
        print e.message
        removed_list.add(key)
    for k in removed_list:
      usher.remove_member(k)
  print '<<<<<<<<<< EXIT' , usher.get_member_num()

def myapp (environ, set_header):
  path = environ["PATH_INFO"]
  if path == '/':
    set_header('200 OK',[("Content-type","text/html")])
    return Asset('/view/index.html').get()
  elif path == '/chat':
    return socket_by_socket(environ)
  elif re.match('.*\.js', path) is not None:
    set_header('200 OK',[('Content-Type','text/javascript')])
    return Asset(path).apply({'host':conf['host'],'port':conf['port']}).get()
  elif re.match('.*\.css', path) is not None:
    set_header('200 OK',[('Content-Type','text/css')])
    return Asset(path).get()
  else:
    set_header('200 OK',[])
    return Asset(path).get()

server = pywsgi.WSGIServer((conf['host'], conf['port']), myapp, handler_class = WebSocketHandler)
server.serve_forever()
