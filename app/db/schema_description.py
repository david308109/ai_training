"""Human-readable schema description optimised for LLM consumption."""

SCHEMA_DESCRIPTION = """
=== Banking Database Schema ===

TABLE: branches
  - branch_id   (INTEGER, PK, auto-increment) — unique identifier for the branch
  - branch_name (TEXT, unique, not null) — display name of the branch, e.g. "Xinyi Branch"
  - city        (TEXT, not null) — city where the branch is located
  - region      (TEXT, not null) — geographic region: "North", "Central", or "South"

TABLE: relationship_managers
  - rm_id     (INTEGER, PK, auto-increment) — unique identifier for the RM
  - rm_name   (TEXT, not null) — full name of the Relationship Manager
  - branch_id (INTEGER, FK → branches.branch_id) — the branch this RM belongs to
  - hire_date (TEXT, ISO-8601 date) — date the RM was hired
  Relationships: Each RM belongs to exactly one branch.

TABLE: customers
  - customer_id   (INTEGER, PK, auto-increment) — unique identifier for the customer
  - customer_name (TEXT, not null) — full name of the customer
  - gender        (TEXT, 'M' or 'F') — customer gender
  - age           (INTEGER) — customer age
  - phone         (TEXT) — contact phone number
  - rm_id         (INTEGER, FK → relationship_managers.rm_id) — assigned Relationship Manager
  - created_date  (TEXT, ISO-8601 date) — date customer account was created
  Relationships: Each customer is assigned to exactly one RM.

TABLE: deposits
  - deposit_id    (INTEGER, PK, auto-increment) — unique identifier for the deposit
  - customer_id   (INTEGER, FK → customers.customer_id) — the customer who owns this deposit
  - deposit_type  (TEXT, one of 'Demand', 'Time', 'Savings') — type of deposit product
  - amount        (REAL, not null) — deposit amount in the specified currency
  - currency      (TEXT, default 'TWD') — currency code (Taiwan Dollar)
  - open_date     (TEXT, ISO-8601 date) — date the deposit was opened
  - maturity_date (TEXT, ISO-8601 date, nullable) — maturity date for time deposits; NULL for demand/savings
  - interest_rate (REAL) — annual interest rate as a percentage, e.g. 1.35
  Relationships: Each deposit belongs to exactly one customer.

=== Common Join Paths ===
  deposits → customers          ON deposits.customer_id = customers.customer_id
  customers → relationship_managers ON customers.rm_id = relationship_managers.rm_id
  relationship_managers → branches  ON relationship_managers.branch_id = branches.branch_id

=== Business Rules ===
  - A "total deposit" for a customer means the SUM of all deposit amounts across all deposit types.
  - Demand deposits have no maturity date.
  - Time deposits always have a maturity date and typically have a higher interest rate.
  - All monetary amounts are in TWD (New Taiwan Dollar) unless stated otherwise.
""".strip()


SCHEMA_DESCRIPTIONS_FOR_INDEX = [
    {
        "table_name": "branches",
        "description": "Bank branch locations. Each branch has a name, city, and region (North/Central/South). Related to relationship_managers.",
        "columns": "branch_id, branch_name, city, region",
    },
    {
        "table_name": "relationship_managers",
        "description": "Relationship Managers (RMs) who manage customer portfolios. Each RM belongs to one branch. Connects branches to customers.",
        "columns": "rm_id, rm_name, branch_id, hire_date",
    },
    {
        "table_name": "customers",
        "description": "Bank customers with personal info. Each customer is assigned to one RM. Primary link to deposits.",
        "columns": "customer_id, customer_name, gender, age, phone, rm_id, created_date",
    },
    {
        "table_name": "deposits",
        "description": "Deposit accounts (Demand, Time, or Savings). Each deposit belongs to one customer. Amount is in TWD. Related to customers.",
        "columns": "deposit_id, customer_id, deposit_type, amount, currency, open_date, maturity_date, interest_rate",
    },
]
