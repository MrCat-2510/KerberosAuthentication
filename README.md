# KerberosAuthentication

## Description
This is a small project that I use for my Security Midterm examination. The teacher ask us to create demo system to demonstrate our topic, because GUI in Python so difficult so I code Web instead. I spend too much time for this project so I decide to push it to github like a small project so it help me feel my work is not wasted.
This project is use **Python Flask** as the main GUI. Encryption algorithms use in this project:
- **cryptograhy.fernet**: use Fernet to create encrypted message and also use Fernet.generate key to create session key, and Token
- **base64** & **os**: use **base64** to encrypt the privated key of Alice and Server. Because I want to create a secret key based on the user name and password of Alice, so I create a string name **Text_String** that contain Alice's username and Alice's password then merge with random characters was created by **os** and then use **based64** to convert it to b64encode so Fernet can use this key to encrypt and decrypt the message. The number with random characters of os is equal (32 - length of **Text_String**).

## How to run it
###**Step 1**: Install Python Flask, cryptography.fernet, base64, os
###**Step 2**: use this command line 
```
python "app.py"

```
=> we have a result like this:
```
 * Serving Flask app 'app' (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 101-980-169
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 ```
###**Step 3**: go to the link http://127.0.0.1:5000/ . You will see the GUI like this:
 ![image](https://user-images.githubusercontent.com/58814046/140594891-19dbb06e-9811-4ac9-8892-ac0e1bc7c21a.png)
###**Step 4**: Follow the tutorial and the demo project is done.
###**Step 5**: Press Ctrl+C to quit. If you cannot turn off the Port, open cmd again and do below code, <PORT> = 5000, after you run first line, take <PID> of a PORT and pass it to the second line.
```
netstat -ano | findstr :<PORT>
taskkill /PID <PID> /F

```
 
 
