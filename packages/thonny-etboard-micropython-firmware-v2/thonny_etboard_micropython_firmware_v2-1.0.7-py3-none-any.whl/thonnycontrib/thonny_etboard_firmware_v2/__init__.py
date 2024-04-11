# ******************************************************************************************
# FileName     : __init__.py
# Description  : ETboard MicroPython Firmware 다운로드 플러그인 불러오기
# Author       : 손철수
# Created Date : 2024.04.10
# Reference    :
# Modified     : 
# ******************************************************************************************


# import
from thonny import get_workbench, get_version
from tkinter.messagebox import showinfo

# import module based on version
thonny_version = get_version()
if (thonny_version > '4'):
    from .thonny_v4 import ETBoardMenu
else:
    from .thonny_v3 import ETBoardMenu

# attach menu to thonny ide    
if get_workbench() is not None:
    run = ETBoardMenu().load_plugin()
    #showinfo("env", "load_plugin() ok")   
                
# ==========================================================================================
#
#  (주)한국공학기술연구원 http://et.ketri.re.kr
#
# ==========================================================================================
