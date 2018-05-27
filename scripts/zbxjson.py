import urllib.request, urllib.parse, urllib.error, urllib.request, urllib.error, urllib.parse
import sys
import json
from docopt import docopt
import codecs
#   from ntlm import HTTPNtlmAuthHandler

# Get element from JSON path
def xpath_get(mydict, path):
  elem = mydict
  try:
    for x in path.strip("/").split("/"):
      try:
        x = int(x)
        elem = elem[x]
      except ValueError:
        elem = elem.get(x)
  except:
    pass

  return elem

def main():

  usage="""
  
Usage:
  zbxjson -u <url> -p <path> [-U <username>] [-P <password>] [-m <GET|POST>] [-d <data>] [-a <basic|ntlm>]
  
Options:
  -u, --url <url>                       The URL to the web service endpoint
  -p, --path <path>                     The path to the JSON element to get. Expects /element1, /array1 or /array1/2/element3...
  -U, --username <username>             The username if authentication is required
  -P, --password <password>             The password if authentication is required
  -m, --method <GET|POST>               The HTTP method to use (GET|POST). [default: get]
  -d, --data <data>                     The POST data to send, if required. Expects --data "key1=value1,key2=value2,..."
  -a, --authentication <basic|ntlm>     The authentication method to use (basic, ntml) [default: ntlm]
"""
  args = docopt(usage, version="0.1")
 
  # Set authentication if required
  if args["--authentication"]:
    authinfo = urllib.request.HTTPPasswordMgrWithDefaultRealm()
    authinfo.add_password(None, args["--url"], args["--username"], args["--password"])
    
    if args["--authentication"] == "basic":
      auth = urllib.request.HTTPBasicAuthHandler(authinfo)   
    #elif args["--authentication"] == "ntlm":
    #  auth = HTTPNtlmAuthHandler.HTTPNtlmAuthHandler(authinfo)
      
    opener = urllib.request.build_opener(auth)
    urllib.request.install_opener(opener)
  
  # Handle POST data
  if args["--data"]:
    data = urllib.parse.urlencode(dict([arg.split('=') for arg in args["--data"].split(',')])).encode("utf-8")
  else:
    data = "None"
  
  # Create HTTP request
  req = urllib.request.Request(args["--url"], data = data.encode("utf-8"))
  req.add_header('User-Agent', 'Zabbix Monitoring')
  req.add_header('Content-Type', 'application/json' )
  
  # Handle the HTTP method
  if args["--method"]:
    method = args["--method"]  
    req.get_method = lambda: method


  try:
    connection = opener.open(req)
  except urllib.error.HTTPError as e:
    print(e)
    sys.exit(1)
  except urllib.error.URLError as e:
    print(e)
    sys.exit(1)

  # Exit if the HTTP response code != 200
  if connection.code != 200:
    print("HTTP response code is %d" % connection.code)
    sys.exit(1)

  # Load the response as a JSON object   
  try:
    reader = codecs.getreader("utf-8")
    obj = json.load(reader(connection))
  except:
    print("Cannot extract the JSON response")
    sys.exit(1)

  # Get the element referenced by the specified path
  element = xpath_get(obj, args["--path"])
  
  if isinstance(element, str) or isinstance(element, bool): # the element is a unicode string
    print(element)
  elif isinstance(element, list): # the element is an array
    output = []
    # format it as an LLD JSON object
    for index, item in enumerate(element, start=0):
      props = { "{#JSON%s}" % k.upper(): v  for k, v in list(item.items()) }
      props["{#JSONPATH}"] = "%s/%d" % (args["--path"], index)
      output.append(dict(props))
    print(json.dumps({ 'data': output}, indent=2))
  elif isinstance(element, dict): # the element is dictionary
    # format it as an LLD JSON object  
    props = { "{#JSON%s}" % k.upper(): v  for k, v in list(element.items()) }
    props["{#JSONPATH}"] = args["--path"]
    print(json.dumps({ 'data': props}, indent=2))

  sys.exit(0)

if __name__ == '__main__':
    main()