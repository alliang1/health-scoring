## Features

- **Customer List** - All accounts sorted by health score (worst first), prospects at bottom. Sortable A-Z/Z-A by clicking on the triangle next to "Customer"
- **Health Scoring** - Automated scores based on contract status and sales pipeline
- **Alerts** - Dashboard of at-risk and critical customers with ARR impact
- **Customer Detail** - Full profile with contacts, opportunities, and health signals, and source system breakdown
- **Search** - Find customers by company name across both systems
- **Possible Duplicate Flagging** - Customers with unconfirmed name matches across systems are flagged for manual review

## New Changes
In the original app, it only scored DataFlow cutsomers. QuickSync data was loaded but it was not connected. This means that the customers that only existed in QuickSync had no health score. So we implemented a unified data model that bridges them so that that both system datas are all under one single "Customer" entity. 

### Customer fields: 
- **customer_id** - unified id (Uses DataFlow id if available and otherwise uses QuickSync id)
- **customer_name** - from DataFlow "name" or QuickSync "company_name" 
- **status** - "customer" or "prospect"
- **primary_contact_name** - normalized from whichever source
- **primary_contact_email** - normalized from whichever source
- **ARR** - normalized annual recurring revenue
- **contract_start** - normalized contract dates
- **contract_end** - normalized contract dates
- **dataflow** - links to source records
- **quicksync** - links to source records
- **possible_duplicate** - duplicate flag fields
- **possible_duplicate_match** - duplicate flag fields

### Customer Matching 
- Matches based on the confidence scale in report 

### Alert Threshold 
If customer's score is below 80 it appears in the Alerts Page & prospects are not scored

## How to Verify
1. Both sources are connected: Go to Customers and each row shows whether it's from DataFlow or QuickSync in the "Source" section. 
2. For health scores the expired or expiring contracts show critical or at risk. 
3. Possible duplicates are flagged and it can be easily checked if alphabetized
4. Alerts is on the alerts page and shows customers from both systems 
5. Sort: the triangle next to "Customers" should default to gray. Click to toggle to A-Z, click again for Z-A, one more time to go back to its original sort. 
6. To search just type in the company and it should appear with the badge it is associated to.


# Nexus Customer Health

Customer health monitoring for the Nexus CRM platform. Currently configured for DataFlow (enterprise) data only.

## Setup

```bash
pip install -r requirements.txt
python3 app.py
```

Open http://localhost:5000 in your browser.


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
