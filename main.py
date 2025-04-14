import requests
import re
import random
import string
import datetime
from urllib.parse import urlparse, parse_qs
from loguru import logger

session = requests.Session()

def generate_strong_password(length=16):
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    special_chars = "!@#$%^&*()-_=+[]{}|;:,.<>?"
    password = [
        random.choice(lowercase),
        random.choice(uppercase),
        random.choice(digits),
        random.choice(special_chars)
    ]
    remaining_length = length - len(password)
    all_chars = lowercase + uppercase + digits + special_chars
    password.extend(random.choice(all_chars) for _ in range(remaining_length))
    random.shuffle(password)
    return ''.join(password)


def generate_random_birthdate(min_age=18, max_age=65):
    today = datetime.date.today()
    age = random.randint(min_age, max_age)
    year = today.year - age
    birthday_passed = random.choice([True, False])
    if not birthday_passed:
        year += 1
        age -= 1
    month = random.randint(1, 12)
    if month == 2:
        is_leap = (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)
        max_day = 29 if is_leap else 28
    elif month in [4, 6, 9, 11]:
        max_day = 30
    else:
        max_day = 31
    day = random.randint(1, max_day)
    birthdate = datetime.date(year, month, day)
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    return birthdate.strftime("%Y-%m-%d"), str(age)

def getTokens():
    response = session.get('https://www.tumblr.com/?source=explore_floating_sign_up')
    text = response.text
    return text.split('"csrfToken":"')[1].split('"')[0] + ':' + text.split('{"API_TOKEN":"')[1].split('"')[0]

def bypass():
    anchor_url = "https://www.google.com/recaptcha/api2/anchor?ar=1&k=6Ld2ca0UAAAAAKzttOGcjomH-5rBIJesbQrCZtfB&co=aHR0cHM6Ly93d3cudHVtYmxyLmNvbTo0NDM.&hl=en&v=-ZG7BC9TxCVEbzIO2m429usb&size=invisible&cb=2t67bid14v9f"
    reload_url = "https://www.google.com/recaptcha/enterprise/reload?k=6Ld2ca0UAAAAAKzttOGcjomH-5rBIJesbQrCZtfB"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0"
    }
    r = session.get(anchor_url, headers=headers)
    token = re.search(r'id="recaptcha-token" value="([^"]+)"', r.text).group(1)
    params = parse_qs(urlparse(anchor_url).query)
    data = {
        "v": params['v'][0],
        "reason": "q",
        "c": token,
        "k": params['k'][0],
        "co": params['co'][0],
        "hl": "en",
        "size": "invisible"
    }
    headers.update({"Referer": r.url, "Content-Type": "application/x-www-form-urlencoded"})
    r = session.post(reload_url, headers=headers, data=data)
    return re.search(r'\["rresp","([^"]+)"', r.text).group(1) if '["rresp","' in r.text else None

try:
    result = getTokens()
except Exception as e:
    exit(1)

headers = {
    'accept': 'application/json;format=camelcase',
    'authorization': 'Bearer ' + result.split(':')[1],
    'cache-control': 'no-cache',
    'content-type': 'application/json; charset=utf8',
    'origin': 'https://www.tumblr.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://www.tumblr.com/?redirect_to=%2F&source=login_register_header_communitiesBrowse',
    'sec-ch-ua': '"Microsoft Edge";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0',
    'x-ad-blocker-enabled': '0',
    'x-csrf': result.split(':')[0],
    'x-version': 'redpop/3/0//redpop/',
}

unique_hash = str(hash(str(result)))[:8].replace('-', '').replace('_', '')
username = 'user' + unique_hash
email = username + '@gmail.com'
password = generate_strong_password()
birth_date, age = generate_random_birthdate()

json_data = {
    'age': age,
    'authentication': 'oauth2_cookie',
    'birth_date': birth_date,
    'email': email,
    'http_referer': 'https://www.google.com/',
    'password': password,
    'redirect_to': '/',
    'source': 'login_register_header_communitiesBrowse',
    'token': bypass(),
    'tumblelog': username,
}

response = session.post('https://www.tumblr.com/api/v2/register/account/validate', headers=headers, json=json_data, allow_redirects=True)
if response.status_code == 200:
    logger.success(f"Account creation successful, {email}:{username}:{password}")
else:
    print(f"\nAccount creation failed with status code: {response.status_code}")
