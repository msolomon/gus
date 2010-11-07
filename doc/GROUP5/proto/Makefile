PROG=gus-test
VERSION=1.0
PARSER=db
CC=g++
INC=-Isrc/mysql-connector-c++-1.1.0-linux-glibc2.3-x86-32bit/include -Isrc/mysql-connector-c++-1.1.0-linux-glibc2.3-x86-32bit/lib -Isrc/mysql-connector-c++-1.1.0-linux-glibc2.3-x86-32bit/include/cppconn
LEX=flex
YACC=bison
CCFLAGS=-g -pg $(INC)
CFLAGS=-g -pg $(INC)
OBJS=main.o db.o $(PARSER).tab.o lex.yy.o

$(PROG): $(OBJS)
	$(CC) $(CCFLAGS) $(OBJS) -lfl -o $(PROG)

main.o: main.cpp gusConf.h
	$(CC) $(CCFLAGS) main.cpp -c

test.o: test.cpp test.h gusConf.h
	$(CC) $(CCFLAGS) test.cpp -c 
	
db.o: db.cpp db.h gusConf.h
	$(CC) $(CCFLAGS) db.cpp -c 

$(PARSER).tab.c $(PARSER).tab.h: $(PARSER).y
	$(YACC) -d -t $(PARSER).y

lex.yy.c: $(PARSER).l $(PARSER).tab.h
	$(LEX) $(PARSER).l

clean:
	rm *.o *.tab.h *.tab.c lex.yy.c $(PROG)
