import subprocess
import sys
import time

def monitor_process(key_word, cmd):
    p1 = subprocess.Popen(['ps', '-ef'], stdout=subprocess.PIPE)
    p2 = subprocess.Popen(['grep', key_word], stdin=p1.stdout, stdout=subprocess.PIPE)
    p3 = subprocess.Popen(['grep', '-v', 'grep'], stdin=p2.stdout, stdout=subprocess.PIPE)
    lines = p3.stdout.readlines()
    if len(lines) > 0:
        return
    subprocess.call(cmd, shell=True)

while True:
    monitor_process("python /root/spider/main.py", 'nohup python /root/spider/main.py &')
    time.sleep(10)

