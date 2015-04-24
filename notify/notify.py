#!/usr/bin/env python
# -*- coding: utf-8 -*-

import smtplib
from smtplib import SMTP as SMTP
import datetime
from email.mime.text import MIMEText
from email.header import Header
import json, requests

class Notify(object):
  username = None
  password = None
  server = None
  port = 587

  API_URL = 'http://finance.yahoo.com/webservice/v1/symbols/allcurrencies/quote?format=json'
  FILTERS = ['USD/KRW', 'USD/EUR', 'USD/VND', 'USD/CYN', 'USD/JPY']

  def __init__(self, username, password, server, port=587):
    self.username = username
    self.password = password
    self.server = server
    self.port = port

  def _getMessage(self, subject):
    resp = requests.get(url=self.API_URL)
    data = json.loads(resp.text)
    message = ''

    for resource in data['list']['resources']:
      fields = resource['resource']['fields']

      if fields['name'] in self.FILTERS:
        print fields['name'], fields['price'], fields['utctime']
        message += fields['name'] + ', ' + fields['price'] + ', ' +fields['utctime'] + '<br />'
        
    msg = MIMEText(message, 'html', 'UTF-8')
    msg['Subject'] =  Header(subject, 'UTF-8').encode()
    msg['From'] = self.username
    
    return msg

  def sendmail(self, subject, recipient):
    msg = self._getMessage(subject)
    msg['To'] = recipient

    conn = SMTP(host=self.server, port=self.port)
    conn.set_debuglevel(False)

    if self.username and self.password:
      conn.login(self.username, self.password)

    try:
        conn.sendmail(self.username, recipient.split(','), msg.as_string())
    finally:
        conn.close()

    print 'Sending...'
