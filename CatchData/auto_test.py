import os
import time
import subprocess

# 预定义的一系列URL
urls = [
    "https://www.rootdata.com/Investors/detail/SevenX%20Ventures?k=MTM2",
    "https://www.rootdata.com/Investors/detail/Multicoin%20Capital?k=MTU0",
    "https://www.rootdata.com/Investors/detail/Solana%20Ventures?k=MTI5",
    "https://www.rootdata.com/Investors/detail/Coinbase%20Ventures?k=MjE5",
    "https://www.rootdata.com/Investors/detail/Polychain?k=MTQ2"
    "https://www.rootdata.com/Investors/detail/Blockchain%20Capital?k=MjI2"
]

# 定义 main.py 文件的绝对路径
main_script_path = '/Users/cryptocharming/D/Develope/vcData/CatchData/main.py'

def run_main_script(url):
    process = subprocess.Popen(['python3', main_script_path], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        stdout, stderr = process.communicate(input=url.encode(), timeout=600)  # 10 minutes timeout
        print(stdout.decode())
        if stderr:
            print(stderr.decode())
    except subprocess.TimeoutExpired:
        process.kill()
        print("Process timeout. Killed the process.")

for url in urls:
    run_main_script(url)
    time.sleep(3)  # 每次运行之间的间隔，防止过快的连续运行

print("All tests completed.")