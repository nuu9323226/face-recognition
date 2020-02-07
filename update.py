import socket
import datetime
from ftplib import FTP
ftp_server='192.168.99.158'
ftp_user='Vincent'
ftp_password='helloworld'
ftp_backup_dir='202002.csv'
newday = datetime.date.today()  #獲取今天的日期
# oldday = datetime.date.today()-timedelta(5)  #獲得5天前的日期
newfile ='RETR 202002.csv'  #本次備份檔名(絕對路徑)
# oldfile = '/home/backup/'   'backup_data_'   str(oldday.year)   '.'   str(oldday.month)   '.'   str(oldday.day)   '.zip'  #5天前備份的檔名(絕對路徑)
def upload():
    socket.setdefaulttimeout(60)  #超時FTP時間設定為60秒
    ftp = FTP(ftp_server)
    print("login ftp...")
#     try:
    ftp.login(ftp_user, ftp_password)
    print(ftp.getwelcome())  #獲得歡迎資訊
#     try:
#         if ftp_backup_dir in ftp.nlst():
#             print("found backup folder in ftp server, upload processing.")
#         else:
#             print("don't found backup folder in ftp server, try to build it.")
#             ftp.mkd(ftp_backup_dir)
#     except:
#         print("the folder"  + ftp_backup_dir +  "doesn't exits and can't be create!")
#         sys.exit()
#     except:
#         print("ftp login failed.exit.")
#         sys.exit()
#         ftp.cwd(ftp_backup_dir)  #設定FTP路徑
#         print("upload data...")
    try:
        ftp.storbinary('STOR ' + newfile, open(ftp_backup_dir,'rb'), 1024)  #上傳備份檔案
    except:
        print("upload failed. check your permission.")
        print("delte old file...")
#     try:
#         ftp.delete(os.path.basename(oldfile))  #刪除5天前的備份檔案
#     except:
#         print("the old file in ftp doesn't exists, jumped.")
#         print("ftp upload successful.exit...")
#         ftp.quit()
    
if __name__== '__main__':
    upload()
