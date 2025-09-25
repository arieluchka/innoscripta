SITE URL = `https://techshopbd.com/`


options:
- Search
- Add items to cart
- make purchases

### Test plan:
#### 1) Registration and login 
1) registration 
    - successful normal registration
    - fields constraints validations (client side(in browser)/server side) (valid email + TLD, valid username, no duplicates on emails/usernames, password complexity, min/max field sizes)
    - expected time to get verification email (1/2/5/10 mins)

2) user verification
    - if there is a verification code:
        - validate cant use another code
        - try registrating twice with same email. if expectable, verify previous code invalidates when registrating second time.
        - if option to resend verification code, verify that after resend, the first code is invalid (if expected).
        - start registering with 2 different emails, validate that verification code for one email is not valid for the other email.
        - verification code is not accepted after it's expired (if it has expiration)

3) password reset
4) automatic logout during login on different session

#### 2) Product Search and Filtering


#### 3) Product Detail Page


#### 4) Cart Operations


#### 5) User Profile


#### 6) Compatibility and Performance