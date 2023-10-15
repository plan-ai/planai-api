from langchain.llms import OpenAI

from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field, field_validator
from typing import List
from similarity import calc_similarity

import configparser

config = configparser.ConfigParser()
config.read("../config.ini")
model_name = config["openAI"]["model"]
temperature = 0.0
model = OpenAI(
    model_name=model_name,
    temperature=temperature,
    openai_api_key=config["openAI"]["apiKey"],
)


def parse_skills(skills_str):
    skills = {}
    lines = skills_str.strip().split("\n")

    current_skill = None
    for line in lines:
        parts = line.strip().split(" (")
        name_parts = parts[0].split(": ")

        if len(name_parts) < 2:
            continue

        skill_name = name_parts[1].strip()
        weightage_part = parts[1].split(": ")
        if len(weightage_part) < 2:
            continue

        weightage = float(weightage_part[1][:-1])

        if "Subskill" not in name_parts[0]:
            skills[skill_name] = {"weightage": weightage, "subskills": {}}
            current_skill = skill_name
        elif current_skill:
            subskill_name = skill_name
            skills[current_skill]["subskills"][subskill_name] = weightage

    return skills


def annotate_task_skills(task: str):
    prompt = """This task involves you building a decision tree of necessary technical skill sets only when assigning this task to a freelancer. Assign weights based on what would make you most comfortable before picking a candidate. 

    Coding Task: {}

    only return the decision tree in the final output, which is in the following format:

    1. Skill Name: Skill 1 (Weightage: its weightage)
        1.1 Subskill Subskill 1 (Weightage: its weightage)
        1.2 Subskill Subskill 2 (Weightage: its weightage)
    2. Skill Name: Skill 2 (Weightage: its weightage)
        2.1 Subskill Subskill 1 (Weightage: its weightage)

    and so on. Need the final output with no extra text as I need to parse it.""".format(
        task
    )
    output = model(prompt)
    parsed = parse_skills(output)
    return parsed


def get_score(skills: list[str], skills_needed: list[str], stakes: list[int], weigh):
    total_score = 0
    for i in range(len(skills)):
        skill = skills[i]
        for skill_needed in skills_needed:
            similarity = calc_similarity(skill, skill_needed)
            if similarity > 0.845:
                total_score += similarity * stakes[i]
    return total_score
