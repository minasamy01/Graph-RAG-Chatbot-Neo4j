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
    Use ONLY this schema: {SCHEMA}

    Rules:
    1. Return ONLY the Cypher query text. No markdown formatting (No ```).
    2. Always use toLower() for string comparisons to ensure matching.
       Example: WHERE toLower(d.name) = toLower("Fever")
    3. Use exact relationship types from the schema.
    
    Question: {question}
    """
    
    response = client.chat.completions.create(
        model=os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"),
        messages=[{"role": "user", "content": prompt}],
        temperature=0 # مهم جداً لضمان ثبات النتيجة
    )

    content = response.choices[0].message.content.strip()
    # تنظيف شامل لأي علامات برمجة قد يضيفها الموديل
    clean_query = content.replace("```cypher", "").replace("```", "").replace("`", "").strip()
    return clean_query

# =========================
# LLM → FINAL ANSWER
# =========================
def generate_answer(question, results):
    # تحويل النتائج لنص واضح عشان الـ LLM ميتوهش
    results_str = str(results) if results else "No data"
    
    prompt = f"""
    You are a chemical assistant. 
    User Question: {question}
    Data from Neo4j Database: {results_str}
    
    Instructions:
    1. If the 'Data from Neo4j Database' contains information, use it to answer the question directly.
    2. If the data is empty or 'No data', say "I'm sorry, I couldn't find information about that in the database."
    3. Keep the answer professional and concise.
    """

    response = client.chat.completions.create(
        model=os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"),
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5 # خلي فيه شوية مرونة في صياغة الجملة
    )
    return response.choices[0].message.content


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