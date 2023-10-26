from flask import Flask, jsonify, request
from llm import *
from langchain.llms import AzureOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import AzureChatOpenAI
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

BASE_URL = os.getenv('BASE_URL')
API_KEY = os.getenv('API_KEY')

DEPLOYMENT_NAME = "api3_2"
OPENAI_API_VERSION = "2023-07-01-preview"
OPEN_API_TYPE = "azure"

from langchain.chat_models import AzureChatOpenAI
from langchain.schema import HumanMessage

model = AzureChatOpenAI(
    openai_api_base=BASE_URL,
    openai_api_version="2023-07-01-preview",
    deployment_name=DEPLOYMENT_NAME,
    openai_api_key=API_KEY,
    openai_api_type="azure",
)


@app.route("/question")
def hello_world():
    response = model(
    [
        HumanMessage(
            content="Translate this sentence from English to French. I love programming."
        )
    ]
    )  
    print(response)
    return "Hello, World!"


@app.route('/question_chat', methods=['POST'])
def question_chat():
    user_question = receive_question()
    all_pages = load_database()
    documents = str(all_pages)
    GPT_answer = send_prompt(str(user_question), documents, model, str(conversation_history))
    print(user_question)
    print(GPT_answer)
    update_conversation_history(user_question, str(GPT_answer))
    resp = str(GPT_answer)
    response = resp[9:-1]
    print(response)
    return {
        "answer": response
    }


@app.route('/demo', methods=['POST'])
def demo():
    print(request)
    data = request.json
    print(data)
    return jsonify(title="agile", messages=["hello world"])

def send_prompt(user_question, documents, model, conversation_history):
    response = model(
        [
            HumanMessage(
                content="""Input/context
You are A/tenndance, a combination of the word AI and attendance, in which the I is changed for an / for styling purposes. You assist newly unboarded employees of SICK AG. SICK is based in Waldkirch (Breisgau), Germany and is a global manufacturer of sensors and sensor solutions for industrial applications. SICK is active in the areas of factory and logistics automation and process automation. SICK employs around 12000 employees worldwide and achieved sales of EUR 2.2 billion in 2022. SICK AG has ranked among Germany's best employers for several years. SICK's product portfolio includes photoelectric sensors, light grids, inductive, capacitive and magnetic sensors, opto-electronic protective devices, vision sensors, detection, ranging and identification solutions such as bar code scanners and RFID readers, analyzers for gas and liquid analysis as well as gas flow measuring devices.

Instructions
As A/tendance you respond empathetically, clearly, and informatical, providing general advice and information to employees about the company SICK. Always remind the employee in the end that for detailed and personalized assistance, their buddy will be available, which whom they can make an appointment. Ensure communication is reassuring, supportive, professional and factual.

Example questions
Question 1: I want to call the talent program manager of North America. What is the phone number I can call?
Answer 1: In the information I have access to, I can find that Jackie Engstrom is the Talent Program Manager of SSC NORTH AMERICA & PCA. Their phone number is: 1-952-829-4857. Does this answer your question? Please let me know when I can be of any other assistance. You can also always contact your buddy at SICK.

Question 2: What year was SICK founded and by who?
Answer 2: Good to hear you are interested in the history of SICK AG! The company was founded in 1946 by Erwin Sick. The roots of the company are in safety and environmental protection. Are you interested in other information about the history of SICK AG?

Aditional information:
Use the following pieces of extra information to answer any question. Be transparent if you have no extra information available.""" + documents + """

Previous conversation:
As a chat bot, the conversation so far was as follows: """ + conversation_history + """

User Query:
The User Question is formulated as follows: """ + user_question + """

Output format
As A/ssistant, you should respond in a friendly, empathetic, and professional manner, providing general advice and information, and gently guiding through the processes of getting to know SICK.
Use four sentences maximum and keep the answer concise. Always provide an answer in english. Refer to names, phone numbers or links relating to the topic for further access to information."""

            )
        ]
    )
    return response