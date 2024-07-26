import os
import platform

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465 
SYSTEM = platform.system()
if SYSTEM == "Windows":
    CHROME_PROFILE_PATH = f"user-data-dir=C:\\Users\\{os.getlogin()}\\AppData\\Local\\Google\\Chrome\\User Data\\Wtsp"
elif SYSTEM == "Linux":
    CHROME_PROFILE_PATH = f"user-data-dir=/home/{os.getlogin()}/.config/google-chrome/Wtsp"
elif SYSTEM=="Darwin":
    CHROME_PROFILE_PATH = f"user-data-dir=Users/{os.getlogin()}/Library/Application Support/Google/Chrome/Wtsp"