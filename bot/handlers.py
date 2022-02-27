from bot.helpers.genius import Genius
from bot.schema import IncomingMessageSchema


def registration(message: IncomingMessageSchema):
    return f'Welcome {message.senderName if message.senderName is not None else ""} to our super duper nice bot. Type ' \
           f'"lyrics" to get lyrics. '


def lyrics(message: IncomingMessageSchema):
    text = message.body
    search_term = ' '.join(text.split()[1:])
    genius = Genius()

    sid = genius.search_song(search_term)
    if 'Could not find' in sid:
        return 'Could not find lyrics'
    try:
        song_id = sid['song_id']
        song_lyrics = genius.lyrics(song_id)
    except IndexError:
        return "Could not find lyrics"

    return song_lyrics
