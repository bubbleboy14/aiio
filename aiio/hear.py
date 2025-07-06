def listen(cb):
	from pocketsphinx import LiveSpeech
	for phrase in LiveSpeech():
		p = str(phrase)
		print(p)
		p and cb(p)
