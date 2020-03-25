import numpy as np
import glob,os
from datetime import datetime
sourcefile=glob.glob(r'../datasets/personout/*')

fileid=[]
count1=0
for fileidinfo in sourcefile:
    
    print(count1,fileidinfo)
    fileinfo=fileidinfo.split('/')
    print(fileinfo[-1])
    idinfo=fileinfo[-1].split('_')
    print(idinfo[0])
    count1=count1+1
    fileid.append(idinfo[0])

print('fileid',fileid)
finalid=sorted(fileid)
print('sort',finalid)


path_database='../models/'
Employeefile = path_database + 'database_Employee.csv'

Employeefile1 = np.loadtxt(Employeefile,dtype=np.str,delimiter=',',usecols=(2,4,5))
print('Employeefile1',Employeefile1)

ironman_zeros = np.zeros((1,3), dtype=int)
sorid=[]
for findid in finalid:
    EmployeeHaveindex=np.argwhere(Employeefile1==findid ) 
    print(findid)
    print('EmployeeHaveindex',EmployeeHaveindex)
    id1=EmployeeHaveindex[:,0]
    print('id1',id1)
    
    print('Employeefile1',Employeefile1[id1])
    ironman_zeros = np.concatenate((ironman_zeros, Employeefile1[id1]), axis = 0)
    
    #sorid.append(id1[0,0])

ironman_zeros = np.delete(ironman_zeros, 0, axis=0)
print('ironman_zeros',ironman_zeros)


xtime=datetime.now().strftime("%Y-%m-%d")


folder = '../models/'+'name-'+xtime+'.txt'
command = 'rm -r %s'%(folder)
result = os.system(command)
if result == 0:
    print ('delete ==> '+folder )
else:
    print ('==> '+folder+' is not exist')    



with open('../models/'+'name-'+xtime+'.txt','a') as f: 
    np.savetxt(f, ironman_zeros,fmt='%s', delimiter="_")
f.close