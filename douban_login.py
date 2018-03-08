import requests
from bs4 import BeautifulSoup


def download_html(url, username, password):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0',
               'Referer': 'https://www.douban.com/accounts/login'}
    data = {
            "source": "index_nav",
            "redir": "https://www.douban.com/?p=1&",
            "login": "登陆",
            "form_email": username,
            "form_password": password}

    my_session = requests.Session()
    my_session.post(url, data=data, headers=headers)      # 方法1：提交表单
    resp = my_session.get('https://www.douban.com/')

    captcha_id, captcha_solution = parse_html(resp.text)
    while captcha_id:
        data['captcha-id'] = captcha_id
        data['captcha-solution'] = captcha_solution
        print(data)
        my_session.post(url, data=data, headers=headers)
        resp = my_session.get('https://www.douban.com/')
        captcha_id, captcha_solution = parse_html(resp.text)
        if captcha_id:
            data['captcha_id'] = captcha_id
            data['captcha_solution'] = captcha_solution
            print(data)
            my_session.post(url, data=data, headers=headers)
            resp = my_session.get('https://www.douban.com/')
    return resp.text


def parse_html(html):
    soup = BeautifulSoup(html, 'lxml')
    captcha_block = soup.find('div', attrs={'class': 'captcha_block'})
    if captcha_block:
        captcha_id = captcha_block.find_all('input')[1]['value']
        login = soup.find('div', attrs={'class': 'login'})
        try:
            captcha_img_url = login.find('img')['src']
            print(captcha_img_url)
            captcha_img = requests.get(captcha_img_url)
            with open('logo.jpg', 'wb') as f:
                f.write(captcha_img.content)
            captcha_solution = input('请输入验证码:')
            print(captcha_id, captcha_solution)
            return captcha_id, captcha_solution
        except Exception as e:
            return None, None
    else:
        return None, None


def main():
    url = 'https://www.douban.com/accounts/login'
    username = input("请输入用户账号:")
    password = input("请输入用户密码:")
    html = download_html(url, username, password)
    print(html)


if __name__ == '__main__':
    main()
