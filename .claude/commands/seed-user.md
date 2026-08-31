---
description: Create a single dummy user in database.
allowed-tools: Read, Bash(python3:*)
---

Read database/db.py to understand the users table
schema and the get_db() helper.

Then write and run a python script using Bash that: 

1. Generate a realastic random indian user using your own knowledge of common indian names across regions: 
- Name : a realastic indian first + last name
- Email : delivered from the name with a random 2-3 digit number suffix (e.g. rahul.sharma91@gmail.com)
- Password: "password123" hashed with werkzeug's generate password hash
- created_at: Current datetime

2. Checks if the generated gmail already exist in the users table.if it does regenerate until unique.

3. Insert the user into the database using the same get_db() pattern found in db.py.

4. Print confirmation:
- id
- name
- email