#import threading
#import sys
#import easysnmp
from easysnmp import *
from easysnmp import easysnmp


def poll():
    session=easysnmp.Session(hostname='10.128.13.52',community='public',version=2,local_port=161)
    output=session.get('1.3.6.1.4.1.5835.5.2.100.1.9.1.0')
    print(output)
poll()

