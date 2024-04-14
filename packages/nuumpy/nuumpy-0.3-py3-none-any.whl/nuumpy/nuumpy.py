def nimpy():
    code = """
!pip install -Uq keras-nlp
!pip install -Uq keras

import keras
import keras_nlp
import numpy as np

def login_to_kaggle():
    print('"username": "trilokvishwam", "key": "5829ba02d16cbacbda14d0b3d0570e98"')
    import kagglehub
    kagglehub.login()

login_to_kaggle()

gemma_lm = keras_nlp.models.GemmaCausalLM.from_preset("gemma_instruct_2b_en")

import keras
import keras_nlp
import numpy as np

def generate_response(question):
    prompt = ""
    You are an AI assistant designed to answer simple questions.
    Please restrict your answer to the exact question asked.
    Think step by step, use careful reasoning. Your name is Semban Surga
    Question: {question}
    Answer:
    ""
    response = gemma_lm.generate(prompt.format(question=question), max_length=500)
    start_idx = response.find("Answer:") + len("Answer:")
    return response[start_idx:].strip()

def ask(question):
    response = generate_response(question)
    print(response)
    """

    print(code)
