# suse_msg

This application consumes amqp events and sends them to irc.

## Testing
1. Adjust config at the top of `suse_msg/consume.py`. In particular, change the channel names to prevent disturbing the the real channels.
2. Install dependencies, most notably the `irc` module. It is not packaged under openSUSE but can be installed via `pip install --user irc`.
3. Run `PATH="~/.local/bin:$PATH" suse_msg/consume.py` to start the script using modules installed via `pip install --user`.
