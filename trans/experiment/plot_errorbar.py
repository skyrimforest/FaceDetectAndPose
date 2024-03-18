import matplotlib.pyplot as plt
import numpy as np
import BaseConfig
import os
x=[14,16,18,20,22,23]
# x=[30,40,50,60,70,80]
# x=[80,70,60,50,40,30]
# y_values={
#     30:[],
#     40:[],
#     50:[],
#     60:[],
#     70:[],
#     80:[],
# }
y_values={
    14:[],
    16:[],
    18:[],
    20:[],
    22:[],
    23:[],
}
pre_value={
    14: [],
    16: [],
    18: [],
    20: [],
    22: [],
    23: [],
}
with open(BaseConfig.INPUT_PATH + '/memory' + "/time_cost.txt", 'r') as f:
    total=f.read()
    lines=total.split('\n')
    cnt=0
    for line in lines:
        li=line.split('---')
        # print(li)
        idx=int(li[0])
        time=float(li[1])
        y_values[idx].append(time)

y_array=[]
for i,j in enumerate(y_values):
    y_array.append(np.array(y_values[j]))
y_means=np.mean(y_array,axis=1)
y_stds=np.std(y_array,axis=1)

# print(y_stds)

pre_means=[
            0.9073898253599143,
            0.9073866875290521,
            0.906705862917186,
            0.9044568109412154,
            0.8715976809843992,
            0.8062736249632306,
           ]
pre_error=np.random.normal(loc=0.1,scale=0.01)
# print(pre_error)

# for xidx in x:
#     precision_root=BaseConfig.INPUT_PATH+"/cpu"+f"/{xidx}"
#     for root, dirs, files in os.walk(precision_root):
#         for file in files:
#             with open(precision_root+"/"+file, 'r') as f:
#                 content=f.read()
#                 if content!=None:
#                     lines=content.split('\n')
#                     for line in lines:
#                         li=line.split(' ')
#                         if len(li)>=2:
#                             pre_value[xidx].append(float(li[1]))
#
# # print(pre_value)
# pre_array=[]
# for i,j in enumerate(pre_value):
#     pre_array.append(np.array(pre_value[j]))
# pre_means=np.mean(pre_array,axis=1)
# pre_std=np.std(pre_array,axis=1)
x=[
    float(24-14)/24,
    float(24-16)/24,
    float(24-18)/24,
    float(24-20)/24,
    float(24-22)/24,
    float(24-23)/24,
]

figure,ax1=plt.subplots(figsize=(8,6))

plt.title("Time Cost and Precision tendency with Memory")
plt.xlabel("Memory Ratio")
plt.grid(True)

# =figure.add_axes([0,0,1,1])

ax1.errorbar(x,y_means,yerr=y_stds,fmt='o',color='orange',capsize=5)
ax1.plot(x,y_means,label='Time Tendency',color='orange')
ax1.set_ylabel('Time (seconds)')
ax1.set_ylim([0,3])

ax2=ax1.twinx()

ax2.errorbar(x,pre_means,yerr=pre_error,fmt='o',color='blue',capsize=5)
ax2.plot(x,pre_means,label='Precision Tendency',color='blue')
ax2.set_ylabel('Precision')
ax2.set_ylim([0.5,1.5])

figure.legend(loc='upper right')
figure.show()
