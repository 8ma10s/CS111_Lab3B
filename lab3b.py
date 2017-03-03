import csv

csvNames = ("super.csv","group.csv","bitmap.csv","inode.csv","directory.csv","indirect.csv")
cf = []
for filename in csvNames:
    f=open(filename, "r")
    cf.append(csv.reader(f))

#PART 1 : UNALLOCATED INODES

freeBlock = set([])
for bitmap in cf[2]:
    if (int(bitmap[0], 16) % 2 ) == 1:
        freeBlock.add(int(bitmap[1], 10))

for iNode in cf[3]:
    for i in range(11,26):
        if int(iNode[i], 16) in freeBlock:
            print "UNALLOCATED BLOCK < " ,int(iNode[i],16) ,  " > REFERENCED BY INODE < " , iNode[0] , " > ENTRY < ",i - 11, " >"
