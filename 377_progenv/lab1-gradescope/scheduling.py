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

	def getDetails(self):
		return [self.name, self.arrival_time, self.total_duration, self.duration_left]

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
task_list = []
with open('workloads/'+input_file+'_'+algorithm+'_output') as f:
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
			else:
				pro = -1

			# timestamp, arrival_queue, temp_queue, index of task in processor, completed_queue, transitioning_task, transition_from, transition_to
			dat = [t, [r for r in row6], [r for r in row7], pro, [r for r in row8], row2[0], row4, row5]
			data.append(dat)

			task_list.append([t.getDetails() for t in tasks])

			row1 = f.readline().strip('\n')
		else:
			avg_turnaround_time = float(row1.split('Time: ')[1])
			nextline = f.readline().strip('\n')
			avg_response_time = float(nextline.split('Time: ')[1])
			break

data = pd.DataFrame(data)
data.columns = ['timestamp', 'arrival_queue', 'temp_queue', 'task_in_processor', 'completed_queue', 'transitioning_task', 'transition_from', 'transition_to']
task_data = pd.DataFrame(task_list)
# print(task_data)
# print(data)
# data.to_csv('results/'+input_file+'_'+algorithm+'_output.csv')
# exit(0)


# -------------- GUI begins -----------------

style="Simple,tail_width=0.5,head_width=4,head_length=8"
kw = dict(arrowstyle=style, color="k")

num_total_jobs = len(data['arrival_queue'][0][0].split(','))
# num_total_jobs = 30

fig, ax = plt.subplots(1,2,sharey=True)


clust_data = np.random.random((num_tasks,4))
collabel=("name", "arrival time", "total duration", "duration_left")
ax[0].axis('tight')
ax[0].axis('off')
the_table = ax[0].table(cellText=clust_data,colLabels=collabel,loc='center')
the_table.auto_set_font_size(False)
the_table.set_fontsize(10)
the_table.scale(1.2, 2)
ax[0].plot(clust_data[:,0],clust_data[:,1])


square_box_size = 8
x_span = np.maximum(100, num_total_jobs*square_box_size + 2*square_box_size)
y_span = 100
ax[1].set_xlim((0, x_span))
ax[1].set_ylim((0, y_span))
ax[1].set_aspect('equal')

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


x_offset_for_all_queues = offset_x + square_box_size
y_offset_temp = offset_y + square_box_size
y_offset_input = offset_y+2*square_box_size+vertical_space_queues
y_offset_process = offset_y+3*square_box_size+2*vertical_space_queues
y_offset_finish = offset_y+4*square_box_size+3*vertical_space_queues

for i in range(num_total_jobs):
	temp_queue[i] = mpatch.Rectangle((x_offset_for_all_queues + square_box_size * i, y_offset_temp),
									 square_box_size, square_box_size, fill=False)
	plt.text(offset_x + square_box_size, y_offset_temp-0.5*square_box_size, "Arrival Q", fontsize=8)

	input_order[i] = mpatch.Rectangle((x_offset_for_all_queues+square_box_size * i, y_offset_input), square_box_size,
									  square_box_size, fill=False)
	plt.text(offset_x + square_box_size, y_offset_input-0.5*square_box_size, "Task list", fontsize=8)


	processing_jobs[i] = mpatch.Rectangle((x_offset_for_all_queues + square_box_size * i, y_offset_process), square_box_size,
											  square_box_size, fill=False)
	plt.text(offset_x + square_box_size, y_offset_process-0.5*square_box_size, "Processing Q", fontsize=8)

	finished_jobs[i] = mpatch.Rectangle((x_offset_for_all_queues + square_box_size * i, y_offset_finish), square_box_size,
										square_box_size, fill=False)
	plt.text(x_offset_for_all_queues, y_offset_finish-0.5*square_box_size, "Completed Q", fontsize=8)

	ax[1].add_artist(temp_queue[i])
	ax[1].add_artist(input_order[i])

	# Remove this if more boxes are needed in processing queue. Currently this will show only 1 box.
	if i == 0:
		ax[1].add_artist(processing_jobs[i])
	ax[1].add_artist(finished_jobs[i])



arrows = {}

temp_input_arrow = mpatch.FancyArrowPatch((offset_x,y_offset_temp+1),
							(offset_x,y_offset_input+1),connectionstyle="arc3,rad=-.5", **kw)
temp_input_reverse = mpatch.FancyArrowPatch((offset_x,y_offset_input+1),
											(offset_x,y_offset_temp+1),
											connectionstyle="arc3,rad=.5", **kw)

temp_process_arrow = mpatch.FancyArrowPatch((offset_x,y_offset_temp+1),
							(offset_x,y_offset_process+1),connectionstyle="arc3,rad=-.5", **kw)
temp_process_reverse = mpatch.FancyArrowPatch((offset_x,y_offset_process+1),
							(offset_x,y_offset_temp+1),connectionstyle="arc3,rad=.5", **kw)

temp_finish_arrow = mpatch.FancyArrowPatch((offset_x,y_offset_temp+1),
							(offset_x,y_offset_finish+1),connectionstyle="arc3,rad=-.5", **kw)
temp_finish_reverse = mpatch.FancyArrowPatch((offset_x,y_offset_finish+1),
							(offset_x,y_offset_temp+1),connectionstyle="arc3,rad=.5", **kw)

arrows['temp'] = {'arrival':temp_input_arrow, 'processing':temp_process_arrow, 'complete':temp_finish_arrow}

input_process_arrow = mpatch.FancyArrowPatch((offset_x,y_offset_input+1),
							(offset_x,y_offset_process+1),connectionstyle="arc3,rad=-.5", **kw)
input_process_reverse = mpatch.FancyArrowPatch((offset_x,y_offset_process+1),
							(offset_x,y_offset_input+1),connectionstyle="arc3,rad=.5", **kw)

input_finish_arrow = mpatch.FancyArrowPatch((offset_x,y_offset_input+1),
							(offset_x,y_offset_finish+1),connectionstyle="arc3,rad=-.5", **kw)
input_finish_reverse = mpatch.FancyArrowPatch((offset_x,y_offset_finish+1),
							(offset_x,y_offset_input+1),connectionstyle="arc3,rad=.5", **kw)

arrows['arrival'] = {'temp':temp_input_reverse, 'processing':input_process_arrow, 'complete':input_finish_arrow}

process_finish_arrow = mpatch.FancyArrowPatch((offset_x,y_offset_process+1),
							(offset_x,y_offset_finish+1),connectionstyle="arc3,rad=-.5", **kw)
process_finish_reverse = mpatch.FancyArrowPatch((offset_x,y_offset_finish+1),
							(offset_x,y_offset_process+1),connectionstyle="arc3,rad=.5", **kw)

arrows['processing'] = {'temp':temp_process_reverse, 'arrival':input_process_reverse, 'complete':process_finish_arrow}
arrows['complete'] = {'temp':temp_finish_reverse, 'arrival':input_finish_reverse, 'processing':process_finish_reverse}

for key1 in arrows:
	for key2 in arrows[key1]:
		plt.gca().add_patch(arrows[key1][key2])


def preprocessTransitionTask(tran_task):
	if type(tran_task)==int:
		return tran_task
	else:
		return int(tran_task.replace('task',''))

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

# the_table = ax.table(cellText='something',
#                       rowLabels=1,
#                       rowColours='white',
#                       colLabels=4,
#                       loc='top')

# Simulate process scheduling
for index, row in data.iterrows():
	print (row["arrival_queue"], row["temp_queue"], row["task_in_processor"], row["completed_queue"])
	arrival_queue = preprocessQueue(row["arrival_queue"], num_total_jobs)
	temp_q = preprocessQueue(row["temp_queue"], num_total_jobs)
	task_in_processor = preprocessQueue(row["task_in_processor"], num_total_jobs)
	completed_queue = preprocessQueue(row["completed_queue"], num_total_jobs)

	transitioning_task = preprocessTransitionTask(row["transitioning_task"])
	transitioning_from = row["transition_from"]
	transitioning_to = row["transition_to"]

	dict_table = the_table.get_celld()
	for i in range(1, num_tasks+1):
		dict_table[(i, 0)].get_text().set_text(task_list[index][i-1][0])
		dict_table[(i, 1)].get_text().set_text(task_list[index][i-1][1])
		dict_table[(i, 2)].get_text().set_text(task_list[index][i-1][2])
		dict_table[(i, 3)].get_text().set_text(task_list[index][i-1][3])
		# dict_table[(i, 4)].get_text().set_text('something')

	ann1Lst, ann2Lst, ann3Lst, ann4Lst = [], [], [], []
	arrowText = None
	for i in range(num_total_jobs):
		finished_x, finished_y = getRectangleCenter(finished_jobs[i])
		input_x, input_y = getRectangleCenter(input_order[i])
		temp_x, temp_y = getRectangleCenter(temp_queue[i])
		processing_x, processing_y = getRectangleCenter(processing_jobs[i])

		ann1 = ax[1].annotate(completed_queue[i] if completed_queue[i]>=0 else '', (finished_x, finished_y), color='b', weight='bold',
						   fontsize=12, ha='center', va='center')
		ann2 = ax[1].annotate(arrival_queue[i] if arrival_queue[i]>=0 else '', (input_x, input_y), color='b', weight='bold',
						   fontsize=12, ha='center', va='center')
		ann3 = ax[1].annotate(temp_q[i] if temp_q[i]>=0 else '', (temp_x, temp_y), color='b', weight='bold',
						   fontsize=12, ha='center', va='center')
		ann4 = ax[1].annotate(task_in_processor[i] if task_in_processor[i] >= 0 else '', (processing_x, processing_y), color='b', weight='bold',
						   fontsize=12, ha='center', va='center')
		ann1Lst.append(ann1), ann2Lst.append(ann2), ann3Lst.append(ann3), ann4Lst.append(ann4)

	for an_arrow in arrows:
		if transitioning_to in arrows[an_arrow] and an_arrow==transitioning_from:
			arrows[an_arrow][transitioning_to].set_visible(True)
			x_text = arrows[an_arrow][transitioning_to]._posA_posB[0][0]
			y_text = (arrows[an_arrow][transitioning_to]._posA_posB[0][1] + arrows[an_arrow][transitioning_to]._posA_posB[1][1])/2
			arrowText = plt.text(x_text, y_text, str(transitioning_task), fontsize=8)
		else:
			for key in arrows[an_arrow]:
				arrows[an_arrow][key].set_visible(False)


	# if index == 0:
	# 	plt.gca().add_patch(a3)
	# else:
	# 	if a3.is_figure_set:
	# 		a3.set_visible(False)
	plt.pause(1)

	# Clear current annotations
	for i, a in enumerate(ann1Lst):
		a.remove()
	for i, a in enumerate(ann2Lst):
		a.remove()
	for i, a in enumerate(ann3Lst):
		a.remove()
	for i, a in enumerate(ann4Lst):
		a.remove()
	if arrowText != None:
		arrowText.remove()

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
