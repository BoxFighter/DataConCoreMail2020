# dkim.d和from不一样
import email
import os
import re

mailre = re.compile(r'[\w\.-]+@[\w\.-]+\.[\w\.]+', re.IGNORECASE)

err = []

for home, dirs, files in os.walk('/home/datacon/coremail/challenge_1/'):
    for filename in files:
        fp = open(home + filename, "r")
        msg = email.message_from_file(fp)

        if ('DKIM-Signature' in msg.keys()):
            key = msg['DKIM-Signature'].replace('\n', '').replace('\r', '').replace('\t', '')
            arr = key.split()
            for a in arr:
                if (('d=' in a) and (len(a) > 3)):
                    all_from = msg.get_all('From')
                    if (len(all_from) > 1):
                        continue
                    else:
                        tmp = mailre.findall(msg['From'])
                        mailfrom = a[a.find("d=") + 2:a.find(";")]
                        if (mailfrom.lower() not in msg['From'].lower()):
                            print(mailfrom)
                            print(msg['From'])
                            print(filename)
                            err.append(filename[:-4])
            continue
        fp.close()
err = list(set(err))
print(len(err))
print(err)
for i in err:
    print(i)