PROG = bin/exec
CC = g++
CPPFLAGS = -O0 -g -W -Wall -pedantic -std=c++11
OBJS = main.o

$(PROG) : $(OBJS)
	$(CC) $(OBJS) -o $(PROG) -lpthread -lm
	mv *.o build/

main.o :
	$(CC) $(CPPFLAGS) -c src/main.cpp

create:
	mkdir bin/
	mkdir build/

remove:
	rm -r bin/
	rm -r build/

clean:
	rm -f build/*.o