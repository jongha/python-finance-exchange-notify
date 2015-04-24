#!/usr/bin/env python
# -*- coding: utf-8 -*-

from notify.notify import Notify

try:
    n = Notify(
        username='',
        password='',
        server=''
        )

    n.sendmail('Daily exchange rate info.', '');
    exit(1)

except:
    exit(0)
