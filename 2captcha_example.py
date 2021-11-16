import requests

captcha_apikey = "key_here"

def submitCaptcha(site_key):
    link = "http://2captcha.com/in.php?key={}&method=userrecaptcha&googlekey={}&pageurl=https://visitorbookings.hkgolfclub.org/Account/Login".format(captcha_apikey, site_key)
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36'
    }
    try:
        resp = requests.get(link, headers=headers).text
    except:
        print("Failed to open {}".format(link))
        return "-1"
    if resp.startswith('OK'):
        task_id = resp.split('|')[-1]
        print("Captcha submitted for solving, task ID is: {}".format(task_id))
        return task_id
    else:
        print("Recaptcha submit error!")
        print(resp)
        return "-1"


def checkRecaptchaStatus(task_id):
    link = "https://2captcha.com/res.php?key={}&action=get&id={}".format(captcha_apikey, task_id)
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36'
    }
    try:
        resp = requests.get(link, headers=headers).text
    except:
        print("Failed to open {}".format(link))
        return "-1"
    if resp.startswith('OK'):
        task_token = resp.split('|')[-1]
        print("Captcha solved, solve token is: {}".format(task_token))
        return task_token
    else:
        print("Recaptcha solve error!")
        print(resp)
        return "-1"

if __name__ == "__main__":
    site_key = "get the site key from the site and place here"
    task_id = submitCaptcha(site_key)
    while True:
        solve_token = checkRecaptchaStatus(task_id)
        if solve_token != "-1":
            break
        sleep(5)
    # now submit the token with the request
