#include <string>
#include <fstream>
#include <iostream>
#include <queue>
#include <list>
#include <string>
#include <queue>
#include <list>

#include "scheduling.h"

using namespace std;

string NONE = "none";
string ARRIVAL = "arrival";
string PROCESSING = "processing";
string COMPLETE = "complete";
string TEMP = "temp";

// pqueue_arrival copy_queue(const pqueue_arrival &Q) {    
                       
//     pqueue_arrival Q2 = Q; 
//     return Q2;
// }
string get_tasks(list<Process> processes){
  string res="";
  if(processes.size()==0){
    return NONE;
  }
  int len = processes.size();
  while(!processes.empty()){
    Process process = processes.front();
    if(res.compare("")!=0){
      res+=",";
    }
    res+=process.name;

    processes.pop_front();
  }
  return res;

}
string get_tasks(pqueue_arrival arrival_workload){
  //pqueue_arrival arrival_workload = copy_queue(workload);
  
  list<Process> tasks;
  while(!arrival_workload.empty()){
    Process p = arrival_workload.top();
    tasks.push_back(p);
    cout << "Name: " << p.name << endl;

    arrival_workload.pop();
  }
    return  get_tasks(tasks);
}

string get_tasks(pqueue_duration duration_workload){
  //pqueue_duration duration_workload = copy_queue(workload);
  
  list<Process> tasks;
  while(!duration_workload.empty()){
    Process p = duration_workload.top();
    tasks.push_back(p);
    duration_workload.pop();
  }
    return  get_tasks(tasks);
}



void print_state(ofstream &output_file,int time,Process process,int processing_time,pqueue_arrival arrival_queue,list<Process> completed,string start,string destination){
      output_file << to_string(time) +"\n";
      output_file << process.name  << "," << process.arrival << "," << process.actual_duration << "," << process.duration << "," << process.first_run << "," << process.completion << "\n";
      output_file << to_string(processing_time) << "\n";
      output_file << start << "\n";
      output_file << destination << "\n";
      output_file << get_tasks(arrival_queue) << "\n";
      output_file << NONE << "\n";
      output_file << get_tasks(completed) << "\n";
    

}
void print_state(ofstream &output_file,int time,pqueue_arrival arrival_queue,list<Process> completed){
      output_file << to_string(time) +"\n";
      output_file << NONE << "\n";
      output_file << NONE << "\n";
      output_file << NONE << "\n";
      output_file << NONE << "\n";
      output_file << get_tasks(arrival_queue) << "\n";
      output_file << NONE << "\n";
      output_file << get_tasks(completed) << "\n";
}
void print_state(ofstream &output_file,int time,pqueue_arrival arrival_queue,list<Process> completed,pqueue_duration temp){
      output_file << to_string(time) +"\n";
      output_file << NONE << "\n";
      output_file << NONE << "\n";
      output_file << NONE << "\n";
      output_file << NONE << "\n";
      output_file << get_tasks(arrival_queue) << "\n";
      output_file << get_tasks(temp) << "\n";
      output_file << get_tasks(completed) << "\n";
}
void print_state(ofstream &output_file,int time,pqueue_arrival arrival_queue,list<Process> completed,list<Process> temp){
      output_file << to_string(time) +"\n";
      output_file << NONE << "\n";
      output_file << NONE << "\n";
      output_file << NONE << "\n";
      output_file << NONE << "\n";
      output_file << get_tasks(arrival_queue) << "\n";
      output_file << get_tasks(temp) << "\n";
      output_file << get_tasks(completed) << "\n";
}
void print_state(ofstream &output_file,int time,Process process,int processing_time,pqueue_arrival arrival_queue,list<Process> completed,string start,string destination,list<Process> temp){
      output_file << to_string(time) +"\n";
      output_file << process.name  << "," << process.arrival << "," << process.actual_duration << ","  << process.duration << "," << process.first_run << "," << process.completion << "\n";
      output_file << to_string(processing_time) << "\n";
      output_file << start << "\n";
      output_file << destination << "\n";
      output_file << get_tasks(arrival_queue) << "\n";
      output_file << get_tasks(temp) << "\n";
      output_file << get_tasks(completed) << "\n";

}

void print_state(ofstream &output_file,int time,Process process,int processing_time,pqueue_arrival arrival_queue,list<Process> completed,string start,string destination,pqueue_duration temp){
      output_file << to_string(time) +"\n";
      output_file << process.name  << "," << process.arrival << "," << process.actual_duration << "," << process.duration << "," << process.first_run << "," << process.completion << "\n";
      output_file << to_string(processing_time) << "\n";
      output_file << start << "\n";
      output_file << destination << "\n";
      output_file << get_tasks(arrival_queue) << "\n";
      output_file << get_tasks(temp) << "\n";
      output_file << get_tasks(completed) << "\n";
}
pqueue_arrival read_workload(string filename)
{
  pqueue_arrival workload;
  // BEGIN PRIVATE CODE
  ifstream infile(filename.c_str());

  int a, d, name;
  int count=0;
  while (infile >> a >> d)
  {
    Process p;
    p.arrival = a;
    p.duration = d;
    p.first_run = -1;
    p.completion = -1;
    p.name = "task"+ to_string(count);
    p.actual_duration = p.duration;

    workload.push(p);
    count+=1;
  }
  infile.close();
  // END PRIVATE CODE
  return workload;
}

void show_workload(pqueue_arrival workload)
{
  pqueue_arrival xs = workload;
  cout << "Workload:" << endl;
  while (!xs.empty())
  {
    Process p = xs.top();
    cout << '\t' << p.arrival << ' ' << p.duration << endl;
    xs.pop();
  }
}

void show_processes(list<Process> processes)
{
  list<Process> xs = processes;
  cout << "Processes:" << endl;
  while (!xs.empty())
  {
    Process p = xs.front();
    cout << "\tarrival=" << p.arrival << ", duration=" << p.duration
         << ", first_run=" << p.first_run << ", completion=" << p.completion << endl;
    xs.pop_front();
  }
}

list<Process> fifo(pqueue_arrival workload, ofstream &output_file)
{
  list<Process> complete;
  // BEGIN PRIVATE CODE
  int t = 0;
  int duration =0;
  cout << "entered here" << endl;
  if(workload.empty()){
    cout << "empty" << endl;
  }
   print_state(output_file,t,workload,complete);
  while (!workload.empty())
  {
    cout << "entered here as well" << endl;
    Process p = workload.top();
    workload.pop();

    if (p.first_run == -1)
      p.first_run = max(t,p.arrival);

    t += p.duration;
    duration = p.duration;
    print_state(output_file,t,p,p.duration,workload,complete,ARRIVAL,PROCESSING);

    p.duration -= p.duration;
    p.completion = t;
    cout << p.name << " " << p.completion << endl;
    complete.push_back(p);
    print_state(output_file,t,p,-1,workload,complete,PROCESSING,COMPLETE);

  }
  print_state(output_file,t,workload,complete);

  // END PRIVATE CODE
  return complete;
}

list<Process> sjf(pqueue_arrival workload,ofstream &output_file)
{
  list<Process> complete;
  // BEGIN PRIVATE CODE
  if (workload.empty())
    return complete;

  pqueue_duration duration_workload;
  int t = 0;
  print_state(output_file,t,workload,complete);

  while (!workload.empty())
  {
    // Get processes that have arrived
    while (!workload.empty() && workload.top().arrival <= t)
    {
      Process p = workload.top();
      duration_workload.push(workload.top());
      workload.pop();
      print_state(output_file,t,p,-1,workload,complete,ARRIVAL,TEMP,duration_workload);

    }

    while (!duration_workload.empty())
    {
      Process p = duration_workload.top();

      duration_workload.pop();
      print_state(output_file,t,p,p.duration,workload,complete,TEMP,PROCESSING,duration_workload);


      if (p.first_run == -1)
        p.first_run = max(t,p.arrival);

      t += p.duration;

      p.duration -= p.duration;
      p.completion = t;

      complete.push_back(p);
      print_state(output_file,t,p,-1,workload,complete,PROCESSING,COMPLETE,duration_workload);

    }
  }
  print_state(output_file,t,workload,complete,duration_workload);

  // END PRIVATE CODE
  return complete;
}

list<Process> stcf(pqueue_arrival workload,ofstream &output_file)
{
  list<Process> complete;
  // BEGIN PRIVATE CODE
  if (workload.empty())
    return complete;

  pqueue_duration duration_workload;
  int t = 0;
    print_state(output_file,t,workload,complete);


  // Get processes that have arrived
  while (!workload.empty() && workload.top().arrival <= t)
  {
    Process p = workload.top();
    duration_workload.push(workload.top());
    workload.pop();
    print_state(output_file,t,p,-1,workload,complete,ARRIVAL,TEMP,duration_workload);

  }

  while (!workload.empty() || !duration_workload.empty())
  {
    Process p = duration_workload.top();
    duration_workload.pop();
    print_state(output_file,t,p,1,workload,complete,TEMP,PROCESSING,duration_workload);

    if (p.first_run == -1)
      p.first_run = max(t,p.arrival);

    t += 1;

    p.duration -= 1;

    if (p.duration == 0)
    {
      p.completion = t;
      complete.push_back(p);
      print_state(output_file,t,p,-1,workload,complete,PROCESSING,COMPLETE,duration_workload);

    }
    else
    {
      duration_workload.push(p);
      print_state(output_file,t,p,-1,workload,complete,PROCESSING,TEMP,duration_workload);

    }

    // Get processes that have arrived
    while (!workload.empty() && workload.top().arrival <= t)
    {
      Process p = workload.top();

      duration_workload.push(workload.top());
      workload.pop();
      print_state(output_file,t,p,-1,workload,complete,ARRIVAL,TEMP,duration_workload);

    }
  }
  print_state(output_file,t,workload,complete,duration_workload);

  // END PRIVATE CODE
  return complete;
}

list<Process> rr(pqueue_arrival workload,ofstream &output_file)
{
  list<Process> complete;
  // BEGIN PRIVATE CODE
  if (workload.empty())
    return complete;

  list<Process> rr_workload;
  int t = 0;
    print_state(output_file,t,workload,complete);


  // Get processes that have arrived
  while (!workload.empty() && workload.top().arrival <= t)
  {
    Process p = workload.top();
    rr_workload.push_back(workload.top());
    workload.pop();
    print_state(output_file,t,p,-1,workload,complete,ARRIVAL,TEMP,rr_workload);

  }

  while (!workload.empty() || !rr_workload.empty())
  {
    Process p = rr_workload.front();
    rr_workload.pop_front();

    print_state(output_file,t,p,1,workload,complete,TEMP,PROCESSING,rr_workload);

    if (p.first_run == -1)
      p.first_run = max(t,p.arrival);

    t += 1;

    p.duration -= 1;

    if (p.duration == 0)
    {
      p.completion = t;
      complete.push_back(p);
      print_state(output_file,t,p,-1,workload,complete,PROCESSING,COMPLETE,rr_workload);

    }
    else
    {
      rr_workload.push_back(p);
      print_state(output_file,t,p,-1,workload,complete,PROCESSING,TEMP,rr_workload);
    }

    // Get processes that have arrived
    while (!workload.empty() && workload.top().arrival <= t)
    {
      Process p = workload.top();

      rr_workload.push_back(workload.top());
      workload.pop();
      print_state(output_file,t,p,-1,workload,complete,ARRIVAL,TEMP,rr_workload);

    }
  }
 print_state(output_file,t,workload,complete,rr_workload);

  // END PRIVATE CODE
  return complete;
}

float avg_turnaround(list<Process> processes)
{
  // BEGIN PRIVATE CODE
  float sum = 0;
  int count = 0;

  list<Process> xs = processes;
  while (!xs.empty())
  {
    Process x = xs.front();
    sum += (x.completion - x.arrival);
    count += 1;
    xs.pop_front();
  }

  return (sum / count);
  // END PRIVATE CODE
  /* BEGIN STUDENT CODE
  return 0;
  END STUDENT CODE */
}

float avg_response(list<Process> processes)
{
  // BEGIN PRIVATE CODE
  float sum = 0;
  int count = 0;

  list<Process> xs = processes;
  while (!xs.empty())
  {
    Process x = xs.front();
    sum += (x.first_run - x.arrival);
    count += 1;
    xs.pop_front();
  }

  return (sum / count);
  // END PRIVATE CODE
  /* BEGIN STUDENT CODE
  return 0;
  END STUDENT CODE */
}

void show_metrics(list<Process> processes,ofstream &output_file)
{
  float avg_t = avg_turnaround(processes);
  float avg_r = avg_response(processes);
  show_processes(processes);
  cout << '\n';
  cout << "Average Turnaround Time: " << avg_t << endl;
  cout << "Average Response Time:   " << avg_r << endl;
  output_file << "Average Turnaround Time: " << to_string(avg_t) << "\n";
  output_file << "Average Response Time: " << to_string(avg_r) << "\n";

}
