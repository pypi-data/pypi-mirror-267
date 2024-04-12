from grpc import insecure_channel
from dig_ass_chat_protos.DigitalAssistantChat_pb2_grpc import DigitalAssistantChatStub
from dig_ass_chat_protos.DigitalAssistantChat_pb2 import DigitalAssistantChatRequest, DigitalAssistantChatResponse, OuterContextItem


class ChatClient:

    def __init__(self, address: str) -> None:
        self._channel = insecure_channel(address)
        self._stub = DigitalAssistantChatStub(self._channel)

    def __call__(self, text: str, outerContextDict: dict):

        request = packageGRPCRequest(text, outerContextDict)
        response: DigitalAssistantChatResponse = self._stub.GetTextResponse(request)
        return response.Text

    # https://stackoverflow.com/a/65131927
    def close(self):
        self._channel.close()

    def __enter__(self):
        return self

    def __exit__(self):
        self.close()


def outerContextDict2GRPC(outerContextDict: dict) -> OuterContextItem:
    """
    outerContextDict must have the following structure
        "outerContext":{
            "sex":,
            "age":,
            "userId":,
            "sessionId"
        }
    """

    # populate outer context
    outerContext = OuterContextItem(Sex=outerContextDict["sex"], Age=outerContextDict["age"], UserId=outerContextDict["userId"], SessionId=outerContextDict["sessionId"])
    return outerContext


def packageGRPCRequest(text: str, outerContextDict: dict) -> DigitalAssistantChatRequest:

    outerContext = outerContextDict2GRPC(outerContextDict)
    # populate request
    request = DigitalAssistantChatRequest(Text=text, OuterContext=outerContext)

    return request
