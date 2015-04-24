#!/usr/bin/env python

from notify.notify import Notify

try:
    n = Notify(
        username='',
        password=''
        )

    n.sendmail();
    exit(1)

except:
    exit(0)
