source venv/bin/activate
amount=$(python main.py)

echo $amount

if [ "$amount" != "yok" ] ; then
	terminal-notifier -title "Altın" -message $amount
fi
