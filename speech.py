import streamlit as st
import speech_recognition as sr

def main():
    st.title("Speech Recognition with Streamlit")
    st.write("Say something! I'm listening...")

    # Initialize the recognizer
    recognizer = sr.Recognizer()

    # Use microphone as input
    with sr.Microphone() as source:
        # Adjust the energy threshold
        recognizer.adjust_for_ambient_noise(source)
        
        # Record the audio
        audio = recognizer.listen(source)

    # Recognize speech using Google Cloud Speech
    try:
        # Recognize the speech using Google Cloud Speech
        text = recognizer.recognize_amazon(audio, language="en-US")
        st.write("You said:", text)

    except sr.UnknownValueError:
        st.error("Google Cloud Speech could not understand audio")
    except sr.RequestError as e:
        st.error(f"Could not request results from Google Cloud Speech service; {e}")

if __name__ == "__main__":
    main()
