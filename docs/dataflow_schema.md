# DataFlow Data Dictionary

DataFlow is Nexus's enterprise CRM product. Data is stored in three tables.

## Accounts

Customer and prospect records.

| Field | Type | Description |
|-------|------|-------------|
| id | string | Unique identifier (e.g., "df-a1") |
| name | string | Company name |
| parent_id | string or null | Links subsidiary to parent account |
| industry | string | Industry classification |
| annual_revenue | integer | Company annual revenue in USD |
| employees | integer | Employee count |
| address | string | Primary address |
| status | string | "customer" or "prospect" |
| contract_value | integer or null | Annual contract value in USD. Null for prospects. |
| contract_start | date or null | Contract start date (YYYY-MM-DD) |
| contract_end | date or null | Contract end date (YYYY-MM-DD) |

**Notes:**
- Parent/subsidiary relationships are tracked via `parent_id`. A subsidiary's `parent_id` points to the parent account's `id`.
- `contract_value` represents annual recurring revenue (ARR) for this specific account.
- Prospects have no contract fields.

## Contacts

People associated with accounts.

| Field | Type | Description |
|-------|------|-------------|
| id | string | Unique identifier (e.g., "df-c1") |
| account_id | string | Foreign key to Accounts |
| first_name | string | First name |
| last_name | string | Last name |
| title | string | Job title |
| email | string | Email address |
| phone | string | Phone number |

**Notes:**
- Each contact belongs to exactly one account.
- Accounts typically have 1-3 contacts.

## Opportunities

Sales pipeline tracking.

| Field | Type | Description |
|-------|------|-------------|
| id | string | Unique identifier (e.g., "df-o1") |
| account_id | string | Foreign key to Accounts |
| name | string | Opportunity name |
| amount | integer | Deal value in USD |
| stage | string | Pipeline stage |
| close_date | date | Expected or actual close date (YYYY-MM-DD) |
| product | string | Product line |

**Stage values:** discovery, proposal, negotiation, closed_won, closed_lost

**Product values:** DataFlow Enterprise, DataFlow Standard, DataFlow Analytics
