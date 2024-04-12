from grpc import insecure_channel
from dig_ass_critic_protos.DigitalAssistantCritic_pb2_grpc import DigitalAssistantCriticStub
from dig_ass_critic_protos.DigitalAssistantCritic_pb2 import (
    DigitalAssistantCriticRequest,
    DigitalAssistantCriticResponse,
    OuterContextItem,
    InnerContextItem,
    ChatItem,
    ReplicaItem,
)


class CriticClient:

    def __init__(self, address: str) -> None:
        self._channel = insecure_channel(address)
        self._stub = DigitalAssistantCriticStub(self._channel)

    def __call__(self, requestDict: dict):

        request = packageRequestDict(requestDict)
        response: DigitalAssistantCriticResponse = self._stub.GetTextResponse(request)
        return response.Score

    # https://stackoverflow.com/a/65131927
    def close(self):
        self._channel.close()

    def __enter__(self):
        return self

    def __exit__(self):
        self.close()


def packageRequestDict(requestDict: dict) -> DigitalAssistantCriticRequest:
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
        "innerContext":{
            "replicas": [{
                "body":,
                "role":,
                "dateTime":
            }]
        }
    }
    """

    # populate outer context
    outerContextDict = requestDict["outerContext"]
    outerContext = OuterContextItem(Sex=outerContextDict["sex"], Age=outerContextDict["age"], UserId=outerContextDict["userId"], SessionId=outerContextDict["sessionId"])

    # populate inner context
    innerContextDict = requestDict["innerContext"]
    replicasList = innerContextDict["replicas"]
    replicas = []
    for replicaDict in replicasList:
        replica = ReplicaItem(Body=replicaDict["body"], Role=replicaDict["role"], DateTime=replicaDict["dateTime"])
        replicas.append(replica)
    innerContext = InnerContextItem(Replicas=replicas)

    # populate chat item
    chat = ChatItem(OuterContext=outerContext, InnerContext=innerContext)

    # populate final request
    request = DigitalAssistantCriticRequest(Text=requestDict["text"], Chat=chat)

    return request
