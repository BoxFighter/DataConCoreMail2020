# header.i和stmp.mail域名不一致
import email
import os
import re

mailre = re.compile(r'[\w\.-]+@[\w\.-]+\.[\w\.]+', re.IGNORECASE)

err = []

for home, dirs, files in os.walk('/home/datacon/coremail/challenge_1/'):
    for filename in files:
        fp = open(home + filename, "r")
        msg = email.message_from_file(fp)

        if ('Authentication-Results' in msg.keys()):
            key = msg['Authentication-Results'].replace('\n', '').replace('\r', '').replace('\t', '')
            arr = key.split()
            mailfrom = ''
            headeri = ''
            for a in arr:
                if (('smtp.mail=' in a) and (len(a) > 11)):
                    mailfrom = a
                if (('header.i=' in a) and (len(a) > 10)):
                    headeri = a[a.find("@"):-1]
            if (mailfrom != '' and headeri != ''):
                if (headeri.lower() not in mailfrom.lower()):
                    print(mailfrom)
                    print(headeri)
                    print(filename)
                    err.append(filename[:-4])
        fp.close()
err = list(set(err))
print(len(err))
print(err)
for i in err:
    print(i)