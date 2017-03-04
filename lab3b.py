import csv

csvNames = ("super.csv","group.csv","bitmap.csv","inode.csv","directory.csv","indirect.csv")
cf = []
for filename in csvNames:
    f=open(filename, "rb")
    cf.append(csv.reader(f))

output = open('lab3b_check.txt', 'w')

#INITIAL SETUP
sb = [0] * 9
for row in cf[0]:
    for i in range(9):
        if i == 0:
            sb[i] = int(row[i], 16)
        else:
            sb[i] = int(row[i])

gd = {}
index=0
bitmapBlock = set()
inodeBlock = set()
for temp in cf[1]:
    gd[index] = temp
    bitmapBlock.add(int(temp[5],16))
    inodeBlock.add(int(temp[4],16))
    index += 1

#PART 1 : UNALLOCATED INODES

freeBlock = set()
freeInode = set()
for bitmap in cf[2]:
    
    if int(bitmap[0],16) in bitmapBlock:
        freeBlock.add(int(bitmap[1]))
    elif int(bitmap[0],16) in inodeBlock:
        freeInode.add(int(bitmap[1]))
usedBlock = {}
dupBlock = {}
listedInode = set()
allocatedInode = set()
linkCount = {}
firstData = sb[8]
tBlocks = sb[2]
errorBlock = {}
indOrigin = {}
for iNode in cf[3]:
    iNodeNum = int(iNode[0])
    linkCount[iNodeNum] = int(iNode[5])
    listedInode.add(iNodeNum)
    if int(iNode[10]) != 0:
        allocatedInode.add(iNodeNum)
    minofTwo = min(int(iNode[10])+11, 26)
    for i in range(11,minofTwo):
        currentBlock = int(iNode[i],16)
        if i > 21 and i < 26:
            indOrigin[currentBlock] = iNodeNum
            continue
        if currentBlock < firstData or currentBlock > tBlocks:
            print >> output,  "INVALID BLOCK <", currentBlock, "> IN INODE <", iNodeNum, "> ENTRY <", i - 11, ">"
        temp = int(iNode[i],16)
        if temp in usedBlock:
            if temp not in dupBlock:
                dupBlock[temp] = [usedBlock[temp]]
            dupBlock[temp].append([iNodeNum,i-11,-1])
        elif temp != 0:
            usedBlock[temp] = [iNodeNum,i-11,-1]
        if temp in freeBlock:
            if temp not in errorBlock:
                errorBlock[temp] = [[iNodeNum,i-11,-1]]
            else:
                errorBlock[temp].append([iNodeNum,i-11,-1])

for indNode in cf[5]:
    temp = int(indNode[2],16)
    iNodeNum = indOrigin[int(indNode[0],16)]
    indBlock = int(indNode[0],16)
    entryNum = int(indNode[1])
    if temp in usedBlock:
        if temp not in dupBlock:
            dupBlock[temp] = [usedBlock[temp]]
        dupBlock[temp].append([iNodeNum,entryNum, indBlock])
    elif temp != 0:
        usedBlock[temp] = [iNodeNum,entryNum,indBlock]
    if temp in freeBlock:
        if temp not in errorBlock:
            errorBlock[temp] = [[iNodeNum,entryNum,indBlock]]
        else:
            errorBlock[temp].append([iNodeNum,entryNum,indBlock])

#SORT
for k,v in dupBlock.items():
    sorted(v, key=lambda x:(x[0],x[2],x[1]))
for k,v in errorBlock.items():
    sorted(v, key=lambda x:(x[0],x[2],x[1]))

for k, v in errorBlock.items():
    count = 0
    print >> output, "UNALLOCATED BLOCK <", k, "> REFERENCED BY",
    for pair in v:
        if count == len(v) - 1:
            print >> output, "INODE <", pair[0], "> ENTRY <", pair[1], ">"
        else:
            print >> output, "INODE <", pair[0], "> ENTRY <", pair[1], ">",

#PART 2: DUPLICATELY ALLOCATED BLOCK

for k, v in dupBlock.items():
    count = 0
    print >> output,  "MULTIPLY REFERENCED BLOCK <", k, "> BY",
    for pair in v:
        if count == len(v) - 1:
            print >> output, "INODE <", pair[0], "> ENTRY <", pair[1], ">"
        else:
            print >> output, "INODE <", pair[0], "> ENTRY <", pair[1], ">",
        count += 1

#PART 3: UNALLOCATED INODE

dirInode = {}
dirLink = {}
dirChild = {}
for dirEntry in cf[4]:
    temp = int(dirEntry[4])
    origin = int(dirEntry[0])
    if temp not in dirLink:
        dirLink[temp] = 1
    else:
        dirLink[temp] += 1

    #for part 6
    if dirEntry[5] == '.' and origin != temp:
        print >> output,  "INCORRECT ENTRY IN <", origin, "> NAME < . > LINK TO <", temp, "> SHOULD BE <", origin, ">"
    if dirEntry[5] == '..':
        dirChild[temp] = origin

    if temp not in dirInode:
        dirInode[temp] = [[origin,int(dirEntry[1])]]
    else:
        dirInode[temp].append([origin,int(dirEntry[1])])


for k,v in dirInode.items():
    count = 0
    if k not in listedInode:
        print >> output,  "UNALLOCATED INODE <", k, "> REFERENCED BY",
        for i in v:
            if count == len(v) - 1:
                print >> output,  "DIRECTORY <", i[0], "> ENTRY <", i[1], ">"
            else:
                print >> output,  "DIRECTORY <", i[0], "> ENTRY <", i[1], ">",

#PART 4: MISSING INODE

tInodes = int(sb[1])
for i in range(11,tInodes):
    if i not in allocatedInode and i not in freeInode:
        group = (i-1) / int(sb[6])
        block = int(gd[group][4],16)
        print >> output,  "MISSING INODE <", i, "> SHOULD BE IN FREE LIST <", block, ">"

#PART 5: INCORRECT LINK COUNT

for k, v in dirLink.items():
    if v != linkCount[k]:
        print >> output, "LINKCOUNT <" , k, "> IS <", linkCount[k], "> SHOULD BE <", v, ">"

#PART 6: INCORRECT LINK

for k, v in dirChild.items():
    if dirInode[v][0][0] != k:
        print >> output, "INCORRECT ENTRY IN <", v, "> NAME < .. > LINK TO <", k, "> SHOULD BE <", dirInode[v][0][0], ">"


