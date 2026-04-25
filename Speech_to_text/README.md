# Speech to Text with Sentiment Analysis

This is a Python-based project that uses speech recognition to convert voice input into text and then performs basic sentiment analysis on that text. It's built using Tkinter for the GUI and leverages popular libraries like SpeechRecognition and TextBlob.

## Project Goal
The main idea was to create a simple tool that can listen to a user, understand what they said, and give immediate feedback on the "vibe" or sentiment of their speech.

## Main Features
*   **Voice to Text**: Captures audio from the microphone and converts it using Google's speech recognition engine.
*   **Sentiment Detection**: Uses NLP to categorize the text as Positive, Negative, or Neutral.
*   **Confidence Score**: Shows a percentage based on how strong the sentiment is.
*   **Simple Interface**: A clean, easy-to-use window with a record button and real-time status updates.

## Libraries Used
*   **Tkinter**: For the desktop interface.
*   **SpeechRecognition**: For handling the audio input and conversion.
*   **TextBlob**: For processing the text and calculating sentiment.
*   **PyAudio**: Necessary for microphone access.

## Setting Up
First, make sure you have Python installed. Then, you'll need to install these packages:

```bash
pip install speechrecognition textblob pyaudio
```

You also need to download the TextBlob data:
```bash
python -m textblob.download_corpora
```

## How to Run
1. Go to the `Speech_to_text` folder.
2. Run the main script:
   ```bash
   python main.py
   ```
3. Click "Start Recording", speak after the calibration, and the results will appear on the screen.

## Project Structure
- `main.py`: Contains both the UI code and the logic for recognition/analysis.
- `README.md`: Project documentation.

## Notes
The accuracy of the speech recognition depends on your internet connection (since it uses Google's API) and the quality of your microphone.
