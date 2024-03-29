#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import codecs
import re
import HTMLParser
import time

from notify.notify import Notify

template = '''
<table style="border: 1px solid black; border-collapse: collapse;">
  <thead>
		<tr>
			<th rowspan="2" style="border: 1px solid black; padding: 10px;">조회일시</th>
			<th rowspan="2" style="border: 1px solid black; padding: 10px;">통화명</th>
			<th rowspan="2" style="border: 1px solid black; padding: 10px;">매매기준표</th>
			<th colspan="2" style="border: 1px solid black; padding: 10px;">송금전신환</th>
		</tr>
		<tr>
			<th style="border: 1px solid black; padding: 10px;">보내실 때</th>
			<th style="border: 1px solid black; padding: 10px;">받으실 때</th>
		</tr>
  </thead>

	<tbody>
		<tr>
			<td rowspan="5" style="border: 1px solid black; padding: 10px;">%s</td>
			<td style="border: 1px solid black; padding: 10px;">%s</td>
			<td style="border: 1px solid black; padding: 10px;">%s</td>
			<td style="border: 1px solid black; padding: 10px;">%s</td>
			<td style="border: 1px solid black; padding: 10px;">%s</td>
		</tr>
		<tr>
			<td style="border: 1px solid black; padding: 10px;">%s</td>
			<td style="border: 1px solid black; padding: 10px;">%s</td>
			<td style="border: 1px solid black; padding: 10px;">%s</td>
			<td style="border: 1px solid black; padding: 10px;">%s</td>
		</tr>
		<tr>
			<td style="border: 1px solid black; padding: 10px;">%s</td>
			<td style="border: 1px solid black; padding: 10px;">%s</td>
			<td style="border: 1px solid black; padding: 10px;">%s</td>
			<td style="border: 1px solid black; padding: 10px;">%s</td>
		</tr>
		<tr>
			<td style="border: 1px solid black; padding: 10px;">%s</td>
			<td style="border: 1px solid black; padding: 10px;">%s</td>
			<td style="border: 1px solid black; padding: 10px;">%s</td>
			<td style="border: 1px solid black; padding: 10px;">%s</td>
		</tr>
		<tr>
			<td style="border: 1px solid black; padding: 10px;">%s</td>
			<td style="border: 1px solid black; padding: 10px;">%s</td>
			<td style="border: 1px solid black; padding: 10px;">%s</td>
			<td style="border: 1px solid black; padding: 10px;">%s</td>
		</tr>
	</tbody>
</table>
'''

def run(file):
  lines = []
  result = None
  htmlParser = HTMLParser.HTMLParser()

  if file:
    with open(file, 'r') as fp:
      for line in fp:
        lines.append(line.rstrip())

      result = ''.join(lines)

  m = re.search('<div class=\'date\'><p>(.*?)<\/p>(.*?)<\/div>',
    result,
    flags=re.MULTILINE|re.UNICODE|re.IGNORECASE
    )

  data = []
  data.append(htmlParser.unescape(m.group(1)).encode('utf-8'))
  for currency in ['usd', 'eur', 'jpy', 'cny', 'vnd']:
    exchange = re.findall('<td class=\'nation\'><img src=\'http://community.fxkeb.com/fxportal/web/img/co/%s.gif\' alt=\'\' />(.*?)<\/td><td class=\'buy\'>(.*?)</td><td class=\'sell\'>(.*?)<\/td>' % (currency),
      result,
      flags=re.MULTILINE|re.UNICODE|re.IGNORECASE|re.DOTALL
      )

    data.append(htmlParser.unescape(exchange[0][0]).encode('utf-8'))
    data.append(exchange[1][1].encode('utf-8'))
    data.append(exchange[0][1].encode('utf-8'))
    data.append(exchange[0][2].encode('utf-8'))

  try:
    n = Notify(
      username='',
      password='',
      server='smtp.works.naver.com'
      )

    n.sendmail(
      subject=time.strftime('[Daily] %Y년 %m월 %d일 환율입니다.'),
      content=template % tuple(data),
      recipient='jongha.ahn@mrlatte.net'
      )

    exit(1)

  except:
    exit(0)

if __name__ == '__main__':
  if len(sys.argv) > 1:
    run(sys.argv[1])
