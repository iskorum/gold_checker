source venv/bin/activate
amount=$(python main.py)

echo $amount


sendNotification() {
	# if it is osx
	if hash terminal-notifier 2>/dev/null; then
		terminal-notifier -sound default -appIcon "./ziraat_amblem.png" -title "Altın" -message "$amount"
	# if it is linux
	elif hash notify-send 2>/dev/null; then
		notify-send -i terminal "Altın" "$amount"
	fi
}


if [ "$amount" != "yok" ] ; then
	sendNotification
fi
