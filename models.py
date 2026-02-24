from dataclasses import dataclass, field
from typing import Optional
from datetime import date

# DataFlow models (enterprise-focused)

@dataclass
class Account:
    id: str
    name: str
    industry: str
    annual_revenue: int
    employees: int
    address: str
    status: str  # customer, prospect
    contract_value: Optional[int]
    contract_start: Optional[date]
    contract_end: Optional[date]
    parent_id: Optional[str] = None

@dataclass
class Contact:
    id: str
    account_id: str
    first_name: str
    last_name: str
    title: str
    email: str
    phone: str

@dataclass
class Opportunity:
    id: str
    account_id: str
    name: str
    amount: int
    stage: str  # discovery, proposal, negotiation, closed_won, closed_lost
    close_date: date
    product: str


# QuickSync models (SMB-focused)

@dataclass
class Company:
    id: str
    company_name: str
    contact_name: str
    contact_email: str
    plan: str  # starter, professional, business
    mrr: int
    billing_cycle: str  # monthly, annual
    signup_date: date
    renewal_date: date
    usage_gb: int
    users: int


# Health scoring models

@dataclass
class HealthSignal:
    signal_type: str
    description: str
    severity: str  # critical, warning, positive
    points: int

@dataclass
class HealthScore:
    score: int  # 0-100
    category: str  # healthy, at_risk, critical
    signals: list[HealthSignal] = field(default_factory=list)

@dataclass
class Alert:
    account_id: str
    account_name: str
    health_score: HealthScore
    arr: int
