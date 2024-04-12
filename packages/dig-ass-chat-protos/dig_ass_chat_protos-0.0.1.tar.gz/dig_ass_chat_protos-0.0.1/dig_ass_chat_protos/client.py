from grpc import insecure_channel
from dig_ass_chat_protos.DigitalAssistantChat_pb2_grpc import DigitalAssistantChatStub
from dig_ass_chat_protos.DigitalAssistantChat_pb2 import DigitalAssistantChatRequest, DigitalAssistantChatResponse, OuterContextItem


class ChatClient:

    def __init__(self, address: str) -> None:
        self._channel = insecure_channel(address)
        self._stub = DigitalAssistantChatStub(self._channel)

    def __call__(self, text: str, image: bytearray, pdf: bytearray, sex: bool, age: int, userId: int, sessionId: int):

        outerContext = OuterContextItem(Sex=sex, Age=age, UserId=userId, SessionId=sessionId)
        request = DigitalAssistantChatRequest(Text=text, OuterContext=outerContext, Image=image, PDF=pdf)
        response: DigitalAssistantChatResponse = self._stub.GetTextResponse(request)

        return response.Text

    # https://stackoverflow.com/a/65131927
    def close(self):
        self._channel.close()

    def __enter__(self):
        return self

    def __exit__(self):
        self.close()
