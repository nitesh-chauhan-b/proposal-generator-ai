from pydantic import BaseModel
from typing import List, Dict


class ProjectScheduleItem(BaseModel):
    name: str
    start_date: str
    end_date: str


class TeamMember(BaseModel):
    name: str
    role: str
    bio: str


class Proposal(BaseModel):
    company_name: str
    company_email: str
    client_name: str
    project_title: str
    proposal_date: str
    executive_summary: str
    about_company: str
    problem_statement: str
    proposed_solution: str
    solution_phases: List[str]
    project_schedule: List[ProjectScheduleItem]
    team_members: List[TeamMember]
    technology_stack: Dict[str, List[str]]
    why_us: List[str]
    pricing: List[Dict[str, str]]
    total_cost: str
    current_year: int
    client_logos: List[str]
