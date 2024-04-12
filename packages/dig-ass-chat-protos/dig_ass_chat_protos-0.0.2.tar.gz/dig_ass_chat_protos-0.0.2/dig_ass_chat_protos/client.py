from grpc import insecure_channel
from dig_ass_chat_protos.DigitalAssistantChat_pb2_grpc import DigitalAssistantChatStub
from dig_ass_chat_protos.DigitalAssistantChat_pb2 import DigitalAssistantChatRequest, DigitalAssistantChatResponse, OuterContextItem


class ChatClient:

    def __init__(self, address: str) -> None:
        self._channel = insecure_channel(address)
        self._stub = DigitalAssistantChatStub(self._channel)

    def __call__(self, requestDict: dict):

        request = packageRequestDict(requestDict)
        response: DigitalAssistantChatResponse = self._stub.GetTextResponse(request)
        return response.Text

    # https://stackoverflow.com/a/65131927
    def close(self):
        self._channel.close()

    def __enter__(self):
        return self

    def __exit__(self):
        self.close()


def packageRequestDict(requestDict: dict) -> DigitalAssistantChatRequest:
    """
    requestDict must have the following structure
    {
        "text":,
        "outerContext":{
            "sex":,
            "age":,
            "userId":,
            "sessionId"
        }
    }
    """

    # populate outer context
    outerContextDict = requestDict["outerContext"]
    outerContext = OuterContextItem(Sex=outerContextDict["sex"], Age=outerContextDict["age"], UserId=outerContextDict["userId"], SessionId=outerContextDict["sessionId"])

    # populate final request
    request = DigitalAssistantChatRequest(Text=requestDict["text"], OuterContext=outerContext)

    return request
