"""fs command will return the CounterACT result for <command>"""
import re
from pyFS import pyFS

ca = pyFS('fsconfig.yml')


## Supported Commands: 
## list hosts 
## list host <ip>  
def fslist(cmd):
	pass 

def fscount(cmd):
	pass

def fshelp(cmd):

	_help = """
	fs bot Usage: 
	fs list hosts # Lists all Hosts IPs 
	fs list host <ip> # List Properties of a certain host
	fs count hosts 
	fs count hostfields
	fs count policies  
	fs help 
	"""
	return _help 

def fs(cmd):

	match = re.findall(r"list (.*)", cmd)
	if match: 
		return fslist(match[0])

	match = re.findall(r"count (.*)", cmd)
	if match: 
		return fscount(match[0])

	match = re.findall(r"help (.*)", cmd)
	if match: 
		return fshelp(match[0])

	answer = "Cannot understand command: %s" %cmd
	return answer

def on_message(msg, server):
    text = msg.get("text", "")
    match = re.findall(r"fs (.*)", text)
    if not match:
        return

    return fs(match[0])
