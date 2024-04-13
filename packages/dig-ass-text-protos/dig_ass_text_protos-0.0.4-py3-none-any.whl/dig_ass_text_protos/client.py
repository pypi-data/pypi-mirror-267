from google.protobuf.json_format import ParseDict
from dig_ass_text_protos.DigitalAssistantText_pb2_grpc import DigitalAssistantTextStub
from dig_ass_text_protos.DigitalAssistantText_pb2 import DigitalAssistantTextRequest, DigitalAssistantTextResponse, ChatItem

from .abstract_client import AbstractClient

class TextClient(AbstractClient):
    def __init__(self, address) -> None:
        super().__init__(address)
        self._stub = DigitalAssistantTextStub(self._channel)

    def __call__(self, text: str, chat: dict):
        request = DigitalAssistantTextRequest(
            Text=text,
            Chat=ParseDict(chat, ChatItem()),
        )
        response: DigitalAssistantTextResponse = self._stub.GetTextResponse(request)
        return response.Text
