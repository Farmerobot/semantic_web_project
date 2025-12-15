# Persuasion-Aware MUSE: Semantic Web Project

**Semantic-Web Explanations of Manipulation in Social Media Posts**

We extend the MUSE misinformation-correction framework with a Semantic Web layer that models persuasion techniques in social media posts as RDF knowledge graphs, linking claims, entities, techniques, and evidence to enable explainable, queryable detection and analysis of manipulative content.

---

## Project Overview

This project combines:
- **LLM-based annotation** for detecting persuasion techniques
- **Knowledge graphs (RDF)** for structured representation
- **Entity linking (Wikidata)** for semantic grounding
- **SPARQL querying** for analytical insights

### Key Features
- Detects 5 core persuasion techniques (Fear Appeal, Loaded Language, Scapegoating, Appeal to Authority, Exaggeration)
- Links entities to Wikidata for disambiguation
- Generates queryable RDF knowledge graphs
- Includes provenance metadata (PROV-O)

---

## Project Structure

```
semantic_web/
├── README.md                    # This file
├── docs/
│   ├── TOOLS.md                 # Tool selection and justification
│   ├── PIPELINE.md              # Pipeline pseudocode
│   └── SPARQL_QUERIES.md        # Example SPARQL queries
├── persuasion_ontology.ttl      # RDF ontology definition
├── pipeline_implementation.py   # Python pipeline implementation
├── pyproject.toml               # Python dependencies
│
├── data/
│   ├── input/
│   │   ├── unprocessed/         # Raw datasets (FALCON, JMBX, MUSE)
│   │   └── processed/           # Processed datasets
│   └── output/
│       ├── annotated_posts.ttl      # Generated RDF (Turtle)
│       ├── annotated_posts.json-ld  # Generated RDF (JSON-LD)
│       └── pipeline_stats.json      # Pipeline statistics
│
├── notebooks/
│   ├── 01_tools_usage.ipynb           # Semantic web tools intro
│   ├── 02_nlp_llm_tools_intro.ipynb   # NLP/LLM tools intro
│   └── 03_data_preprocessing.ipynb    # Data preprocessing
│
├── scripts/
│   ├── generate_dataset_stats.py      # Dataset statistics generation
│   └── process_datasets.py            # Dataset processing
│
└── reports/
    ├── dataset_stats.md               # Generated statistics
    └── datasets_exploratory_analysis.md
```

---

## Datasets

**Primary Dataset:**
- **FALCON** (2,916 tweets) - Multi-label fallacy classification dataset for COVID-19 misinformation

**Auxiliary Datasets (EDA only):**
- **JMBX** (1,877 tweets) - Propaganda detection with bias labels
- **MUSE** (988 entries) - Misinformation with corrections

---

## Ontology

The `persuasion_ontology.ttl` defines:

**Core Classes:** Post, Claim, Evidence, Entity, Correction

**Persuasion Techniques:**
- FearAppeal, LoadedLanguage, AppealToAuthority, Scapegoating, Exaggeration

**Verification Status:** True, False, MostlyTrue, MostlyFalse, Misleading, Unverified

---

## Pipeline

```
Input Posts → Claim Extraction (LLM) → Persuasion Detection (LLM) 
    → Entity Recognition & Wikidata Linking → RDF Triple Generation → Output RDF
```

See `docs/PIPELINE.md` for detailed pseudocode and `pipeline_implementation.py` for Python implementation.

---

## Installation

```bash
# Using uv (recommended)
uv sync

# Or using pip
pip install -e .
```

---

## Usage

```bash
# Run dataset statistics
python scripts/generate_dataset_stats.py

# View notebooks
jupyter notebook notebooks/
```

---

## Technologies

- **Python 3.12+** with RDFLib, SPARQLWrapper, spaCy, OpenAI
- **RDF/OWL** for ontology, **Turtle** for serialization
- **SPARQL** for querying

See `docs/TOOLS.md` for complete tool justification.

---

## References

1. Zhou et al. (2024). *Correcting Misinformation on Social Media with a Large Language Model (MUSE)*
2. Da San Martino et al. (2019). *Fine-grained Propaganda Detection in News Articles*, ACL
3. Idziejczak et al. (2025). *Among Them: A Game-Based Framework for Assessing Persuasion Capabilities of LLMs*

---

## Contributors

- **Mateusz Idziejczak** - Poznań University of Technology
- **Mateusz Stawicki** - Poznań University of Technology

**Institute of Computing Science, Poznań University of Technology**

---

## License

Academic research purposes. Data sources and LLM APIs have their own terms of service.
