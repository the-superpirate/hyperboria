import asyncio
import logging

from izihawa_utils.pb_to_json import MessageToDict
from library.telegram.base import RequestContext
from nexus.models.proto.operation_pb2 import \
    DocumentOperation as DocumentOperationPb
from nexus.models.proto.operation_pb2 import Vote as VotePb
from nexus.translations import t
from telethon import events

from .base import BaseCallbackQueryHandler


class VoteHandler(BaseCallbackQueryHandler):
    filter = events.CallbackQuery(pattern='^/vote([ab])?_([A-Za-z0-9]+)_([0-9]+)_([bo])$')

    def parse_pattern(self, event: events.ChatAction):
        short_schema = event.pattern_match.group(1)
        schema = self.short_schema_to_schema(short_schema.decode()) if short_schema else None
        session_id = event.pattern_match.group(2).decode()
        document_id = int(event.pattern_match.group(3).decode())
        vote = event.pattern_match.group(4).decode()
        vote_value = {'b': -1, 'o': 1}[vote]

        return schema, session_id, document_id, vote, vote_value

    async def handler(self, event: events.ChatAction, request_context: RequestContext):
        schema, session_id, document_id, vote, vote_value = self.parse_pattern(event)

        request_context.add_default_fields(mode='vote', session_id=session_id)
        request_context.statbox(
            action='vote',
            document_id=document_id,
            query=vote,
            schema=schema,
        )

        document_operation_pb = DocumentOperationPb(
            vote=VotePb(
                document_id=document_id,
                value=vote_value,
                voter_id=request_context.chat.chat_id,
            ),
        )
        logging.getLogger('operation').info(
            msg=MessageToDict(document_operation_pb),
        )

        message = await event.get_message()

        # ToDo: Generalize nexus.views.telegram.common.remove_button and use it here
        return await asyncio.gather(
            self.application.telegram_client.edit_message(
                request_context.chat.chat_id,
                message.id,
                message.text,
                buttons=None,
            ),
            event.answer(t('TANKS_BRUH')),
        )
