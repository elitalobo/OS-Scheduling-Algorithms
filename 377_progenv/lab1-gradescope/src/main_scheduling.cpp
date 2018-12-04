#include <iostream>
#include "scheduling.h"
#include <fstream>

int main(int argc, char* argv[]) {
  if (argc != 3) {
    cout << "usage: [fifo|sjf|stcf|rr] workload_file" << endl;
    exit(1);
  }

  string algorithm     = argv[1];
  string workload_file = argv[2];
  string output = workload_file + "_output";
  std::ofstream output_file;
  output_file.open (output);
  pqueue_arrival workload = read_workload(workload_file);


  if (algorithm == "fifo") {
    show_metrics(fifo(workload,output_file),output_file);
  }
  else if (algorithm == "sjf") {
    show_metrics(sjf(workload,output_file),output_file);
  }
  else if (algorithm == "stcf") {
    show_metrics(stcf(workload,output_file),output_file);
  }
  else if (algorithm == "rr") {
    show_metrics(rr(workload,output_file),output_file);
  }   
  else {
    cout << "Error: Unknown algorithm: " << algorithm << endl;
    cout << "usage: [fifo|sjf|stcf|rr] workload_file" << endl;
    exit(1);
  }
  output_file.close();
  
  return 0;
}
