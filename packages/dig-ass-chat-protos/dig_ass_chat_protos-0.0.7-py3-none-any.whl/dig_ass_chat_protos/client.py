from google.protobuf.json_format import ParseDict
from dig_ass_chat_protos.DigitalAssistantChatManager_pb2_grpc import DigitalAssistantChatManagerStub
from dig_ass_chat_protos.DigitalAssistantChatManager_pb2 import DigitalAssistantChatManagerRequest, DigitalAssistantChatManagerResponse, OuterContextItem

from .abstract_client import AbstractClient

class ChatManagerClient(AbstractClient):
    def __init__(self, address) -> None:
        super().__init__(address)
        self._stub = DigitalAssistantChatManagerStub(self._channel)

    def __call__(self, text: str, outer_context: dict):
        request = DigitalAssistantChatManagerRequest(
            Text=text,
            OuterContext=ParseDict(outer_context, OuterContextItem()),
        )
        response: DigitalAssistantChatManagerResponse = self._stub.GetTextResponse(request)
        return response.Text
