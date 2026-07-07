"""Business context documents describing banking domain concepts."""

BUSINESS_CONTEXT: list[dict] = [
    {
        "topic": "Relationship Manager (RM)",
        "content": (
            "A Relationship Manager (RM) is a bank employee responsible for managing "
            "a portfolio of high-value customers. Each RM is assigned to a specific branch "
            "and handles customer onboarding, financial advisory, and deposit product sales. "
            "RM performance is typically measured by total Assets Under Management (AUM), "
            "which is the sum of all deposit amounts across their assigned customers."
        ),
    },
    {
        "topic": "Deposit Types",
        "content": (
            "The bank offers three types of deposit products:\n"
            "1. Demand Deposit — a checking/current account where funds can be withdrawn "
            "at any time without penalty. Has the lowest interest rate (around 0.20%).\n"
            "2. Savings Deposit — earns a moderate interest rate (0.45%-0.55%) and allows "
            "flexible withdrawals, though some restrictions may apply.\n"
            "3. Time Deposit (Fixed Deposit) — funds are locked for a fixed term (maturity date). "
            "Offers the highest interest rate (1.10%-1.50%) but early withdrawal incurs penalties."
        ),
    },
    {
        "topic": "Branch Hierarchy",
        "content": (
            "The bank operates branches across Taiwan, organized into three regions:\n"
            "- North: Taipei, New Taipei, Hsinchu\n"
            "- Central: Taichung\n"
            "- South: Tainan, Kaohsiung\n"
            "Each branch has multiple RMs. A branch's total deposits are the sum of all "
            "deposits belonging to customers managed by RMs at that branch."
        ),
    },
    {
        "topic": "Customer Segmentation",
        "content": (
            "Customers are segmented by total deposit volume:\n"
            "- VIP / High-Net-Worth: total deposits > 5,000,000 TWD\n"
            "- Affluent: total deposits between 1,000,000 and 5,000,000 TWD\n"
            "- Mass: total deposits < 1,000,000 TWD\n"
            "RM attention and product offerings vary by segment."
        ),
    },
    {
        "topic": "Assets Under Management (AUM)",
        "content": (
            "AUM refers to the total value of deposits managed by a specific entity "
            "(RM, branch, or region). It is calculated as: "
            "SUM(deposits.amount) for all deposits belonging to customers under that entity. "
            "AUM is the primary metric for branch and RM performance evaluation."
        ),
    },
    {
        "topic": "Currency",
        "content": (
            "All deposit amounts in this system are denominated in TWD (New Taiwan Dollar). "
            "The currency field exists to support future multi-currency expansion, but "
            "currently all records use TWD."
        ),
    },
    {
        "topic": "Interest Rate",
        "content": (
            "Interest rates are stored as annual percentages (e.g. 1.35 means 1.35% per year). "
            "Demand deposits have the lowest rates (~0.20%), Savings deposits are moderate "
            "(~0.45-0.55%), and Time deposits offer the highest rates (~1.10-1.50%). "
            "Higher deposit amounts may qualify for promotional rates."
        ),
    },
]
