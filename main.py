import requests
from bs4 import BeautifulSoup

from datetime import datetime

DOLLAR = True


def main():

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

	t = requests.get("https://www.ziraatbank.com.tr/tr/_layouts/15/Ziraat/HomePage/Ajax.aspx/GetZiraatVerileri", headers=headers, cookies=r.cookies)


	if not t.status_code == 200:
		print("yok")
		return False

	try:
		soup = BeautifulSoup(t.json()['d']['Data'], 'html.parser')
	except Exception as e:
		print("yok")
		return False


	if DOLLAR:
		try:
			amount = soup.find(text="AMERIKAN DOLARI").parent.find_next_sibling().find(text="BANKA ALIŞ").parent.find_next_sibling().text.strip()
			satin_alma = soup.find(text="AMERIKAN DOLARI").parent.find_next_sibling().find(text="BANKA SATIŞ").parent.find_next_sibling().text.strip()
			update_date = soup.find(text="Makroekonomik Analizler").parent.find_previous_sibling().text.strip()
		except Exception as e:
			print("yok")
			return False
	else:
		try:
			amount = soup.find(text="A02 ALTIN (1000/1000)").parent.find_next_sibling().find(text="BANKA ALIŞ").parent.find_next_sibling().text.strip()
			satin_alma = soup.find(text="A02 ALTIN (1000/1000)").parent.find_next_sibling().find(text="BANKA SATIŞ").parent.find_next_sibling().text.strip()
			update_date = soup.find(text="Makroekonomik Analizler").parent.find_previous_sibling().text.strip()
		except Exception as e:
			print("yok")
			return False

	# ------------- read latest amount -----------------
	latest_amount = None
	try:

		file = open("latest_amount.txt", mode="r")
		latest_amount = file.read().strip()

	except Exception as e: pass
	# --------------------------------------------------

	# if latest amount equls new then do nothing
	if latest_amount == amount:
		print("yok")
		return False

	# --------- store latest amount --------------------
	file = open("latest_amount.txt", mode="w")
	file.write(amount)
	file.close()
	# --------------------------------------------------

	# ------------ store new amount --------------------
	if DOLLAR:
		file = open("amounts_dollar.txt", mode="a")
	else:
		file = open("amounts.txt", mode="a")
	file.write("%s||%s||%s\n" % (amount, update_date, ("%s" % datetime.now()).split(".")[0]))
	file.close()
	# --------------------------------------------------

	# ---------- get differenece ------------------------
	diff = 0
	try:
		diff = float(amount.replace(",", ".")) - float(latest_amount.replace(",", "."))
	except Exception as e: pass

	print("%s / %s - %s\n%s" % (latest_amount, amount, satin_alma, round(diff, 4)))

main()
