CXXOPT=-std=c++14 -pedantic
CXXFLAGS=$(CXXOPT) -g -O3 -Wall -Wextra

SOURCE=PyBootstrap.pyx Bootstrap.cpp Bootstrap.hpp
OBJS=Bootstrap.o

.PHONY: all
all: test

test: $(OBJS) test.o
	$(CXX) -o test $(OBJS) test.o

.PHONY: doc
doc: $(SOURCES)
	doxygen doxy/config.doxy

%.o: %.cpp $(HDRS)
	$(CXX) $(CXXFLAGS) -c $<

.PHONY: clean
clean:
	$(RM) *.so
	$(RM) *.o
	$(RM) -r build/
	$(RM) test