# Databases — Notes

### Transactions & Concurrency

## Concurrency Control in DBMS — Notes

**1. Definition**
"Concurrency control is a mechanism in DBMS that allows simultaneous execution of transactions while maintaining ACID properties." It handles conflicting operations on shared data, inconsistent states, and lost/incorrect updates.

**2. The three named concurrency problems**
- **Dirty Read**: "A transaction reads uncommitted data from another transaction that may later roll back."
- **Lost Update**: "Two transactions update the same data and one update overwrites the other."
- **Inconsistent Read**: "A transaction reads the same data multiple times and the data changes in between reads."

**3. Lock-Based Concurrency Control**
Uses locks (shared = read, exclusive = write) to restrict access to data items during a transaction; ensures serializability and prevents conflicts.
*e.g. Two-Phase Locking (2PL) guarantees that once a transaction releases a lock, it cannot obtain any new locks.*

**4. Timestamp-Based Concurrency Control**
Each transaction is assigned a timestamp; the DBMS orders transactions and resolves conflicts based on start time.

**5. Recoverable Schedules**
"A transaction commits only if all transactions it depends on have committed." Prevents inconsistencies from dependent transactions.
*e.g. Strict 2PL ensures recoverability by delaying commits until all dependent transactions commit.*

**6. Cascadeless Schedules**
Avoids cascading rollbacks — a transaction may read data only after the transaction that wrote it has committed.

No worked numerical example (schedule with actual T1/T2 operations) is given on this specific page — it stays at the definition/protocol-name level. See the Conflict Serializability and Two-Phase Locking notes below for the actual worked schedules.

**Priority for your prep:** the three problem names (dirty read / lost update / inconsistent read) and the lock-based vs timestamp-based distinction are common one-line/MCQ fodder. The real numerical practice — schedules, precedence graphs, lock sequences — comes from the next two topics; treat this page as the vocabulary layer underneath them.

---

## ACID Properties in DBMS — Notes

**1. Atomicity**
"A transaction is all-or-nothing — either all its operations succeed, or none are applied." On failure, roll back to original state; no partial changes persist.
*Worked example (from page): Transaction T = T1 + T2 = "Transfer of $100 from account X to account Y." If the transaction fails after T1 completes but before T2 completes, the database would be left inconsistent — Atomicity forces a full rollback instead of a partial one.*

**2. Consistency**
"The database must remain in a valid state before and after a transaction," obeying all defined rules/constraints (PK, FK, etc.). A transaction that deducts from one account without crediting another violates consistency and is rolled back.
> Worked example (from page):
> `Total before T occurs = 500 + 200 = 700`
> `Total after T occurs = 400 + 300 = 700`
> The sum across accounts must stay invariant across the transaction.

**3. Isolation**
Transactions run independently; "changes made by one transaction are not visible to others until they are committed." Prevents dirty reads, non-repeatable reads, phantom reads.
> Worked example (from page): X = 500, Y = 500.
> Transaction **T**: transfers $50 from X to Y → reads Y(500), deducts $50 from X (new X = 450), adds $50 to Y (new Y = 550).
> Transaction **T″**: starts concurrently, reads X (500) and Y (500), computes sum = 500 + 500 = 1000. Meanwhile X, Y become 450, 550 — so the *correct* sum is 450 + 550 = 1000. Isolation requires T″ not see the in-flight (dirty) values of T — it must only see X, Y once T commits, otherwise it could read one updated and one stale value and get a wrong sum.

**4. Durability**
"Once a transaction is committed, its changes are permanently saved, even if the system fails" — stored in non-volatile memory so recovery restores the last committed state.
*e.g. After a committed transfer from Account A to B, a crash immediately after commit still leaves the transfer intact on recovery.*

**5. Responsibility mapping (from page table)**
| Property | Responsible component |
|---|---|
| Atomicity | Transaction Manager |
| Consistency | Application programmer |
| Isolation | Concurrency Control Manager |
| Durability | Recovery Manager |

**Priority for your prep:** the bank-transfer numbers (500+200=700 / 400+300=700, and the X=500,Y=500 isolation example) are exactly the shape ISRO/GATE like for "which ACID property is violated" questions — memorize the pattern, not just the property names. The responsibility-mapping table is a good quick MCQ trap (e.g. "which property does the concurrency control manager enforce?").

---

## Conflict Serializability in DBMS — Notes

**1. Definition**
"Conflict Serializability ensures that a concurrent schedule produces the same result as some serial execution by reordering non-conflicting operations." Stricter than View Serializability.

**2. Conflicting operations — rule**
Two operations conflict iff **all three** hold: (a) different transactions, (b) same data item, (c) at least one is a write.
| Op by Tᵢ | Op by Tⱼ | Status |
|---|---|---|
| read(Q) | read(Q) | No Conflict |
| read(Q) | write(Q) | Conflict |
| write(Q) | read(Q) | Conflict |
| write(Q) | write(Q) | Conflict |

**3. Checking serializability by swapping (from page)**
> Worked example (from page) — Schedule S1:
> `S1: R1(A), W1(A), R2(A), W2(A), R1(B), W1(B), R2(B), W2(B)`
> Split by transaction (order within each Tᵢ must be preserved):
> `T1: R1(A), W1(A), R1(B), W1(B)`
> `T2: R2(A), W2(A), R2(B), W2(B)`
> Possible serial schedules: T1→T2 or T2→T1.
> Step 1 — swap non-conflicting `R2(A)` and `R1(B)` in S1:
> `S11: R1(A), W1(A), R1(B), W2(A), R2(A), W1(B), R2(B), W2(B)`
> Step 2 — swap non-conflicting `W2(A)` and `W1(B)` in S11:
> `S12: R1(A), W1(A), R1(B), W1(B), R2(A), W2(A), R2(B), W2(B)`
> S12 is serial (all of T1 before all of T2) → **S1 is conflict serializable** (equivalent to T1→T2).

> Worked example (from page) — Schedule S2 (not serializable):
> `S2: R2(A), W2(A), R1(A), W1(A), R1(B), W1(B), R2(B), W2(B)`
> `T1: R1(A), W1(A), R1(B), W1(B)` ; `T2: R2(A), W2(A), R2(B), W2(B)`
> Swap non-conflicting `R1(A)` and `R2(B)`:
> `S21: R2(A), W2(A), R2(B), W1(A), R1(B), W1(B), R1(A), W2(B)`
> Swap non-conflicting `W1(A)` and `W2(B)`:
> `S22: R2(A), W2(A), R2(B), W2(B), R1(B), W1(B), R1(A), W1(A)`
> In S22 all of T2 comes first, but T1's own operations are out of their required order (should be R1(A),W1(A),R1(B),W1(B)) → **S2 is NOT conflict serializable.**

**4. Precedence Graph (Serialization Graph) method — algorithm (from page)**
Build directed graph G(V,E): one node per transaction. Draw edge Tᵢ→Tⱼ whenever a conflicting operation of Tᵢ precedes the corresponding conflicting operation of Tⱼ:
1. read_item(X) by Tⱼ after write_item(X) by Tᵢ → edge Tᵢ→Tⱼ
2. write_item(X) by Tⱼ after read_item(X) by Tᵢ → edge Tᵢ→Tⱼ
3. write_item(X) by Tⱼ after write_item(X) by Tᵢ → edge Tᵢ→Tⱼ
"Schedule S is serializable if there is no cycle in the precedence graph." If acyclic, **Topological Sort** of the graph gives a valid equivalent serial order (may be more than one).

> Worked example (from page) — cyclic (NOT serializable):
> `S: r1(x) r1(y) w2(x) w1(x) r2(y)`
> Nodes: T1, T2. Edge T1→T2 from conflicting pair `r1(x)` before `w2(x)`. Edge T2→T1 from conflicting pair `w2(x)` before `w1(x)`. Graph has a cycle (T1→T2→T1) → **not conflict serializable**, no serial schedule can be derived.

> Worked example (from page) — acyclic (serializable):
> `S1: r1(x) r3(y) w1(x) w2(y) r3(x) w2(x)`
> Graph is acyclic. Topological sort: pick in-degree-0 node first (T1), then T3, then T2 → **conflict serializable**, equivalent to serial schedule **T1 T3 T2**.

**Priority for your prep:** this is the single highest-yield "complex" topic — practice the swap method on a 2-transaction schedule AND the precedence-graph + topological-sort method on a 3-transaction schedule (both patterns are given above, verbatim from the page). Expect a schedule to be given and asked "is it conflict serializable, and if so what serial order is it equivalent to."

---

## Two Phase Locking Protocol — Notes

**1. Definition**
2PL "manage[s] how multiple concurrent transactions access and modify data" via two phases per transaction.

**2. Growing Phase**
Transaction acquires all locks it needs; "During this phase, it cannot release any locks."

**3. Shrinking Phase**
"Once a transaction starts releasing locks, it cannot acquire any new ones."

**4. Lock types**
- **Shared Lock (S)** — `lock-S`, read-only, multiple transactions can hold it simultaneously.
- **Exclusive Lock (X)** — `lock-X`, read+write, held by only one transaction at a time.

**5. Lock conversion rules**
- **Upgrade** (S→X): only allowed during the **Growing Phase**. *e.g. a transaction reads a value (S) then decides to modify it, so it upgrades to X while still growing.*
- **Downgrade** (X→S): only allowed during the **Shrinking Phase**. *e.g. a transaction holds X to modify a value, then decides it only needs to read, so it downgrades to S while shrinking.*

**6. Lock Point**
"The moment when the transaction finishes acquiring all the locks it needs" — after this point no new locks can be acquired; releasing begins.

**7. Variants**
- **Strict 2PL**: "release their locks only after they commit, preventing other transactions from accessing uncommitted changes." (Fixes cascading rollback risk of basic 2PL.)
- **Rigorous 2PL**: extends strict 2PL to hold **both** read and write locks until commit — even stronger guarantee.
- **Conservative 2PL** is also named on the page as a third variant (acquires all locks upfront to avoid deadlock) but not detailed further there.

**8. Worked example (from page) — lock sequence for T1, T2**
| Step | T1 | T2 |
|---|---|---|
| 1 | lock-S(A) | |
| 2 | | lock-S(A) |
| 3 | lock-X(B) | |
| 4 | .......... | .......... |
| 5 | Unlock(A) | |
| 6 | | Lock-X(C) |
| 7 | Unlock(B) | |
| 8 | | Unlock(A) |
| 9 | | Unlock(C) |
| 10 | .......... | .......... |

Reading off the table (from page):
- **T1**: Growing Phase = steps 1–3, **Lock Point at step 3**, Shrinking Phase = steps 5–7.
- **T2**: Growing Phase = steps 2–6, **Lock Point at step 6**, Shrinking Phase = steps 8–9.

**9. Worked example (added for practice, not from page) — checking legality**
Given the table above: is it valid 2PL for both transactions? Check each transaction independently — T1 acquires (1,3) then only releases (5,7): no acquire after a release → legal. T2 acquires (2,6) then only releases (8,9): no acquire after a release → legal. So the whole schedule obeys 2PL even though T1 and T2's phases overlap in wall-clock time — 2PL is a per-transaction rule, not a global ordering rule.

**Priority for your prep:** memorize Growing→Shrinking (never the reverse) and the Lock Point definition — that is the direct MCQ. The step-table above is exactly the shape of a "given this lock sequence, state the lock point and classify strict vs rigorous" numerical; practice reading growing/shrinking phases off a table like this. Conservative 2PL is lower-yield background.

---

### SQL & Relational Basics

## Structured Query Language (SQL) — Notes

**1. Definition**
"Structured Query Language (SQL) is the standard language used to interact with relational databases," to "store, retrieve, update and manage data efficiently through simple commands."

**2. Syntax rules (from page)**
- Statements end with a semicolon.
- Keywords are case-insensitive.
- String values must be enclosed in single quotes.
- Identifiers: start with a letter, max 30 characters, letters/numbers/underscores only.

**3. Query execution pipeline (from page)**
`Input → Parsing (syntax check) → Optimization (pick fastest plan) → Execution → Output.`

**4. Command categories (from linked GFG "DDL, DQL, DML, DCL, TCL Commands" page — fetched to fill in the categorization this page only references)**

- **DDL — Data Definition Language**: defines/alters/deletes schema objects.
  | Command | Description | Syntax |
  |---|---|---|
  | CREATE | create DB or objects | `CREATE TABLE table_name (column1 data_type, ...);` |
  | DROP | delete objects | `DROP TABLE table_name;` |
  | ALTER | alter structure | `ALTER TABLE table_name ADD COLUMN column_name data_type;` |
  | TRUNCATE | remove all records, free allocated space | `TRUNCATE TABLE table_name;` |
  | RENAME | rename an object | `RENAME TABLE old_table_name TO new_table_name;` |
  > Worked example (from page): `CREATE TABLE employees (employee_id INT PRIMARY KEY, first_name VARCHAR(50), last_name VARCHAR(50), hire_date DATE);`

- **DQL — Data Query Language**: only one real command, `SELECT`; FROM/WHERE/GROUP BY/HAVING/DISTINCT/ORDER BY/LIMIT are clauses of SELECT, not separate commands (page explicitly notes this).
  > Worked example (from page): `SELECT first_name, last_name, hire_date FROM employees WHERE department = 'Sales' ORDER BY hire_date DESC;` — employees in Sales, sorted by hire date descending.

- **DML — Data Manipulation Language**: `INSERT INTO table_name (col1,...) VALUES (val1,...);` / `UPDATE table_name SET col1=val1 WHERE condition;` / `DELETE FROM table_name WHERE condition;`
  > Worked example (from page): `INSERT INTO employees (first_name, last_name, department) VALUES ('Jane', 'Smith', 'HR');`

- **DCL — Data Control Language**: `GRANT privilege_type ON object_name TO user [WITH GRANT OPTION];` / `REVOKE privilege_type ON object_name FROM user [CASCADE];`
  > Worked example (from page): `GRANT SELECT, UPDATE ON employees TO user_name;`

- **TCL — Transaction Control Language**: `BEGIN TRANSACTION;` / `COMMIT;` / `ROLLBACK;` / `SAVEPOINT savepoint_name;`
  > Worked example (from page):
  > ```
  > BEGIN TRANSACTION;
  > UPDATE employees SET department = 'Marketing' WHERE department = 'Sales';
  > SAVEPOINT before_update;
  > UPDATE employees SET department = 'IT' WHERE department = 'HR';
  > ROLLBACK TO SAVEPOINT before_update;
  > COMMIT;
  > ```

**Priority for your prep:** knowing which command belongs to which category (DDL vs DML vs DCL vs TCL) is classic ISRO/GATE MCQ bait — especially TRUNCATE (DDL, not DML) and the fact DQL is really just SELECT + its clauses. The exact CREATE/INSERT/GRANT/SAVEPOINT syntax templates above are worth copying verbatim into your notebook.

---

## SQL Joins (Inner, Left, Right, Full) — Notes

**1. INNER JOIN**
"Used to retrieve rows where matching values exist in both tables." Only matched rows from both sides survive.
`SELECT table1.column1, table2.column1, ... FROM table1 INNER JOIN table2 ON table1.matching_column = table2.matching_column;`

**2. LEFT JOIN**
"Used to retrieve all rows from the left table and matching rows from the right table." Unmatched right-side columns come back NULL.
`SELECT table1.column1, table2.column1, ... FROM table1 LEFT JOIN table2 ON table1.matching_column = table2.matching_column;`

**3. RIGHT JOIN**
"Used to retrieve all rows from the right table and the matching rows from the left table." Unmatched left-side columns come back NULL.
`SELECT table1.column1, table2.column1, ... FROM table1 RIGHT JOIN table2 ON table1.matching_column = table2.matching_column;`

**4. FULL JOIN**
"Used to combine the results of both LEFT JOIN and RIGHT JOIN." All rows from both tables; non-matches padded with NULL on whichever side lacks a match.
`SELECT table1.column1, table2.column1, ... FROM table1 FULL JOIN table2 ON table1.matching_column = table2.matching_column;`

**5. Schema used on page**
The page's running example is a `Student(ROLL_NO, NAME, AGE)` table joined to a `StudentCourse(COURSE_ID, ROLL_NO)` table on `ROLL_NO`, plus a second Employee/Department pair for a NATURAL JOIN example. **Flag:** the actual sample rows and output tables on this page are rendered as embedded images, not text/HTML tables — they could not be extracted verbatim even from the raw page source. Only the column names and the SQL syntax templates above are genuinely verbatim from the page.

> Worked example (added for practice, not from page) — using the page's real schema:
> `Student`: (1, 'Amit', 21), (2, 'Neha', 22), (3, 'Ravi', 23)
> `StudentCourse`: (101, 1), (102, 1), (103, 2)  — columns (COURSE_ID, ROLL_NO)
> `INNER JOIN` on ROLL_NO → rows for Amit (×2, courses 101/102) and Neha (course 103); Ravi dropped (no course).
> `LEFT JOIN` (Student as left) → adds Ravi back with COURSE_ID = NULL.
> `RIGHT JOIN` (StudentCourse as right) → same matched rows as inner join here since every course row has a matching student.
> `FULL JOIN` → Amit×2, Neha×1, Ravi with NULL course — union of left and right results.

**Priority for your prep:** the four definitions and which side keeps unmatched rows (LEFT keeps left, RIGHT keeps right, FULL keeps both, INNER keeps neither) are the direct exam question — practice tracing a small join like the one above by hand since the page's own numeric table wasn't recoverable.

---

## Database Normalization — Notes

**1. First Normal Form (1NF)**
A relation is in 1NF if "every attribute in that relation is single-valued attribute" (no repeating groups / multi-valued attributes in a cell).

**2. Second Normal Form (2NF)**
Must be in 1NF, and "every non-primary-key attribute is fully functionally dependent on the primary key" (no partial dependency on part of a composite key).

**3. Third Normal Form (3NF)**
Must be in 2NF with no transitive dependency for non-prime attributes. Formally: for every non-trivial FD `X → Y`, at least one holds:
- X is a super key, **or**
- Y is a prime attribute (part of some candidate key).

**4. Boyce-Codd Normal Form (BCNF)**
Must be in 3NF, **and** for every FD `X → Y`, X must be a super key (stricter — no exception for Y being prime).

**5. Fourth Normal Form (4NF)**
Must be in BCNF **and** have no multi-valued dependency.

**6. Fifth Normal Form (5NF)**
Must be in 4NF **and** "cannot be further non loss decomposed" — no join dependency left to exploit.

**7. Why normalize — the page's own example (verbatim reasoning, "Employee_Department Relation")**
The page discusses an `Employee_Department` relation (structure/rows not textually recoverable — likely rendered as an image on the page) and lists these four concrete problems:
- **Insertion anomaly**: "If a new department is created but no employee is assigned to it yet, we cannot store its location because we need an employee record to insert."
- **Update anomaly**: "If the location of the HR department changes, we must update it in multiple rows (for both Nick Wise and Lily Case). If one row is missed, the data becomes inconsistent."
- **Deletion anomaly**: "If all employees in the IT department leave, we lose the department information, including its location."
- **Redundancy**: "The department location is repeated for every employee in the same department."
(Note: "Nick Wise" and "Lily Case" are the actual employee names used in the page's example, confirming a real table existed there even though its rows weren't extractable as text.)

**8. Worked example (added for practice, not from page) — building the same shape of relation and normalizing it**
`Employee_Department(Emp_ID, Emp_Name, Dept_ID, Dept_Location)` with FD: `Emp_ID → Emp_Name, Dept_ID` and `Dept_ID → Dept_Location` (transitive dependency `Emp_ID → Dept_ID → Dept_Location`).
Sample rows: (1, Nick Wise, D1, HR), (2, Lily Case, D1, HR), (3, Raj, D2, IT).
This is in 2NF (single-attribute PK, so no partial dependency possible) but **not 3NF**, because `Dept_Location` depends transitively on `Emp_ID` through `Dept_ID`. Decompose into:
`Employee(Emp_ID, Emp_Name, Dept_ID)` and `Department(Dept_ID, Dept_Location)` — now both relations are in 3NF/BCNF, and updating HR's location is a single-row edit instead of two.

**Priority for your prep:** the 1NF/2NF/3NF/BCNF one-line definitions (especially the 3NF vs BCNF distinction: 3NF allows the "Y is prime" escape hatch, BCNF doesn't) are the most frequently tested. Practice decomposing a small relation with a transitive FD like the one above — that is the standard numerical/short-answer format. 4NF/5NF are lower-yield; know the one-line definitions only.

---

## Types of Keys in Relational Model — Notes

**1. Candidate Key**
"The minimal set of attributes that can uniquely identify a tuple." Must have unique values, no redundant attributes; every table has at least one; a table can have multiple candidate keys but only one becomes the primary key.
*e.g. `STUD_NO` in the `STUDENT` relation.*

**2. Super Key**
"The set of one or more attributes (columns) that can uniquely identify a tuple (record)" — may include unnecessary extra attributes beyond what's needed for uniqueness.
*e.g. `STUD_NO`, or `(STUD_NO, STUD_NAME)`, or `(STUD_NO, PHONE)` — all uniquely identify a student.*

**3. Primary Key**
Chosen from the candidate keys to uniquely identify each record. "It cannot be NULL, as each record must have a valid identifier." May be single-column or composite.
*e.g. `Student(STUD_NO, SNAME, ADDRESS, PHONE)` with `STUD_NO` as primary key.*

**4. Alternate Key**
Any candidate key **not** chosen as primary key; also called a secondary key.
*e.g. If `STUD_NO` is primary key and `PHONE` is also a candidate key, then `PHONE` is the alternate key.*

**5. Foreign Key**
"An attribute in one table that refers to the primary key in another table." Establishes a relationship between a referencing table and a referenced table; unlike a primary key it can contain duplicates and NULLs.
*e.g. `STUD_NO` in `STUDENT_COURSE` refers to `STUD_NO` (primary key) in `STUDENT`; it repeats because a student can take multiple courses.*

**6. Composite Key**
"A combination of multiple attributes" used together when no single column is unique enough on its own.
*e.g. `{STUD_NO, COURSE_NO}` as the candidate/primary key of `STUDENT_COURSE`.*

**7. Partial Key**
Chosen from a weak entity; identifies its records only when combined with the strong entity it depends on; cannot be NULL.
*e.g. in `STUDENT_COURSE`, the combination of `STUD_NO` and `COURSE_CODE`.*

**8. Secondary Key**
An attribute (or combination) used to search/index records quickly but that does **not** guarantee uniqueness (multiple rows can share a value).

**Flag:** the page's actual `STUDENT` / `STUDENT_COURSE` example tables are rendered as images, so exact sample row values are not text-extractable from the page — only the schema (`Student(STUD_NO, SNAME, ADDRESS, PHONE)`, `STUDENT_COURSE(STUD_NO, COURSE_NO)`) and the key relationships above are verbatim from the page text.

> Worked example (added for practice, not from page):
> `STUDENT`: (101, John, 123 Oak St, 555-1001), (102, Emily, 456 Pine St, 555-1002), (103, Michael, 789 Maple St, 555-1003).
> Candidate keys: `STUD_NO`, `PHONE`. Primary key: `STUD_NO`. Alternate key: `PHONE`.
> `STUDENT_COURSE`: (101, C1), (101, C2), (102, C1). Composite key: `{STUD_NO, COURSE_NO}`. Foreign key `STUD_NO` → `STUDENT.STUD_NO`.

**Priority for your prep:** Candidate vs Super vs Primary vs Alternate vs Foreign is a guaranteed definitional MCQ set — the STUD_NO/PHONE candidate-key pair and the STUD_NO foreign-key link above are the exact pattern to reproduce on paper. Partial key and secondary key are lower-yield (mostly relevant if a weak-entity ER question shows up).

---

**General note on method:** every fetch above was cross-checked against the raw page HTML (not just the summarized fetch) to catch cases where sample-data tables are embedded as images rather than text (SQL Joins page, Normalization's Employee_Department table, Keys page's STUDENT tables) — those are explicitly flagged above rather than silently invented as if verbatim.
