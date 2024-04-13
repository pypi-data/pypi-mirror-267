from grpc import insecure_channel
from google.protobuf.json_format import MessageToDict, ParseDict
from dig_ass_chat_protos.DigitalAssistantChatManager_pb2_grpc import DigitalAssistantChatStub
from dig_ass_chat_protos.DigitalAssistantChatManager_pb2 import DigitalAssistantChatRequest, DigitalAssistantChatResponse


class ChatManagerClient:

    def __init__(self, address: str) -> None:
        self._channel = insecure_channel(address)
        self._stub = DigitalAssistantChatStub(self._channel)

    def __call__(self, text: str, outerContextDict: dict):

        request = dict2Message(text, outerContextDict)
        response: DigitalAssistantChatResponse = self._stub.GetTextResponse(request)
        responseDict = message2Dict(response)

        return responseDict["Text"]

    # https://stackoverflow.com/a/65131927
    def close(self):
        self._channel.close()

    def __enter__(self):
        return self

    def __exit__(self):
        self.close()


def dict2Message(text: str, outerContextDict: dict) -> DigitalAssistantChatRequest:

    messageDict = {"Text": text, "OuterContext": outerContextDict}
    message = ParseDict(messageDict, DigitalAssistantChatRequest())
    return message


def message2Dict(message: DigitalAssistantChatResponse) -> dict:

    messageDict = MessageToDict(message, preserving_proto_field_name=True, use_integers_for_enums=False, including_default_value_fields=True)
    return messageDict
