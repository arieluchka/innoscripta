SITE URL = `https://techshopbd.com/`
user1:
    email: ariel.agra.archive@gmail.com
    password: test123A!


options:
- Search
- Add items to cart
- make purchases

---
# Flows
## Signup
1) press "sign in" button
2) enter new email -> redirected to sign up page
3) Enter full name, phone, password


---
# Test plan:
## 1) Registration and login 
### 1) registration 
- successful normal registration
- fields constraints validations (client side(in browser)/server side) (valid email + TLD, valid username, no duplicates on emails/usernames, password complexity, min/max field sizes) [UI + API constraints]
- expected time to get verification email (1/2/5/10 mins)
    
### 2) user verification

- if there is a verification code:
    - validate cant use another code
    - try registrating twice with same email. if expectable, verify previous code invalidates when registrating second time.
    - if option to resend verification code, verify that after resend, the first code is invalid (if expected).
    - start registering with 2 different emails, validate that verification code for one email is not valid for the other email.
    - verification code is not accepted after it's expired (if it has expiration)

### 3) password reset
- cant use old password after reseting
- cant reset password for non registered emails/usernames
- ? password reset for registered and non confirmed emails/users
- (? if acount deletion possible) cant reset password after deleting user

### 4) automatic logout during login on different session

## 2) Product Search and Filtering


## 3) Product Detail Page


## 4) Cart Operations


## 5) User Profile


## 6) Compatibility and Performance


# Suggestions and improvements
- have a dedicated "sign up" button
- the "Google" sign in button is an old logo of a deprecated product "Google plus". updating to the current google logo makes sense and will be more intuitive to the users. keeping a logo from 2019 show users the site is unmaintained.
- when an email is filled and it redirects to sign-up, the email field is locked and cant be edited, which is pointless, useless and could be annoying for users that need to fix their email address if a mistake was made. (for the user to fix the email he needs to go to home page and click sign-in again OR click sign in button on top right (the previous page should be the sign in page!))
- make the "Phone" field in signup only accept numbers (so user cant even write letters/characters). will ensure user writes in the correct format the first time
- Dont make the "Send OTP" button clickable if phone field has illegal characters (make it behave the same as the password field)
- dont hide error messages on sign up page. Has only negative effects.
- make error messages appear near relevant field + highlight the field, instead of showing it on the top of the page.

