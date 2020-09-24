# CommanderBot

Command-line interface for running an instance of CommanderBot.

## Running your bot

You can run your own bot without writing any code.

You will need the following:

1. Your own [Discord Application](https://discordapp.com/developers/applications) with a bot token.
2. A [configuration file](configuring-your-bot) for the bot.
3. A Python 3.8+ environment with the `commanderbot` package installed.
    - It is recommended to use a [virtual environment](https://docs.python.org/3/tutorial/venv.html) for this.
    - Run `pip install commanderbot` to install the bot core package.
4. (Optional) The `commanderbot-ext` package; if you are using any of the provided extensions.
    - Run `pip install commanderbot-ext` to install the bot extensions package.

The first thing you should do is check the CLI help menu:

```bash
python -m commanderbot --help
```

There are three ways to provide your bot token:
1. (Recommended) As the `BOT_TOKEN` environment variable: `BOT_TOKEN=put_your_bot_token_here`
2. As a CLI option: `--token put_your_bot_token_here`
3. Manually, when prompted during start-up

Here's an example that provides the bot token as an argument:

```bash
python -m commanderbot bot.json --token put_your_bot_token_here
```
