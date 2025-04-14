# Tumblr Account Generator

<img src="https://i.imgur.com/dQsAkhV.png">

---

### ✅ Features:

- Automatically generates strong passwords and valid birthdates
- Bypasses reCAPTCHA v3 challenge using a reload token trick
- Uses Tumblr's public registration API
- Randomizes user details for each registration
- Logs successfully created account with email, username, and password

---

### ⚙️ Requirements:
```python
pip install loguru requests
```

---

### 🛠 Usage:

- Make sure you are connected to a stable network (VPN/proxy recommended for bulk usage).

Run the script:
```
python main.py
```

If successful, you'll see:
```
Account creation successful, user12345678@gmail.com:user12345678:YourSecurePass!
```

---

### 🧠 Notes:

- This script simulates a real browser using headers and proper flow.
- CAPTCHA bypass may not be permanent if Google or Tumblr updates their flow.
- Respect service terms and use responsibly.

---

### ⚠️ Disclaimer
This project has been developed for educational purposes only. Unauthorized system access is strictly prohibited and constitutes a criminal offense. The developer cannot be held responsible for any misuse.
