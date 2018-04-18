import paramiko
import time
# import sys
import os
import ConfigParser
import argparse
import re

argParser = argparse.ArgumentParser(description="Automation tool to reload dns files",epilog="further information: gopal_007gautam@hotmail.com")
argParser.add_argument("-w","--view",default="internal,external",help="Comma Separated names of dns view zone")
argParser.add_argument("-s","--server",default="ns1,ns2",help="Comma Separated names of dns server")
argParser.add_argument("-v","--verbose",action="store_true",help="View the verbose output")
argParser.add_argument("host",help="host to update in DNS Server")
argParser.add_argument("--debug",action="store_true",help="debug the whole operation")
argParser.add_argument("-t","--type",choices=['reverse','forward'],default='reverse',help="Type of dns record forward|reverse")
argParser.add_argument("--no-dig-operation",action="store_true",help="specify this option if you dont want to execute dig command after dns reload")
args = argParser.parse_args()

availableServers = ['ns1','ns2']
availableViews = ['internal','external']

dnsType = args.type
viewZone = args.view
dnsServers = args.server
host = args.host

dnsServerList = dnsServers.split(',')
dnsViewZoneList = viewZone.split(',')

config = ConfigParser.RawConfigParser()
configFile = "autodnsreload.conf"
config.read(configFile)
user = config.get("serverauth","username")
passwd = config.get("serverauth","password")

slp = 5

#user = sys.argv[1]
#passwd = sys.argv[2]
#ip = sys.argv[1]
if args.verbose:
	print "list of server specified are: "
	print dnsServerList
	print "list of viewzone specified are: "
	print dnsViewZoneList

def dns_reload(server,viewzone,host,user,passwd,slp):
	if args.debug:
		print "Inside the module: dns_reload with parameters: {},{},{},{},{},{}".format(server,viewzone,host,user,passwd,slp)
	if dnsType == 'reverse':
		ip = host
		if not re.search('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}',ip):
			print "No ip-address is specified for reverse dns reload...Please specify correct one"
			exit(0)
		octets = ip.split(".")
		octets.reverse()
		rev_ip_str = ".".join(octets[1:4])

	ssh = paramiko.SSHClient()
	ssh.load_system_host_keys()
	try:
		ssh.connect(hostname=server,username=user,password=passwd)
	except BadHostKeyException:
		print "The servers host key could not be verified"
		exit(0)
	except AuthenticationException:
		print "Authentication Failed"
		exit(0)
	except SSHException:
		print "Error connecting or establishing an SSH session"
		exit(0)
	except socket.error:
		print "Socket error occurred while connecting"
		exit(0)
	if args.verbose:
		print "ssh connection successfull"
	shell = ssh.invoke_shell()
	shell.send('sudo -i\n')
	time.sleep(slp)
	shell.send(passwd + '\n')
	if dnsType == 'reverse':
		shell.send('rndc reload %s.in-addr.arpa in %s\n' % (rev_ip_str,viewzone))
	else:
		shell.send('rndc reload %s in %s\n' %(host,viewzone))
	time.sleep(slp)
	if args.verbose:
		print shell.recv(1024)
	shell.send("exit\n")
	time.sleep(slp)
	ssh.close()

def do_dig_operation(host,type):
	if args.verbose:
		print "performing dig operation on host: {}".format(host)
	if type == 'reverse':
		dig = os.popen("dig -x %s" %host)
	else:
		dig = os.popen("dig %s" %host)
	out = dig.readlines()
	for res in out:
		print res[0:-2]


for serv in dnsServerList:
	for view in dnsViewZoneList:
		if serv not in availableServers:
			print "Server {} is not a valid DNS Server".format(view)
			continue
		if view not in availableViews:
			print "View {} is not a valid DNS View".format(view)
			continue
		if args.verbose:
			print "Starting the dns reload operation:"
			print "Trying in server: {} with viewzone: {}".format(serv,view)
		dns_reload(serv, view, host, user, passwd, slp)
if not args.no_dig_operation:
	do_dig_operation(host,dnsType)


# octets = ip.split(".")
# octets.reverse()
# rev_ip_str = ".".join(octets[1:4])

# ssh = paramiko.SSHClient()
# ssh.load_system_host_keys()
# ssh.connect(hostname='ns1',username='%s'%user,password='%s'%passwd)
# shell = ssh.invoke_shell()
# shell.send('sudo -i\n')
# time.sleep(slp)
# shell.send(passwd + '\n')
# shell.send('rndc reload %s.in-addr.arpa in internal\n' % rev_ip_str)
# time.sleep(slp)
# print shell.recv(1024)
# shell.send("exit\n")
# ssh.close()
# ssh.connect(hostname='ns1',username=user,password=passwd)
# shell = ssh.invoke_shell()
# shell.send('sudo -i\n')
# time.sleep(slp)
# shell.send(passwd + '\n')
# shell.send('rndc reload %s.in-addr.arpa in internal\n' % rev_ip_str)
# time.sleep(slp)
# print shell.recv(1024)
# shell.send("exit\n")
# ssh.close()

# dig = os.popen("dig -x %s" %ip)
# out = dig.readlines()
# for res in out:
# 	print res[0:-2]
