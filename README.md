# WP4 Analytic: Privacy-Aware Speech Recognition

[![Actions Status][actions badge]][actions]
[![CodeCov][codecov badge]][codecov]
[![LICENSE][license badge]][license]

<!-- Links -->
[actions]: https://github.com/sifis-home/flask-whisper-speech-recognition/actions
[codecov]: https://codecov.io/gh/sifis-home/flask-whisper-speech-recognition
[license]: LICENSES/MIT.txt

<!-- Badges -->
[actions badge]: https://github.com/sifis-home/flask-whisper-speech-recognition/workflows/flask-whisper-speech-recognition/badge.svg
[codecov badge]: https://codecov.io/gh/sifis-home/flask-whisper-speech-recognition/branch/master/graph/badge.svg
[license badge]: https://img.shields.io/badge/license-MIT-blue.svg

The Privacy-Aware Speech Recognition (PSR) model is designed to accurately convert spoken language into written text while also prioritizing privacy. This analytic utilizes computational linguistics to analyze audio signals and generate a verbatim and editable transcription of the spoken content. Importantly, any sensitive information within the audio is anonymized to protect privacy. Additionally, the PSR system allows for the generation of privacy-preserving versions of the original audio. By converting the anonymized text back into speech through text-to-speech translation, an audio output is created that maintains privacy while still conveying the intended message. These privacy-preserving transcriptions and audio can then be securely shared with external services, as they do not disclose any sensitive information. 

The Privacy-Aware Speech Recognition system requires an audio sample containing voice as its input data for translation. The analytic is designed to process WAV audio samples with specific requirements, including a sampling rate of 16000Hz, a single channel (mono) representation, and a 16-bit format. If the audio sample is in a different format, a preprocessing step may be necessary to adjust it to meet the input requirements of the analytic. In addition to the audio sample, the analytic also defines a list of textual entities to be anonymized from the audio. These textual entities are predefined and managed by the analytics like "PERSON", "ADDRESS", and "DATE".

- **Speech to Text**: We employ the advanced [Whisper automatic speech recognition (ASR) model](https://github.com/openai/whisper), developed and maintained by OpenAI, to convert spoken language into written text. Whisper stands out as a highly precise and efficient model that harnesses cutting-edge deep learning techniques, specifically the transformer architecture. This state-of-the-art approach has transformed numerous natural language processing (NLP) tasks, including speech recognition. By leveraging the transformer architecture, the Whisper model excels in handling the complexities of speech recognition tasks. It can capture contextual information, recognize patterns, and generate accurate transcriptions by effectively modeling the relationships between different elements of the audio sequence. 
- **Named Entity Recognition**: is concerned with locating key phrases and nouns in texts as entities, and these entities fall under several categories, i.e., names, locations, and addresses. The sensitivity of these entities depends on the context where the data analysis is applied. For example, names of people and locations are highly sensitive when performing data analysis and processing. However, to protect the privacy of the user, these entities can be removed from the text. Thus, still providing data valid for analysis, but without violating privacy. We used [SpaCy deep learning model](https://github.com/explosion/spaCy) to perform entity recognition on the text recognized from the previous step. The process for Named Entity Recognition is composed of the below steps: 
- **Sentence Segmentation**: to split the text into sentences. 
- **Tokenization**: to split each sentence resulting from the previous step into tokens which are usually numbers, words, and punctuation marks. 
- **Tokens Classification**: each token is classified according to its part-of-speech (POS). Entity Detection: classifies the word entities according to their type as an address, a time, a location, a name, etc. 

## Deploying

### Privacy-Aware Speech Recognition in a container

Privacy-Aware Speech Recognition is intended to run in a docker container on port 5040. The Dockerfile at the root of this repo describes the container. To build and run it execute the following commands:

`docker build -t flask-whisper-speech-recognition .`

`docker-compose up`


## REST API of Privacy-Aware Speech Recognition

Description of the REST endpoint available while Privacy-Aware Speech Recognition is running.

---

#### GET /whisper

Description: Returns the classification of a series of 48 items of temperature data whether they are anomalous or not.

Command: 

`curl -F "file=@file_location" http://localhost:5040/whisper/<file_name.wav>/<requestor_id>/<requestor_type>/<request_id>`

---
## License

Released under the [MIT License](LICENSE).

## Acknowledgements

This software has been developed in the scope of the H2020 project SIFIS-Home with GA n. 952652.
