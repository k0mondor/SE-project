from typing import List, Optional

from pydantic import BaseModel


class EnterpriseIn(BaseModel):
    name: str
    credit_code: Optional[str] = None
    founded_year: Optional[int] = None
    legal_person: Optional[str] = None
    reg_capital: Optional[float] = None
    employee_scale: Optional[str] = None
    revenue_scale: Optional[str] = None
    industry_code: str
    industry_name: str
    chain_segment: str
    region: str
    production_bases: Optional[str] = None
    tech_qualifications: Optional[str] = None
    investment_events: Optional[str] = None
    source: str
    source_url: str


class PolicyIn(BaseModel):
    title: str
    region: str
    industry: Optional[str] = None
    policy_type: str
    issuer: str
    publish_date: Optional[str] = None
    eligibility: Optional[str] = None
    content: str
    source_url: str


class EnterpriseImportRequest(BaseModel):
    source: str = "manual"
    dry_run: bool = False
    records: List[EnterpriseIn]


class PolicyImportRequest(BaseModel):
    dry_run: bool = False
    records: List[PolicyIn]
