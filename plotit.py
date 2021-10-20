import csv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

file=open('data.txt','r')
x2=[]
y2=[]
x4=[]
y4=[]
x8=[]
y8=[]
lit=[]
for i in file:
    if (len(i)==1):
        break
    lit=i.split(',')
    #print(lit)
    if (int(lit[2])==2):
        x2.append(int(lit[1]))
        y2.append(float(lit[0]))
    if (int(lit[2])==4):
        x4.append(int(lit[1]))
        y4.append(float(lit[0]))
    if (int(lit[2])==8):
        x8.append(int(lit[1]))
        y8.append(float(lit[0]))
        
plt.plot(x2,y2,'--b',label='assoc:2')#,color='green')
plt.plot(x4,y4,'--r',label='assoc:4')#,color='red')
plt.plot(x8,y8,'--g',label='assoc:8')#,color='blue')
plt.title('Variation in L2 Cache MissRate')
plt.xlabel('L2 Cache Sizes (in kB)')
plt.ylabel('Miss Rates')
plt.legend()
plt.grid(True)
#plt.xticks([16,32,64,128,256,512,1024])
plt.savefig('Q2.png')

