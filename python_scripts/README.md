# 🚀 Multithreaded OTP Brute Force Security Testing Script

This Python script is designed for security testing of password reset OTP (One-Time Password) verification systems. It tests whether OTP codes can be brute-forced for a given email address using **high-performance multithreading** for dramatically faster execution.

## ⚠️ **IMPORTANT WARNING**

**This tool is for security testing purposes only!** Only use this script on:
- Systems you own
- Systems you have explicit written permission to test
- Authorized penetration testing engagements

Unauthorized testing is illegal and unethical.

## 🔥 Features

- **🚀 MULTITHREADED EXECUTION**: Up to 10-20x faster with concurrent OTP testing
- **🧠 Smart Brute Force**: Tests common OTP patterns first before full brute force
- **⚡ High Performance**: Configurable thread count (1-50+ threads)
- **🎯 Custom Range Testing**: Test specific OTP ranges with multiple threads
- **🛡️ Rate Limiting Detection**: Automatically detects and handles rate limiting
- **📊 Multiple Attack Strategies**: Common patterns, timestamp-based, sequential
- **🔍 Response Analysis**: Intelligent analysis of server responses
- **🍪 Session Management**: Proper cookie and CSRF token handling
- **🔒 Thread Safety**: Safe concurrent execution with proper synchronization
- **⏱️ Progress Tracking**: Real-time progress updates across all threads

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Command Line Interface

```bash
# Basic multithreaded usage (DEFAULT - uses 10 threads)
python brute_force_password_change.py email@example.com

# High-performance with 20 threads
python brute_force_password_change.py email@example.com --threads 20

# Smart multithreaded brute force (RECOMMENDED)
python brute_force_password_change.py email@example.com --smart --threads 15

# Test only common patterns (fast, single-threaded)
python brute_force_password_change.py email@example.com --common-only

# Custom range with multithreading
python brute_force_password_change.py email@example.com --start 100000 --end 200000 --threads 25

# Force single-threaded mode (slower)
python brute_force_password_change.py email@example.com --no-threading

# Specify custom URL with multithreading
python brute_force_password_change.py email@example.com --url https://target.com --threads 12
```

### Command Line Options

- `email`: Target email address (required)
- `--url`: Base URL of target system (default: https://techshopbd.com)
- `--start`: Starting OTP number (default: 0)
- `--end`: Ending OTP number (default: 999999)
- `--delay`: Delay between requests in seconds PER THREAD (default: 0.1)
- `--threads`: Number of concurrent threads (default: 10, max recommended: 50)
- `--smart`: Use smart brute force with common patterns first
- `--common-only`: Test only common OTP patterns
- `--multithreaded`: Force multithreaded mode (default for regular brute force)
- `--no-threading`: Disable multithreading (use single-threaded mode)

### Programmatic Usage

```python
from brute_force_password_change import OTPBruteForcer

# Initialize with 15 threads for high performance
brute_forcer = OTPBruteForcer("https://example.com", "test@example.com", max_threads=15)
brute_forcer.setup_session()

# Test single OTP
success, status, message = brute_forcer.test_otp("123456")

# Multithreaded smart brute force (FASTEST)
result = brute_forcer.smart_brute_force(delay=0.05, use_multithreading=True)

# High-speed multithreaded brute force
result = brute_forcer.multithreaded_brute_force(
    start_range=0, 
    end_range=999999, 
    delay=0.01,
    max_threads=20
)

# Single-threaded (slower, for comparison)
result = brute_forcer.brute_force(start_range=0, end_range=999, delay=0.1)
```

## 🎯 Attack Strategies

### 1. Common Patterns (Single-threaded for speed)
Tests predictable OTP codes first:
- Sequential: 000000, 111111, 222222, etc.
- Patterns: 123456, 654321, 012345
- Date-based: Current date in various formats

### 2. Timestamp-based (Single-threaded)
Tests OTP codes based on current time:
- HHMMSS format
- MMSS00 format
- Recent timestamps (last hour)

### 3. **🚀 MULTITHREADED Sequential Brute Force**
Systematically tests all possible 6-digit combinations with **concurrent execution**:
- **Up to 50 concurrent threads**
- **10-20x faster than single-threaded**
- Thread-safe execution with proper synchronization
- Automatic load balancing across threads
- Real-time progress tracking

### 4. Performance Comparison
- **Single-threaded**: ~1-2 OTPs/second
- **10 threads**: ~15-25 OTPs/second  
- **20 threads**: ~30-50 OTPs/second
- **Full 6-digit range**: ~3-5 hours vs 15-30+ hours single-threaded

## Response Analysis

The script analyzes server responses to determine success:

**Success Indicators:**
- HTTP 200 with success messages
- Redirect to dashboard/profile
- "Password changed successfully" messages

**Failure Indicators:**
- "Invalid OTP" messages
- "OTP expired" messages
- HTTP error codes

**Rate Limiting:**
- HTTP 429 responses
- "Too many requests" messages
- Automatic retry with delays

## Configuration

### Custom Cookies
Update the `setup_session()` method with current cookies from your browser:

```python
custom_cookies = {
    "csrftoken": "your_csrf_token",
    "_ga": "your_ga_cookie",
    # Add other required cookies
}
brute_forcer.setup_session(custom_cookies)
```

### Custom Headers
Modify the headers in `__init__()` method to match your target application.

## Security Testing Methodology

1. **Reconnaissance**: Understand the OTP system
2. **Common Patterns**: Test predictable codes first
3. **Rate Limiting**: Test for protection mechanisms
4. **Time-based**: Test timestamp patterns
5. **Full Brute Force**: Last resort if patterns fail

## Recommendations for Developers

If this script succeeds against your system, implement these security measures:

1. **Rate Limiting**: Limit OTP attempts per IP/email
2. **Account Lockout**: Lock accounts after failed attempts
3. **CAPTCHA**: Require CAPTCHA after failures
4. **Longer OTPs**: Use 8+ digit codes
5. **Shorter Expiry**: Reduce OTP validity time
6. **Monitoring**: Log and alert on brute force attempts

## Ethical Guidelines

- ✅ Test your own systems
- ✅ Get written authorization
- ✅ Report findings responsibly
- ❌ Test systems without permission
- ❌ Use for malicious purposes
- ❌ Access unauthorized accounts

## Legal Disclaimer

This tool is provided for educational and authorized security testing purposes only. Users are solely responsible for compliance with applicable laws and regulations. The authors are not responsible for any misuse or damage caused by this software.

## Examples

See `example_usage.py` for detailed usage examples.