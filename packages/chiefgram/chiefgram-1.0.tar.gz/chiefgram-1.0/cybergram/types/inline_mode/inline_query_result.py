#  chiefgram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2024-present Dan <https://github.com/delivrance>
#
#  This file is part of chiefgram.
#
#  chiefgram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  chiefgram is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with chiefgram.  If not, see <http://www.gnu.org/licenses/>.

from uuid import uuid4

import chiefgram
from chiefgram import types
from ..object import Object


class InlineQueryResult(Object):
    """One result of an inline query.

    - :obj:`~chiefgram.types.InlineQueryResultCachedAudio`
    - :obj:`~chiefgram.types.InlineQueryResultCachedDocument`
    - :obj:`~chiefgram.types.InlineQueryResultCachedAnimation`
    - :obj:`~chiefgram.types.InlineQueryResultCachedPhoto`
    - :obj:`~chiefgram.types.InlineQueryResultCachedSticker`
    - :obj:`~chiefgram.types.InlineQueryResultCachedVideo`
    - :obj:`~chiefgram.types.InlineQueryResultCachedVoice`
    - :obj:`~chiefgram.types.InlineQueryResultArticle`
    - :obj:`~chiefgram.types.InlineQueryResultAudio`
    - :obj:`~chiefgram.types.InlineQueryResultContact`
    - :obj:`~chiefgram.types.InlineQueryResultDocument`
    - :obj:`~chiefgram.types.InlineQueryResultAnimation`
    - :obj:`~chiefgram.types.InlineQueryResultLocation`
    - :obj:`~chiefgram.types.InlineQueryResultPhoto`
    - :obj:`~chiefgram.types.InlineQueryResultVenue`
    - :obj:`~chiefgram.types.InlineQueryResultVideo`
    - :obj:`~chiefgram.types.InlineQueryResultVoice`
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

    async def write(self, client: "chiefgram.Client"):
        pass
