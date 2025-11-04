📘 README.md
# Module 9 - FastAPI + PostgreSQL + pgAdmin (IS601)

### Author: Megha Saju  
### Course: IS601 – Web Systems Development  
### Semester: Fall 2025  


## 📋 Overview
This project demonstrates how to containerize a FastAPI application with a PostgreSQL database and pgAdmin using **Docker Compose**.  
It also includes raw SQL operations for creating, inserting, querying, updating, and deleting data inside pgAdmin.

---

## 🧱 Project Architecture

**Services (via Docker Compose):**
- **FastAPI** → Runs the calculator web application on port `8000`
- **PostgreSQL** → Stores user and calculation data (port `5432`)
- **pgAdmin** → Database GUI client accessible at [http://localhost:5050](http://localhost:5050)

**Network:** All services share a bridge network (`app-network`).

---

## 🚀 How to Run the Project

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/ms328/module9_is601.git
cd module9_is601

2️⃣ Build and Start the Containers
docker compose up --build


✅ Expected running containers:

fastapi_calculator → http://localhost:8000

pgadmin → http://localhost:5050

postgres_db → healthy on port 5432

🧠 pgAdmin Setup

Go to http://localhost:5050

Log in using:

Email: admin@example.com

Password: admin

Register a new server:

Host name: db

Port: 5432

Username: postgres

Password: postgres

Select the database fastapi_db and open the Query Tool.

🧩 SQL Commands Used
(A) Create Tables
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE calculations (
    id SERIAL PRIMARY KEY,
    operation VARCHAR(20) NOT NULL,
    operand_a FLOAT NOT NULL,
    operand_b FLOAT NOT NULL,
    result FLOAT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

(B) Insert Records
INSERT INTO users (username, email) 
VALUES ('msaju20', 'ms328@njit.edu');

INSERT INTO calculations (operation, operand_a, operand_b, result, user_id)
VALUES
('add', 2, 3, 5, 2),
('divide', 10, 2, 5, 2),
('multiply', 4, 5, 20, 2);

(C) Query Data
SELECT * FROM users;
SELECT * FROM calculations;
SELECT u.username, c.operation, c.operand_a, c.operand_b, c.result
FROM calculations c
JOIN users u ON c.user_id = u.id;

(D) Update a Record
UPDATE calculations
SET result = 6
WHERE id = 1;

(E) Delete a Record
DELETE FROM calculations
WHERE id = 2;

📸 Documentation

Screenshots of each SQL command’s output and Docker container status are included in the /screenshots folder or Module9_Report.docx.
Each screenshot demonstrates:

Successful table creation

Data insertion and relationships

Query results

Record update and deletion

🧩 Learning Reflection

Through this module, I learned how to use Docker Compose to integrate multiple services, configure PostgreSQL containers, and manage database schemas using pgAdmin. Writing raw SQL helped reinforce one-to-many relationships and the importance of foreign key constraints when connecting tables.

🧰 Technologies Used

Python 3.10

FastAPI

PostgreSQL 18+

pgAdmin 4

Docker & Docker Compose

🏁 How to Stop Containers
docker compose down


To remove all containers and volumes:

docker compose down -v

✅ Author

Megha Saju
📧 ms328@njit.edu

GitHub: ms328
