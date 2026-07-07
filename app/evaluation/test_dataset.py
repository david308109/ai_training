"""Test dataset with ground truth Q&A pairs for evaluation."""

TEST_CASES: list[dict] = [
    # --- Single-table lookups ---
    {
        "question": "How many customers are there?",
        "expected_sql": "SELECT COUNT(*) AS total_customers FROM customers",
    },
    {
        "question": "List all branch names.",
        "expected_sql": "SELECT branch_name FROM branches",
    },
    {
        "question": "Show the 5 most recently created customer accounts.",
        "expected_sql": "SELECT * FROM customers ORDER BY created_date DESC LIMIT 5",
    },
    # --- Aggregation ---
    {
        "question": "What is the total amount of all deposits?",
        "expected_sql": "SELECT SUM(amount) AS total_deposits FROM deposits",
    },
    {
        "question": "What is the average deposit amount?",
        "expected_sql": "SELECT AVG(amount) AS avg_deposit FROM deposits",
    },
    {
        "question": "How many deposits are there for each deposit type?",
        "expected_sql": "SELECT deposit_type, COUNT(*) AS count FROM deposits GROUP BY deposit_type",
    },
    # --- Sorting / Ranking ---
    {
        "question": "Who has the highest total deposit?",
        "expected_sql": "SELECT c.customer_name, SUM(d.amount) AS total_deposit FROM deposits d JOIN customers c ON d.customer_id = c.customer_id GROUP BY c.customer_id ORDER BY total_deposit DESC LIMIT 1",
    },
    {
        "question": "List the top 5 customers by total deposit amount.",
        "expected_sql": "SELECT c.customer_name, SUM(d.amount) AS total_deposit FROM deposits d JOIN customers c ON d.customer_id = c.customer_id GROUP BY c.customer_id ORDER BY total_deposit DESC LIMIT 5",
    },
    # --- Filtering ---
    {
        "question": "Which customers have total deposits exceeding 5 million TWD?",
        "expected_sql": "SELECT c.customer_name, SUM(d.amount) AS total_deposit FROM deposits d JOIN customers c ON d.customer_id = c.customer_id GROUP BY c.customer_id HAVING total_deposit > 5000000",
    },
    {
        "question": "Show all time deposits with interest rate above 1.3%.",
        "expected_sql": "SELECT c.customer_name, d.amount, d.interest_rate, d.maturity_date FROM deposits d JOIN customers c ON d.customer_id = c.customer_id WHERE d.deposit_type = 'Time' AND d.interest_rate > 1.3 ORDER BY d.interest_rate DESC",
    },
    # --- Joins ---
    {
        "question": "What is the total deposit for each branch?",
        "expected_sql": "SELECT b.branch_name, SUM(d.amount) AS total_deposit FROM deposits d JOIN customers c ON d.customer_id = c.customer_id JOIN relationship_managers rm ON c.rm_id = rm.rm_id JOIN branches b ON rm.branch_id = b.branch_id GROUP BY b.branch_id ORDER BY total_deposit DESC",
    },
    {
        "question": "How many customers does each RM manage?",
        "expected_sql": "SELECT rm.rm_name, COUNT(c.customer_id) AS customer_count FROM relationship_managers rm LEFT JOIN customers c ON c.rm_id = rm.rm_id GROUP BY rm.rm_id ORDER BY customer_count DESC",
    },
    {
        "question": "Which RM has the highest total AUM?",
        "expected_sql": "SELECT rm.rm_name, SUM(d.amount) AS total_aum FROM relationship_managers rm JOIN customers c ON c.rm_id = rm.rm_id JOIN deposits d ON d.customer_id = c.customer_id GROUP BY rm.rm_id ORDER BY total_aum DESC LIMIT 1",
    },
    # --- GROUP BY ---
    {
        "question": "Total deposits by region.",
        "expected_sql": "SELECT b.region, SUM(d.amount) AS total_deposit FROM deposits d JOIN customers c ON d.customer_id = c.customer_id JOIN relationship_managers rm ON c.rm_id = rm.rm_id JOIN branches b ON rm.branch_id = b.branch_id GROUP BY b.region ORDER BY total_deposit DESC",
    },
    {
        "question": "Show deposit type breakdown: count, total, and average.",
        "expected_sql": "SELECT deposit_type, COUNT(*) AS count, SUM(amount) AS total, AVG(amount) AS average FROM deposits GROUP BY deposit_type",
    },
    # --- More complex ---
    {
        "question": "Which branch has the most customers?",
        "expected_sql": "SELECT b.branch_name, COUNT(DISTINCT c.customer_id) AS customer_count FROM customers c JOIN relationship_managers rm ON c.rm_id = rm.rm_id JOIN branches b ON rm.branch_id = b.branch_id GROUP BY b.branch_id ORDER BY customer_count DESC LIMIT 1",
    },
    {
        "question": "List all customers managed by Alice Wang with their total deposits.",
        "expected_sql": "SELECT c.customer_name, SUM(d.amount) AS total_deposit FROM customers c JOIN relationship_managers rm ON c.rm_id = rm.rm_id JOIN deposits d ON d.customer_id = c.customer_id WHERE rm.rm_name = 'Alice Wang' GROUP BY c.customer_id",
    },
    {
        "question": "What is the average age of customers?",
        "expected_sql": "SELECT AVG(age) AS avg_age FROM customers",
    },
]