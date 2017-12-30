"""fs command will return the CounterACT result for <command>"""
import re
from socket import inet_aton, inet_ntoa


import warnings; warnings.simplefilter('ignore')
from pyFS import pyFS

MAX_RESP = 15*1024
counterACT = pyFS('/app/limbo/plugins/fsconfig.yml')

## Supported Commands: 
## list hosts 
## list hosts <ip filter>
## list hosts prop <property> value <value> 

## list host properties <ip>
## list host fields <ip>  


def fslist(cmd):
	resp = ""

	match = re.findall(r"hosts prop (.*) value (.*)", cmd)
	if match:
		prop = match[0][0]
		val = match[0][1]
		resp += "Listing Hosts with %s = %s :\n" % (prop, val)
		_hosts = counterACT.gethostsByProp(prop, val)
		if _hosts:
			for host in _hosts:
				resp += "%s\n" % host[u'ip']
		return resp[:MAX_RESP]

	match = re.findall(r"hosts (.*)", cmd)
	if match:
		resp += "Listing filtered Hosts:\n"
		 # temp var (list) to generate sorted array of IP addresses filtered by given param
                resulting_ip_list = []
                counterACT.gethosts()
                for host in counterACT.hosts:
                        if host[u'ip'].find(str(match[0]))!= -1:
                                resulting_ip_list.append(host[u'ip'])
                # now convert IP addresses into binary straings and sort it, then convert it to readable IP addresses back and compose resulting string
                for host in map(inet_ntoa, sorted(map(inet_aton, resulting_ip_list))):
                        resp += "{0}\n".format(host)

                return resp[:MAX_RESP]


	match = re.findall(r"hosts(.*)", cmd)
	if match:
		resp += "Listing Hosts:\n"
		counterACT.gethosts()
		for host in counterACT.hosts:
			resp += "%s\n" % host[u'ip']
		return resp[:MAX_RESP]

	match = re.findall(r"host (.*) fields", cmd)
	if match:
		counterACT.gethosts()
		resp += "Listing Host fields of %s:\n" % str(match[0])
		resp+= match[0]
		hostID = counterACT.gethostIDbyIP(str(match[0]))
		
		res, dev = counterACT.gethostByID(hostID)
		if res: 
			devFields = counterACT.getEndPointFieldsNames(dev)
			for field in devFields: 
			        resp+= "%s\n" % field
		else: 
			resp += '\nHost Not Found!' 

		return resp[:MAX_RESP]

	match = re.findall(r"host (.*) properties", cmd)
	if match:
		counterACT.gethosts()
		resp += "Listing Host Properties of %s:\n" % str(match[0])
		#resp+= match[0]
		hostID = counterACT.gethostIDbyIP(str(match[0]))
		
		res, dev = counterACT.gethostByID(hostID)
		if res: 
			devFields = counterACT.getEndPointFieldsNames(dev)
			for field in devFields: 
			    if type(dev[u'fields'][field]) != type([]):
			        resp+= "%s : %s\n" %(field, dev[u'fields'][field]['value'] )
			    else: 
			        resp+= "%s:\n" % field 
			        for v in dev[u'fields'][field]:
			            resp+= "\t - %s\n" % v['value']
		else: 
			resp += '\nHost Not Found!' 

		return resp[:MAX_RESP]
	
	match = re.findall(r"host (.*) match (.*)", cmd)
	if match:
		counterACT.gethosts()
		resp += "Listing Host Properties of %s:\n" % str(match[0][0])
		#resp+= match[0][0]
		hostID = counterACT.gethostIDbyIP(str(match[0][0]))
		
		res, dev = counterACT.gethostByID(hostID)
		if res: 
			devFields = counterACT.getEndPointFieldsNames(dev)
			for field in devFields: 
				if field.find(match[0][1])!= -1:
				    if type(dev[u'fields'][field]) != type([]):
				        resp+= "%s : %s\n" %(field, dev[u'fields'][field]['value'] )
				    else: 
				        resp+= "%s:\n" % field 
				        for v in dev[u'fields'][field]:
				            resp+= "\t - %s\n" % v['value']
		else: 
			resp += '\nHost Not Found!' 

		return resp[:MAX_RESP]

	match = re.findall(r"policy (.*) rule (.*)", cmd)
	if match:
		resp += "Listing Hosts matching Policy / rule:\n" 
		counterACT.getpolicies()

		polId = counterACT.getPolicyId(match[0][0])
		rulesList = counterACT.getRules(polId)
		rule1 = counterACT.getRuleId(match[0][1], rulesList)
		results = counterACT.gethostsByRules([rule1])
		if results == None: 
			resp += '\nNo Hosts Found!' 
			return resp[:MAX_RESP]

		if len(results) >0: 
			resp += 'Found %s Hosts in Selected Rule.\n' % len(results)
			for res in results: 
				resp += '%s \n' % res[u'ip']
		else: 
			resp += '\nNo Hosts Found!' 

		return resp[:MAX_RESP]

		#for host in counterACT.hosts:
		#	resp += "%s\n" % host[u'ip']

	return resp[:MAX_RESP]
	 
# fs count hosts 
# fs count hostfields
# fs count policies 
def fscount(cmd):
	resp = "Reached count!"

	match = re.findall(r"hosts(.*)", cmd)
	if match:
		resp = "Count of Hosts: "
		counterACT.gethosts()
		resp += str(len(counterACT.hosts))
		return resp 

	match = re.findall(r"host (.*) fields", cmd)
	if match:
		resp = "Count of fields in host %s: " % match[0]
		counterACT.gethosts()
		hostID = counterACT.gethostIDbyIP(str(match[0]))
		
		res, dev = counterACT.gethostByID(hostID)
		if res: 
			devFields = counterACT.getEndPointFieldsNames(dev)
			resp += str(len(devFields))

		return resp 

	match = re.findall(r"hostfields(.*)", cmd)
	if match:
		resp = "Count of hostfields: "
		counterACT.getAllHostsFields()
		resp += str(len(counterACT.hostfields))
		return resp 
	
	match = re.findall(r"policies(.*)", cmd)
	if match:
		resp = "Count of Policies: "
		counterACT.getpolicies()
		resp += str(len(counterACT.policies))
		return resp 

	return resp

# fs find ip <ip>  
# fs find mac <mac> 
def fsfind(cmd):
	resp = "Host Not Found!"
	fields = ['sw', 'wifi', 'compliance_state']
	match = re.findall(r"ip (.*)", cmd)
	if match:
		resp = "Searching for IP: %s\n" % match[0]
		counterACT.gethosts()
		for host in counterACT.hosts:
			if host[u'ip'] == match[0]:
				resp += 'MAC: %s\n' % host[u'mac']
				hostID = counterACT.gethostIDbyIP(str(host[u'ip']))
				res, dev = counterACT.gethostByID(hostID)
				if res: 
					devFields = counterACT.getEndPointFieldsNames(dev)
					for field in devFields: 
						for ffield in fields:
							if field.find(ffield) != -1:
								if type(dev[u'fields'][field]) != type([]):
									resp+= "%s : %s\n" %(field, dev[u'fields'][field]['value'] )
								else:
									resp+= "%s:\n" % field 
									for v in dev[u'fields'][field]:
										resp+= "\t - %s\n" % v['value']  

		return resp 

	match = re.findall(r"mac (.*)", cmd)
	if match:
		resp = "Searching for MAC: %s\n" % match[0]
		counterACT.gethosts()
		for host in counterACT.hosts:
			if host[u'mac'] == match[0]:
				resp += 'IP: %s\n' % host[u'ip']
				hostID = counterACT.gethostIDbyIP(str(host[u'ip']))
				res, dev = counterACT.gethostByID(hostID)
				if res: 
					devFields = counterACT.getEndPointFieldsNames(dev)
					for field in devFields: 
						for ffield in fields:
							if field.find(ffield) != -1:
								if type(dev[u'fields'][field]) != type([]):
									resp+= "%s : %s\n" %(field, dev[u'fields'][field]['value'] )
								else: 
									resp+= "%s:\n" % field 
									for v in dev[u'fields'][field]:
										resp+= "\t - %s\n" % v['value'] 

		return resp 

	return resp

def fsupdate(cmd):
	"""POST Data via DEX Web-Services"""

	match = re.findall(r"host (.*) property (.*) value (.*)", cmd) 
	if match: 
		res, resp = counterACT.postDEX(counterACT.DEXAuth, match[0][0], match[0][1], match[0][2] )
		if res:  
			return  "Success!\n" + resp
		else: 
			return  "Failure!\n" + resp

	return "Can't understand your update command!"

def fsdelete(cmd):
	"""Deletes a Property Data via DEX Web-Services"""

	match = re.findall(r"host (.*) property (.*)", cmd) 
	if match: 
		res, resp = counterACT.deleteDEX(counterACT.DEXAuth, match[0][0], match[0][1])
		if res:  
			return  "Success!\n" + resp
		else: 
			return  "Failure!\n" + resp

	return "Can't understand your update command!"

def fshelp(cmd):

	_help = """
	fs bot Usage: 
	
	fs find ip <ip>  
	fs find mac <mac> 

	fs list hosts 				  
	fs list hosts <filter>
	fs list hosts prop <property> value <value> 

	fs list host <ip> properties 	 
	fs list host <ip> match <pattern>  
	fs list host <ip> fields 	
	fs list policy <policy-match> rule <rule-match> 
	
	fs count hosts 
	fs count host <ip> fields
	fs count hostfields
	fs count policies  

	fs update host <ip> property <prop_name> value <new_value> 
	fs delete host <ip> property <prop_name> 
	
	fs help 
	"""
	return _help 

def fs(cmd):

	match = re.findall(r"list (.*)", cmd)
	if match: 
		return fslist(match[0])[:MAX_RESP]

	match = re.findall(r"find (.*)", cmd)
	if match: 
		return fsfind(match[0])[:MAX_RESP]

	match = re.findall(r"count (.*)", cmd)
	if match: 
		return fscount(match[0])

	match = re.findall(r"update (.*)", cmd)
	if match: 
		return fsupdate(match[0])

	match = re.findall(r"delete (.*)", cmd)
	if match: 
		return fsdelete(match[0])

	match = re.findall(r"help(.*)", cmd)
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
