# truss.py
from fastapi import FastAPI
from pydantic import BaseModel
from truss_definitions import Truss
import os
from dotenv import load_dotenv

load_dotenv()

MATERIAL_COST_PER_FOOT = float(os.getenv("MATERIAL_COST_PER_FOOT", 10.0))

app = FastAPI()

class CostOverride(BaseModel):
    material_cost_per_foot: float

@app.get("/calculate_cost/{truss_name}")
def calculate_cost(truss_name: str, cost_override: CostOverride = None):
    trusses = Truss.load_from_file('synthetic_data.json')
    truss = next((t for t in trusses if t.name == truss_name), None)

    if truss is None:
        return {"error": "Truss not found"}

    material_cost = cost_override.material_cost_per_foot if cost_override else MATERIAL_COST_PER_FOOT
    cost = truss.calculate_cost(material_cost)

    return {"name": truss.name, "cost": cost, "chord_length": truss.chord_length, "web_length": truss.web_length}

