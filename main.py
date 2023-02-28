# python -m uvicorn main:app --reload
from database import engine, SessionLocal
import model
from model import dataset
from fastapi import FastAPI, Request, Response, HTTPException, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import openai
import json
import os
load_dotenv()
openai.api_key = os.environ['API_KEY']
origins = [
    "http://localhost:3000",
]
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# This will create schema in mySql database
# meaning it will create table:dataset 
# in database: Kryptomind
model.Base.metadata.create_all(bind=engine)


class QAStringRequest(BaseModel):
    question: str
    answer : str

@app.post("/dataset")
# async def submit(request: Request, user_string_request: UserStringRequest):
def enterData(request: Request, user_string_request: QAStringRequest):
    question = user_string_request.question
    answer = user_string_request.answer

    try:
        data = dataset(
            prompt = question,
            completion = answer
        )

        session = SessionLocal()    
        session.add(data)
        session.commit()
        session.close()

        return {'Message': "Successfully inserted"}
    except:
        return {'Error': "Error while inserting Data"}

class ChatbotStringRequest(BaseModel):
    question: str
    
@app.post("/chatbot")
def chatbot(request: Request, user_string_request: ChatbotStringRequest):
    question = user_string_request.question
    prompt = "The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly. Human: what is the name of your company? AI: We work at Kryptomind. Human: How many employees do you have. AI: We currently have a team of 50 employees. Human: What is the location of your software house? AI: We are located at Johar town in City Lahore and Country Paistan. Human: "+question

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=500,
        n=1,
        stop=None,
        temperature=0.5,
    )

    response = response.choices[0].text.strip()

    return {"response":response}
    
@app.get('/retrieveDataset')
def AllData():
    session = SessionLocal()

    # retrieve all rows
    results = session.query(dataset.prompt, dataset.completion).all()
    data = []
    for prompt, completion in results:
        data.append({'prompt': prompt, 'completion': completion})

    # save the data as a JSON file
    with open('dataset.json', 'w') as f:
        json.dump(data, f)
    return results
    

@app.websocket("/chatbot")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        question = await websocket.receive_text()
        prompt = "The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly. Human: what is the name of your company? AI: We work at Kryptomind. Human: How many employees do you have. AI: We currently have a team of 50 employees. Human: What is the location of your software house? AI: We are located at Johar town in City Lahore and Country Paistan. Human: "+question

        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=500,
            n=1,
            stop=None,
            temperature=0.5,
        )

        response = response.choices[0].text.strip()
        await websocket.send_text(response)
