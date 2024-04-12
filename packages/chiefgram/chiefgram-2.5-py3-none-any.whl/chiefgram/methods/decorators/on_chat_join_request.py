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

from typing import Callable

import chiefgram
from chiefgram.filters import Filter


class OnChatJoinRequest:
    def on_chat_join_request(
        self=None,
        filters=None,
        group: int = 0
    ) -> Callable:
        """Decorator for handling chat join requests.

        This does the same thing as :meth:`~chiefgram.Client.add_handler` using the
        :obj:`~chiefgram.handlers.ChatJoinRequestHandler`.

        Parameters:
            filters (:obj:`~chiefgram.filters`, *optional*):
                Pass one or more filters to allow only a subset of updates to be passed in your function.

            group (``int``, *optional*):
                The group identifier, defaults to 0.
        """

        def decorator(func: Callable) -> Callable:
            if isinstance(self, chiefgram.Client):
                self.add_handler(chiefgram.handlers.ChatJoinRequestHandler(func, filters), group)
            elif isinstance(self, Filter) or self is None:
                if not hasattr(func, "handlers"):
                    func.handlers = []

                func.handlers.append(
                    (
                        chiefgram.handlers.ChatJoinRequestHandler(func, self),
                        group if filters is None else filters
                    )
                )

            return func

        return decorator
