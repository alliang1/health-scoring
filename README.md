# Nexus Customer Health

Customer health monitoring for the Nexus CRM platform. Currently configured for DataFlow (enterprise) data only.

## Setup

```bash
pip install -r requirements.txt
python3 app.py
```

Open http://localhost:5000 in your browser.

## Features

- **Customer List** - All accounts sorted by health score (worst first), prospects at bottom
- **Health Scoring** - Automated scores based on contract status and sales pipeline
- **Alerts** - Dashboard of at-risk and critical customers with ARR impact
- **Customer Detail** - Full profile with contacts, opportunities, and health signals
- **Search** - Find customers by company name

## Health Scoring

Each customer starts at 100. Signals adjust the score up or down.

| Signal | Points |
|--------|--------|
| Contract expired (over 90 days) | -50 |
| Contract expired | -40 |
| Contract expiring within 30 days | -30 |
| Contract expiring within 90 days | -15 |
| No active pipeline | -10 |
| Active opportunities in pipeline | +15 |

**Categories:** Healthy (80-100), At Risk (50-79), Critical (0-49)

Customers with status "prospect" are not scored.

## Data

```
data/
  dataflow_accounts.json       33 accounts (enterprise)
  dataflow_contacts.json       57 contacts
  dataflow_opportunities.json  40 opportunities
  quicksync_companies.json     40 companies (SMB) - NOT CONNECTED
```

See `docs/` for data dictionaries describing each field.

## Current Models

```
Account
  id, name, industry, annual_revenue, employees, address
  status (customer | prospect)
  contract_value, contract_start, contract_end

Contact
  id, first_name, last_name, title, email, phone
  account_id -> Account

Opportunity
  id, name, amount, product
  stage (discovery | proposal | negotiation | closed_won | closed_lost)
  close_date
  account_id -> Account
```

## Known Issues

- QuickSync data exists in the database but is not connected to the application
- Some customers appear in both data sources with inconsistent naming
