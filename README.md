# YouTubeDownloads_bot
YoutubeDownloadsBot source!


This bot using:
PyTube
MoviePy
Flask
pyTelegramBotAPI

It's a test version. And bot has some bugs. I keep working on it.



# How works this bot

1) The user sends a "/start" command then the bot asks him a URL.
2) Then user sends URL video and bot ask him about File Format.
3) if user choose the "mp4" format, bot download the first stream in resolution 720p or 360p(depends on the video stream)
Unfortunately, other streams with different resolutions do not have an audio codec. Only 720 or 360! And it seems like I’m guessing how to fix it.
if a user chooses the "mp3" format, bot downloads the first stream in resolution 720p or 360p. And then the bot convert "mp4" to "mp3"(moviepy)!
4) Bot send video or audio and delete downloaded files from the server.
