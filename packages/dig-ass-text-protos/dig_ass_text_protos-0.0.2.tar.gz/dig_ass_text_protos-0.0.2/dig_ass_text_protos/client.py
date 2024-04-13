from grpc import insecure_channel
from google.protobuf.json_format import MessageToDict, ParseDict
from dig_ass_text_protos.DigitalAssistantText_pb2_grpc import DigitalAssistantTextStub
from dig_ass_text_protos.DigitalAssistantText_pb2 import DigitalAssistantTextRequest, DigitalAssistantTextResponse


class TextClient:

    def __init__(self, address: str) -> None:
        self._channel = insecure_channel(address)
        self._stub = DigitalAssistantTextStub(self._channel)

    def __call__(self, text: str, chatDict: dict):

        request = dict2Message(text, chatDict)
        response: DigitalAssistantTextResponse = self._stub.GetTextResponse(request)
        responseDict = message2Dict(response)

        return responseDict["Text"]

    # https://stackoverflow.com/a/65131927
    def close(self):
        self._channel.close()

    def __enter__(self):
        return self

    def __exit__(self):
        self.close()


def dict2Message(text: str, chatDict: dict) -> DigitalAssistantTextRequest:

    messageDict = {"Text": text, "Chat": chatDict}
    message = ParseDict(messageDict, DigitalAssistantTextRequest())
    return message


def message2Dict(message: DigitalAssistantTextResponse) -> dict:

    messageDict = MessageToDict(message, preserving_proto_field_name=True, use_integers_for_enums=False, including_default_value_fields=True)
    return messageDict
