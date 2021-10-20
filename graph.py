import csv
file=open("stats.txt",'r')
out=open("data.txt",'a')
ini=open("config.ini",'r')
list_miss=[]
#list_hit=[]
miss=''
#hit=''
flag=0
assoc=''
asoc=[]
l2=''
l2_c=[]
for i in file:
  #  if (i[:36]=="system.l2cache.overall_misses::total"):   # assumption: this line is unique loop enter only onces
   #     miss=i
    if (i[:39]=="system.l2cache.overall_miss_rate::total"):   
        miss=i
   # elif (i[:34]=="system.l2cache.overall_hits::total"):
   #     hit=i
for j in ini:
    if (j[:21]=="[system.l2cache.tags]"):
        flag=1
    if (flag==1):
        if (j[:5]=="assoc"):
            assoc=j
            asoc=assoc[5:]#.split('=')
        if (j[:4]=="size"):
            l2=j
            l2_c=l2.split('=')            
            size=int(l2_c[1])/1024  # in int

#asoc=assoc[1]  # in str
#list_hit=hit.split()
list_miss=miss.split()
#print(list_miss)
#print(list_hit)
#print(list_miss)
#print("Overall Hit",list_hit[1])
mr=float(list_miss[1])
print("Overall Miss Rate",mr)
print("size",size)
print("associativity",asoc[1])
#miss_rate=float((float(list_miss[1]))/((float(list_miss[1]))+(float(list_hit[1]))))
#hit_rate=float((float(list_hit[1]))/((float(list_miss[1]))+(float(list_hit[1]))))
#print("Miss rate",miss_rate)
#print("Hit rate",hit_rate)
#out.write(str(miss_rate)+',')
out.write(str(mr)+',')
out.write(str(size)+',')
out.write(asoc[1]+'\n')
#out.write(str(hit_rate)+'\n')   # also add cache size
file.close()        
out.close()
