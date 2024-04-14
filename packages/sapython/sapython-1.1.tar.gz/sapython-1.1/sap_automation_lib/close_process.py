import psutil

def close_process(name_process):
    dict_pids = {
        p.info["pid"]: p.info["name"]
        for p in psutil.process_iter(attrs=["pid", "name"])
        }

    for pid, name in dict_pids.items():
        if name == name_process:
            print(pid)
            a = pid
            try:
                print('pid close {}'.format(a))
                b = psutil.Process(a)
                b.terminate()
            except:
                pass