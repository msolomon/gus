PROG=gus-test
VERSION=1.0
CC=g++
CCFLAGS=-g -pg
CFLAGS=-g -pg
OBJS= main.o test.o db.o

$(PROG): $(OBJS)
	$(CC) $(CCFLAGS) $(OBJS) -o $(PROG)

main.o: main.cpp gusConf.h
	$(CC) $(CCFLAGS) main.cpp -c

test.o: test.cpp test.h gusConf.h
	$(CC) $(CCFLAGS) test.cpp -c 
	
db.o: db.cpp db.h gusConf.h
	$(CC) $(CCFLAGS) db.cpp -c 
