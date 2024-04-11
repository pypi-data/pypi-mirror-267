<h1 align="center">AmioLightPy</h1>

![gif](https://d142ifyzxiteda.cloudfront.net/s3qk21%2Fpreview%2F57156938%2Fmain_large.gif?response-content-disposition=inline%3Bfilename%3D%22main_large.gif%22%3B&response-content-type=image%2Fgif&Expires=1712770066&Signature=LGr3nJ2CpCtpLryFHYP7rZlXtHFEfad9BbpxIXBAo0W7LBbdVQaLxNQHYmZHGpDNc67aec9sdJuXBnA3sA9KS3DvbLkNOTPaJwUNoVOF1MGxiX30TUto57peJ0lI99vFQwfeSZJF6FW6Q02YfgVhXa12L30mCZv49jFp0crKkMfBx85jOJMuYLbMdNNBHAsB3RKIj6a9ISNIxcJSZ2RyZCmqA8DqkDIdyBOZmodgS3TsL~orHDMwNdL6OSsKqBA3P5gT67erTrSGJM9Aw4ijC~SQADAmBdgpuT3YRx2J4ZOg9hGHAYb37gpTCc~KP8Ea3fl4xJzrlBVpXZrigccc-w__&Key-Pair-Id=APKAJT5WQLLEOADKLHBQ)

<p align="center">
AminoApps python framework to create bots and scripts easily.
</p>

<p align="center">
    <a href="https://github.com/AugustLigh/AminoLightPy/releases"><img src="https://img.shields.io/github/release/AugustLigh/AminoLightPy.svg" alt="GitHub release" />
    <a href="https://aminopy.readthedocs.io/en/latest/index.html"><img src="https://img.shields.io/website?down_message=failing&label=docs&up_color=green&up_message=passing&url=https://aminopy.readthedocs.io/en/latest/index.html" alt="Docs" /></a>
    <a href="https://github.com/AugustLigh/AminoLightPy/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="licence" /></a>
</p>

<p align="center">
  <a href="#features">Features</a> •
  <a href="#usage">Usage</a> •
  <a href="#example">Example</a> •
  <a href="#notes">Notes</a>
  <br>
  <a href="https://aminopy.readthedocs.io/en/latest/index.html" target="_blank">Documentation</a>
</p>

<h2 align="center">Features</h2>

*  ⚡ **Optimization** : Most of the code has been rewritten.
* ⚙ **Backward compatibility** : Write code with correct syntax.
* 🎮 **Commands support** : Go even further with new requests.

<h2 align="center">Usage</h2>

Install the package :

`pip install amino.light.py`

---

Import the `Client` and `SubClient` objects into your bot's code, and create your own help manual :

```py
from AminoLightPy import Client, SubClient
# Your help message
help_message = """
Welcome!
This is help page.
"""
# Create Client object
client = Client()
# Login into account
client.login("example_mail@gmail.com", "example_password")
# And display the help !
@client.event("on_text_message")
def on_message(data):
	if data.message.author.userId != client.profile.userId:  # Do not answer to myself
		# Create SubClient object
		sub_client = SubClient(comId=data.comId, profile=client.profile)
		if data.message.content.startswith('/help'):
			sub_client.send_message(chatId=data.message.chatId, message=help_message)
```

<h2 align="center">Example</h2>

Simply copy code above, and type `/help` in the chat.

Also, take a look at the code for this interactive help !

---

If you can't find what you're looking for or need help with this library, you can [telegram me](https://t.me/augustlight) or an Discord - *engineer48*. We will be glad to help !


<h2 align="center">Notes</h2>

* *This is not my project. Amino libraries already existed before me. I just wanted to create a simple and effective way to support bots*

* *This is working only with the Python.*