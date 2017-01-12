SETUP
=======


### OSX

notification için `terminal-notifier` kullanılıyor bunun yüklenmesi lazım.
https://github.com/julienXX/terminal-notifier

	> brew install terminal-notifier

sürekli çalıştırabilmek için de `watch` komutunu kullanıyorum bunun da yüklenmesi lazım.
http://unix.stackexchange.com/a/10650/208791

	> brew install watch


#### python gereksinimleri

Daha temiz bir ortam için `virtualenv` gerekli.
https://virtualenv.pypa.io/en/stable/installation/

	> virtualenv venv
	> source venv/bin/activate
	> pip install -r python_reqs.txt


###### Çalıştırmak için:

	> watch --interval=120 bash check.sh

o dizinin içinde bu komut çalıştırılır. 120 --> 120 saniye
