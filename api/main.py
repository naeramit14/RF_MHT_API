from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import history_taking as ht

app = FastAPI()

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Recorded(BaseModel):
    cc: list
    pd: list
    ph_ud: list
    pi_p: list
    pi_n: list

@app.get("/")
def read_root():
    return {"result": "welcome history taking"}


@app.post("/history-taking/")
def history_taking(recorded: Recorded):
    record = {
        "cc": recorded.cc,
        "ph_ud": recorded.ph_ud,
        "pd":recorded.pd,
        "pi_p": recorded.pi_p,
        "pi_n": recorded.pi_n 
        }
    print("record: ", record)
    return ht.get_question(record)


@app.post("/probable-disease/")
def probaple_disease(recorded: Recorded):
    record = {
        "cc": recorded.cc,
        "ph_ud": recorded.ph_ud,
        "pd":recorded.pd,
        "pi_p": recorded.pi_p,
        "pi_n": recorded.pi_n 
        }
    print("record: ", record)
    return ht.get_probaple_disease(record)

@app.get("/cheif_complaint/")
def cheif_complaint():
    return ht.get_cheif_complaint()