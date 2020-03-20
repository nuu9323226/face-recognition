import numpy as np

path_database='../models/'
Employeefile = path_database + 'database_Employee.csv'

Employeefile1 = np.loadtxt(Employeefile,dtype=np.str,delimiter=',',usecols=(4))
print('Employeefile1',Employeefile1)



namelist=[]
for Employeelist in Employeefile1:
    
    Employeelist=Employeelist.replace("  ", "") #2個空白
    Employeelist=Employeelist.replace(" ", "")  #1個空白
    Employeelist=Employeelist.replace(",", "")  
    Employeelist=Employeelist.replace(" ", "") #全形
 
    print(Employeelist)
