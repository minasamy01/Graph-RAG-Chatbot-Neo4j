# 🧠 Neo4j Graph RAG Chatbot

A natural language interface over a **Neo4j knowledge graph**, powered by **Azure OpenAI GPT-4**. Ask questions in plain English — the system automatically generates Cypher queries, retrieves graph data, and returns intelligent answers.

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg?style=for-the-badge&logo=python&logoColor=white)
![Azure OpenAI](https://img.shields.io/badge/Azure_OpenAI-GPT--4-0089D6?style=for-the-badge&logo=microsoftazure&logoColor=white)
![Neo4j](https://img.shields.io/badge/Neo4j-Graph_DB-008CC1?style=for-the-badge&logo=neo4j&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Cypher](https://img.shields.io/badge/Query_Language-Cypher-4A90D9?style=for-the-badge&logo=neo4j&logoColor=white)
![LangChain](https://img.shields.io/badge/Pattern-Graph_RAG-121212?style=for-the-badge&logo=chainlink&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)

---

## 📐 Architecture

```
User Question
     │
     ▼
LLM (GPT-4) ──── schema.txt ──▶ Cypher Query
                                      │
                                      ▼
                               Neo4j Database
                                      │
                                      ▼
                            LLM (GPT-4) ──▶ Final Answer
```

The pipeline runs in three stages:

1. **Cypher Generation** — GPT-4 reads the schema and converts the user's question into a valid Cypher query.
2. **Graph Execution** — The query is executed against Neo4j and raw records are returned.
3. **Answer Synthesis** — GPT-4 reads the raw results and formulates a clean, human-readable response.

---

## 🗂️ Project Structure

```
├── graph_rag.py          # Core RAG pipeline (Cypher generation, execution, answer synthesis)
├── streamlit_app.py      # Streamlit chat UI
├── graph_setup.cypher    # Sample graph data (elements, reactions, compounds, drugs, diseases)
├── schema.txt            # Neo4j graph schema (nodes, relationships, rules, examples)
├── requirements.txt      # Python dependencies
└── .env                  # Environment variables (not committed to source control)
```

---

## 🧬 Graph Schema

The knowledge graph models a **biomedical domain** connecting chemistry to clinical outcomes.

### Node Types

| Label      | Properties              |
|------------|-------------------------|
| `Element`  | `symbol`, `name`        |
| `Reaction` | `equation`              |
| `Compound` | `name`, `formula`       |
| `Drug`     | `name`                  |
| `Disease`  | `name`                  |
| `Organism` | `type`                  |

### Relationships

```
(:Element)-[:REACTANT {ratio}]->(:Reaction)
(:Reaction)-[:PRODUCT]->(:Compound)
(:Compound)-[:USED_IN]->(:Drug)
(:Drug)-[:TREATS]->(:Disease)
(:Disease)-[:AFFECTS]->(:Organism)
```

### Sample Data (from `graph_setup.cypher`)

The setup file seeds the graph with the following example data:

**Elements:** Carbon (`C`), Hydrogen (`H`), Oxygen (`O`)

**Reactions & Products:**

| Reaction          | Product              |
|-------------------|----------------------|
| `C + 4H → CH4`   | Methane (CH4)        |
| `C + O2 → CO2`   | Carbon Dioxide (CO2) |

**Drugs & Treatments:**

| Drug         | Compound Used | Treats   | Affects       |
|--------------|---------------|----------|---------------|
| Paracetamol  | CH4           | Fever    | Human         |
| Aspirin      | CO2           | Headache | Human, Mouse  |

---

## ⚙️ Setup

### Prerequisites

- Python 3.9+
- A running [Neo4j](https://neo4j.com/) instance (local or cloud)
- An [Azure OpenAI](https://azure.microsoft.com/en-us/products/ai-services/openai-service) resource with a GPT-4 deployment

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the project root:

```env
# Neo4j
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password

# Azure OpenAI
AZURE_OPENAI_API_KEY=your_api_key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_VERSION=2024-08-01-preview
AZURE_OPENAI_CHAT_DEPLOYMENT_NAME=your_deployment_name
```

> ⚠️ **Never commit `.env` to version control.** Add it to `.gitignore`.

### 4. Load Sample Data into Neo4j

Run the setup Cypher file to populate the graph with sample nodes and relationships:

```bash
# Using cypher-shell
cypher-shell -u neo4j -p your_password < graph_setup.cypher
```

Or paste the contents of `graph_setup.cypher` directly into the **Neo4j Browser** and execute.

To verify the data was loaded correctly, run this query in Neo4j Browser:

```cypher
MATCH (n)
OPTIONAL MATCH (n)-[r]->(m)
RETURN n, r, m;
```

---

## 🚀 Running the App

```bash
streamlit run streamlit_app.py
```

Then open your browser at `http://localhost:8501`.

---

## 💬 Usage

Type any natural language question into the chat input. Examples based on the sample data:

```
What drug treats fever?
Which organisms are affected by headache?
What compound is used in Aspirin?
What reaction produces methane?
Which diseases affect humans?
```

Each response includes expandable **debug panels**:

- **🧾 Generated Cypher** — the exact query sent to Neo4j
- **📊 Raw Results** — the raw records returned from the graph

To clear the conversation, click the **🗑 Clear Chat** button.

---

## 🧩 Core API (`graph_rag.py`)

The pipeline can be used programmatically without the UI:

```python
from graph_rag import chat

# Standard usage
answer = chat("What drug treats fever?")
print(answer)
# → "Paracetamol treats Fever."

# Debug mode — returns (answer, cypher_query, raw_results)
answer, cypher, results = chat("What drug treats fever?", debug=True)
print(cypher)
# → MATCH (d:Drug)-[:TREATS]->(dis:Disease)
#   WHERE toLower(dis.name) = toLower("fever")
#   RETURN d.name
print(results)
# → [{'d.name': 'Paracetamol'}]
```

---

## 📦 Dependencies

| Package         | Purpose                         |
|-----------------|---------------------------------|
| `neo4j`         | Neo4j Python driver             |
| `openai`        | Azure OpenAI SDK                |
| `python-dotenv` | Environment variable management |
| `streamlit`     | Chat UI                         |
| `fastapi`       | (Optional) REST API layer       |
| `uvicorn`       | (Optional) ASGI server for API  |

---

## 🛡️ Security Notes

- All string matching in generated Cypher uses `toLower()` to prevent case-sensitivity issues.
- The LLM is strictly constrained to the provided schema — it cannot invent new nodes, labels, or relationships.
- Database credentials and API keys are loaded exclusively from environment variables.

---

## 🔧 Extending the Graph

To add new data, follow the pattern in `graph_setup.cypher`:

1. **Create nodes** using `MERGE` to avoid duplicates.
2. **Create relationships** using `MATCH` + `MERGE` to link existing nodes.
3. **Update `schema.txt`** if you add new node types or relationship types so the LLM stays aware of them.

Example — adding a new drug:

```cypher
MERGE (:Drug {name: "Ibuprofen"});
MERGE (:Disease {name: "Inflammation"});

MATCH (d:Drug {name: "Ibuprofen"}), (dis:Disease {name: "Inflammation"})
MERGE (d)-[:TREATS]->(dis);
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit -m 'Add my feature'`
4. Push to the branch: `git push origin feature/my-feature`
5. Open a Pull Request

---

## 👨‍💻 Author

# **Mina Samy**
### *AI & NLP Engineer*

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/mina-data-ai/?lipi=urn%3Ali%3Apage%3Ad_flagship3_profile_view_base_contact_details%3BaJL%2F1WTcT2eyQjurm1ZczQ%3D%3D) 
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/minasamy01)

---