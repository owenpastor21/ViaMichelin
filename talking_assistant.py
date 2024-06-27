import streamlit as st
from audio_recorder_streamlit import audio_recorder
from openai import OpenAI


API_KEY=st.secrets['openai']['OPENAI_KEY']

content='''You are a traveller counsellar and suggest great travelling ideas.You should suggest the best places to see and must-visit places in the route from Paris to Bordeaux.
If user asks for restaurants then Suggest good restaurants on this route.
suggest places to visit, restaurants to try out and hotels to stay in during my trip to Bordeaux, as I'd like to discover more about France and make new discoveries. 
If you are asked which place to visit at the start of the day and giving me some facts about the seeings, you can refer from the below URL:
https://www.getyourguide.fr/chateau-du-clos-luce-l96466/chateau-du-clos-luce-maison-de-leonard-de-vinci-t194510/?partner_id=TFVI0WE&psrc=partner_api&currency=EUR
Give some history and facts about the place and Château. 
You can also suggest another option which is to visit the Château Royal d'Amboise, and tells me the history of the château.
Try to find as much resources from the ViaMichelin website and the guides. You can can give the URL of the ViaMichelin website in your response. 
'''

def transcribe_text_to_voice(audio_location):
    client = OpenAI(api_key=API_KEY)
    audio_file= open(audio_location, "rb")
    transcript = client.audio.transcriptions.create(model="whisper-1", file=audio_file)
    return transcript.text

def chat_completion_call(text):
    client = OpenAI(api_key=API_KEY)
    messages = [{"role": "system", "content": content},{"role": "user", "content": text}]
    response = client.chat.completions.create(model="gpt-3.5-turbo-1106", messages=messages)
    return response.choices[0].message.content


def text_to_speech_ai(speech_file_path, api_response):
    client = OpenAI(api_key=API_KEY)
    response = client.audio.speech.create(model="tts-1",voice="nova",input=api_response)
    response.stream_to_file(speech_file_path)

def submit():
    # Set entered_prompt to the current value of prompt_input
    st.session_state.entered_prompt = st.session_state.prompt_input
    # Clear prompt_input
    st.session_state.prompt_input = ""

st.title("🧑‍💻 Travel buddy 💬 Powered by: ViaMichelin ")

"""
Hello! I am your Travelling buddy Mea 🤖 Just click on the voice recorder and let me know how I can help you today?
"""

logo_url = 'Logo_viamichelin.jpg'
st.sidebar.image(logo_url)

st.text_input('YOU: ', key='prompt_input', on_change=submit)

audio_bytes = audio_recorder()
if audio_bytes:
    ##Save the Recorded File
    audio_location = "audio_file.wav"
    with open(audio_location, "wb") as f:
        f.write(audio_bytes)

    #Transcribe the saved file to text
    text = transcribe_text_to_voice(audio_location)
    st.write(text)

    #Use API to get an AI response
    api_response = chat_completion_call(text)
    st.write(api_response)

    # Read out the text response using tts
    speech_file_path = 'audio_response.mp3'
    text_to_speech_ai(speech_file_path, api_response)
    st.audio(speech_file_path)


st.markdown("""
---
Made with 🤖 by Vijayant Kumar(Valtech) :[LinkedIn](https://www.linkedin.com/in/vijayantkumarbansal/)
                                 [Github](https://github.com/vizzyno1)""")   