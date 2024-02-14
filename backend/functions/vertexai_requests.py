import io
import os
import json
import logging
from google.cloud import speech_v1p1beta1 as speech
from vertexai.language_models import TextGenerationModel, \
                                     TextEmbeddingModel, \
                                     ChatModel, \
                                     InputOutputTextPair, \
                                     CodeGenerationModel, \
                                     CodeChatModel, \
                                     ChatMessage
from langchain.llms import VertexAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.prompts.prompt import PromptTemplate
from langchain.memory import ChatMessageHistory
import pickle


# Import custom functions
from functions.database import get_recent_messages

# Convert audio to text
def convert_audio_to_text(audio_input):
    client = speech.SpeechClient()

    # The content of the audio file to transcribe
    audio_content = audio_input
    
    # transcribe speech
    audio = speech.RecognitionAudio(content=audio_content)

    config = speech.RecognitionConfig(
        #encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        #sample_rate_hertz=24000,
        language_code="en-US",
        model="default",
        audio_channel_count=1,
        enable_word_confidence=True,
        enable_word_time_offsets=True,
    )

    # Detects speech in the audio file
    operation = client.long_running_recognize(config=config, audio=audio)

    print("Waiting for operation to complete...")
    response = operation.result(timeout=90)

    for result in response.results:
        return(result.alternatives[0].transcript)

# Example usage:
# audio_file_path = './voice.wav'
# convert_audio_to_text(audio_file_path)




memory=ConversationBufferMemory(human_prefix="Friend")

# Get Response to our Message
def get_chat_response(message_input):

    llm=VertexAI(max_output_tokens=300, model_name="gemini-pro")
    template = """The following is a friendly conversation between a human and an AI. The AI is talkative and provides lots of specific details from its context. If the AI does not know the answer to a question, it truthfully says it does not know.

    Current conversation:
    {history}
    Friend: {input}
    AI:"""
    PROMPT = PromptTemplate(input_variables=["history", "input"], template=template)
    conversation = ConversationChain(
        prompt=PROMPT,
        llm=llm,
        verbose=True,
        memory=memory,
    )

    result = conversation.predict(input=message_input)
    return result
    #print(result)

# Reset chat history
def reset_chat_history():
    global memory
    memory=ConversationBufferMemory(human_prefix="Friend")