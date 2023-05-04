import requests

dbc_username = "username here"  # deathbycaptcha username
dbc_password = "password here"  # deathbycaptcha password
target_site_link = "https://link to the login/form that contains captcha"

def submitCaptcha(site_key):
    link = "http://api.dbcapi.me/api/captcha"
    headers = {
        'Expect': '',
        'Content-Type': 'application/x-www-form-urlencoded',
        'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36'
    }
    data = {
        'username': dbc_username,
        'password': dbc_password,
        'type': '4',
        'token_params': '{"googlekey": "' + site_key + '", "pageurl": "' + target_site_link + '", "action": "verify","min_score": 0.3}'
    }
    try:
        resp = requests.post(link, headers=headers, data=data).text
    except:
        print("Failed to open {}".format(link))
        return "-1"
    task_id = re.findall(r'captcha=(.+?)&', resp)
    if len(task_id) == 1:
        print("Captcha submitted! Task id is: {}".format(task_id[0]))
        return task_id[0]
    else:
        print("Recaptcha submit error!")
        return "-1"


def checkRecaptchaStatus(task_id):
    link = "http://api.dbcapi.me/api/captcha/{}".format(task_id)
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36'
    }
    try:
        resp = requests.get(link, headers=headers).text
    except:
        print("Failed to open {}".format(link))
        return "-1"
    result_token = re.findall(r'&text=(.+?)&', resp)
    if len(result_token) == 1:
        print("Captcha solved! Result token is: {}".format(result_token[0]))
        return result_token[0]
    else:
        print("Captcha not ready yet! Returned value is: {}".format(resp))
        return "-1"

if __name__ == "__main__":
    site_key = "get the site key and place here"
    task_id = submitCaptcha(site_key)
    if task_id == '-1':
        print("fails to submit the captcha")
        exit(0)
    sleep(15)
    while True:
        solve_token = checkRecaptchaStatus(task_id)
        if solve_token != "-1":
            break
        sleep(5)
    # now send the solve_token with the request
