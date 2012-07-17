SRC = $(wildcard *.tmpl)

all:	Compile	clean

.PHONY: all Compile clean

clean:
	rm *.bak
	
Compile: $(SRC)
	cheetah compile $(SRC)
