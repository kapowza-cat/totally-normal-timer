import time
import multiprocessing

def lucas_lehmer(p, stop_flag):
    """
    Tests if M_p = 2^p - 1 is prime using the Lucas-Lehmer algorithm.
    Mimics the core mathematical verification function of Prime95.
    """
    if p == 2:
        return True
    
    # Mersenne number to test
    m_p = (1 << p) - 1
    
    # Initial state
    s = 4
    
    # Perform iterations (p - 2 times)
    for _ in range(p - 2):
        s = (s * s - 2) % m_p
        if stop_flag.is_set():
            break
        
    return s == 0

def stress_test_worker(worker_id, stop_flag):
    """
    A single-core worker thread that continuously generates and tests 
    Mersenne primes to maximize CPU utilization, similar to Prime95's Torture Test.
    """
    #print(f"[Worker {worker_id}] Started.")
    
    # Simple list of prime exponents to test continuously
    # In a real scenario, this would dynamically pull from a server assignment
    test_exponents = [9941, 11213, 19937, 21701, 23209, 44497]
    
    idx = 0
    while not stop_flag.is_set():
        p = test_exponents[idx % len(test_exponents)]
        
        start_time = time.time()
        is_prime = lucas_lehmer(p, stop_flag)
        duration = time.time() - start_time
        
        #print(f"[Worker {worker_id}] Tested M_{p} in {duration:.4f}s. Result Prime: {is_prime}")
        
        idx += 1

def stress_cpu(length):
    """
    Main controller to spin up workers across all available CPU threads.
    """
    cpu_count = multiprocessing.cpu_count()
    # print(f"--- Starting Python Prime95 Mimic ---")
    # print(f"Detecting {cpu_count} CPU cores. Initializing Torture Test...")
    
    manager = multiprocessing.Manager()
    stop_flag = manager.Event()
    processes = []
    
    # Spawn a worker process for every logical CPU core
    for i in range(cpu_count):
        p = multiprocessing.Process(target=stress_test_worker, args=(i, stop_flag))
        processes.append(p)
        p.start()
        
    try:
        # Run the stress test until manually stopped or time has passed
        start_time = time.perf_counter()
        while True:
            time.sleep(1)
            if time.perf_counter() - start_time >= length:
                raise KeyboardInterrupt
    except KeyboardInterrupt:
        #print("\nStopping stress test... Waiting for workers to terminate.")
        stop_flag.set()
        for p in reversed(processes):
            p.join()
        #print("Test stopped successfully.")

if __name__ == "__main__":
    stress_cpu(5)
