import requests
import json
import os
import sys

SUPABASE_URL = "https://ywhocytfjiubouhehiuj.supabase.co/rest/v1"
ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inl3aG9jeXRmaml1Ym91aGVoaXVqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzY4MzEwMDMsImV4cCI6MjA5MjQwNzAwM30.PUDifIyK48oJRQZkUYWAArgsG6VkCyaMBOUcvbqy0GM"

headers = {
    "apikey": ANON_KEY,
    "Authorization": f"Bearer {ANON_KEY}"
}

tables = ["projects", "project_images", "experience", "services"]

# We will generate standard PostgreSQL CREATE and INSERT statements
sql_content = """-- Dynamically Generated Seed Script from Supabase
-- Created for FA23-BCS-161 Final Exam Submission

-- Drop existing tables to ensure clean state
DROP TABLE IF EXISTS project_images CASCADE;
DROP TABLE IF EXISTS projects CASCADE;
DROP TABLE IF EXISTS experience CASCADE;
DROP TABLE IF EXISTS services CASCADE;

-- Create tables
CREATE TABLE experience (
    id VARCHAR(255) PRIMARY KEY,
    title VARCHAR(255),
    company VARCHAR(255),
    date_range VARCHAR(100),
    employment_type VARCHAR(100),
    bullets TEXT,
    status VARCHAR(50),
    order_index INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE projects (
    id VARCHAR(255) PRIMARY KEY,
    title VARCHAR(255),
    slug VARCHAR(255) UNIQUE,
    description TEXT,
    cover_image_url VARCHAR(512),
    link VARCHAR(512),
    github_link VARCHAR(512),
    technologies TEXT,
    tools TEXT,
    case_study_content TEXT,
    status VARCHAR(50),
    is_featured BOOLEAN,
    order_index INTEGER,
    category VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE project_images (
    id VARCHAR(255) PRIMARY KEY,
    project_id VARCHAR(255) REFERENCES projects(id) ON DELETE CASCADE,
    url VARCHAR(512),
    order_index INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE services (
    id VARCHAR(255) PRIMARY KEY,
    title VARCHAR(255),
    slug VARCHAR(255) UNIQUE,
    tagline VARCHAR(255),
    description TEXT,
    features TEXT,
    order_index INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

print("Connecting to Supabase to fetch tables...")

# Fetch and generate insert statements
fetched_counts = {}

import time

for table in tables:
    url = f"{SUPABASE_URL}/{table}"
    print(f"Fetching data from {table}...")
    success = False
    for attempt in range(1, 4):
        try:
            r = requests.get(url, headers=headers, timeout=15)
            if r.status_code == 200:
                data = r.json()
                fetched_counts[table] = len(data)
                
                if not data:
                    print(f"-> Table {table} is empty on Supabase.")
                    success = True
                    break
                    
                print(f"-> Successfully fetched {len(data)} rows.")
                
                # Write SQL Insert Statements
                sql_content += f"\n\n-- Seeding data for {table}\n"
                for row in data:
                    columns = []
                    values = []
                    for k, v in row.items():
                        if v is None:
                            continue
                        columns.append(k)
                        
                        if isinstance(v, (int, float, bool)):
                            values.append(str(v))
                        else:
                            escaped_val = str(v).replace("'", "''")
                            values.append(f"'{escaped_val}'")
                    
                    cols_str = ", ".join(columns)
                    vals_str = ", ".join(values)
                    sql_content += f"INSERT INTO {table} ({cols_str}) VALUES ({vals_str}) ON CONFLICT DO NOTHING;\n"
                success = True
                break
            else:
                print(f"-> Error fetching {table}: Status {r.status_code} - {r.text}", file=sys.stderr)
                break
        except Exception as e:
            print(f"-> Attempt {attempt} failed: {str(e)}", file=sys.stderr)
            if attempt < 3:
                print("Retrying in 2 seconds...", file=sys.stderr)
                time.sleep(2)
            else:
                print("\n[CRITICAL ERROR] Could not connect to Supabase after 3 attempts.", file=sys.stderr)
                sys.exit(1)


# Ensure the db folder exists
os.makedirs("db", exist_ok=True)
sql_file_path = os.path.join("db", "init.sql")

with open(sql_file_path, "w", encoding="utf-8") as f:
    f.write(sql_content)

print(f"\n[SUCCESS] Sync completed. Generated file: {sql_file_path}")
print(f"Fetched counts: {fetched_counts}")
