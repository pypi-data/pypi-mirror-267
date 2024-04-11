<p align="center">
    <a href="https://github.com/rizaldevs/chiefgram">
        <img src="https://docs.chiefgram.org/_static/chiefgram.png" alt="chiefgram" width="128">
    </a>
    <br>
    <b>Telegram MTProto API Framework for Python</b>
    <br>
    <a href="https://chiefgram.org">
        Homepage
    </a>
    •
    <a href="https://docs.chiefgram.org">
        Documentation
    </a>
    •
    <a href="https://docs.chiefgram.org/releases">
        Releases
    </a>
    •
    <a href="https://t.me/chiefgram">
        News
    </a>
</p>

## chiefgram

> Elegant, modern and asynchronous Telegram MTProto API framework in Python for users and bots

``` python
from chiefgram import Client, filters

app = Client("my_account")


@app.on_message(filters.private)
async def hello(client, message):
    await message.reply("Hello from chiefgram!")


app.run()
```

**chiefgram** is a modern, elegant and asynchronous [MTProto API](https://docs.chiefgram.org/topics/mtproto-vs-botapi)
framework. It enables you to easily interact with the main Telegram API through a user account (custom client) or a bot
identity (bot API alternative) using Python.

### Support

If you'd like to support chiefgram, you can consider:

- [Become a GitHub sponsor](https://github.com/sponsors/rizaldevs).
- [Become a LiberaPay patron](https://liberapay.com/rizaldevs).
- [Become an OpenCollective backer](https://opencollective.com/chiefgram).

### Key Features

- **Ready**: Install chiefgram with pip and start building your applications right away.
- **Easy**: Makes the Telegram API simple and intuitive, while still allowing advanced usages.
- **Elegant**: Low-level details are abstracted and re-presented in a more convenient way.
- **Fast**: Boosted up by [tgcyber](https://github.com/rizaldevs/tgcyber), a high-performance cryptography library written in C.  
- **Type-hinted**: Types and methods are all type-hinted, enabling excellent editor support.
- **Async**: Fully asynchronous (also usable synchronously if wanted, for convenience).
- **Powerful**: Full access to Telegram's API to execute any official client action and more.

### Installing

``` bash
pip3 install chiefgram
```

### Resources

- Check out the docs at https://docs.chiefgram.org to learn more about chiefgram, get started right
away and discover more in-depth material for building your client applications.
- Join the official channel at https://t.me/chiefgram and stay tuned for news, updates and announcements.
