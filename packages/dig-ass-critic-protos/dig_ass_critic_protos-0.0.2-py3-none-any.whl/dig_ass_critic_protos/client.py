from grpc import insecure_channel
from google.protobuf.json_format import MessageToDict, ParseDict
from dig_ass_critic_protos.DigitalAssistantCritic_pb2_grpc import DigitalAssistantCriticStub
from dig_ass_critic_protos.DigitalAssistantCritic_pb2 import DigitalAssistantCriticRequest, DigitalAssistantCriticResponse


class CriticClient:

    def __init__(self, address: str) -> None:
        self._channel = insecure_channel(address)
        self._stub = DigitalAssistantCriticStub(self._channel)

    def __call__(self, text: str, chatDict: dict):

        request = dict2Message(text, chatDict)
        response: DigitalAssistantCriticResponse = self._stub.GetTextResponse(request)
        responseDict = message2Dict(response)

        return responseDict["Score"]

    # https://stackoverflow.com/a/65131927
    def close(self):
        self._channel.close()

    def __enter__(self):
        return self

    def __exit__(self):
        self.close()


def dict2Message(text: str, chatDict: dict) -> DigitalAssistantCriticRequest:

    messageDict = {"Text": text, "Chat": chatDict}
    message = ParseDict(messageDict, DigitalAssistantCriticRequest())
    return message


def message2Dict(message: DigitalAssistantCriticResponse) -> dict:

    messageDict = MessageToDict(message, preserving_proto_field_name=True, use_integers_for_enums=False, including_default_value_fields=True)
    return messageDict
