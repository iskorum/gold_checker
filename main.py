import requests
from bs4 import BeautifulSoup

from datetime import datetime

def main():

	response = requests.get("http://www.ziraat.com.tr/BankData/ZiraatDataTr.htm")

	if not response.status_code == 200:
		print("yok")
		return False

	soup = BeautifulSoup(response.text, 'html.parser')
	try:
		amount = soup.find(text="A02 ALTIN 1000/1000").parent.parent.find_next_sibling().text.strip()
		update_date = soup.find(attrs={"class":"odd first"}).find(attrs={"class":"firstTd"}).text.strip()
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
	file = open("amounts.txt", mode="a")
	file.write("%s||%s||%s\n" % (amount, update_date, ("%s" % datetime.now()).split(".")[0]))
	file.close()
	# --------------------------------------------------

	# ---------- get differenece ------------------------
	diff = 0
	try:
		diff = float(amount.replace(",", ".")) - float(latest_amount.replace(",", "."))
	except Exception as e: pass

	print("%s / %s\n%s" % (latest_amount, amount, diff))

main()
