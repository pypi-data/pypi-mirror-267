from grpc import insecure_channel
from dig_ass_ocr_protos.DigitalAssistantOCR_pb2_grpc import DigitalAssistantOCRStub
from dig_ass_ocr_protos.DigitalAssistantOCR_pb2 import DigitalAssistantOCRRequest, DigitalAssistantOCRResponse


class OCRClient:

    def __init__(self, address: str) -> None:
        self._channel = insecure_channel(address)
        self._stub = DigitalAssistantOCRStub(self._channel)

    def __call__(self, image: bytearray, pdf: bytearray):
        request = DigitalAssistantOCRRequest(Image=image, PDF=pdf)
        response: DigitalAssistantOCRResponse = self._stub.GetTextResponse(request)

        return response.Text

    # https://stackoverflow.com/a/65131927
    def close(self):
        self._channel.close()

    def __enter__(self):
        return self

    def __exit__(self):
        self.close()
