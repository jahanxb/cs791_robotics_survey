Ubuntu 22.04 

Install dependencies for PyAudio

For MAC 

xcode-select --install
brew remove portaudio
brew install portaudio
pip3 install pyaudio


------

Technology - Duckiebot (DB-J)
Autonomous robot platform for interaction studies
Equipped with sensors for real-time data collection
Technology - NVIDIA Jetson Nano
AI computing platform for processing and analysis
Enabled complex data computation for the study


-------------------

Programming Language - Python

Speech Recognition: Use speech_recognition for converting speech to text (pip install SpeechRecognition).
Text-to-Speech: Use gtts for text-to-speech conversion (pip install gTTS).
NLP: Utilize nltk for natural language processing (pip install nltk).
VAD: Employ webrtcvad for detecting speech presence (pip install webrtcvad).
Audio: Use pyaudio for audio I/O interfacing (pip install PyAudio).
Dialogue: Implement ChatterBot for dialogue management (pip install chatterbot).