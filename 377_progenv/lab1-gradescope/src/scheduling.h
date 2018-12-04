#include <string>
#include <queue>
#include <list>

using namespace std;

typedef struct Process Process;
struct Process {
  int arrival;
  int first_run;
  int duration;
  int completion;
  int actual_duration;
  string name;
};

class ArrivalComparator {
public:
  bool operator()(const Process lhs, const Process rhs)  const {
    if(lhs.arrival==rhs.arrival){
      return lhs.duration > rhs.duration;
    }
    return lhs.arrival > rhs.arrival;
  }
};

class DurationComparator {
public:
  bool operator()(const Process lhs, const Process rhs)  const {
    if(lhs.duration==rhs.duration){
      return lhs.arrival > rhs.arrival;
    }
    return lhs.duration > rhs.duration;
  }
};

typedef priority_queue<Process, vector<Process>, ArrivalComparator> pqueue_arrival;
typedef priority_queue<Process, vector<Process>, DurationComparator> pqueue_duration;

pqueue_arrival read_workload(string filename);
void show_workload(pqueue_arrival workload);
void show_processes(list<Process> processes);

void print_state(ofstream &output_file,int time,Process process,int processing_time,pqueue_arrival arrival_queue,list<Process> completed,string start,string destination);
void print_state(ofstream &output_file,int time,pqueue_arrival arrival_queue,list<Process> completed);
void print_state(ofstream &output_file,int time,pqueue_arrival arrival_queue,list<Process> completed,list<Process> temp);
void print_state(ofstream &output_file,int time,pqueue_arrival arrival_queue,list<Process> completed,pqueue_duration temp);
void print_state(ofstream &output_file,int time,Process process,int processing_time,pqueue_arrival arrival_queue,list<Process> completed,string start,string destination,list<Process> temp);
void print_state(ofstream &output_file,int time,Process process,int processing_time,pqueue_arrival arrival_queue,list<Process> completed,string start,string destination,pqueue_duration temp);
//pqueue_arrival copy_queue(const pqueue_arrival &Q);
string get_tasks(pqueue_arrival workload);
string get_tasks(pqueue_duration workload);
string print_tasks(list<Process> processes);





list<Process> fifo(pqueue_arrival workload,ofstream &output_file);
list<Process> sjf(pqueue_arrival workload, ofstream &output_file);
list<Process> stcf(pqueue_arrival workload, ofstream & output_file);
list<Process> rr(pqueue_arrival workload, ofstream &output_file);

float avg_turnaround(list<Process> processes);
float avg_response(list<Process> processes);
void show_metrics(list<Process> processes, ofstream &output_file);
