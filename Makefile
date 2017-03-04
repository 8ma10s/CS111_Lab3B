build: lab3b.py
	@echo "You do not need to compile this python script. type in make run to execute it"

run: lab3b.py super.csv group.csv bitmap.csv inode.csv directory.csv indirect.csv
	python lab3b.py

clean:
	rm -f lab3b_check.txt lab3b-804608241.tar.gz

dist: lab3b.py Makefile README
	tar -czvf lab3b-804608241.tar.gz lab3b.py Makefile README
