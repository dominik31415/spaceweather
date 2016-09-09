#This script checks periodically the Resources Canada website
# for the current space weather conditions. If the Kr values exceed the threshold for a visible aurora 
# in my town it sends me a simple email, which is forwarded to my cell phone.

import re
import urllib.request as ur
from datetime import datetime, time
from time import sleep
import smtplib

user = "dominiksXXXXX@hotmail.com" #this is just a dummy email I use for this script
passwd = "XXXXXX"

#Most cell phone providers have an email-to-text gateway
from_addr = user
to_addr = "123456789@txt.windmobile.ca"	
smtp_srv = "smtp.live.com"

#Open connection, login, send 'message' and log out
def sendtxt(message):
	smtp = smtplib.SMTP(smtp_srv,587)
	smtp.ehlo()
	smtp.starttls()
	smtp.ehlo()
	smtp.login(user, passwd)
	smtp.sendmail(from_addr, to_addr, message)
	smtp.quit()



# This function requests the current and future Kr iindices from  Natural Resources Canada
# There a different links for various regions in Canada. I only need the numbers from the table in the bottom
website = "http://www.spaceweather.gc.ca/forecast-prevision/regional/sr-1-en.php?region=ott&mapname=east_n_america"
def check_weather():
	try:
		s = ur.urlopen(website)
		html_content = s.read().decode('utf-8')

		#the table has three rows for current and two future values of Kr
		m = re.search('(<td header="current-txt kr-txt" class=")[a-z-]+">[0-9]</td>', html_content)
		m2 = re.findall('>[0-9]<',m.group())[0]
		kr1 = int(m2[1])

		m = re.search('(<td header="forecast0t3-txt kr-txt" class=")[a-z-]+">[0-9]</td>', html_content)
		m2 = re.findall('>[0-9]<',m.group())[0]
		kr2 = int(m2[1])

		m = re.search('(<td header="forecast3t6-txt kr-txt" class=")[a-z-]+">[0-9]</td>', html_content)
		m2 = re.findall('>[0-9]<',m.group())[0]
		kr3 = int(m2[1])
	except:
		print('Could not open website')
		(kr1,kr2,kr3) = (0,0,0)

	return (kr1,kr2,kr3)


################ main program
while True:
	tt = datetime.today().strftime('%H:%M')
	kr = check_weather()
	msg = "It is %s and the kr indices are %d, %d, %d"%(tt,kr[0],kr[1],kr[2])
	print(msg)
	if max(kr)>4:		#this is just the threshold for having a visible Aurora in Ottawa
		try:
			sendtxt(msg)
			sleep(3000)
		except:
			print('Failure sending email')
			sleep(1000)
		


