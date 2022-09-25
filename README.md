## Meme Machine

This is a bot that scrapes Reddit for the top memes, then combines them into a compilation video. It then generates
a thumbnail, description, title and other such metadata and uploads the video to your YouTube channel!

### Running
1. Modify the `config.txt` file to your liking
2. Add your YouTube API credentials in the specified folder (specified in `config.txt`). You can generate these
credentials at `console.cloud.google.com`
3. Run `pip install -r requirements.txt` to install all the necessary dependencies.
4. Open a terminal, and type ```python -m src.main```.
5. The bot will begin running, when prompted click on the login link to log into your Google account and select 
the YouTube channel to upload to.