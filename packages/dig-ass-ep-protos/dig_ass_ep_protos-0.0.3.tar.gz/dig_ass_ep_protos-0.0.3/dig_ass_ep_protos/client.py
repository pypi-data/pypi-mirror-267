from grpc import insecure_channel
from dig_ass_ep_protos.DigitalAssistantEntryPoint_pb2_grpc import DigitalAssistantEntryPointStub
from dig_ass_ep_protos.DigitalAssistantEntryPoint_pb2 import DigitalAssistantEntryPointRequest, DigitalAssistantEntryPointResponse, OuterContextItem


class EntryPointClient:

    def __init__(self, address: str) -> None:
        self._channel = insecure_channel(address)
        self._stub = DigitalAssistantEntryPointStub(self._channel)

    def get_stub(self):
        return self._stub

    def __call__(self, text: str, image: bytearray, pdf: bytearray, sex: bool, age: int, userId: int, sessionId: int):

        outerContext = OuterContextItem(Sex=sex, Age=age, UserId=userId, SessionId=sessionId)
        request = DigitalAssistantEntryPointRequest(Text=text, OuterContext=outerContext, Image=image, PDF=pdf)
        response: DigitalAssistantEntryPointResponse = self.get_stub().GetTextResponse(request)

        return response.Text

    # https://stackoverflow.com/a/65131927
    def close(self):
        self._channel.close()

    def __enter__(self):
        return self

    def __exit__(self):
        self.close()
