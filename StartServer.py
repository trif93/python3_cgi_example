import os, sys, threading, time
from http.server import HTTPServer, CGIHTTPRequestHandler

port = 81
webdir = '.'
if len(sys.argv) > 1:
	webdir = sys.argv[1]
if len(sys.argv) > 2:
	port = int(sys.argv[2])

def launcher():
	time.sleep(3)
	os.system("start http://localhost:{0}/cgi-bin/PyCGIExample.py".format(port))

def main():
	print('webdir "%s", port %s' % (webdir, port))
	os.chdir(webdir)

	threading.Thread(target=launcher).start()
	HTTPServer(('', port), CGIHTTPRequestHandler).serve_forever()

try:
	main()
except:
	print("bye")

