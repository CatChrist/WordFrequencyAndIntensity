import numpy as np
from pyparsing import col
from tick.plot import plot_point_process
from tick.hawkes import HawkesSumExpKern
import matplotlib.pyplot as plt

def timestampsFromWord(word):
  with open("words/" + word + ".csv") as rf:
    timestamps = []
    comments = rf.readlines()
    for line in comments:
      comment_fields = line.split(',')
      timestamp = comment_fields[4]
      timestamps.append(timestamp)
  timestamps.sort()
  return timestamps

def normalizeTimestamps(timestamps):
  shrunk_timestamps = []
  for timestamp in timestamps:
    shrunk_timestamps.append(np.float64(timestamp) / 10 ** 8)
  normal_timestamps = []
  start_time = min(shrunk_timestamps)
  for timestamp in shrunk_timestamps:
    normal_timestamps.append(timestamp - start_time)
  return normal_timestamps

# def minAndMaxTimestamp(subredditName = 0):
#     if (subredditName == 0):
#         return 0
#     document = subredditName + "_comment_data.csv"
#     with open(document) as rf:
#       rf.readline() # discard header
#       document = rf.readlines()
#       timestamps = []
#       for comment in document:
#         timestamp = comment.split(',')[4]
#         timestamps.append(timestamp)
    
#     minimum = min(timestamps)
#     maximum = max(timestamps)

#     return [minimum, maximum]

# conspiracyMinMax = minAndMaxTimestamp('conspiracy')
# coronaMinMax = minAndMaxTimestamp('coronavirus')

# if (conspiracyMinMax[0] < coronaMinMax[0]):
#   earliestTimeStamp = conspiracyMinMax[0]
# else:
#   earliestTimeStamp = coronaMinMax[0]

# if (conspiracyMinMax[1] > coronaMinMax[1]):
#   latestTimeStamp = conspiracyMinMax[1]
# else:
#   latestTimeStamp = coronaMinMax[1]



words = ['covid',
         'vaccine',
         'government',
         'news',
         'work',
         'money',
         'old',
         'time',
         'fuck',
         'years',
         'mask',
         'public']
all_timestamps = []

for word in words:
  timestamp = timestampsFromWord(word)
  all_timestamps.append(timestamp)

### TLDR: word[x] => all_timestamps[x]

x = 0
row = 0
column = 0
fig_1, ax_list_1 = plt.subplots(nrows=2, ncols=2)
fig_2, ax_list_2 = plt.subplots(nrows=2, ncols=2)
fig_3, ax_list_3 = plt.subplots(nrows=2, ncols=2)
for timestamps in all_timestamps:
  if column > 1:
    column = 0
    row+=1
  if row > 1:
    row = 0
  print("Calculating Hawkes for " + words[x])
  timestamps = normalizeTimestamps(timestamps)
  # print(timestamps)
  decays = [0.8, 0.8]
  learner = HawkesSumExpKern(decays)

  learner.fit([np.array(timestamps)])
  if (x < 4):
    learner.plot_estimated_intensity([np.array(timestamps)], n_points=len(timestamps), ax=ax_list_1[row][column])
  elif (x < 8):
    learner.plot_estimated_intensity([np.array(timestamps)], n_points=len(timestamps), ax=ax_list_2[row][column])
  else:
    learner.plot_estimated_intensity([np.array(timestamps)], n_points=len(timestamps), ax=ax_list_3[row][column])

  learner = words[x]
  x+=1
  column+=1

x = 0
for rows in ax_list_1:
  for ax in rows:
    ax.set_title(words[x])
    ax.set_xlabel('')
    x+=1

for rows in ax_list_2:
  for ax in rows:
    ax.set_title(words[x])
    ax.set_xlabel('')
    x+=1

for rows in ax_list_3:
  for ax in rows:
    ax.set_title(words[x])
    ax.set_xlabel('')
    x+=1

plt.show()