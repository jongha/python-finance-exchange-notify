#!/usr/bin/env python

import smtplib
from smtplib import SMTP as SMTP
import datetime
from email.mime.text import MIMEText
from email.header import Header
import json, requests

class Notify(object):
  username = None
  password = None

  API_URL = 'http://finance.yahoo.com/webservice/v1/symbols/allcurrencies/quote?format=json'
  FILTERS = ['USD/KRW', 'USD/EUR', 'USD/VND', 'USD/CYN', 'USD/JPY']

  def __init__(self, username, password):
    self.username = username
    self.password = password

  def _getMessage(self):
    resp = requests.get(url=self.API_URL)
    data = json.loads(resp.text)

    for resource in data['list']['resources']:
      fields = resource['resource']['fields']

      if fields['name'] in self.FILTERS:
        print fields['name'], fields['price'], fields['utctime']

    message = 'test'
    subject = 'subject'

    msg = MIMEText(message, "html", "UTF-8")
    msg["Subject"] =  Header(subject.encode('utf-8'), 'UTF-8').encode()

    return msg

  def sendmail(self):
    msg = self._getMessage()
    conn = SMTP(host='smtp.works.naver.com', port=587)
    conn.set_debuglevel(False)

    if self.username and self.password:
      conn.login(self.username, self.password)

    try:
        conn.sendmail('admin@tellustech.co.kr', 'jongha.estsoft@gmail.com', msg.as_string())
    finally:
        conn.close()

    print 'mail sending...'