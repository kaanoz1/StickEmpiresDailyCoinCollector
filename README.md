# StickEmpiresDailyCoinCollector

First of all, if you are not familiar with software, code or similar concepts, you can use any AI in order to get help. They are pretty basic.

## Purpose

This project collects your daily coins in Stick Empires for you. It logs in to the game server on your behalf, checks your empire points (coins), compares them with the previous value and then waits until the next day to do it all over again. This way you do not have to open the game every day.

## Login Credentials

The program does not ask for your username or password. It logs in by sending the same login message your game client sends, so you need that message **in hex format**.

You can get it with the [StickEmpiresLoginMessageExtractor](https://github.com/kaanoz1/StickEmpiresLoginMessageExtractor) project. Follow its instructions and come back here with the hex string it saves into `login_messages.txt`.

> **Warning:** The login message contains your account credentials in hashed form. Do not share it with anyone and never commit it to a repository.

## Prerequisites

- [uv](https://docs.astral.sh/uv/getting-started/installation/) (it also takes care of the required Python version, 3.14 or newer)
- Your login message in hex format (see above)
- A [ntfy](https://ntfy.sh) topic name, only if you want phone notifications (optional, see the Ntfy section)

## Installation and Execution

```bash
git clone https://github.com/kaanoz1/StickEmpiresDailyCoinCollector
cd StickEmpiresDailyCoinCollector
```

Create your `.env` file (see below), then run:

```bash
uv run start
```

The program keeps running and repeats its job by itself, so leave the terminal open.

## .env

Copy `.env-example` to `.env` (`Copy-Item .env-example .env` on PowerShell, `cp .env-example .env` elsewhere) and fill it in:

```env
LOGIN_MESSAGE_IN_HEX=
NTFY_TOPIC_NAME=
```

| Variable               | Required | Description                                                                                                   |
| ---------------------- | -------- | ------------------------------------------------------------------------------------------------------------- |
| `LOGIN_MESSAGE_IN_HEX` | Yes      | The hex string you got from StickEmpiresLoginMessageExtractor. Copy the whole line from `login_messages.txt`. |
| `NTFY_TOPIC_NAME`      | No       | Your ntfy topic name. Leave it empty to disable notifications. See the Ntfy section.                          |

While running, the program also creates `app.log` (logs) and `previous_coin.txt` (the last coin amount it saw) in the folder you run it from.

## How It Works

The project is event based. A loop (`StickEmpiresDailyCoinCollectorLoop`) connects to the server, sends your login message, reads the server's replies and fires an **event** at every important step. For each event you can define a **callback**, a function that runs when that event happens.

Basically:

1. Connect to the server and send the login message.
2. If the server rejects the login, the program notifies you and stops. Your login message is probably invalid or expired, so get a new one with the extractor and run the program again.
3. If the server accepts the login, read your empire points.
4. Compare them with the previous amount in `previous_coin.txt`.
   - **Not changed:** check again in 1 hour.
   - **Changed:** save the new amount and wait about 24 hours until the next run.

Available events (every callback is optional, and can be a normal or an `async` function):

- `callback_execution_started`, `callback_execution_ended`
- `callback_loop_started`, `callback_loop_ended`, `callback_if_loop_timeouted`
- `callback_login_process_started`, `callback_if_login_validated`, `callback_if_login_failed`
- `callback_if_empire_points_found`, `callback_if_no_empire_points_found`
- `callback_previous_state_fetched`, `callback_new_state_saved`
- `callback_if_coin_amount_changed`, `callback_if_coin_amount_not_changed`

Some callbacks receive values as arguments, for example the current coin amount. You can find ready-made examples in [`predefinedCallbacks.py`](src/stick_empires_daily_coin_collection/predefinedCallbacks.py). They are written by the author and you can customize them as you want.

To register your callbacks, edit [`main.py`](src/stick_empires_daily_coin_collection/main.py). Each callback is passed to `StickEmpiresDailyCoinCollectorLoop.run(...)` there.

If you do not know how to write code, you can ask any AI to do it for you. Just give it `predefinedCallbacks.py` and `main.py` and tell it what you want to happen on which event.

## Ntfy (Optional)

[ntfy](https://ntfy.sh) is a free service that sends push notifications to your phone. As the author, I use it to get a notification on my phone every time the program collects coins (and on some other events).

To use it:

1. Install the ntfy app on your phone.
2. Subscribe to a topic with a long, hard to guess name. Anyone who knows the topic name can read its messages.
3. Put the same name into `NTFY_TOPIC_NAME` in your `.env`.

If you do not want notifications, leave `NTFY_TOPIC_NAME` empty in your `.env` and they will be skipped. You can also replace them with another method (Telegram, Discord webhook, e-mail, etc.), the callbacks are yours to change.

## License

This project is licensed under the [MIT License](LICENSE).
