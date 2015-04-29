#!/usr/bin/env python
# -*- coding: utf-8 -*-

import smtplib
from smtplib import SMTP as SMTP
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

import json, requests

class Notify(object):
  username = None
  password = None
  server = None
  port = None

  def __init__(self, username, password, server, port=587):
    self.username = username
    self.password = password
    self.server = server
    self.port = port

  def sendmail(self, subject='', content='', recipient=None):
    conn = SMTP(host=self.server, port=self.port)
    conn.set_debuglevel(False)

    if self.username and self.password:
      conn.login(self.username, self.password)

    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = self.username
    msg['To'] = recipient

    part1 = MIMEText(content, 'plain')
    part2 = MIMEText(content, 'html')
    msg.attach(part1)
    msg.attach(part2)

    try:
      conn.sendmail(self.username, recipient, msg.as_string())

    finally:
      conn.close()

    print 'Sending...'
