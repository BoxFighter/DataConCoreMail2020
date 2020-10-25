# Sender和From不一样
import email
import os
import re

mailre = re.compile(r'[\w\.-]+@[\w\.-]+\.[\w\.]+', re.IGNORECASE)

err = []
for home, dirs, files in os.walk('/home/datacon/coremail/challenge_1/'):
    for filename in files:
        fp = open(home + filename, "r")
        msg = email.message_from_file(fp)
        if ('Sender' in msg.keys()):
            tmp = mailre.findall(msg['From'])
            for t in tmp:
                if (msg['Sender'].lower() == t.lower()):
                    continue
                else:
                    if (msg['Sender'][msg['Sender'].find("@"):] == t[t.find("@"):]):
                        continue
                    print(msg['Sender'])
                    print(t + '\n')
                    err.append(filename[:-4])
        fp.close()

print(len(err))
print(err)
for i in err:
    print(i)