## Bugs:
- !!! current log-in system is insecute as it is very easy to determine if an email is registered or not. (as it redirects to sign up if email is not registered)
- !! on sign up, after requesting an OTP code, if user goes a page back, he appears to be logged in (without finishing verification code process)

----

## Suggestions:
- have sign up page be a different page (so when clicking back, it will go to the sign in page, instead of the home page)
- check TLD of email, as part of the field validations
- have "Login" button grayed out if The password field is empty
- more secure validation/2FA than the OTP code (pretty easy to brute force)