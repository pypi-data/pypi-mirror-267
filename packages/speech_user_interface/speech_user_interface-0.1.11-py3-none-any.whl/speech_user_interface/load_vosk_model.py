import os
from vosk import Model

from .CONSTANTS import VOSK_MODEL_PATH
from .download_file import download_file


def load_vosk_model():
    # Resolve the model path
    model_path = os.path.abspath(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "..",
            VOSK_MODEL_PATH,
        )
    )

    # Check if the model path exists
    if not os.path.exists(model_path):
        download_file(
            "https://alphacephei.com/vosk/models/vosk-model-en-us-0.22.zip",
            model_path,
        )

    # Load the Vosk model
    return Model(model_path)
