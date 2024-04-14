#Biblioteca para automações no SAP Gui

Funções disponíveis

open_sap(ogin, password, ambient_name, mandante, path_sap_gui)

close_process(name_process)

init_sap() - quando se utiliza sapscript deve rodar essa função para estabelecer a conexão com o SAP (como sap já aberto e logado)

create_file_time_exec(path_file) - caminho da pasta (Logs)

log_task_sucess(file_name_path, rpa_name, task_name)

log_erro(file_name_path, rpa_name)

log_sucess(file_name_path,rpa_name)