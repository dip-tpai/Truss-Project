import random
import math
import json
from typing import List
from dataclasses import dataclass
from random import uniform



@dataclass
class Point:
    x: float
    y: float

    def distance_to(self, other: "Point") -> float:
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)


@dataclass
class TrussMember:
    start: Point
    end: Point

    @property
    def length(self) -> float:
        return self.start.distance_to(self.end)


@dataclass
class Truss:
    members: List[TrussMember]

    @property
    def total_length(self) -> float:
        return sum(member.length for member in self.members)

    def calculate_cost(self, cost_per_foot: float) -> float:
        return self.total_length * cost_per_foot


def generate_random_points(num_points: int, max_x: int = 50, max_y: int = 50):
    points = []
    for _ in range(num_points):
        x = uniform(0, max_x)
        y = uniform(0, max_y)
        points.append(Point(x, y))
    return points


def generate_synthetic_trusses(truss_type: str, num_points: int = 5):
    points = generate_random_points(num_points)

    members = []

    for i in range(num_points - 1):
        for j in range(i + 1, num_points):
            if random.random() > 0.5:  # Randomly decide whether to connect points
                members.append(TrussMember(points[i], points[j]))

    truss = Truss(members)

    material_cost_per_foot = round(uniform(5, 15), 2)
    total_cost = truss.calculate_cost(material_cost_per_foot)

    return {
        "truss_type": truss_type,
        "points": [{"x": point.x, "y": point.y} for point in points],
        "total_length": truss.total_length,
        "cost_per_foot": material_cost_per_foot,
        "total_cost": total_cost
    }


def generate_multiple_trusses(num_trusses: int = 10):
    trusses_data = []
    for _ in range(num_trusses):
        truss_type = random.choice(["A", "B", "C"])
        truss_data = generate_synthetic_trusses(truss_type)
        trusses_data.append(truss_data)
    return trusses_data

synthetic_trusses = generate_multiple_trusses(10)

with open('synthetic_trusses.json', 'w') as file:
    json.dump(synthetic_trusses, file, indent=4)

#print(json.dumps(synthetic_trusses, indent=4))
