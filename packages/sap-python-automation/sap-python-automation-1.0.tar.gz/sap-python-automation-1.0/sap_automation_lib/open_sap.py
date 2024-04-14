import os
import time
import win32com.client

def open_sap(login, password, ambient_name, mandante, path_sap_gui):
    #INPUTS:
    #login = usuario
    #senha = senha
    #ambiente = IMPLEMENTAR
    #atalho = IMPLEMENTAR
    os.startfile (path_sap_gui)
    time.sleep(5)
    sapguiauto = win32com.client.GetObject("SAPGUI")
    application = sapguiauto.GetScriptingEngine
    connection = application.OpenConnection(ambient_name, True)
    time.sleep(5)
    connection = application.Children(0)
    session = connection.Children(0)
    session.findById("wnd[0]/usr/txtRSYST-MANDT").text = mandante
    session.findById("wnd[0]/usr/txtRSYST-BNAME").text = login
    session.findById("wnd[0]/usr/pwdRSYST-BCODE").text = password
    session.findById("wnd[0]/usr/pwdRSYST-BCODE").setFocus
    session.findById("wnd[0]/usr/pwdRSYST-BCODE").caretPosition = 10
    session.findById("wnd[0]/tbar[0]/btn[0]").press()
    
    return (f"Login Sucess in ambient {ambient_name} - {mandante}")
