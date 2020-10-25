# X-Return-Path和From不一样
import email
import os
import re

err = []

mailre = re.compile(r'[\w\.-]+@[\w\.-]+\.[\w\.]+', re.IGNORECASE)

for home, dirs, files in os.walk('/home/datacon/coremail/challenge_1/'):
    for filename in files:
        fp = open(home + filename, "r")
        msg = email.message_from_file(fp)
        if ('X-Return-Path' in msg.keys()):
            tmp1 = mailre.findall(msg['X-Return-Path'])
            tmp2 = mailre.findall(msg['From'])
            if (len(tmp1) > 1):
                print(tmp1)
                print(filename)
            for t in tmp2:
                if (tmp1[0].lower() == t.lower()):
                    continue
                else:
                    print(tmp1)
                    print(t + '\n')
                    err.append(filename[:-4])
            if (len(tmp2) == 0 and msg['From'] != tmp1[0]):
                print(msg['From'])
                print(tmp1[0] + '\n')
                err.append(filename[:-4])
        fp.close()

print(len(err))
print(err)