from datetime import datetime, timedelta, date
import sys


def create_file_time_exec(path_file):
    data_e_hora_execute = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
    path = path_file
    file = path + data_e_hora_execute + ".txt"
    print(f"Create file: {file}")
    return file

def log_task_sucess(file_name_path, rpa_name, task_name):
    data_e_hora = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    msg = f"\n{rpa_name} - TASK: {task_name}\nData e Hora: {data_e_hora}\nExecução realizada com sucesso\n-----------"
    with open(file_name_path, "a") as f:
        f.write(msg)

def log_erro(file_name_path, rpa_name):
    tipo_erro, valor_erro, traceback_obj = sys.exc_info()
    linha_de_erro = f"Linha de erro: {traceback_obj.tb_lineno}"
    data_e_hora = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    info_erro = f"{rpa_name}Data e Hora: {data_e_hora}\nErro: {tipo_erro}\nDescrição: {valor_erro}\n{linha_de_erro}\n-----------------------------------------------------------------------------------  "
    print(info_erro)
    with open(file_name_path, "a") as f:
        f.write(info_erro)

def log_sucess(file_name_path,rpa_name):
    data_e_hora = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    msg = f"\n{rpa_name}\nData e Hora: {data_e_hora}\nExecução realizada com sucesso\n-----------------------------------------------------------------------------------  "
    with open(file_name_path, "a") as f:
        f.write(msg)