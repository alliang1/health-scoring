# QuickSync Data Dictionary

QuickSync is Nexus's self-serve SMB product. Data is stored in a single flat table.

## Companies

| Field | Type | Description |
|-------|------|-------------|
| id | string | Unique identifier (e.g., "qs-1") |
| company_name | string | Company name |
| contact_name | string | Primary contact full name |
| contact_email | string | Primary contact email |
| plan | string | Subscription tier |
| mrr | integer | Monthly recurring revenue in USD |
| billing_cycle | string | "monthly" or "annual" |
| signup_date | date | Account creation date (YYYY-MM-DD) |
| renewal_date | date | Next renewal date (YYYY-MM-DD) |
| usage_gb | integer | Current storage usage in GB |
| users | integer | Number of active users |

**Plan tiers:**

| Plan | MRR Range | Typical Usage |
|------|-----------|---------------|
| starter | $299 | 1-5 users, up to 15 GB |
| professional | $899-$1,499 | 5-30 users, up to 150 GB |
| business | $2,499 | 20-100 users, up to 500 GB |

**Notes:**
- Flat structure: no account hierarchy, no separate contacts table, no opportunity tracking.
- Each company has exactly one contact on file.
- `mrr` is the monthly rate regardless of `billing_cycle`. Annual billing is `mrr * 12` per year.
- `renewal_date` may be in the past if the subscription has lapsed.
