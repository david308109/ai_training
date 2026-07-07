-- Banking Domain Schema for Data Agent
-- Tables: branches, relationship_managers, customers, deposits

PRAGMA foreign_keys = ON;

-- ============================================================
-- DDL
-- ============================================================

CREATE TABLE IF NOT EXISTS branches (
    branch_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    branch_name TEXT    NOT NULL UNIQUE,
    city        TEXT    NOT NULL,
    region      TEXT    NOT NULL
);

CREATE TABLE IF NOT EXISTS relationship_managers (
    rm_id       INTEGER PRIMARY KEY AUTOINCREMENT,
    rm_name     TEXT    NOT NULL,
    branch_id   INTEGER NOT NULL,
    hire_date   TEXT    NOT NULL,  -- ISO-8601 date
    FOREIGN KEY (branch_id) REFERENCES branches(branch_id)
);

CREATE TABLE IF NOT EXISTS customers (
    customer_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name TEXT    NOT NULL,
    gender        TEXT    CHECK(gender IN ('M', 'F')),
    age           INTEGER,
    phone         TEXT,
    rm_id         INTEGER NOT NULL,
    created_date  TEXT    NOT NULL,  -- ISO-8601 date
    FOREIGN KEY (rm_id) REFERENCES relationship_managers(rm_id)
);

CREATE TABLE IF NOT EXISTS deposits (
    deposit_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id   INTEGER NOT NULL,
    deposit_type  TEXT    NOT NULL CHECK(deposit_type IN ('Demand', 'Time', 'Savings')),
    amount        REAL    NOT NULL,
    currency      TEXT    NOT NULL DEFAULT 'TWD',
    open_date     TEXT    NOT NULL,  -- ISO-8601 date
    maturity_date TEXT,              -- NULL for demand deposits
    interest_rate REAL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- ============================================================
-- Seed Data
-- ============================================================

-- Branches (6)
INSERT OR IGNORE INTO branches (branch_name, city, region) VALUES
    ('Xinyi Branch',     'Taipei',     'North'),
    ('Banqiao Branch',   'New Taipei', 'North'),
    ('Taichung Branch',  'Taichung',   'Central'),
    ('Tainan Branch',    'Tainan',     'South'),
    ('Kaohsiung Branch', 'Kaohsiung',  'South'),
    ('Hsinchu Branch',   'Hsinchu',    'North');

-- Relationship Managers (8)
INSERT OR IGNORE INTO relationship_managers (rm_name, branch_id, hire_date) VALUES
    ('Alice Wang',   1, '2018-03-15'),
    ('Bob Chen',     1, '2019-07-01'),
    ('Carol Lin',    2, '2017-11-20'),
    ('David Wu',     3, '2020-01-10'),
    ('Eva Huang',    4, '2016-05-22'),
    ('Frank Liu',    5, '2021-09-01'),
    ('Grace Tsai',   6, '2019-02-14'),
    ('Henry Chang',  3, '2022-06-30');

-- Customers (20)
INSERT OR IGNORE INTO customers (customer_name, gender, age, phone, rm_id, created_date) VALUES
    ('James Lee',        'M', 45, '0912-345-678', 1, '2020-01-15'),
    ('Mary Kao',         'F', 38, '0923-456-789', 1, '2020-03-22'),
    ('Robert Tseng',     'M', 52, '0934-567-890', 2, '2019-08-10'),
    ('Linda Ho',         'F', 29, '0945-678-901', 2, '2021-05-05'),
    ('Michael Su',       'M', 61, '0956-789-012', 3, '2018-12-01'),
    ('Jennifer Hsu',     'F', 34, '0967-890-123', 3, '2019-06-18'),
    ('William Cheng',    'M', 47, '0978-901-234', 4, '2020-09-30'),
    ('Patricia Yang',    'F', 55, '0911-012-345', 4, '2017-04-12'),
    ('Richard Huang',    'M', 40, '0922-123-456', 5, '2021-01-20'),
    ('Barbara Lai',      'F', 33, '0933-234-567', 5, '2020-07-15'),
    ('Charles Chou',     'M', 58, '0944-345-678', 6, '2016-11-08'),
    ('Susan Wu',         'F', 42, '0955-456-789', 6, '2019-10-25'),
    ('Joseph Fang',      'M', 36, '0966-567-890', 7, '2022-02-14'),
    ('Margaret Kuo',     'F', 50, '0977-678-901', 7, '2018-08-30'),
    ('Thomas Yeh',       'M', 44, '0988-789-012', 8, '2021-11-11'),
    ('Dorothy Pan',      'F', 39, '0912-890-123', 1, '2020-06-06'),
    ('Daniel Liao',      'M', 53, '0923-901-234', 3, '2019-03-17'),
    ('Nancy Chiang',     'F', 31, '0934-012-345', 5, '2022-04-22'),
    ('Steven Hsieh',     'M', 48, '0945-123-456', 6, '2017-09-05'),
    ('Karen Shih',       'F', 41, '0956-234-567', 8, '2021-07-19');

-- Deposits (50+)
INSERT OR IGNORE INTO deposits (customer_id, deposit_type, amount, currency, open_date, maturity_date, interest_rate) VALUES
    -- James Lee
    (1,  'Time',    5000000,  'TWD', '2020-02-01', '2025-02-01', 1.35),
    (1,  'Demand',  1200000,  'TWD', '2020-01-20', NULL,         0.20),
    (1,  'Savings', 800000,   'TWD', '2021-06-15', NULL,         0.50),
    -- Mary Kao
    (2,  'Time',    3000000,  'TWD', '2020-04-10', '2024-04-10', 1.25),
    (2,  'Demand',  500000,   'TWD', '2020-03-25', NULL,         0.20),
    -- Robert Tseng
    (3,  'Time',    8000000,  'TWD', '2019-09-01', '2024-09-01', 1.40),
    (3,  'Savings', 2000000,  'TWD', '2020-01-10', NULL,         0.55),
    -- Linda Ho
    (4,  'Demand',  350000,   'TWD', '2021-05-10', NULL,         0.20),
    (4,  'Savings', 150000,   'TWD', '2021-07-20', NULL,         0.45),
    -- Michael Su
    (5,  'Time',    10000000, 'TWD', '2019-01-15', '2024-01-15', 1.50),
    (5,  'Time',    5000000,  'TWD', '2020-06-01', '2025-06-01', 1.30),
    (5,  'Demand',  3000000,  'TWD', '2018-12-05', NULL,         0.20),
    -- Jennifer Hsu
    (6,  'Savings', 1200000,  'TWD', '2019-07-01', NULL,         0.50),
    (6,  'Demand',  600000,   'TWD', '2019-06-20', NULL,         0.20),
    -- William Cheng
    (7,  'Time',    2000000,  'TWD', '2020-10-15', '2023-10-15', 1.20),
    (7,  'Demand',  900000,   'TWD', '2020-10-01', NULL,         0.20),
    -- Patricia Yang
    (8,  'Time',    7000000,  'TWD', '2017-05-01', '2022-05-01', 1.45),
    (8,  'Savings', 3500000,  'TWD', '2018-03-20', NULL,         0.55),
    (8,  'Demand',  1500000,  'TWD', '2017-04-15', NULL,         0.20),
    -- Richard Huang
    (9,  'Time',    1500000,  'TWD', '2021-02-10', '2024-02-10', 1.15),
    (9,  'Demand',  400000,   'TWD', '2021-01-25', NULL,         0.20),
    -- Barbara Lai
    (10, 'Savings', 700000,   'TWD', '2020-08-01', NULL,         0.50),
    (10, 'Demand',  250000,   'TWD', '2020-07-20', NULL,         0.20),
    -- Charles Chou
    (11, 'Time',    6000000,  'TWD', '2017-01-10', '2022-01-10', 1.40),
    (11, 'Time',    4000000,  'TWD', '2019-05-15', '2024-05-15', 1.30),
    (11, 'Savings', 2500000,  'TWD', '2018-09-01', NULL,         0.55),
    -- Susan Wu
    (12, 'Demand',  800000,   'TWD', '2019-11-01', NULL,         0.20),
    (12, 'Savings', 1000000,  'TWD', '2020-02-14', NULL,         0.50),
    -- Joseph Fang
    (13, 'Time',    500000,   'TWD', '2022-03-01', '2025-03-01', 1.10),
    (13, 'Demand',  200000,   'TWD', '2022-02-20', NULL,         0.20),
    -- Margaret Kuo
    (14, 'Time',    4500000,  'TWD', '2018-09-15', '2023-09-15', 1.35),
    (14, 'Savings', 1800000,  'TWD', '2019-04-01', NULL,         0.50),
    (14, 'Demand',  700000,   'TWD', '2018-09-01', NULL,         0.20),
    -- Thomas Yeh
    (15, 'Time',    1000000,  'TWD', '2021-12-01', '2024-12-01', 1.15),
    (15, 'Demand',  300000,   'TWD', '2021-11-15', NULL,         0.20),
    -- Dorothy Pan
    (16, 'Savings', 2200000,  'TWD', '2020-07-01', NULL,         0.50),
    (16, 'Demand',  900000,   'TWD', '2020-06-10', NULL,         0.20),
    -- Daniel Liao
    (17, 'Time',    3500000,  'TWD', '2019-04-01', '2024-04-01', 1.25),
    (17, 'Savings', 1500000,  'TWD', '2020-08-15', NULL,         0.50),
    (17, 'Demand',  600000,   'TWD', '2019-03-20', NULL,         0.20),
    -- Nancy Chiang
    (18, 'Demand',  180000,   'TWD', '2022-05-01', NULL,         0.20),
    (18, 'Savings', 120000,   'TWD', '2022-06-10', NULL,         0.45),
    -- Steven Hsieh
    (19, 'Time',    9000000,  'TWD', '2017-10-01', '2022-10-01', 1.45),
    (19, 'Time',    3000000,  'TWD', '2020-03-15', '2025-03-15', 1.25),
    (19, 'Savings', 2000000,  'TWD', '2019-01-20', NULL,         0.55),
    (19, 'Demand',  1100000,  'TWD', '2017-09-10', NULL,         0.20),
    -- Karen Shih
    (20, 'Time',    2500000,  'TWD', '2021-08-01', '2024-08-01', 1.20),
    (20, 'Savings', 800000,   'TWD', '2021-09-15', NULL,         0.50),
    (20, 'Demand',  350000,   'TWD', '2021-07-25', NULL,         0.20),
    -- Extra deposits for volume
    (1,  'Time',    2000000,  'TWD', '2022-01-01', '2025-01-01', 1.20),
    (5,  'Savings', 1500000,  'TWD', '2021-03-01', NULL,         0.50),
    (8,  'Time',    2000000,  'TWD', '2020-11-01', '2023-11-01', 1.20),
    (11, 'Demand',  1000000,  'TWD', '2020-06-01', NULL,         0.20);
