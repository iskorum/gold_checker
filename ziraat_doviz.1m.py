#!/usr/bin/env /usr/local/opt/python@3.8/bin/python3.8

import requests
from bs4 import BeautifulSoup

from datetime import datetime


def get_request():
	r = requests.get("https://www.ziraatbank.com.tr/tr")

	soup = BeautifulSoup(r.text, 'html.parser')

	digest = soup.find(attrs={'id':"__REQUESTDIGEST"}).attrs['value']

	headers = {
		'Pragma': 'no-cache',
		'Accept-Encoding': 'gzip, deflate, br',
		'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
		'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
		'Content-Type': 'core/json',
		'Accept': 'text/plain, */*; q=0.01',
		'Cache-Control': 'no-cache',
		'X-Requested-With': 'JQuery PageEvents',
		'Connection': 'keep-alive',
		'Referer': 'https://www.ziraatbank.com.tr/tr',

		# 'X-RequestDigest': '0xD6885A02A17C90225FB4CC8CD1FC0323D40C28B83B2F8942556C4B5A48FD4FB23C00ADAECC2250B1B67AD05122C80A28A9AC5561414FDE94EE23D0152D4499D5,04 Jul 2018 12:00:11 -0000',
		'X-RequestDigest': digest,
		# 'Cookie': 'BehaviorPad_Profile=26119d6a-d7a3-4b46-838a-1215437d1f49; NSC_OFX_ajsbbucbol.dpn.us_443_WJQ=ffffffffaf181f3845525d5f4f58455e445a4a423660; ASP.NET_SessionId=qar2rqepulvzwrcxzsnq5thz; cerezPolitikasi=1',
	}

	return requests.get("https://www.ziraatbank.com.tr/tr/_layouts/15/Ziraat/HomePage/Ajax.aspx/GetZiraatVerileri", headers=headers, cookies=r.cookies)


def main():
	t = get_request()

	if not t.status_code == 200:
		print("req error")
		return False

	try:
		soup = BeautifulSoup(t.json()['d']['Data']['Html'], 'html.parser')
	except Exception as e:
		print("parse error")
		return False


	try:
		bank_buy = soup.find(text="A02 ALTIN (1000/1000)").parent.find_next_sibling().find(text="BANKA ALIŞ").parent.find_next_sibling().text.strip()
		bank_sell = soup.find(text="A02 ALTIN (1000/1000)").parent.find_next_sibling().find(text="BANKA SATIŞ").parent.find_next_sibling().text.strip()
		update_date = soup.find(text="Makroekonomik Analizler").parent.find_previous_sibling().text.strip()
	except Exception as e:
		print("data error")
		return False

	# ------------- read latest amount -----------------
	latest_amount = None
	try:

		file = open("/Users/yasin/projects/gold_checker/latest_amount.txt", mode="r")
		latest_amount = file.read().strip()

	except Exception as e: pass
	# --------------------------------------------------


	# --------- store latest amount --------------------
	file = open("/Users/yasin/projects/gold_checker/latest_amount.txt", mode="w")
	file.write(bank_buy)
	file.close()
	# --------------------------------------------------


	# ---------- get differenece ------------------------
	diff = 0
	try:
		diff = float(bank_buy.replace(",", ".")) - float(latest_amount.replace(",", "."))
	except Exception as e: pass


	print("%s - %s / %s" % (bank_buy, bank_sell, round(diff, 4)))

if __name__ == "__main__":
    main()
