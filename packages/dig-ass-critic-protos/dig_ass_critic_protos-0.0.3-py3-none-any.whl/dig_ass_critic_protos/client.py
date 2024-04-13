from google.protobuf.json_format import ParseDict
from dig_ass_critic_protos.DigitalAssistantCritic_pb2_grpc import DigitalAssistantCriticStub
from dig_ass_critic_protos.DigitalAssistantCritic_pb2 import DigitalAssistantCriticRequest, DigitalAssistantCriticResponse, ChatItem

from abstract_client import AbstractClient

class CriticClient(AbstractClient):
    def __init__(self, address) -> None:
        super().__init__(address)
        self._stub = DigitalAssistantCriticStub(self._channel)

    def __call__(self, text: str, chat: dict):
        request = DigitalAssistantCriticRequest(
            Text=text,
            Chat=ParseDict(chat, ChatItem()),
        )
        response: DigitalAssistantCriticResponse = self._stub.GetTextResponse(request)
        return response.Score
