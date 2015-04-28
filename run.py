#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import codecs
import re
import HTMLParser

from notify.notify import Notify

template = '''
<table style="border: 1px solid black; border-collapse: collapse;">
  <thead>
		<tr>
			<th rowspan="2" style="border: 1px solid black">날짜</th>
			<th rowspan="2" style="border: 1px solid black">통화명</th>
			<th rowspan="2" style="border: 1px solid black">매매기준표</th>
			<th colspan="2" style="border: 1px solid black">송금전신환</th>
		</tr>
		<tr>
			<th style="border: 1px solid black">보내실 때</th>
			<th style="border: 1px solid black">받으실 때</th>
		</tr>
  </thead>

	<tbody>
		<tr>
			<td rowspan="5" style="border: 1px solid black">%s</td>
			<td style="border: 1px solid black">%s</td>
			<td style="border: 1px solid black">%s</td>
			<td style="border: 1px solid black">%s</td>
			<td style="border: 1px solid black">%s</td>
		</tr>
		<tr>
			<td style="border: 1px solid black">%s</td>
			<td style="border: 1px solid black">%s</td>
			<td style="border: 1px solid black">%s</td>
			<td style="border: 1px solid black">%s</td>
		</tr>
		<tr>
			<td style="border: 1px solid black">%s</td>
			<td style="border: 1px solid black">%s</td>
			<td style="border: 1px solid black">%s</td>
			<td style="border: 1px solid black">%s</td>
		</tr>
		<tr>
			<td style="border: 1px solid black">%s</td>
			<td style="border: 1px solid black">%s</td>
			<td style="border: 1px solid black">%s</td>
			<td style="border: 1px solid black">%s</td>
		</tr>
		<tr>
			<td style="border: 1px solid black">%s</td>
			<td style="border: 1px solid black">%s</td>
			<td style="border: 1px solid black">%s</td>
			<td style="border: 1px solid black">%s</td>
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
        subject='Daily exchange rate info.',
        content=template % tuple(data),
        recipient='jongha.ahn@mrlatte.net'
        );
      exit(1)

  except:
      exit(0)

if __name__ == '__main__':
  run(sys.argv[1])