import os
import subprocess
import re
import time
import matplotlib.pyplot as plt
from statistics import mean

ROOT_DIR = f'{os.path.abspath(os.getcwd())}'
LOOP_NUM = 100
SLEEP = 1 # seconds to sleep after each loop iteration, this is to prevent errors such as overflow

def make():
    subprocess.run(['make', 'clean'], cwd=ROOT_DIR)
    subprocess.run(['make'], cwd=ROOT_DIR)
    
    return 0

def perf_base_echo():
    # Because this server closes when client stops
    proc = subprocess.Popen([f'{ROOT_DIR}/server/echo-server'], stdout=subprocess.PIPE)
    result = subprocess.run(['time',f'{ROOT_DIR}/client/echo-client-auto'], stderr=subprocess.PIPE)
    proc.terminate()
    return result.stderr.decode("utf-8")

def perf_iouring_echo():
    result = subprocess.run(['time',f'{ROOT_DIR}/client/echo-client-auto'], stderr=subprocess.PIPE)
    return result.stderr.decode("utf-8") 



def format_perf(perf_output):
    print(perf_output)
    perf_list = perf_output.split(' ')

    raw_time = perf_list[2].replace('elapsed','').split(':')
    minutes = int(raw_time[0])
    seconds = float(raw_time[1])
    p_time = (minutes*60.0) + seconds

    try:
        p_cpu = float(perf_list[3].replace('%CPU',''))
    except:
        p_cpu = 0.0

    # faults = re.search(r'\(([0-9]*)major\+([0-9])*minor\)pagefaults', perf_list[6])
    # p_faults = int(faults.group(1)) + int(faults.group(2))

    # p_swaps = float(perf_list[7].replace('swaps\n',''))

    return [p_time, p_cpu]

def perf_summary(perf):
    s_time = {
        'min': min(perf['time']),
        'mean': round(mean(perf['time']),2),
        'max': max(perf['time'])
    }
    s_cpu = {
        'min': min(perf['cpu']),
        'mean': round(mean(perf['cpu']),2),
        'max': max(perf['cpu'])
    }

    return {
        'time': s_time,
        'cpu': s_cpu
    }

def minyaxis(values):
    m = min(values)
    r = m-20 if m-20>0 else 0
    return int(r)

def maxyaxis(values):
    m = max(values)
    return m*2

def main():
    base_perf = {
        'time': list(),
        'cpu': list()
    }
    iouring_perf = {
        'time': list(),
        'cpu': list()
    }

    make()

    print('Running client on base echo server...')
    for _ in range(0, LOOP_NUM):
        perf = format_perf(perf_base_echo())
        base_perf['time'].append(perf[0])
        base_perf['cpu'].append(perf[1])
        # base_perf['pagefaults'].append(perf[2])
        # base_perf['swaps'].append(perf[3])
        time.sleep(SLEEP)

    print('Running client on io_uring echo server...')
    proc = subprocess.Popen([f'{ROOT_DIR}/server/io_uring-echo-server'], stdout=subprocess.PIPE)
    for _ in range(0, LOOP_NUM):
        perf = format_perf(perf_iouring_echo())
        iouring_perf['time'].append(perf[0])
        iouring_perf['cpu'].append(perf[1])
        # iouring_perf['pagefaults'].append(perf[2])
        # iouring_perf['swaps'].append(perf[3])
        time.sleep(SLEEP)
    proc.terminate()

    print('Base:',base_perf)
    print('io_uring:',iouring_perf)

    print('\n\n')

    base_perf_summary = perf_summary(base_perf)
    uring_perf_summary = perf_summary(iouring_perf)
    print('Base info:',base_perf_summary)
    print('io_uring info:',uring_perf_summary)

    plt_x = range(0,LOOP_NUM)

    red = 'tab:red'
    blue = 'tab:blue'

    fig, ax1 = plt.subplots()
    ax1.set_ylabel('CPU(%)', color=red)
    ax1.plot(plt_x, base_perf['cpu'], color=red)
    ax1.set_ylim(ymin=minyaxis(base_perf['cpu']))
    ax1.tick_params(axis='y', labelcolor=red)

    ax2 = ax1.twinx()
    ax2.set_ylabel('Tiempo(segundos)', color=blue)
    ax2.plot(plt_x, base_perf['time'], color=blue)
    ax2.set_ylim(ymax=maxyaxis(base_perf['time']))
    ax2.tick_params(axis='y', labelcolor=blue)

    fig.tight_layout()
    plt.title(f'{base_perf_summary}'[1:-1].replace("'",''),fontsize=7)
    plt.savefig(f'{ROOT_DIR}/benchmark/base_echo.png')

    plt.clf()

    fig, ax1 = plt.subplots()
    ax1.set_ylabel('CPU(%)', color=red)
    ax1.plot(plt_x, iouring_perf['cpu'], color=red)
    ax1.set_ylim(ymin=minyaxis(iouring_perf['cpu']))
    ax1.tick_params(axis='y', labelcolor=red)

    ax2 = ax1.twinx()
    ax2.set_ylabel('Tiempo(segundos)', color=blue)
    ax2.plot(plt_x, iouring_perf['time'], color=blue)
    ax2.set_ylim(ymax=maxyaxis(iouring_perf['time']))
    ax2.tick_params(axis='y', labelcolor=blue)

    fig.tight_layout()
    plt.title(f'{uring_perf_summary}'[1:-1].replace("'",''),fontsize=7)
    plt.savefig(f'{ROOT_DIR}/benchmark/iouring_echo.png')
    
    
if __name__ == "__main__":
    main()