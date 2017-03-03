import csv

csvNames = ("super.csv","group.csv","bitmap.csv","inode.csv","directory.csv","indirect.csv")
cf = []
for filename in csvNames:
    f=open(filename, "r")
    cf.append(csv.reader(f))

#PART 1 : UNALLOCATED INODES

freeBlock = set()
for bitmap in cf[2]:
    if (int(bitmap[0], 16) % 2 ) == 1:
        freeBlock.add(int(bitmap[1], 10))

usedBlock = {}
dupBlock = {}
listedInode = set()
for iNode in cf[3]:
    iNodeNum = int(iNode[0])
    listedInode.add(iNodeNum)
    for i in range(11,26):
        temp = int(iNode[i],16)
        if temp in usedBlock:
            if temp not in dupBlock:
                dupBlock[temp] = [usedBlock[temp]]
            dupBlock[temp].append([iNodeNum,i-11])
        elif temp != 0:
            usedBlock[temp] = [iNodeNum,i-11]
        if temp in freeBlock:
            print "UNALLOCATED BLOCK <" ,temp ,  "> REFERENCED BY INODE <" , iNodeNum , "> ENTRY <",i - 11, ">"

#PART 2: DUPLICATELY ALLOCATED BLOCK

for k, v in dupBlock.items():
    print "MULTIPLY REFERENCED BLOCK <", k, "> BY",
    for pair in v:
        print "INODE <", pair[0], "> ENTRY <", pair[1], ">",
    print '\n',

#PART 3: UNALLOCATED INODE

dirInode = {}
for dirEntry in cf[4]:
    temp = dirEntry[4]
    if temp not in dirInode:
        dirInode[temp] = [[int(dirEntry[0]),int(dirEntry[1])]]
    else:
        dirInode[temp].append([int(dirEntry[0]),int(dirEntry[1])])

for k,v in dirInode.items():
    if int(k) not in listedInode:
        print "UNALLOCATED INODE <", k, "> REFERENCED BY",
        for i in v:
            print "DIRECTORY <", i[0], "> ENTRY <", i[1], ">",
        print '\n',

#PART 4:
