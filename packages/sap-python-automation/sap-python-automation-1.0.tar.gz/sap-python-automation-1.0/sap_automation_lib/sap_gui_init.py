import win32com.client

def init_sap():
    sapguiauto = win32com.client.GetObject("SAPGUI")
    application = sapguiauto.GetScriptingEngine
    connection = application.Children(0)
    session = connection.Children(0)
    connection = application.Children(0)
    session = connection.Children(0)