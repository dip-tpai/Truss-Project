# truss_definitions.py
import json
from pydantic import BaseModel
from typing import List

class Truss(BaseModel):
    name: str
    chord_length: float  # Length of the chord in feet
    web_length: float  # Length of each web member in feet
    num_webs: int  # Number of web members
    num_chords: int  # Number of chord members

    def calculate_cost(self, material_cost_per_foot: float) -> float:
        total_length = self.chord_length * self.num_chords + self.web_length * self.num_webs
        return total_length * material_cost_per_foot

    @staticmethod
    def load_from_file(file_path: str) -> List['Truss']:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return [Truss(**truss_data) for truss_data in data]