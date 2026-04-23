import os
from dotenv import load_dotenv
from neo4j import GraphDatabase
from openai import AzureOpenAI

# =========================
# LOAD ENV
# =========================
load_dotenv()

URI = os.getenv("NEO4J_URI")
USER = os.getenv("NEO4J_USER")
PASSWORD = os.getenv("NEO4J_PASSWORD")

driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))

# Azure OpenAI client
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION")
)

# =========================
# LOAD SCHEMA
# =========================
def load_schema():
    with open("schema.txt", "r", encoding="utf-8") as f:
        return f.read()

SCHEMA = load_schema()

# =========================
# RUN CYPHER
# =========================
def run_cypher(query):
    with driver.session() as session:
        result = session.run(query)
        return [record.data() for record in result]

# =========================
# LLM → CYPHER GENERATION
# =========================
def generate_cypher(question):
    prompt = f"""
You are a Neo4j Cypher expert.

Use ONLY this schema:
{SCHEMA}

Rules:
- Do NOT invent nodes or relationships
- Return ONLY Cypher query
- No explanation
- Do NOT include ``` or comments

IMPORTANT:
- Always use toLower() when matching string values

Question:
{question}
"""

    response = client.chat.completions.create(
        model=os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"),
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    content = response.choices[0].message.content.strip()

    # تنظيف
    clean_query = content.replace("```cypher", "").replace("```", "").strip()
    clean_query = "\n".join(
        [line for line in clean_query.split("\n") if not line.strip().startswith("//")]
    )

    return clean_query.strip()

# =========================
# LLM → FINAL ANSWER
# =========================
def generate_answer(question, results):
    prompt = f"""
You are a helpful assistant.

User Question:
{question}

Graph Results:
{results}

Rules:
- Answer ONLY using the provided data
- If data is empty say "No relevant data found"
"""

    response = client.chat.completions.create(
        model=os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"),
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    return response.choices[0].message.content.strip()

# =========================
# MAIN CHAT FUNCTION
# =========================
def chat(question, debug=False):
    cypher = generate_cypher(question)
    results = run_cypher(cypher)
    answer = generate_answer(question, results)

    if debug:
        return answer, cypher, results

    return answer