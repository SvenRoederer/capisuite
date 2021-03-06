#!/usr/bin/python
#
#
import sys,os
import email
from email.Parser import Parser as EmailParser
import tempfile
import syslog
import subprocess

#http://stackoverflow.com/questions/377017/test-if-executable-exists-in-python
def testForBinary(binaryname):
    try:
        subprocess.call([binaryname, '--help'])
        return True
    except OSError:
        syslog.syslog("%s not found on path" % binaryname)
        return False

def handle_content_plain(payload,fax) :
    errMsg = ""
#    print payload
    tmpinput = tempfile.NamedTemporaryFile()
    tmpinput.write(payload)
    tmpinput.flush()
    if ( not testForBinary("a2ps")):
        errMsg = "unable to find a2ps binary in path"
    else:
        command="a2ps -Bq -M A4 -1 --borders=no -o " + fax.name + " " + tmpinput.name
#    print command
        ret=(os.system(command))>>8
        tmpinput.close()
        if (ret):
            errMsg += "Error detected during converting ascii to ps."

    if (errMsg):
        syslog.syslog(syslog.LOG_ERR, errMsg)
        sys.stderr.write(errmsg)
        sys.exit(1)
    return()

def handle_content_pdf(payload,fax) :
    fax.write(payload)
    fax.flush
    return()

def sendfax(fax,dest):
    os.system("capisuitefax -d " + dest + " " + fax)
    return()
    
def sendfax_subject(fax,dest,subject):
    subject = subject.replace("'", "")
    param = "capisuitefax -S '" + subject + "' -d " + dest + " " + fax
    syslog.syslog(syslog.LOG_DEBUG, "param: " + param)
    os.system(param)
    return()
    
syslog.openlog("csfax_helper")
msg = sys.stdin.readlines()
msg = "".join(msg) 
#print msg

faxdest = sys.argv[1]
faxfile = tempfile.NamedTemporaryFile()
errormsgs = ""
hassubject = False

parser = EmailParser()
content = parser.parsestr(msg)
#print content.get_payload()

if content.get("Subject") :
    syslog.syslog(syslog.LOG_DEBUG, "has subject header")
    hassubject = True
    
if content.is_multipart() :
    syslog.syslog(syslog.LOG_DEBUG, "is multipart")
    for mime_part in content.walk() :
	syslog.syslog(syslog.LOG_DEBUG, mime_part.get_content_type())
	if mime_part.get_content_type() == "application/pdf" :
#	    print mime_part.get_payload(decode=True)
	    handle_content_pdf(mime_part.get_payload(decode=True),faxfile)
	    continue
	elif mime_part.get_content_type() == "text/plain" :
	    syslog.syslog(syslog.LOG_DEBUG, "text/plain - doing nothing")
#	    handle_content_plain(mime_part.get_payload(partno),faxfile)
else :
    syslog.syslog(syslog.LOG_DEBUG, "is singlepart")
    handle_content_plain(content.get_payload(),faxfile)
#    syslog.syslog(content.get_payload())

faxfile.flush()
#os.system("ls -l " + faxfile.name)
if hassubject :
    sendfax_subject(faxfile.name,faxdest,content.get("Subject"))
else :
    sendfax(faxfile.name,faxdest)
faxfile.close()
syslog.closelog()
