CXX=g++
CXXFLAGS += -g -Wall -Wextra -pthread
CPPFLAGS += -isystem src -std=c++14

MKDIR_P = mkdir -p
OBJ_DIR = obj

all: tsh shell_tests scheduling scheduling_tests submission

${OBJ_DIR}:
	${MKDIR_P} ${OBJ_DIR}

submission:
	zip -r shell-submission.zip src

obj/%.o: src/%.cpp ${OBJ_DIR}
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) -c -o $@ $<

obj/shell_tests.o: test/shell_tests.cpp
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) -c -o $@ $<

obj/scheduling_tests.o: test/scheduling_tests.cpp
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) -c -o $@ $<

tsh: obj/tsh.o obj/main_tsh.o
	$(CXX) -o $@ $^

scheduling: obj/scheduling.o obj/main_scheduling.o
	$(CXX) -o $@ $^

shell_tests : obj/tsh.o obj/shell_tests.o /usr/lib/libgtest.a /usr/lib/libgtest_main.a
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) $^ -o $@

scheduling_tests : obj/scheduling.o obj/scheduling_tests.o /usr/lib/libgtest.a /usr/lib/libgtest_main.a
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) $^ -o $@

clean:
	rm -f *~ obj/*.o obj/*.a *.zip
	rm -f tsh scheduling shell_tests scheduling_tests
