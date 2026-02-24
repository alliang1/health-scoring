import json
from pathlib import Path
from datetime import datetime, date
from models import Account, Contact, Opportunity, Company, HealthSignal, HealthScore, Alert

DATA_DIR = Path(__file__).parent / "data"

def parse_date(date_str):
    if date_str:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    return None

def load_accounts() -> list[Account]:
    with open(DATA_DIR / "dataflow_accounts.json") as f:
        data = json.load(f)
    accounts = []
    for a in data:
        accounts.append(Account(
            id=a["id"],
            name=a["name"],
            parent_id=a.get("parent_id"),
            industry=a["industry"],
            annual_revenue=a["annual_revenue"],
            employees=a["employees"],
            address=a["address"],
            status=a["status"],
            contract_value=a.get("contract_value"),
            contract_start=parse_date(a.get("contract_start")),
            contract_end=parse_date(a.get("contract_end"))
        ))
    return accounts

def load_contacts() -> list[Contact]:
    with open(DATA_DIR / "dataflow_contacts.json") as f:
        data = json.load(f)
    return [Contact(**c) for c in data]

def load_opportunities() -> list[Opportunity]:
    with open(DATA_DIR / "dataflow_opportunities.json") as f:
        data = json.load(f)
    opportunities = []
    for o in data:
        opportunities.append(Opportunity(
            id=o["id"],
            account_id=o["account_id"],
            name=o["name"],
            amount=o["amount"],
            stage=o["stage"],
            close_date=parse_date(o["close_date"]),
            product=o["product"]
        ))
    return opportunities

def load_companies() -> list[Company]:
    with open(DATA_DIR / "quicksync_companies.json") as f:
        data = json.load(f)
    return [Company(
        id=c["id"],
        company_name=c["company_name"],
        contact_name=c["contact_name"],
        contact_email=c["contact_email"],
        plan=c["plan"],
        mrr=c["mrr"],
        billing_cycle=c["billing_cycle"],
        signup_date=parse_date(c["signup_date"]),
        renewal_date=parse_date(c["renewal_date"]),
        usage_gb=c["usage_gb"],
        users=c["users"],
    ) for c in data]


def get_account(account_id: str) -> Account | None:
    accounts = load_accounts()
    return next((a for a in accounts if a.id == account_id), None)

def get_contacts_for_account(account_id: str) -> list[Contact]:
    contacts = load_contacts()
    return [c for c in contacts if c.account_id == account_id]

def get_opportunities_for_account(account_id: str) -> list[Opportunity]:
    opportunities = load_opportunities()
    return [o for o in opportunities if o.account_id == account_id]

def get_child_accounts(parent_id: str) -> list[Account]:
    accounts = load_accounts()
    return [a for a in accounts if a.parent_id == parent_id]

def get_parent_account(account: Account) -> Account | None:
    if account.parent_id:
        return get_account(account.parent_id)
    return None

def search_accounts(query: str) -> list[Account]:
    accounts = load_accounts()
    query = query.lower()
    return [a for a in accounts if query in a.name.lower()]


# Health scoring (DataFlow only)

ALERT_THRESHOLD = 80

def calculate_health_score(account: Account, opportunities: list[Opportunity]) -> HealthScore | None:
    # Skip prospects
    if account.status != "customer":
        return None

    signals = []
    today = date.today()

    # Contract signals
    if account.contract_end:
        days_remaining = (account.contract_end - today).days
        if days_remaining < -90:
            signals.append(HealthSignal("contract_expired_long", "Contract expired over 90 days ago", "critical", -50))
        elif days_remaining < 0:
            signals.append(HealthSignal("contract_expired", "Contract expired", "critical", -40))
        elif days_remaining <= 30:
            signals.append(HealthSignal("contract_expiring_30", "Contract expiring within 30 days", "critical", -30))
        elif days_remaining <= 90:
            signals.append(HealthSignal("contract_expiring_90", "Contract expiring within 90 days", "warning", -15))

    # Pipeline signals
    open_stages = {"discovery", "proposal", "negotiation"}
    open_opps = [o for o in opportunities if o.stage in open_stages]
    if open_opps:
        signals.append(HealthSignal("active_pipeline", f"{len(open_opps)} active opportunity(s) in pipeline", "positive", 15))
    else:
        signals.append(HealthSignal("no_pipeline", "No active opportunities in pipeline", "warning", -10))

    score = max(0, min(100, 100 + sum(s.points for s in signals)))

    if score >= 80:
        category = "healthy"
    elif score >= 50:
        category = "at_risk"
    else:
        category = "critical"

    return HealthScore(score=score, category=category, signals=signals)


def get_all_alerts() -> list[Alert]:
    accounts = load_accounts()
    opportunities = load_opportunities()
    alerts = []

    for account in accounts:
        account_opps = [o for o in opportunities if o.account_id == account.id]
        health = calculate_health_score(account, account_opps)
        if health and health.score < ALERT_THRESHOLD:
            arr = account.contract_value or 0
            alerts.append(Alert(
                account_id=account.id,
                account_name=account.name,
                health_score=health,
                arr=arr,
            ))

    alerts.sort(key=lambda a: a.health_score.score)
    return alerts
