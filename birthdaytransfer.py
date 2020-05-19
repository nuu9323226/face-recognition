import numpy as np
import glob,os
from datetime import datetime
#sourcefile=glob.glob(r'../datasets/personout/*')

#fileid=[]
#count1=0
#for fileidinfo in sourcefile:
    
    #print(count1,fileidinfo)
    #fileinfo=fileidinfo.split('/')
    #print(fileinfo[-1])
    #idinfo=fileinfo[-1].split('_')
    #print(idinfo[0])
    #count1=count1+1
    #fileid.append(idinfo[0])

#print('fileid',fileid)
#finalid=sorted(fileid)
#print('sort',finalid)


path_database='sourcefile/'
Employeefile = path_database + 'database_Employee.csv'

Employeefile1 = np.loadtxt(Employeefile,dtype=np.str,delimiter=',',usecols=(0,1,2,3,4,5,6,7))
print('Employeefile1',Employeefile1)
finalid=Employeefile1[:,2]


path_database='sourcefile/'
builtbirthday = path_database + 'birtday.csv'

builtbirthday1 = np.loadtxt(builtbirthday,dtype=np.str,delimiter=',',usecols=(0,3))
print('builtbirthday1',builtbirthday1)


#ironman_zeros = np.zeros((1,3), dtype=int)
realindexbirthday=[]
for findid in finalid:
    builtbirthday1index=np.argwhere(builtbirthday1==findid ) 
    print('findid',findid)
    
    
    print('builtbirthday1index',builtbirthday1index)
    id1=builtbirthday1index[:,0]
    print('id1',id1)
    
    print('builtbirthday1',builtbirthday1[id1])
    #ironman_zeros = np.concatenate((ironman_zeros, Employeefile1[id1]), axis = 0)
    person=builtbirthday1[id1]
    personid1=person[:,1]
    print('personid1',personid1)
    dataperson=personid1.tolist()
    #personid1.astype(np.int32)
    realindexbirthday.append(personid1)
    
    #print(personid1.)
    
    
    ##per=personid1.tolist()[0]
    
    ###print('personid1',personid1(0:3))
    ##print('per',str( per[0] ) )
    ##find=1911+int(  per[0][1:3]  ) 
    ##print(str(find))
    ###pty=per.split('/')
    ###print('pty',pty[0])
    ###print('puu',pty[0][3:5])
    ###rightyear=pty[0][3:5]
    ###rightyear=int(rightyear)
    ###print('rightyear',str(rightyear)  )
    ###righttt=1911+rightyear
    ###print('righttt',str(righttt)  )
print('realindexbirthday',realindexbirthday)





#np.savetxt(path_database+'database_Employee.csv', finalid,fmt='%s', delimiter=',')
with open(path_database+'database-birthday.csv','a') as f: 
    np.savetxt(f, realindexbirthday,fmt='%s', delimiter=',')
f.close    