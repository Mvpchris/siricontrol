import time
import imaplib
import email
import os
import webbrowser

##########################################

#Add your gmail username and password here

username = "voicecommands1000@gmail.com"
password = "commands1000"

#Edit to these arrays to add your own commands

voicecommand = ["chrome","notepad","search","log off","shutdown"]
shellcommand = ["start Chrome","start Notepad++","shutdown -L","shutdown -h"]

##########################################

global last_checked
last_checked = -1

def fetch_siri_command(mail):
    global last_checked
    mail.list()
    mail.select("Inbox")
    result, uidlist = mail.search(None, "ALL")
    latest_email_id = uidlist[0].split()[-1]
    if latest_email_id == last_checked:
        return
    last_checked = latest_email_id
    result, data = mail.fetch(latest_email_id, "(RFC822)")
    voice_command = email.message_from_string(data[0][1].decode('utf-8'))
    c = str(voice_command.get_payload()).lower().strip()
    return c

def main(username, password):
    global last_checked
    mail = imaplib.IMAP4_SSL('imap.gmail.com', 993)
    mail.login(username, password)
    mail.list()
    mail.select("Inbox")
    result, uidlist = mail.search(None, "ALL")
    latest_email_id = uidlist[0].split()[-1]
    last_checked = latest_email_id
    while True:
        try:
            global c
            c = fetch_siri_command(mail)
            print(c)
            try:
                if("search" in c):
                    search(c)
                else:
                    for x in range(0, len(voicecommand)):
                        if(voicecommand[x] in c):
                            os.system(shellcommand[x])
            except TypeError:
                pass
        except Exception as exc:
            print("Received an exception while running: {exc}"
                  "\nRestarting...".format(**locals()))
        time.sleep(1)

def search(c):
    ie = webbrowser.get(webbrowser.iexplore)
    a = "https://www.google.co.uk/#safe=strict&q="
    s = a + c
    ie.open(c)
    
if __name__ == '__main__':
    main(username, password)
