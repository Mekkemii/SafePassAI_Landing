
from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
import json
import random

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешаем все домены для теста
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

with open("questions.json", "r", encoding="utf-8") as f:
    QUESTIONS = json.load(f)

@app.get("/")
def root():
    return {"message": "Akinator backend is running."}

@app.get("/get-questions")
def get_questions():
    return {"questions": QUESTIONS}

@app.post("/get-followups")
def get_followups(answers: dict = Body(...)):
    followups = []
    for q in QUESTIONS:
        if answers.get(q["id"]):
            if "followup" in q:
                followups.append(q["followup"])
    return {"followups": followups}

@app.post("/guess-passwords")
def guess_passwords(data: dict = Body(...)):
    bools = data.get("bools", {})
    texts = data.get("texts", {})

    guesses = []

    if bools.get("use_birth_date") and "birth_date" in texts:
        guesses.append("mybday" + texts["birth_date"][-4:])
    if bools.get("use_pet_name") and "pet_name" in texts:
        guesses.append(texts["pet_name"].lower() + "123")
    if bools.get("use_favorite_game") and "favorite_game" in texts:
        guesses.append(texts["favorite_game"].lower() + "2024")
    if bools.get("use_company_name") and "company_name" in texts:
        guesses.append(texts["company_name"].lower() + "01")
    if bools.get("use_city") and "city_name" in texts:
        guesses.append(texts["city_name"].lower() + "!")
    if bools.get("use_nickname") and "nickname" in texts:
        guesses.append(texts["nickname"].lower() + "321")

    guesses += random.sample([
        "password123", "qwerty2023", "admin!", "letmein", "welcome@",
        "pass" + str(random.randint(100, 999)), "abc" + str(random.randint(1000, 9999))
    ], k=3)

    return {"guesses": guesses[:10]}
