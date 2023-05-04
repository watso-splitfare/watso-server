from dependency_injector.wiring import inject, Provide
from src.common_container import CommonContainer
from logic.common.push_message.application.port.outgoing.TokenQueryDao import TokenQueryDao
from logic.common.push_message.application.port.outgoing.MessagePusher import MessagePusher

from blinker import signal

post_event = signal('post-event')


@post_event.connect_via('ordered')
@inject
def push_ordered_message(sender, users,
                         token_query_dao: TokenQueryDao = Provide[CommonContainer.token_query_dao],
                         message_pusher: MessagePusher = Provide[CommonContainer.message_pusher]):
    tokens = token_query_dao.find_all_registration_token_user_id(users)

    title = '주문이 완료되었습니다!'
    body = '조금만 기다려주세요!'

    message_pusher.send(title, body, tokens)


@post_event.connect_via('delivered')
@inject
def push_delivered_message(sender, users, place,
                           token_query_dao: TokenQueryDao = Provide[CommonContainer.token_query_dao],
                           message_pusher: MessagePusher = Provide[CommonContainer.message_pusher]):
    tokens = token_query_dao.find_all_registration_token_user_id(users)

    title = '배달이 완료되었습니다!'
    body = f'{place}로 와주세요!'

    message_pusher.send(title, body, tokens)
