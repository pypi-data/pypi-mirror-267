from grpc import insecure_channel
from google.protobuf.json_format import MessageToDict, ParseDict
from dig_ass_ep_protos.DigitalAssistantEntryPoint_pb2_grpc import DigitalAssistantEntryPointStub
from dig_ass_ep_protos.DigitalAssistantEntryPoint_pb2 import DigitalAssistantEntryPointRequest, DigitalAssistantEntryPointResponse, OuterContextItem


class EntryPointClient:

    def __init__(self, address: str) -> None:
        self._channel = insecure_channel(address)
        self._stub = DigitalAssistantEntryPointStub(self._channel)

    def __call__(self, text: str, outerContextDict: dict, image: bytearray, pdf: bytearray):

        request = dict2Message(text, outerContextDict, image, pdf)
        response: DigitalAssistantEntryPointResponse = self._stub.GetTextResponse(request)
        responseDict = message2Dict(response)

        return responseDict["Text"]

    # https://stackoverflow.com/a/65131927
    def close(self):
        self._channel.close()

    def __enter__(self):
        return self

    def __exit__(self):
        self.close()


def dict2Message(text: str, outerContextDict: dict, image: bytearray, pdf: bytearray) -> DigitalAssistantEntryPointRequest:

    messageDict = {"Text": text, "OuterContext": outerContextDict, "Image": image, "PDF": pdf}
    message = ParseDict(messageDict, DigitalAssistantEntryPointRequest())
    return message


def message2Dict(message: DigitalAssistantEntryPointResponse) -> dict:

    messageDict = MessageToDict(message, preserving_proto_field_name=True, use_integers_for_enums=False, including_default_value_fields=True)
    return messageDict
