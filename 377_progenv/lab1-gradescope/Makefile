CXX=g++
CXXFLAGS += -g -Wall -Wextra -pthread
CPPFLAGS += -isystem src -std=c++14

MKDIR_P = mkdir -p
OBJ_DIR = obj

all:  scheduling submission

${OBJ_DIR}:
	${MKDIR_P} ${OBJ_DIR}

submission:
	zip -r shell-submission.zip src

obj/%.o: src/%.cpp ${OBJ_DIR}
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) -c -o $@ $<




scheduling: obj/scheduling.o obj/main_scheduling.o
	$(CXX) -o $@ $^



clean:
	rm -f *~ obj/*.o obj/*.a *.zip
