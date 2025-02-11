import os

from fastapi import FastAPI
from pydantic import BaseModel
import random
from dotenv import load_dotenv

from truss_definitions import Truss

load_dotenv()

MATERIAL_COST_PER_FOOT = float(os.getenv("MATERIAL_COST_PER_FOOT", 10.0))

class Truss(BaseModel):
    name: str
    chord_length: float
    web_length: float
    num_webs: int
    num_chords: int

    def calculate_cost(self):
        total_length = self.chord_length * self.num_chords + self.web_length * self.num_webs
        return total_length * MATERIAL_COST_PER_FOOT

def generate_synthetic_data():
    trusses = [
        Truss(name="Truss A", chord_length=random.uniform(10, 20), web_length=random.uniform(5, 15), num_webs=5, num_chords=2),
        Truss(name="Truss B", chord_length=random.uniform(15, 25), web_length=random.uniform(7, 18), num_webs=6, num_chords=3),
        Truss(name="Truss C", chord_length=random.uniform(12, 22), web_length=random.uniform(6, 16), num_webs=4, num_chords=2)
    ]
    return trusses

app = FastAPI()

@app.get("/calculate_cost/{truss_name}")
def calculate_cost(truss_name: str, material_cost_per_foot: float = None):
    trusses = generate_synthetic_data()
    truss = next((t for t in trusses if t.name == truss_name), None)

    if truss is None:
        return {"error": "Truss not found"}

    if material_cost_per_foot:
        global MATERIAL_COST_PER_FOOT
        MATERIAL_COST_PER_FOOT = material_cost_per_foot

    cost = truss.calculate_cost()
    return {"name": truss.name, "cost": cost, "chord_length": truss.chord_length, "web_length": truss.web_length}