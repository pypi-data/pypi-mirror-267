import requests
import time

class info_instagram:
    def L7N(user):
    	time_now = int(time.time())
    	csrftoken_url = 'https://i.instagram.com/api/v1/public/landing_info/'
    	csrftoken_headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/105 Version/11.1.1 Safari/605.1.15',
        'X-IG-App-ID': '936619743392459',
    }
    	session = requests.Session()
    	csrftoken_r = session.get(csrftoken_url, headers=csrftoken_headers)
    	cookies = csrftoken_r.cookies.get_dict()
    	mid = cookies['mid']
    	ig_did = cookies['ig_did']
    	csrftoken = cookies['csrftoken']
    	headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15',
        'X-IG-App-ID': '936619743392459',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': f'csrftoken={csrftoken}; ig_did={ig_did}; ig_nrcb=1; mid={mid}',
        'X-CSRFToken': f'{csrftoken}',
    }
    	username = "g_4_q"
    	password = "L7NL7NL7N"
    	url_login = 'https://www.instagram.com/accounts/login/ajax/'
    	data = f'enc_password=#PWD_INSTAGRAM_BROWSER:0:{time_now}:{password}&username={username}&queryParams=%7B%7D&optIntoOneTap=false&stopDeletionNonce=&trustedDeviceRecords=%7B%7D'
    	login = session.post(url_login, headers=headers, data=data)
    	with open('cookies.txt', 'w') as f:
    	       for cookie in session.cookies:
    	       	f.write(f"{cookie.name}={cookie.value}; ")
    	       	headers2 = {
    'X-Pigeon-Session-Id': '50cc6861-7036-43b4-802e-fb4282799c60',
    'X-Pigeon-Rawclienttime': '1700251574.982',
    'X-IG-Connection-Speed': '-1kbps',
    'X-IG-Bandwidth-Speed-KBPS': '-1.000',
    'X-IG-Bandwidth-TotalBytes-B': '0',
    'X-IG-Bandwidth-TotalTime-MS': '0',
    'X-Bloks-Version-Id': '009f03b18280bb343b0862d663f31ac80c5fb30dfae9e273e43c63f13a9f31c0',
    'X-IG-Connection-Type': 'WIFI',
    'X-IG-Capabilities': '3brTvw==',
    'X-IG-App-ID': '567067343352427',
    'User-Agent': 'Instagram 100.0.0.17.129 Android (29/10; 420dpi; 1080x2129; samsung; SM-M205F; m20lte; exynos7904; en_GB; 161478664)',
    'Accept-Language': 'en-GB, en-US',
     'Cookie': 'mid=ZVfGvgABAAGoQqa7AY3mgoYBV1nP; csrftoken=9y3N5kLqzialQA7z96AMiyAKLMBWpqVj',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Accept-Encoding': 'gzip, deflate',
    'Host': 'i.instagram.com',
    'X-FB-HTTP-Engine': 'Liger',
    'Connection': 'keep-alive',
    'Content-Length': '356',
}
    	       	data2 = {
    'signed_body': '0d067c2f86cac2c17d655631c9cec2402012fb0a329bcafb3b1f4c0bb56b1f1f.{"_csrftoken":"9y3N5kLqzialQA7z96AMiyAKLMBWpqVj","adid":"0dfaf820-2748-4634-9365-c3d8c8011256","guid":"1f784431-2663-4db9-b624-86bd9ce1d084","device_id":"android-b93ddb37e983481c","query":"'+user+'"}',
    'ig_sig_key_version': '4',
}
    	       	api_url = f'https://i.instagram.com/api/v1/users/web_profile_info/?username={user}';req = requests.post('https://i.instagram.com/api/v1/accounts/send_recovery_flow_email/',headers=headers2,data=data2,)
    	       	api_headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15',
        'X-IG-App-ID': '936619743392459',
        'Cookie': f'csrftoken={csrftoken}; ig_did={ig_did}; mid={mid}',
    }
    	       	response = session.get(api_url, headers=api_headers)
    	       	rr = response.json()
    	       	Id =rr['data']['user']['id']
    	       	name=rr['data']['user']['full_name']
    	       	bio =rr['data']['user']['biography']
    	       	flos =rr['data']['user']['edge_followed_by']['count']
    	       	flog =rr['data']['user']['edge_follow']['count']
    	       	pr=rr['data']['user']['is_private']
    	       	verifide=rr['data']['user']['is_verified'];business=rr['data']['user']['business_email']
    	       	re = requests.get(f"https://o7aa.pythonanywhere.com/?id={Id}").json();da = re['date'];rest = req.json()['email']
    	       	info_get = {"user":user,"name":name,"id":Id,"private":pr,"date":da,"following":flog,"followers":flos,"bio":bio,"reset":rest,"verifide":verifide,"business_email":business,"Programmer": "Fahal And L7N"}
    	       	return info_get