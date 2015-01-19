 #!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib2
import json
import os
import sys
import logging
import traceback

def log_except_hook(*exc_info):
  logging.exception("".join(traceback.format_exception(*exc_info)))

def vote(amount):
  settings = []
  with open("settings.json") as json_file:
    settings = json.load(json_file)

  data = {
    'target':settings['id'],
    'action':'rigadevday',
    'amount':amount,
    'comment':''
  }

  logging.debug(data)

  req = urllib2.Request('http://dmi3.net/plusminus/')
  req.add_header('Content-Type', 'application/json')
  urllib2.urlopen(req, json.dumps(data))

logging.basicConfig(filename=os.path.dirname(os.path.realpath(__file__))+'/log.log', 
  level=logging.DEBUG, 
  format='%(asctime)s %(levelname)s %(message)s')
sys.excepthook = log_except_hook
