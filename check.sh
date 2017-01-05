source venv/bin/activate
amount=$(python main.py)

echo $amount

if [ "$amount" != "yok" ] ; then
	terminal-notifier -sound default -title "Altın" -message $amount
fi
