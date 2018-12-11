import sys
import subprocess
import csv
import pandas as pd
from itertools import islice
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.pyplot import text
import matplotlib.patches as mpatch
import numpy as np

class Task():
	def __init__(self, name, arrival_time, total_duration, duration_left):
		self.name = name
		self.arrival_time = arrival_time
		self.total_duration = total_duration
		self.duration_left = duration_left

	def getDescription(self):
		return 'Task '+self.name.split('task')[1]+' - Arrival Time: '+self.arrival_time+ \
			   ', Total Duration: '+self.total_duration+', Remaining Duration: '+self.duration_left

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



# -------------- GUI begins -----------------


num_total_jobs = len(data['arrival_queue'][0][0].split(','))
# num_total_jobs = 30

fig, ax = plt.subplots()
square_box_size = 8
x_span = np.maximum(100, num_total_jobs*square_box_size + 2*square_box_size)
y_span = 100
ax.set_xlim((0, x_span))
ax.set_ylim((0, y_span))
ax.set_aspect('equal')

temp_queue = [None] * num_total_jobs
input_order = [None]*num_total_jobs
finished_jobs = [None]*num_total_jobs
processing_jobs = [None]*num_total_jobs


def getRectangleCenter(rectangle):
	rx, ry = rectangle.get_xy()
	cx = rx + rectangle.get_width() / 2.0
	cy = ry + rectangle.get_height() / 2.0
	return cx, cy


offset_x = np.maximum(x_span/2 - square_box_size*num_total_jobs,0)
offset_y = y_span/2 - 4*square_box_size
vertical_space_queues = square_box_size

for i in range(num_total_jobs):
	temp_queue[i] = mpatch.Rectangle((offset_x + square_box_size * i + square_box_size, offset_y + square_box_size),
									 square_box_size, square_box_size, fill=False)
	plt.text(offset_x + square_box_size, offset_y+0.5*square_box_size, "Temp Q", fontsize=8)

	input_order[i] = mpatch.Rectangle((offset_x+square_box_size * i + square_box_size, offset_y+2*square_box_size+vertical_space_queues), square_box_size,
									  square_box_size, fill=False)
	plt.text(offset_x + square_box_size, offset_y+1.5*square_box_size+vertical_space_queues, "Arrival Q", fontsize=8)

	processing_jobs[i] = mpatch.Rectangle((offset_x+square_box_size * i + square_box_size, offset_y+3*square_box_size+2*vertical_space_queues), square_box_size,
										  square_box_size, fill=False)
	plt.text(offset_x + square_box_size, offset_y+2.5*square_box_size+2*vertical_space_queues, "Processing Q", fontsize=8)

	finished_jobs[i] = mpatch.Rectangle((offset_x+square_box_size * i + square_box_size, offset_y+4*square_box_size+3*vertical_space_queues), square_box_size,
										square_box_size, fill=False)
	plt.text(offset_x + square_box_size, offset_y+3.5*square_box_size+3*vertical_space_queues, "Completed Q", fontsize=8)

	ax.add_artist(temp_queue[i])
	ax.add_artist(input_order[i])
	ax.add_artist(processing_jobs[i])
	ax.add_artist(finished_jobs[i])



def preprocessQueue(queue, num_total_jobs):
	arr = np.ones(num_total_jobs, dtype=np.int8) * -1
	if type(queue) == int:
		arr[0] = queue
	elif (len(queue)>0):
		str = queue[0]
		tasks = str.split(",")
		idx = 0
		for task in tasks:
			arr[idx] = int(task.replace('task',''))
			idx += 1

	return arr

# Simulate process scheduling
for index, row in data.iterrows():
	print (row["arrival_queue"], row["temp_queue"], row["task_in_processor"], row["completed_queue"])
	arrival_queue = preprocessQueue(row["arrival_queue"], num_total_jobs)
	temp_q = preprocessQueue(row["temp_queue"], num_total_jobs)
	task_in_processor = preprocessQueue(row["task_in_processor"], num_total_jobs)
	completed_queue = preprocessQueue(row["completed_queue"], num_total_jobs)

	ann1Lst, ann2Lst, ann3Lst, ann4Lst = [], [], [], []
	for i in range(num_total_jobs):
		finished_x, finished_y = getRectangleCenter(finished_jobs[i])
		input_x, input_y = getRectangleCenter(input_order[i])
		temp_x, temp_y = getRectangleCenter(temp_queue[i])
		processing_x, processing_y = getRectangleCenter(processing_jobs[i])

		ann1 = ax.annotate(completed_queue[i] if completed_queue[i]>=0 else '', (finished_x, finished_y), color='b', weight='bold',
						   fontsize=12, ha='center', va='center')
		ann2 = ax.annotate(arrival_queue[i] if arrival_queue[i]>=0 else '', (input_x, input_y), color='b', weight='bold',
						   fontsize=12, ha='center', va='center')
		ann3 = ax.annotate(temp_q[i] if temp_q[i]>=0 else '', (temp_x, temp_y), color='b', weight='bold',
						   fontsize=12, ha='center', va='center')
		ann4 = ax.annotate(task_in_processor[i] if task_in_processor[i] >= 0 else '', (processing_x, processing_y), color='b', weight='bold',
						   fontsize=12, ha='center', va='center')
		ann1Lst.append(ann1), ann2Lst.append(ann2), ann3Lst.append(ann3), ann4Lst.append(ann4)

	plt.pause(1.5)

	# Clear current annotations
	for i, a in enumerate(ann1Lst):
		a.remove()
	for i, a in enumerate(ann2Lst):
		a.remove()
	for i, a in enumerate(ann3Lst):
		a.remove()
	for i, a in enumerate(ann4Lst):
		a.remove()

	ann1Lst[:], ann2Lst[:], ann3Lst[:], ann4Lst[:] = [], [], [], []


#plt.show()

# Simulate process scheduling
# for t in range(10):
#     new_x = np.random.randint(10, size=num_total_jobs)
#     new_y = np.random.randint(10, size=num_total_jobs)
#     ann1Lst, ann2Lst, ann3Lst = [], [], []
#     for i in range(num_total_jobs):
#         finished_x, finished_y = getRectangleCenter(finished_jobs[i])
#         input_x, input_y = getRectangleCenter(input_order[i])
#         temp_x, temp_y = getRectangleCenter(temp_queue[i])
#
#         ann1 = ax.annotate(new_x[i], (finished_x, finished_y), color='b', weight='bold',
#                     fontsize=12, ha='center', va='center')
#         ann2 = ax.annotate(new_x[i], (input_x, input_y), color='b', weight='bold',
#                     fontsize=12, ha='center', va='center')
#         ann3 = ax.annotate(new_y[i], (temp_x, temp_y), color='b', weight='bold',
#                     fontsize=12, ha='center', va='center')
#         ann1Lst.append(ann1), ann2Lst.append(ann2), ann3Lst.append(ann3)
#
#     plt.pause(0.5)
#
#     # Clear current annotations
#     for i, a in enumerate(ann1Lst):
#         a.remove()
#     for i, a in enumerate(ann2Lst):
#         a.remove()
#     for i, a in enumerate(ann3Lst):
#         a.remove()
#
#     ann1Lst[:], ann2Lst[:], ann3Lst[:] = [], [], []
