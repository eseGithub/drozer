# -*- coding: utf-8 -*-
#python2.7
import subprocess
import sys
import time
import re

packName = ""
cmdForward = ""
cmdConect = ""
cmdAttacksurface = ""
exit = ""
Num=[]

cmdActivity = ""
cmdaAttck = ""
aAttck=[]

cmdService = ""
cmdsAttck = ""
sAttck=[]

cmdBroadcast= ""
cmdbAttck = ""
bAttck=[]

providerUrl=""
providerFile=""
providerSql=""

def setCmd(pName):
	global packName,exit,cmdForward,cmdConect,cmdAttacksurface,cmdActivity,cmdaAttck,cmdService,cmdsAttck
	global cmdBroadcast,cmdbAttck,providerUrl,providerFile,providerSql
	exit = "exit()"+"\r\n"
	packName = pName
	cmdForward = "adb forward tcp:31415 tcp:31415"+"\r\n"
	cmdConect = "drozer console connect"+"\r\n"
	cmdAttacksurface = "run app.package.attacksurface "+packName+"\r\n"

	cmdActivity = "run app.activity.info -a "+packName+"\r\n"
	cmdaAttck = "run app.activity.start --component "+packName+" "

	cmdService = "run app.service.info -a "+packName+"\r\n"
	cmdsAttck = "run app.service.start --component "+packName+" "

	cmdBroadcast = "run app.broadcast.info -a "+packName+"\r\n"
	cmdbAttck = "run app.broadcast.send --component "+packName+" "

	cmdProvider = "run app.provider.info -a "+packName+"\r\n"
	providerUrl="run scanner.provider.finduris -a "+packName+"\r\n"
	providerFile="run scanner.provider.traversal -a "+packName+"\r\n"
	providerSql="run scanner.provider.injection -a "+packName+"\r\n"

def RunForward():
    s = subprocess.Popen(str(cmdForward), stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
    stderrinfo, stdoutinfo = s.communicate()
    return s.returncode

def ObtainAllNumber(infomation):
	global Num
	key = infomation
	try:
		p1 = r"(.*?dz>)([\s\S]*?)(dz>)"
		pattern1 = re.compile(p1)
		m1 = re.search(pattern1,key)
		info1 = m1.group(0)   #require activity
		print(info1)
		Num = re.findall(r'\d+',info1)
	except :
		print("please connect drozer,drozer connect fail!")
		sys.exit(1)

def getAllNumber():
    s = subprocess.Popen(str(cmdConect), stderr=subprocess.PIPE, stdin=subprocess.PIPE,stdout=subprocess.PIPE, shell=True)
    s.stdin.write(cmdAttacksurface)
    s.stdin.write(exit)
    s.stdin.flush()  	
    stderrinfo, stdoutinfo = s.communicate()
    results = ''.join([stdoutinfo, stderrinfo])
    ObtainAllNumber(results)
    return s.returncode

def ObtainActivty(activitStr):
	global aAttck
	key = activitStr
	p1 = r"(.*?dz>)([\s\S]*?)(dz>)"
	pattern1 = re.compile(p1)
	m1 = re.search(pattern1,key)
	activity=m1.group(0)   #require activity
	st = re.split("\r\n",activity)
	for i in range(len(st)-2):
		if i%2==1:
			aAttck.append(st[i].replace(" ",""))

def RunActivty():
    s = subprocess.Popen(str(cmdConect), stderr=subprocess.PIPE, stdin=subprocess.PIPE,stdout=subprocess.PIPE, shell=True)
    s.stdin.write(cmdActivity)
    s.stdin.flush()  		
    s.stdin.write(exit)
    s.stdin.flush()  	
    stderrinfo, stdoutinfo = s.communicate()
    results = ''.join([stdoutinfo, stderrinfo])
    ObtainActivty(results)
    return s.returncode

def RunActivtyAttack():
	s = subprocess.Popen(str(cmdConect), stderr=subprocess.PIPE, stdin=subprocess.PIPE,stdout=subprocess.PIPE, shell=True)
	
	for i in range(len(aAttck)):
		s.stdin.write(cmdaAttck+aAttck[i]+"\r\n")
		print(aAttck[i])
		time.sleep(3)
		s.stdin.flush()  		
	s.stdin.write(exit)
	s.stdin.flush()  		 
	stderrinfo, stdoutinfo = s.communicate()
	results = ''.join([stdoutinfo, stderrinfo])
	return s.returncode


def ObtainService(ServiceStr):
	global sAttck
	key = ServiceStr
	p1 = r"(.*?dz>)([\s\S]*?)(dz>)"
	pattern1 = re.compile(p1)
	m1 = re.search(pattern1,key)
	service = m1.group(0)   #require service
	st = re.split("\r\n",service)
	for i in range(len(st)-2):
		if i%2==1:
			sAttck.append(st[i].replace(" ",""))

def RunService():
    s = subprocess.Popen(str(cmdConect), stderr=subprocess.PIPE, stdin=subprocess.PIPE,stdout=subprocess.PIPE, shell=True)
    s.stdin.write(cmdService) 		
    s.stdin.write(exit)
    s.stdin.flush()  	
    stderrinfo, stdoutinfo = s.communicate()
    results = ''.join([stdoutinfo, stderrinfo])
    ObtainService(results)
    return s.returncode

def RunServiceAttack():
	s = subprocess.Popen(str(cmdConect), stderr=subprocess.PIPE, stdin=subprocess.PIPE,stdout=subprocess.PIPE, shell=True)
	for i in range(len(sAttck)):
		s.stdin.write(cmdsAttck+sAttck[i]+"\r\n")
		print(sAttck[i])
		time.sleep(3)
		s.stdin.flush()  		
	s.stdin.write(exit)
	s.stdin.flush()  		 
	stderrinfo, stdoutinfo = s.communicate()
	results = ''.join([stdoutinfo, stderrinfo])
	return s.returncode

def ObtainBroadcast(Broadcast):
	global bAttck
	key = Broadcast
	p1 = r"(.*?dz>)([\s\S]*?)(dz>)"
	pattern1 = re.compile(p1)
	m1 = re.search(pattern1,key)
	result = m1.group(0)   
	st = re.split("\r\n",result)
	for i in range(len(st)-2):
		if i%2==1:
			bAttck.append(st[i].replace(" ",""))


def RunBroadcast():
    s = subprocess.Popen(str(cmdConect), stderr=subprocess.PIPE, stdin=subprocess.PIPE,stdout=subprocess.PIPE, shell=True)
    s.stdin.write(cmdBroadcast)	
    s.stdin.write(exit)
    s.stdin.flush()  	
    stderrinfo, stdoutinfo = s.communicate()
    results = ''.join([stdoutinfo, stderrinfo])
    ObtainBroadcast(results)
    return s.returncode

def RunBroadcastAttack():
	s = subprocess.Popen(str(cmdConect), stderr=subprocess.PIPE, stdin=subprocess.PIPE,stdout=subprocess.PIPE, shell=True)
	for i in range(len(bAttck)):
		s.stdin.write(cmdbAttck+bAttck[i]+"\r\n")
		print(bAttck[i])
		time.sleep(3)
		s.stdin.flush()  		
	s.stdin.write(exit)
	s.stdin.flush()  		 
	stderrinfo, stdoutinfo = s.communicate()
	results = ''.join([stdoutinfo, stderrinfo])
	return s.returncode

def RunProviders():
    s = subprocess.Popen(str(cmdConect), stderr=subprocess.PIPE, stdin=subprocess.PIPE,stdout=subprocess.PIPE, shell=True)
    s.stdin.write(providerUrl)
    s.stdin.write(providerFile)
    s.stdin.write(providerSql)	
    s.stdin.write(exit)
    s.stdin.flush()  	
    stderrinfo, stdoutinfo = s.communicate()
    results = ''.join([stdoutinfo, stderrinfo])

    print(results[870:])
    return s.returncode

def test():
	RunForward()
	getAllNumber()
	if Num[3]!="0":
		RunService()
		print("Service Attack")
		RunServiceAttack()
		print("Service Attack\r\n")
	if Num[1]!="0":
		RunBroadcast()
		print("Broadcast Attack")
		RunBroadcastAttack()
		print("Broadcast Attack\r\n")
	if Num[0]!="0":
		RunActivty()
		print("Avtity Attack")
		RunActivtyAttack()
		print("Avtity Attack\r\n")
	if Num[2]!="99": #must execute
		print("Providers Attack")
		RunProviders()
		print("Providers Attack\r\n")


def main(argv):
	if len(argv) != 2:
		print("you must run in the drozer directory and you must input two arg")
		print("For exanple: python drozer.py packName")
	else:
		setCmd(argv[1])
		test()

if __name__ == "__main__":
	main(sys.argv)