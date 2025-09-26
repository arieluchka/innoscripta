# 🌶️🌶️🌶️🌶️🌶️ Bug reports 🌶️🌶️🌶️🌶️🌶️

---

<details>
<summary><h2> BUG_TITLE 🌶️</h2></summary>



</details>

---

## 🚨 Critical 🚨

<details>
<summary><h2> Brute forcing Password Change 🌶️🌶️🌶️🌶️🌶️</h2></summary>

The OTP code received on registration/password change is always 6 digits, (meaning at most 1,000,000 options).

When using the site and abusing/spamming/running DoS scripts, i didn't face any rate limits/blocks/timeouts.

No matter how much a user inputs the wrong OTP code during password reset, the code is not expired, which means an attacker can try as many times as he wants to guess the OTP code, to reset a password (in a 10 minute time frame)

(video demonstraing how even after many wrong guessm the original OTP can still be used)

<video controls src="OTP will not expire on wrong guesses.mp4" title="Title"></video>

#### PoC using a python script
I used an AI to generate a Proof of Concept script that spans many threads to parallelly send API requests for a password reset confirmation, and could successfully brute force a password change for my account multiple times.

The script can be found in the [python_scripts folder](../python_scripts/maximum_performance_brute_force.py).

(do note that it is not fully optimize, and is a PoC ONLY! but as long as the OTP is not disabled and an account is not blocked, it is 100% an attack vector)

</details>

## Registration and login 

<details>
<summary><h2>Only one error is present, even if there are multiple 🌶️🌶️</h2></summary>

The "Full Name" is empty and the phone has illegal characters, but the error message is only about missing fields.

![alt text](<Bug evidences/sign-in_sign-up/multiple_errors_only_one_is_showed.png>)

</details>


<details>
<summary><h2> UI indicates a OTP code was sent, but there was an error with a field 🌶️🌶️🌶️ </h2></summary>

The code wasn't actually sent, but the UI indicates it was.

![alt text](<Bug evidences/sign-in_sign-up/bad_phone_number_but_says_OTP_was_sent.png>)

</details>


## Product Search and Filtering


## Product Detail Page

<details>
<summary><h2> For some product pages hovering over item images doesn't zoom in 🌶️🌶️</h2></summary>

Bug was found in [this product page](https://techshopbd.com/product/obstacle-avoiding-robot-kit-arduino)

<video controls src="Bug evidences/item_page/on some products, hovering over the product image doesnt zoom in.mp4" title="Title"></video>

</details>

## Cart Operations


## User Profile


## Compatibility and Performance

