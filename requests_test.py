import requests

def request_get_content(url):
    try:
        response = requests.get(
            url, headers={'Content-Type': 'application/json'})
        print(response.status_code, response.headers['Content-Type'])
        print(response.json())

    except:
        print('通信に失敗')
        raise

def request_post_content(url):
    try:
        data = {
            'x': 3,
            'y': 4,
        }
        response = requests.post(
            url, json=data)
        print(response.status_code, response.headers)

    except:
        print('通信に失敗')
        raise

if __name__ == '__main__':
    url1 = 'https://selfcare_prot-1-v6064451.deta.app/'
    url2 = 'http://127.0.0.1:8000'

    request_post_content(url1)
