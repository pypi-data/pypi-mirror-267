# ******************************************************************************************
# FileName     : thonny_v4.py
# Description  : ETboard MicroPython Firmware 다운로드 플러그인 for Thonny V4
# Author       : 손철수
# Created Date : 2024.04.10
# Reference    :
# Modified     : 
# ******************************************************************************************

# import for global
import tkinter as tk
from thonny import get_workbench, ui_utils
from tkinter.messagebox import showinfo

# import for custom dialog
from thonny.plugins.micropython.esptool_dialog import ESPFlashingDialog
# ==========================================================================================
class ETboardESPFlashingDialog(ESPFlashingDialog):
# ==========================================================================================
    def get_variants_url(self) -> str:
        #return f"https://raw.githubusercontent.com/thonny/thonny/master/data/{self.firmware_name.lower()}-variants-esptool.json"
        return f"https://raw.githubusercontent.com/etboard/ETboard_Public_Data/master/3rdparty/thonny/data/{self.firmware_name.lower()}-variants-esptool.json"

# ==========================================================================================        
class ETBoardMenu:
# ==========================================================================================    
    def __init__(self):
        self.workbench = get_workbench()
        
    def __del__(self):
        pass

    
    def test(self):
        from thonny import get_version
        env = get_version()
        showinfo("env", str(env))
        
                
    def firmware_upload_4(self):
        # refered try_launch_esptool_dialog() in esptool_dialog.py
        try:
            import esptool
        except ImportError:
            from tkinter import messagebox
            messagebox.showerror(
                "Can't find esptool",
                "esptool not found.\n" + "Install it via 'Tools => Manage plug-ins'",
                master=master,
            )
            return        
    
        from thonny.running import get_front_interpreter_for_subprocess
        cmd = [get_front_interpreter_for_subprocess(), "-u", "-m", "esptool"]   
        
        # 2024.04.09 : SCS
        #github.com/thonny/data에서 json 형태로 가져옮
        #https://raw.githubusercontent.com/etboard/thonny/master/data/micropython-variants-esptool.json        
        firmware_name = "MicroPython"  # 주의!! 변경하면 json 다운로드 불가, 펌웨어 쓰기 시작 주소 변경 오류
        from thonny.plugins.micropython.esptool_dialog import ESPFlashingDialog        
        dlg = ETboardESPFlashingDialog(get_workbench().winfo_toplevel(), firmware_name, cmd)
        dlg._family_combo.set('ESP32')  # 2024.04.11 : SCS : default MCU family
        ui_utils.show_dialog(dlg)
                

    def interpreter_select(self):        
        from thonny import get_runner
        from thonny.plugins.micropython import list_serial_ports

        def get_port_list():
            port_info_list = {port.description : port.device for port in list_serial_ports()}

            return port_info_list

        def get_ch340_port():
            port_info_list = get_port_list()
            if not port_info_list:
                return ""

            for desc, device in port_info_list.items():
                if not desc or not device:
                    continue

                desc = desc.upper()
                if "CH340" in desc:
                    return device
            
            return ""

        self.workbench.set_option("run.backend_name", "ESP32")        
        
        port_name = get_ch340_port()
        self.workbench.set_option("ESP32.port", port_name)
        get_runner().restart_backend(False)
        self.workbench.show_options("interpreter")
        
    def load_plugin(self):        
        self.workbench.add_command(command_id="et-firmware",
                                menu_name="file",
                                command_label="ET-board 펌웨어 업로드",
                                handler=self.firmware_upload_4,
                                group=10)
        
        self.workbench.add_command(command_id="et-interpreter",
                                menu_name="file",
                                command_label="ET-board 인터프리터 설정",
                                handler=self.interpreter_select,
                                group=10)
        
        ''' for test
        self.workbench.add_command(command_id="et-test",
                                menu_name="file",
                                command_label="ET-board test",
                                handler=self.test,
                                group=10)        
        '''                                

# ==========================================================================================
#
#  (주)한국공학기술연구원 http://et.ketri.re.kr
#
# ==========================================================================================
