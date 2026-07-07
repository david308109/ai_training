"""SQL query templates with business descriptions for RAG retrieval."""

SQL_TEMPLATES: list[dict] = [
    # --- Top / Ranking ---
    {
        "sql": "SELECT c.customer_name, SUM(d.amount) AS total_deposit FROM deposits d JOIN customers c ON d.customer_id = c.customer_id GROUP BY c.customer_id ORDER BY total_deposit DESC LIMIT 1",
        "description": "Find the customer with the highest total deposit amount across all deposit types.",
        "tables": ["deposits", "customers"],
    },
    {
        "sql": "SELECT c.customer_name, SUM(d.amount) AS total_deposit FROM deposits d JOIN customers c ON d.customer_id = c.customer_id GROUP BY c.customer_id ORDER BY total_deposit DESC LIMIT 10",
        "description": "List the top 10 customers ranked by total deposit amount.",
        "tables": ["deposits", "customers"],
    },
    {
        "sql": "SELECT c.customer_name, SUM(d.amount) AS total_deposit FROM deposits d JOIN customers c ON d.customer_id = c.customer_id GROUP BY c.customer_id ORDER BY total_deposit ASC LIMIT 5",
        "description": "Find the 5 customers with the lowest total deposit amount.",
        "tables": ["deposits", "customers"],
    },
    # --- Branch Aggregation ---
    {
        "sql": "SELECT b.branch_name, SUM(d.amount) AS total_deposit FROM deposits d JOIN customers c ON d.customer_id = c.customer_id JOIN relationship_managers rm ON c.rm_id = rm.rm_id JOIN branches b ON rm.branch_id = b.branch_id GROUP BY b.branch_id ORDER BY total_deposit DESC",
        "description": "Total deposit amount per branch, ranked from highest to lowest.",
        "tables": ["deposits", "customers", "relationship_managers", "branches"],
    },
    {
        "sql": "SELECT b.branch_name, COUNT(DISTINCT c.customer_id) AS customer_count FROM customers c JOIN relationship_managers rm ON c.rm_id = rm.rm_id JOIN branches b ON rm.branch_id = b.branch_id GROUP BY b.branch_id ORDER BY customer_count DESC",
        "description": "Count of customers per branch.",
        "tables": ["customers", "relationship_managers", "branches"],
    },
    # --- RM Portfolio ---
    {
        "sql": "SELECT rm.rm_name, COUNT(c.customer_id) AS customer_count FROM relationship_managers rm LEFT JOIN customers c ON c.rm_id = rm.rm_id GROUP BY rm.rm_id ORDER BY customer_count DESC",
        "description": "Relationship Manager portfolio summary: customer count per RM, including those with zero customers.",
        "tables": ["relationship_managers", "customers"],
    },
    {
        "sql": "SELECT rm.rm_name, SUM(d.amount) AS total_aum FROM relationship_managers rm JOIN customers c ON c.rm_id = rm.rm_id JOIN deposits d ON d.customer_id = c.customer_id GROUP BY rm.rm_id ORDER BY total_aum DESC LIMIT 1",
        "description": "Find the RM with the largest total assets under management.",
        "tables": ["relationship_managers", "customers", "deposits"],
    },
    # --- Deposit Type Analysis ---
    {
        "sql": "SELECT deposit_type, COUNT(*) AS count, SUM(amount) AS total, AVG(amount) AS average FROM deposits GROUP BY deposit_type",
        "description": "Breakdown of deposit count, total amount, and average amount by deposit type (Demand, Time, Savings).",
        "tables": ["deposits"],
    },
    {
        "sql": "SELECT c.customer_name, d.amount, d.interest_rate, d.maturity_date FROM deposits d JOIN customers c ON d.customer_id = c.customer_id WHERE d.deposit_type = 'Time' ORDER BY d.amount DESC",
        "description": "List all time deposits with customer name, amount, interest rate, and maturity date.",
        "tables": ["deposits", "customers"],
    },
    # --- Filtering ---
    {
        "sql": "SELECT c.customer_name, SUM(d.amount) AS total_deposit FROM deposits d JOIN customers c ON d.customer_id = c.customer_id GROUP BY c.customer_id HAVING total_deposit > 5000000",
        "description": "Find customers whose total deposits exceed 5,000,000 TWD.",
        "tables": ["deposits", "customers"],
    },
    {
        "sql": "SELECT c.customer_name, SUM(d.amount) AS total_deposit FROM deposits d JOIN customers c ON d.customer_id = c.customer_id GROUP BY c.customer_id HAVING total_deposit BETWEEN 1000000 AND 5000000",
        "description": "Find customers whose total deposits are between 1,000,000 and 5,000,000 TWD.",
        "tables": ["deposits", "customers"],
    },
    # --- Customer Lookup ---
    {
        "sql": "SELECT c.customer_name, c.age, c.gender, rm.rm_name, b.branch_name, SUM(d.amount) AS total_deposit FROM customers c JOIN relationship_managers rm ON c.rm_id = rm.rm_id JOIN branches b ON rm.branch_id = b.branch_id LEFT JOIN deposits d ON d.customer_id = c.customer_id WHERE c.customer_name LIKE '%{name}%' GROUP BY c.customer_id",
        "description": "Look up a customer by name and show their details including RM, branch, and total deposits.",
        "tables": ["customers", "relationship_managers", "branches", "deposits"],
    },
    {
        "sql": "SELECT * FROM customers ORDER BY created_date DESC LIMIT 5",
        "description": "List the 5 most recently created customer accounts.",
        "tables": ["customers"],
    },
    # --- Aggregation ---
    {
        "sql": "SELECT COUNT(*) AS total_customers FROM customers",
        "description": "Count the total number of customers.",
        "tables": ["customers"],
    },
    {
        "sql": "SELECT SUM(amount) AS total_deposits FROM deposits",
        "description": "Calculate the total amount of all deposits in the bank.",
        "tables": ["deposits"],
    },
    {
        "sql": "SELECT AVG(amount) AS avg_deposit FROM deposits",
        "description": "Calculate the average deposit amount across all accounts.",
        "tables": ["deposits"],
    },
    {
        "sql": "SELECT AVG(age) AS avg_age FROM customers",
        "description": "Calculate the average age of all customers.",
        "tables": ["customers"],
    },
    # --- Region / Geography ---
    {
        "sql": "SELECT b.region, SUM(d.amount) AS total_deposit FROM deposits d JOIN customers c ON d.customer_id = c.customer_id JOIN relationship_managers rm ON c.rm_id = rm.rm_id JOIN branches b ON rm.branch_id = b.branch_id GROUP BY b.region ORDER BY total_deposit DESC",
        "description": "Total deposit amount by region (North, Central, South).",
        "tables": ["deposits", "customers", "relationship_managers", "branches"],
    },
    # --- Interest Rate ---
    {
        "sql": "SELECT c.customer_name, d.amount, d.interest_rate, d.maturity_date FROM deposits d JOIN customers c ON d.customer_id = c.customer_id WHERE d.interest_rate > 1.3 ORDER BY d.interest_rate DESC",
        "description": "Find deposits with interest rate above 1.3%, showing customer name, amount, interest rate, and maturity date.",
        "tables": ["deposits", "customers"],
    },
]
