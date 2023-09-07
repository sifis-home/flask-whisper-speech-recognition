import datetime
import hashlib
import json
import os
import platform
from tempfile import NamedTemporaryFile

import rel
import spacy
import torch
import websocket
import whisper
from flask import Flask, abort, request
from gtts import gTTS

entity_types = [
    "PERSON",
    "NORP",
    "FAC",
    "ORG",
    "GPE",
    "LOC",
    "PRODUCT",
    "EVENT",
    "WORK_OF_ART",
    "LAW",
    "LANGUAGE",
    "DATE",
    "TIME",
    "PERCENT",
    "MONEY",
    "QUANTITY",
    "ORDINAL",
    "CARDINAL",
]

spacy.cli.download("en_core_web_sm")
nlp = spacy.load("en_core_web_sm")

# Check if NVIDIA GPU is available
torch.cuda.is_available()
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# Load the Whisper model:
model = whisper.load_model("base", device=DEVICE)


def on_error(ws, error):
    print(error)


def on_close(ws, close_status_code, close_msg):
    print("### Connection closed ###")


def on_open(ws):
    print("### Connection established ###")


def get_data():
    analyzer_id = platform.node()
    print(analyzer_id)

    return analyzer_id


app = Flask(__name__)


@app.route(
    "/whisper/<file_name>/<requestor_id>/<requestor_type>/<request_id>",
    methods=["POST"],
)
def handler(file_name, requestor_id, requestor_type, request_id):
    if not request.files:
        # If the user didn't submit any files, return a 400 (Bad Request) error.
        abort(400)

    analyzer_id = get_data()

    # Get current date and time
    now = datetime.datetime.now()

    # Generate a random hash using SHA-256 algorithm
    hash_object = hashlib.sha256()
    hash_object.update(bytes(str(now), "utf-8"))
    hash_value = hash_object.hexdigest()

    # Concatenate the time and the hash
    analysis_id = str(analyzer_id) + str(now) + hash_value

    # For each file, let's store the results in a list of dictionaries.
    results = []

    # Loop over every file that the user submitted.
    for filename, handle in request.files.items():
        # Create a temporary file.
        # The location of the temporary file is available in `temp.name`.
        temp = NamedTemporaryFile()
        # Write the user's uploaded file to the temporary file.
        # The file will get deleted when it drops out of scope.
        handle.save(temp)
        # Let's get the transcript of the temporary file.
        result = model.transcribe(temp.name)

        doc = nlp(result["text"])
        text2 = result["text"]

        # print("------Entities------")
        for ent in doc.ents:
            # print(ent.text, ent.start, ent.end, ent.start_char, ent.end_char, ent.label_)
            length = ent.end_char - ent.start_char
            text2 = (
                text2[: ent.start_char] + "x" * length + text2[ent.end_char :]
            )

        Private_Text = ""

        for item in text2.split():
            if item.count("xx") >= 1:
                # print(item, item.count('xx'))
                Private_Text = Private_Text + "Privat Data "
            else:
                # print(item, item.count('xx'))
                Private_Text = Private_Text + item + " "

        # Now we can store the result object for this file.
        results.append(
            {
                "filename": filename,
                "transcript": result["text"],
                "Private_Text": Private_Text,
            }
        )

        language = "en"

        myobj = gTTS(text=Private_Text, lang=language, slow=False)

        myobj.save("Private_Audio.mp3")
        ws_req_final = {
            "RequestPostTopicUUID": {
                "topic_name": "SIFIS:Privacy_Aware_Speech_Recognition_Results",
                "topic_uuid": "Speech_Recognition_Results",
                "value": {
                    "description": "Speech Recognition Results",
                    "requestor_id": str(requestor_id),
                    "requestor_type": str(requestor_type),
                    "request_id": str(request_id),
                    "analyzer_id": str(analyzer_id),
                    "analysis_id": str(analysis_id),
                    "connected": True,
                    "filename": filename,
                    "Private_Text": Private_Text,
                    "Private_Audio": "Private_Audio.mp3",
                    "private_audio_path": str(os.getcwd()),
                },
            }
        }

    ws.send(json.dumps(ws_req_final))
    return ws_req_final


if __name__ == "__main__":
    ws = websocket.WebSocketApp(
        "ws://localhost:3000/ws",
        on_open=on_open,
        on_error=on_error,
        on_close=on_close,
    )

    ws.run_forever(dispatcher=rel)  # Set dispatcher to automatic reconnection
    rel.signal(2, rel.abort)  # Keyboard Interrupt
    app.run(host="0.0.0.0", port=5040)
