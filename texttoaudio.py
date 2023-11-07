import os
import streamlit as st
from openai import OpenAI
import tempfile
from pydub import AudioSegment
import openai

## provide api key
openai.api_key = st.secrets["api_secret_key"]
client = OpenAI(api_key=st.secrets["api_secret_key"])

st.title("Responses From LLM in Audio")
# user prompt
user_prompt = st.text_input("Write your question to llm")

## use prompt
system_prompt = "You are a storyteller"

#st.audio(audio_file, format="audio/mp3")
if st.button("Generate Audio"):
    # Response from GPT-3
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )
    story = response.choices[0].message.content

    # Generate audio from the text
    audio_response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=story,
    )

      # Save the audio content to a temporary file
    audio_content = audio_response.content

    with open("temp_audio.mp3", "wb") as audio_file:
        audio_file.write(audio_content)

    # Display and play the audio
    st.audio("temp_audio.mp3", format="audio/mp3")

