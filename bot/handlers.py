import logging

from requests import HTTPError

from bot.helpers.genius import Genius
from bot.schema import IncomingMessageSchema


logger = logging.getLogger(__name__)


def registration(message: IncomingMessageSchema, cfg: dict):
    return f'Welcome {message.senderName if message.senderName is not None else ""} to our super duper nice bot. Type ' \
           f'"lyrics" to get lyrics. '


def lyrics(message: IncomingMessageSchema, cfg: dict):
    text = message.body
    search_term = ' '.join(text.split()[1:])
    genius = Genius(cfg)
    logger.info(f'searching lyrics for {search_term}')
    sid = genius.search_song(search_term)
    if 'Could not find' in sid:
        return 'Could not find lyrics'
    try:
        song_id = sid['song_id']
        song_lyrics = genius.lyrics(song_id)
    except IndexError as e:
        logger.warning(str(e))
        return "Could not find lyrics"
    except Exception as e:
        logger.exception(str(e))
        return "Error getting lyrics. Try again some time later"

    return song_lyrics
