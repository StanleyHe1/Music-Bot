**Discord music bot for personal use**

Set ffmpeg as the enrionmental variable or include the ffmpeg executable within the same directory\
[`ffmpeg`](https://ffmpeg.org/download.html) will be required for this the execution

Install the libraries required through\
`pip install discord`\
`pip install PyNaCl`\
`pip install yt_dlp`

To run the bot, simply cd to the bot and run the command:\
`python main.py`

**The bot uses the discord developer TOKEN, please set the TOKEN into the environment yourself as TOKEN or change it in main.py**

The command of the bot is as follows:\
`General commands:`\
`!help - displays all the available commands`\
`!q - displays the current music queue`\
`!p <keywords> - finds the song on youtube and plays it in your current channel. Will resume playing the current song if it was paused`\
`!skip - skips the current song being played`\
`!clear - Stops the music and clears the queue`\
`!leave - Disconnect the bot from the voice channel`\
`!pause - pauses the current song being played or resumes if already paused`\
`!resume - resumes playing the current song`

