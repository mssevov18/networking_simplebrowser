#!/usr/bin/env python3

from http.connection_helper import *

con_helper = HttpConnectionHelper()
con_helper.connect("127.0.0.1", 8000, False)
con_helper.send_request("GET /example HTTP/1.1\r\nHost: 127.0.0.1:8000\r\n\r\n")
response = con_helper.receive_response()
print(response)
