#  chiefgram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2024-present Dan <https://github.com/rizaldevs>
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

from io import BytesIO

from chiefgram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from chiefgram.raw.core import TLObject
from chiefgram import raw
from typing import List, Optional, Any

# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #


class ChatInviteAlready(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~chiefgram.raw.base.ChatInvite`.

    Details:
        - Layer: ``158``
        - ID: ``5A686D7C``

    Parameters:
        chat (:obj:`Chat <chiefgram.raw.base.Chat>`):
            N/A

    Functions:
        This object can be returned by 1 function.

        .. currentmodule:: chiefgram.raw.functions

        .. autosummary::
            :nosignatures:

            messages.CheckChatInvite
    """

    __slots__: List[str] = ["chat"]

    ID = 0x5a686d7c
    QUALNAME = "types.ChatInviteAlready"

    def __init__(self, *, chat: "raw.base.Chat") -> None:
        self.chat = chat  # Chat

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "ChatInviteAlready":
        # No flags
        
        chat = TLObject.read(b)
        
        return ChatInviteAlready(chat=chat)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.chat.write())
        
        return b.getvalue()
