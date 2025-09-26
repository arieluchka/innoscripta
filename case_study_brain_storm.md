SITE URL = `https://techshopbd.com/`
user1:
    email: ariel.agra.archive@gmail.com
    password: Aa123!9fas
    new: qwerty_123!A

user2:
    email: ariel.agra@gmail.com
    password: banana!A2

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
4) press Send OTP
5) enter code from email and press "Registration"


---
# Test plan:
## 1) Registration and login 
### 1) registration 
- successful normal registration
- successful registration with "Google" button
- successful registration with "Facebook" button
- after registering with email manually, user can still log in with same email but through "Google" button. (NEED TO VERIFY WHAT IS EXPECTED)


- fields constraints validations (client side(in browser)/server side) (valid email + TLD, valid username, no duplicates on emails/usernames, password complexity, min/max field sizes, spaces before/after) [UI + API constraints]
- expected time to get verification email (1/2/5/10 mins)

### 1.1) Log in for existing user
- cant log in if password empty
- cant log in if password wrong


### 2) user verification

- if there is a verification code:
    - validate cant use another random string/int
    - try registrating twice with same email. Verify the system handles that a registration is in process.
    - After resend of OTP code, assert the first code is invalid.
    - start registering with 2 different emails, validate that verification code for one email is not valid for the other email.
    - verification code is not accepted after it's expired

### 3) password reset
- cant use old password after reseting
- password cant be reset for registered and not OTP confirmed emails
- (? if acount deletion possible) cant reset password after deleting user
- if user is logged in at a session, and in another session he resets the password of the same email, it terminates all open sessions (VERIFY THIS IS THE EXPECTED BEHAVIOR)

### 4) automatic logout during login on different session
- if user is logged in at a browser session and in another session he is logging in again with same email, the first session/token will be terminated. (VERIFY THIS IS THE EXPECTED BEHAVIOR)
- if user is logged in and open a new tab of the same logged in account, if he logs out in one tab, it will terminate the other tab as well


### 5) Extras
- a logged in user that logs out presses the go back page, wont be logged in again.










---






















## 2) Product Search and Filtering
+ Search result accuracy
+ functionality of filter options
+ results are aligned with expected data

<br>

- When making the same search query, the results and their order stay the same.
- drop down in search field is the same as "Discover Products Matching *****"
w

### Filters
#### Individual filters checks
First we will check every filter by itself (then we will test filter combinations)

- price filter low to high works
- price filter high to low works

- 













## 3) Product Detail Page
+ verify the display of 
    + product images
    + descriptions
    + prices
    + user reviews

<br>

- hovering over images and move to image corners -> zoomed in popup
    - use mouse scroll to zoom more in/out

































## 4) Cart Operations


## 5) User Profile


## 6) Compatibility and Performance


# Things to verify
- is it possible to brute force the OTP code? will the API block/rate limit users that try to brute force it? (better create a clickable link that is more random?)


---



# Suggestions and improvements
- have a dedicated "sign up" button
- the "Google" sign in button is an old logo of a deprecated product "Google plus". updating to the current google logo makes sense and will be more intuitive to the users. keeping a logo from 2019 show users the site is unmaintained.
- when an email is filled and it redirects to sign-up, the email field is locked and cant be edited, which is pointless, useless and could be annoying for users that need to fix their email address if a mistake was made. (for the user to fix the email he needs to go to home page and click sign-in again OR click sign in button on top right (the previous page should be the sign in page!))
- make the "Phone" field in signup only accept numbers (so user cant even write letters/characters). will ensure user writes in the correct format the first time
- Dont make the "Send OTP" button clickable if phone field has illegal characters (make it behave the same as the password field)
- dont hide error messages on sign up page. Has only negative effects.
- make error messages appear near relevant field + highlight the field, instead of showing it on the top of the page.

