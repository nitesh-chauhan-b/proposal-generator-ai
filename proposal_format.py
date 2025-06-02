from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import date


class Subtask(BaseModel):
    name: str
    hours: int


class Task(BaseModel):
    name: str
    subtasks: List[Subtask]


class ProjectScheduleItem(BaseModel):
    name: str
    description: str
    start_date: str  # or use `date` if actual date objects are needed
    end_date: str


class TeamMember(BaseModel):
    name: str
    role: str
    bio: str


class CaseStudy(BaseModel):
    client: str
    challenge: str
    solution: str
    results: str


class PricingItem(BaseModel):
    description: str
    cost: str


# class TechnologyStack(BaseModel):
#     Frontend: List[str]
#     Backend: List[str]
#     Database: List[str]
#     DevOps: List[str]
#     AI_ML: List[str]


class ProposalData(BaseModel):
    company_name: str
    company_email: str
    client_name: str
    project_title: str
    proposal_date: str  # use `date` if needed as a date object
    executive_summary: str
    project_goals: List[str]
    success_metrics: List[str]
    about_company: str
    problem_statement: str
    proposed_solution: str
    assumptions: List[str]
    solution_phases: List[str]
    project_schedule: List[ProjectScheduleItem]
    team_members: List[TeamMember]
    technology_stack: Dict[str, List[str]]
    task_breakdown: List[Task]
    why_us: List[str]
    case_study: CaseStudy
    next_steps: List[str]
    support_details: str
    pricing: List[PricingItem]
    total_cost: str
    current_year: int
