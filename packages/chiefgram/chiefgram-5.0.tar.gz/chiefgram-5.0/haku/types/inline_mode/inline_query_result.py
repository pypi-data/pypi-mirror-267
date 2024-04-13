#  Pyrofork - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#  Copyright (C) 2022-present Mayuri-Chan <https://github.com/Mayuri-Chan>
#
#  This file is part of Pyrofork.
#
#  Pyrofork is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrofork is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrofork.  If not, see <http://www.gnu.org/licenses/>.

from uuid import uuid4

import haku
from haku import types
from ..object import Object


class InlineQueryResult(Object):
    """One result of an inline query.

    - :obj:`~haku.types.InlineQueryResultCachedAudio`
    - :obj:`~haku.types.InlineQueryResultCachedDocument`
    - :obj:`~haku.types.InlineQueryResultCachedAnimation`
    - :obj:`~haku.types.InlineQueryResultCachedPhoto`
    - :obj:`~haku.types.InlineQueryResultCachedSticker`
    - :obj:`~haku.types.InlineQueryResultCachedVideo`
    - :obj:`~haku.types.InlineQueryResultCachedVoice`
    - :obj:`~haku.types.InlineQueryResultArticle`
    - :obj:`~haku.types.InlineQueryResultAudio`
    - :obj:`~haku.types.InlineQueryResultContact`
    - :obj:`~haku.types.InlineQueryResultDocument`
    - :obj:`~haku.types.InlineQueryResultAnimation`
    - :obj:`~haku.types.InlineQueryResultLocation`
    - :obj:`~haku.types.InlineQueryResultPhoto`
    - :obj:`~haku.types.InlineQueryResultVenue`
    - :obj:`~haku.types.InlineQueryResultVideo`
    - :obj:`~haku.types.InlineQueryResultVoice`
    """

    def __init__(
        self,
        type: str,
        id: str,
        input_message_content: "types.InputMessageContent",
        reply_markup: "types.InlineKeyboardMarkup"
    ):
        super().__init__()

        self.type = type
        self.id = str(uuid4()) if id is None else str(id)
        self.input_message_content = input_message_content
        self.reply_markup = reply_markup

    async def write(self, client: "haku.Client"):
        pass
