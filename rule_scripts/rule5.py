# From特殊字符
import email
import os

err = []

for home, dirs, files in os.walk('/home/datacon/coremail/challenge_1/'):
    for filename in files:
        fp = open(home + filename, "r")
        msg = email.message_from_file(fp)
        symbols = ['~', '!', '#', '$', '%', '^', '&', '*', ':', ';', '[', ']', '--']
        for symbol in symbols:
            if (symbol in msg['From']):
                err.append(filename[:-4])
        fp.close()

print(len(err))
print(err)
for i in err:
    print(i)