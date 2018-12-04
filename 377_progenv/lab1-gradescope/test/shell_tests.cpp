#include "../src/tsh.h"
#include <gtest/gtest.h>
#include <iostream>
#include <fstream>
#include <string>

using namespace std;

class ShellTest : public ::testing::Test
{
    protected:
        ShellTest(){} //constructor runs before each test
        virtual ~ShellTest(){} //destructor cleans up after tests
        virtual void SetUp(){} //sets up before each test (after constructor)
        virtual void TearDown(){} //clean up after each test, (before destructor)
};

//Testing isQuit for "quit"
TEST(ShellTest, Test1) {
    simple_shell s;
    EXPECT_TRUE(s.isQuit((char *)"quit"));
}

// BEGIN PRIVATE CODE

//Testing isQuit for some random string
TEST(ShellTest, Test2) {
    simple_shell s;
    EXPECT_FALSE(s.isQuit((char *)"stop"));
}

//Testing parse_command with one arg
TEST(ShellTest, Test3) {
    simple_shell s;
    char cmd[81] = "hostname\n";
    char* token[20];
    memset(token, 0, 20*sizeof(char*));
    s.parse_command(cmd,token);
    EXPECT_STREQ("hostname",token[0]);
    EXPECT_STREQ(NULL,token[1]);
}

//Testing parse_command multiple arg
TEST(ShellTest, Test4) {
    simple_shell s;
    char cmd[81] = "run file1.txt file2.txt\n";
    char* token[20];
    memset(token, 0, 20*sizeof(char*));
    s.parse_command(cmd,token);
    EXPECT_STREQ("run",token[0]);
    EXPECT_STREQ("file1.txt",token[1]);
    EXPECT_STREQ("file2.txt",token[2]);
    EXPECT_STREQ(NULL,token[3]);
}

//Runs the script from exec_command and validate the text
TEST(ShellTest, Test5){
    simple_shell s;
    char* token[20];
    memset(token, 0, 20*sizeof(char*));
    token[0] =(char*)"python3";
    token[1] =(char*)"script.py";
    token[2] = NULL;

    remove("script.txt");

    s.exec_command(token);

    string line = "Test failed";
    std::ifstream myfile ("script.txt");
    if (myfile.is_open()){
        getline(myfile,line);
    }
    myfile.close();

    remove("script.txt");

    EXPECT_STREQ("Test passed", line.c_str());
}

// END PRIVATE CODE

int main(int argc, char **argv) {
    testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}
