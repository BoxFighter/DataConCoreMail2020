# 多个From
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
            all_from = msg.get_all('From')
            if (len(all_from) > 1):
                print(all_from)
                print(filename)
                err.append(filename[:-4])
        fp.close()

err = list(set(err))
print(len(err))
print(err)
for i in err:
    print(i)