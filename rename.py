import os
import sys
import shutil

dir = '/Users/Bill/Desktop/LL/keyakiblog'
all_subdirs = []
for d in os.listdir(dir):
    if os.path.isdir(os.path.join(dir, d)):
        all_subdirs.append(os.path.join(dir, d))
id = 0

for line in all_subdirs:
    for fd in os.listdir(line):
        if not os.path.isdir(os.path.join(line, fd)):
            continue
        # name = fd.split(' ')[-1]
        # id = (int(name) if int(name) > id else id)
        # newname = '%s %s %s %s' % (name[2], name[0], name[1], name[3])
        # os.rename(os.path.join(line, fd), os.path.join(line, newname))

        # templist = fd.split('.')
        # if len(templist[1]) <= 2:
        #     subpath = templist[0] + '.' + templist[1]
        # else:
        #     subpath = templist[0] + '.' + templist[1][0:2]
        # newpath = os.path.join(line, subpath)
        # oldfolder = os.path.join(line, fd)
        # newfolder = os.path.join(newpath, fd)
        # if not os.path.exists(newpath):
        #     os.makedirs(newpath)
        # shutil.move(oldfolder, newfolder)
print(id)