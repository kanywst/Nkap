#!/usr/bin/python3

import subprocess
import sys
import os
import string
import argparse
import shutil
import appdirs
import yaml

# Globals
config = None
global_default = None

def _init():
	global config
	global global_default

	appname = 'nkap'
	rootdir = os.path.dirname(os.path.realpath(__file__))
	default_config_dir = os.path.join(rootdir,"config")
	config_dir = appdirs.user_config_dir(appname)
	service_profile_file = os.path.join(config_dir,"service-profile.yml")
	global_default_file = os.path.join(config_dir,"global-default.yml")

	if not os.path.exists(config_dir):
		os.makedirs(config_dir,exist_ok=True)
		shutil.copy(
			os.path.join(default_config_dir,"service-profile.yml"),
			service_profile_file,
		)
		shutil.copy(
			os.path.join(default_config_dir,"global-default.yml"),
			global_default_file
		)

	with open(service_profile_file,"r") as p:
		try:
			config = yaml.load(p, Loader=yaml.SafeLoader)

			if len(config) == 0:
				fail('Not Found config file.')

		except:
			fail(service_profile_file)

	with open(global_default_file,"r") as c:
		try:
			global_default = yaml.load(c, Loader=yaml.SafeLoader)

			if len(global_default) == 0:
				fail('Not Found global-default.yml')

		except:
			fail(global_default_file)



def cprint(*args,char='',end='\n',sep=' ',color='bgreen',frame_index=1,**kvargs):
	frame = sys._getframe(frame_index)

	bright = '\x1b[1m'

	dic = {'black': '\033[30m',
		   'red': '\033[31m',
		   'green': '\033[32m',
		   'yellow': '\033[33m',
		   'blue': '\033[34m',
		   'magenta': '\033[35m',
		   'cyan': '\033[36m',
		   'white': '\033[37m',
		   'bred': '\033[31m'+bright,
		   'bgreen': '\033[32m'+bright,
		   'byellow': '\033[33m'+bright,
		   'bblue': '\033[34m'+bright,
		   'bmagenta': '\033[35m'+bright,
		   'bcyan': '\033[36m'+bright,
		   'bold': '\033[1m',
		   'bg_black': '\033[40m',
		   'bg_red': '\033[41m',
		   'bg_green': '\033[42m',
		   'bg_yellow': '\033[43m',
		   'bg_blue': '\033[44m',
		   'bg_magenta': '\033[45m',
		   'bg_cyan': '\033[46m',
		   'bg_white': '\033[47m',
		   'reset': '\033[0m'
	}

	fmt = ''

	if char != '':
		fmt += dic[color] + '[' + char + ']' + dic['reset'] + ' '

	dic.update(frame.f_locals)
	dic.update(frame.f_globals)
	dic.update(kvargs)

	fmt += string.Formatter().vformat(sep.join(args),args,dic)

	print(fmt,sep=sep,end=end)

def info(*args,end='\n',sep=' ',**kvargs):
	cprint(*args,char='*',color='bgreen',end=end,sep=sep,frame_index=2,**kvargs)

def warn(*args,end='\n',sep=' ',**kvargs):
	cprint(*args,char='!',color='byellow',end=end,sep=sep,frame_index=2,**kvargs)

def error(*args,end='\n',sep=' ',**kvargs):
	cprint(*args,char='!',color='bred',end=end,sep=sep,frame_index=2,**kvargs)

def fail(*args,end='\n',sep=' ',**kvargs):
	cprint(*args,char='!',color='bred',end=end,sep=sep,frame_index=2,**kvargs)


def run_cmd(commands):
	commands = commands.split(' ')
	ret = {}
	response = subprocess.run(commands, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	
	ret['stdout'] = response.stdout.decode("utf-8")
	ret['stderr'] = response.stderr.decode("utf-8")

	return ret

def parse_nmap(result):
	ports = {}

	tmp = result.split('\n')

	start,end = -1,-1
	for i in range(len(tmp)):
		if 'PORT' in tmp[i] and 'STATE' in tmp[i] and 'SERVICE' in tmp[i]:
			start = i+1
		if 'MAC Address:' in tmp[i] or 'Nmap done' in tmp[i]:
			end = i
			break

	if start == -1 or end == -1:
		error('Error')
		sys.exit(1)

	for line in tmp[start:end]:
		if not('unrecognized' in line):
			ports_info = line.split()
			if len(ports_info) == 3:
				port = ports_info[0]
				state = ports_info[1]
				service = ' '.join(ports_info[2:])

			ports[service] = port + '/' + state
		else:
			break

	return ports

def parse_nikto(result):
	tmp = result.split('\n')[6:-2]
	return '\n'.join(tmp)

def parse_gobuster(result):
	files = {}
	for i in result.split('\n')[:-1]:
		tmp = i.split(' ')

		file = tmp[0]
		status_code = tmp[2].rstrip(')')
		if not(status_code in files.keys()):
			files[status_code] = [file]
		else:
			files[status_code] += [file]

	return files

def parse_scan(target,scan_type,response):
	if response['stderr'] and response['stdout'] == '':
		error(response['stderr'])
	else:
		result = response['stdout']

		scandir = target.scandir
		with open(os.path.join(scandir, scan_type+'.txt'),'a') as file:
			file.write(result)
		
		if scan_type == 'nmap':
			return parse_nmap(result)

		elif scan_type == 'nikto':
			return parse_nikto(result)

		elif scan_type == 'gobuster':
			return parse_gobuster(result)
		else:
			return
	return

def nmap(target):
	ports = {}

	cprint("{bg_green}[NMAP]{reset}")
	cmd = string.Formatter().vformat(config['default']['nmap']['command'],(),{'address':target.address})

	response = run_cmd(cmd)

	ports = parse_scan(target,'nmap',response)

	# output
	for service,value in ports.items():
		tmp = value.split('/')
		port = tmp[0]
		prot = tmp[1]
		state = tmp[2]
		cprint("{bgreen}{port}{reset}/{bgreen}{service}{reset}  \t{prot} {state}")

	return ports

def nmap_extra(target,ports):
	scandir = target.scandir
	address = target.address
	for service,value in ports.items():
		tmp = value.split('/')
		port = tmp[0]
		prot = tmp[1]

		info("Running port scan: {byellow}{address}{reset}:{byellow}{port}{reset}")

		cmd = string.Formatter().vformat(config['default']['nmap-extra']['command'],(),{"port":port,"address":target.address})
		
		name = '{0}_{1}_{2}_nmap'.format(prot,port,service)
		parse_scan(target,name,run_cmd(cmd))


def nikto(target):
	cprint("\n{bg_green}[NIKTO]{reset}")
	cmd = string.Formatter().vformat(config['default']['nikto']['command'],(),{"address":target.address})
	
	response = run_cmd(cmd)
	print(parse_scan(target,'nikto',response))

def gobuster(target,wordlist):
	cprint("\n{bg_green}[GOBUSTER]{reset}")
	cmd = string.Formatter().vformat(config['default']['gobuster']['command'],(),{"address":target.address,"wordlist":wordlist})

	response = run_cmd(cmd)
	files = parse_scan(target,'gobuster',response)
	
	# output
	for status_code,file in sorted(files.items()):
		status_msg = global_default['default']['status_code'][int(status_code)] #status_codes[int(status_code)]
		info("{bgreen}{status_code} {status_msg}{reset}")
		for f in file:
			print("\t"+f)

class Target:
	def __init__(self,address):
		self.address = address
		self.basedir = ''
		self.scandir = ''

def main():
	_init()

	# PARSER
	parser = argparse.ArgumentParser(description='Nkap is a simple network reconnaissance tool')

	# OPTIONS
	parser.add_argument('target',help='The target URL')
	parser.add_argument('-w','--wordlist',default="/usr/share/dirb/wordlists/big.txt", help='Path to the wordlist')
	parser.add_argument('-o', '--output', action='store', default='results', dest='output_dir', help='The output directory for results. Default: %(default)s')

	parser.error = lambda s: fail(s[0].upper() + s[1:])
	args = parser.parse_args()

	errors = False

	if args.target == None:
		error('required target URL')
		errors = True

	wordlist = args.wordlist

	if errors:
		sys.exit(1)

	target = Target(args.target)

	outdir = os.path.abspath(args.output_dir)

	target.basedir = outdir


	# SCAN
	scandir = os.path.join(outdir,target.address,'scans')
	if not os.path.exists(scandir):
		os.makedirs(scandir, exist_ok=True)

	target.scandir = scandir

	# NMAP 
	ports = nmap(target)
	nmap_extra(target,ports)

	# HTTP
	if 'http' in ports:
		# NIKTO
		nikto(target)

		# GOBUSTER
		gobuster(target,wordlist)

	# FINISH
	info("{bgreen}Finished{reset}")

if __name__ == "__main__":
	main()