#include "tsh.h"

using namespace std;

void simple_shell::parse_command(char* cmd, char** cmdTokens) {
// BEGIN PRIVATE CODE
    cmd[strlen(cmd) - 1] = '\0'; // drop trailing newline
    unsigned long i = 0;
    cmdTokens[i] = strtok(cmd, " "); // tokenize on spaces
    while (cmdTokens[i++] && i < sizeof(cmdTokens)) {
        cmdTokens[i] = strtok(NULL, " ");
    }
// END PRIVATE CODE
/* BEGIN STUDENT CODE
  // TODO: tokenize the command string into arguments
END STUDENT CODE */
}

void simple_shell::exec_command(char **argv)
{
// BEGIN PRIVATE CODE
	pid_t pid;
	if ((pid = fork()) == 0)
	{
		// child process
		cout << "Process id  %d beginning execution " << getpid() << endl;
		execvp(argv[0],argv);
		cout << "invalid command" << endl;
		exit(1);
	}
	else{
		// parent process
		cout << "Parent process waiting for child to complete" << endl;
		waitpid(pid,0,0);
	}
// END PRIVATE CODE
/* BEGIN STUDENT CODE
  // TODO: fork a child process to execute the command.
  // parent process should wait for the child process to complete and reap it
END STUDENT CODE */
}

bool simple_shell::isQuit(char *cmd){
// BEGIN PRIVATE CODE
	if (strcmp(cmd,"quit") == 0){
		return true;
	}
	else return false;
// END PRIVATE CODE
/* BEGIN STUDENT CODE
  // TODO: check for the command "quit" that terminates the shell
  return false;
END STUDENT CODE */
}
