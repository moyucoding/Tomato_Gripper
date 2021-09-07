#%%
file = open('log.log','r')
data = {'Detect':[], 'Match':[], 'Shoot':[], 'COUNT': [], 'RESEND':[]}
while True:
    line = file.readline()
    if not line:
        break
    line = line[26:]
    line = line.split(':')
    try:
        data[line[0]].append(float(line[1]))
    except:
        pass
size = len(data['Detect'])
file.close()
for i in range(size):
    data['Detect'][i] *= 1000
    data['Match'][i] *= 1000
    data['Shoot'][i] *= 1000
# %%
import matplotlib
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
#sns.kdeplot(data['Detect'],shade = True)
detect_data = data['Detect']
print(min(detect_data))
print(max(detect_data))
plt.hist(detect_data, bins=5000)
plt.xlim(30,70)
plt.title('Detect time = ms')
plt.show()

# %%
match_data = data['Match']
print(len(match_data))
print(min(match_data))
print(max(match_data))
plt.hist(match_data,bins=100)
plt.xlim(3,8)
plt.title('Match time=ms')
plt.show()
# %%
shoot_data = data['Shoot']
print(min(shoot_data))
print(max(shoot_data))
plt.hist(shoot_data,bins=5000)
plt.xlim(7,20)
plt.title('Shoot time=ms')
plt.show()
# %%
print(data['COUNT'][-1])
print(len(data['RESEND']))
resend_data = []
pre,cur = 0,0
for cur in data['RESEND']:
    if pre == 0:
        resend_data.append(int(cur))
        pre = cur
    elif cur > pre:
        resend_data[-1] = int(cur)
        pre = cur
    else:
        pre = 0
resend_data += [0] * int(data['COUNT'][-1] - len(resend_data))
plt.hist(resend_data,bins=1000)
plt.xlim(0,5)
plt.title('Resend')
plt.show()
# %%
