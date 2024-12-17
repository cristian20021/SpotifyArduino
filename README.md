# SpotifyArduino


This project redefines the music experience by integrating a voice recognition system, NFC reader, and a rotary potentiometer with Arduino to control Spotify playback. Users can play songs, albums, and playlists, as well as adjust the volume, all through voice commands or hardware components.
[![Watch the video](https://github.com/user-attachments/assets/437488be-01d5-43bf-aa19-7f6fc41ab4fa)](https://youtu.be/FsM7y3w8bAo)

### [Watch the final renders on YouTube]([https://youtu.be/0EDKDWhR2Do](https://youtu.be/FsM7y3w8bAo))


## Circuits
![3D model smart sys proj](https://github.com/user-attachments/assets/1ee31bfc-039a-4246-8d72-a1c56a849a5d)


## Features

- Voice Command Control: Using natural language commands to control playback via a microphone.
- NFC Control: Use NFC tags to play specific songs.
- Rotary Potentiometer for Volume Control: Physically adjust the playback volume with a rotary knob.
- Spotify API Integration: Supports playback control, including songs, albums, playlists, and volume adjustments.
- Threaded Execution: Concurrent handling of voice and NFC inputs for seamless control.


## Tech Stack
**Languages:** Python, C++

Python Libraries:
- serial  - Communication with Arduino.
- spotipy - Spotify API interaction.
- speech_recognition - Voice recognition.
- threading - Multi-threading for concurrent tasks.

C++:
- For data transfer between Arduino and Python.




## Run Locally

### Hardware Requirement 

- Arduino Board with NFC reader and rotary potentiometer.
- Microphone for voice input.

### Software Requirement 

- Spotify Developer Account
- Python 3.x and C++ Compiler

Install Python libraries:
```bash
  pip install spotipy SpeechRecognition pyserial
```
### Setup Instructions

Clone the project

```bash
  git clone https://link-to-project
```

Go to the project directory

```bash
  cd my-project
```

Configure Spotify API Credentials

```python
  client_id = 'your_client_id'
  client_secret = 'your_client_secret'
  redirect_uri = 'your_url_spotify'
```

Arduino & C++ Configuration
 
 - Use C++ to write a program that handles NFC and potentiometer data from Arduino and sends it to Python over serial communication.
 - Compile and upload the C++ program to Arduino.

### How to Run

```bash
    python spotify_oauth.py
```
## Sample Commands

- Play a Song: "Play song Blinding Lights"

- Play an Album: "Play album Thriller"

- Pause Playback: "pause"

- Exit: "exit"




## Error Handling
- Spotify API Rate Limit:
If the rate limit is exceeded, the program will pause for 10 seconds and retry.

- Speech Recognition Failures:
Gracefully handles unrecognized commands or errors.

## Gallery:

![FinRender4](https://github.com/user-attachments/assets/f356737b-c545-416c-b71f-d413fc256d6b)
![FinRender3](https://github.com/user-attachments/assets/e13efd7c-eeb7-4e27-90ad-e2012b67cdd8)
![FinRender5](https://github.com/user-attachments/assets/25026f94-b70d-4bb1-9b87-93cd4ff6fb52)
![fin2](https://github.com/user-attachments/assets/8e9a56e8-3231-475c-ba17-8f36a46307ee)
![fin5](https://github.com/user-attachments/assets/a27b21e7-3a21-48a8-9a50-6f43ab396976)

![fin4](https://github.com/user-attachments/assets/d0a0725b-af4a-42cc-bf20-6b718d97770c)
![fin3](https://github.com/user-attachments/assets/75a7d9bf-cfd8-4d97-a6fe-4dafe378e402)



## License

[MIT](https://choosealicense.com/licenses/mit/)
