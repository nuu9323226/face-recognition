import numpy as np
import glob,os
from datetime import datetime

path_database='sourcefile/'
Employeefile = path_database + 'database-birthday.csv'
train_name = open(Employeefile,'r') 

lines = train_name.readlines()
count=0
for a in lines:
    print('a',a)
    a=a[2:10]
    print('a',a)
    b=a.split('\n')
    lines[count]=b[0]
    count += 1
train_name.close

print('lines',lines)




#np.savetxt(path_database+'database_Employee.csv', finalid,fmt='%s', delimiter=',')
with open(path_database+'database-birthday2.csv','a') as f: 
    np.savetxt(f, lines,fmt='%s', delimiter=',')
f.close    