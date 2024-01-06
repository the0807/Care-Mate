import os
import time

os.system("python /home/the0807/Pillbox/DB/PillBox/PillBox_db.py")
time.sleep(0.5)

os.system("python /home/the0807/Pillbox/DB/PillBox/patient_info_tbl.py")
time.sleep(0.5)

os.system("python /home/the0807/Pillbox/DB/PillBox/pillbox_no_tbl.py")
time.sleep(0.5)

os.system("python /home/the0807/Pillbox/DB/PillBox/patient_pillbox_tbl.py")
time.sleep(0.5)