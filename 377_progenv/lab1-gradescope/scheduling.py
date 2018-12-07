import sys
import subprocess
import csv
import pandas as pd
from itertools import islice

class Task():
	def __init__(self, name, arrival_time, total_duration, duration_left):
		self.name = name
		self.arrival_time = arrival_time
		self.total_duration = total_duration
		self.duration_left = duration_left

	def getDescription(self):
		return 'Task '+self.name.split('task')[1]+' - Arrival Time: '+arrival_time+', Total Duration: '+total_duration+', Remaining Duration: '+duration_left

if len(sys.argv)==3:
	algorithm = sys.argv[1]
	input_file = sys.argv[2]
else:
	print('Run as scheduling.py <scheduling-algorithm> <input-file>')
	sys.exit(2)

if algorithm not in ['fifo', 'sjf', 'stcf', 'rr']:
	print('Unknown scheduling algorithm.')
	sys.exit(2)

num_tasks = 0
tasks = []
with open('workloads/'+input_file, 'r') as f:
	row = f.readline().strip('\n').split(' ')
	while row!=['']:
		if len(row)==2:
			tname = 'task'+str(num_tasks)
			task = Task(num_tasks, row[0], row[1], row[1])
			num_tasks+=1
			tasks.append(task)
		else:
			print('Incorrect input file format.')
			sys.exit(2)
		row = f.readline().strip('\n').split(' ')

s = subprocess.call(['./scheduling', algorithm, 'workloads/'+input_file])
print('-----------')

data = []
with open('workloads/'+input_file+'_output') as f:
	pro = -1
	row1 = f.readline().strip('\n')

	while row1:
		if not row1.startswith('Average '):
			t = int(row1)

			row2 = f.readline().strip('\n')
			if row2=='none':
				row2=[-1]
			else:
				row2 = row2.split(',')
				ind = int(row2[0].split('task')[1])
				tasks[ind].duration_left = row2[3]

			row3 = f.readline()
			row4 = f.readline().strip('\n')
			row5 = f.readline().strip('\n')

			row6 = f.readline().strip('\n')
			if row6=='none':
				row6=[]
			else:
				row6=row6.split('\n')

			row7 = f.readline().strip('\n')
			if row7=='none':
				row7=[]
			else:
				row7=row7.split('\n')

			row8 = f.readline().strip('\n')
			if row8=='none':
				row8=[]
			else:
				row8=row8.split('\n')

			if row5=='processing':
				pro = row2[0].split('task')[1]

			# timestamp, arrival_queue, temp_queue, index of task in processor, completed_queue, transitioning_task, transition_from, transition_to
			dat = [t, [r for r in row6], [r for r in row7], pro, [r for r in row8], row2[0], row4, row5]
			data.append(dat)

			row1 = f.readline().strip('\n')
		else:
			avg_turnaround_time = float(row1.split('Time: ')[1])
			nextline = f.readline().strip('\n')
			avg_response_time = float(nextline.split('Time: ')[1])
			break

data = pd.DataFrame(data)
data.columns = ['timestamp', 'arrival_queue', 'temp_queue', 'task_in_processor', 'completed_queue', 'transitioning_task', 'transition_from', 'transition_to']

print(data)
