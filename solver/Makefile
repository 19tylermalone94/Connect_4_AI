CXX=g++
CXXFLAGS=--std=c++11 -W -Wall -O3 -DNDEBUG -I/usr/include
BOOST_LIBS=-lboost_system -lboost_thread -lpthread

# Source files for the main Connect4 Solver
MAIN_SRCS=main.cpp Solver.cpp
MAIN_OBJS=$(MAIN_SRCS:.cpp=.o)
MAIN_EXEC=connect4_solver

# Source files for the server
SERVER_SRCS=server.cpp Solver.cpp
SERVER_OBJS=$(SERVER_SRCS:.cpp=.o)
SERVER_EXEC=http_server

# Main target
all: $(MAIN_EXEC) $(SERVER_EXEC)

# Build and link the main program
$(MAIN_EXEC): $(MAIN_OBJS)
	$(CXX) $(CXXFLAGS) -o $(MAIN_EXEC) $(MAIN_OBJS) $(BOOST_LIBS)

# Build and link the server program
$(SERVER_EXEC): $(SERVER_OBJS)
	$(CXX) $(CXXFLAGS) -o $(SERVER_EXEC) $(SERVER_OBJS) $(BOOST_LIBS)

# To obtain object files
%.o: %.cpp
	$(CXX) $(CXXFLAGS) -c $< -o $@

# Clean objects and executables in the directory
clean:
	rm -f $(MAIN_OBJS) $(SERVER_OBJS) $(MAIN_EXEC) $(SERVER_EXEC)

.PHONY: clean
