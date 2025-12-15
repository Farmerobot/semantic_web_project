# Tool Selection and Justification

**Persuasion-Aware MUSE: Semantic Web Project**

This document describes all tools selected for the project, including technologies, programming languages, and specific libraries, with justifications for their selection.

---

## Table of Contents

1. [Programming Languages](#1-programming-languages)
2. [Semantic Web Tools](#2-semantic-web-tools)
3. [NLP and Machine Learning Tools](#3-nlp-and-machine-learning-tools)
4. [Data Processing Tools](#4-data-processing-tools)
5. [Development and Collaboration Tools](#5-development-and-collaboration-tools)
6. [Tool-Dataset-Method Alignment](#6-tool-dataset-method-alignment)

---

## 1. Programming Languages

### Python 3.10+

**Selection Justification:**
- **Ecosystem**: Rich ecosystem for semantic web (RDFLib), NLP (spaCy), and ML (transformers)
- **LLM Integration**: Native SDKs for OpenAI, Anthropic, and other LLM providers
- **Data Science**: Pandas, NumPy for data preprocessing and analysis
- **Community**: Extensive documentation and community support for all required tasks

**Alternatives Considered:**
- Java (Jena): More verbose, less suitable for rapid prototyping
- JavaScript: Weaker semantic web library support

---

## 2. Semantic Web Tools

### 2.1 RDFLib (v7.0.0)

**Purpose**: RDF graph creation, manipulation, and serialization

**Selection Justification:**
- **Native Python**: Seamless integration with our Python pipeline
- **Format Support**: Turtle, RDF/XML, JSON-LD, N-Triples serialization
- **SPARQL**: Built-in SPARQL query engine for local graphs
- **Ontology Support**: OWL reasoning capabilities via OWL-RL plugin
- **Maturity**: Actively maintained, well-documented, production-ready

**Usage in Project:**
- Creating RDF triples for annotated posts
- Serializing knowledge graphs to Turtle format
- Querying local graphs with SPARQL
- Loading and validating our persuasion ontology

**Introductory Notebook**: `notebooks/01_tools_usage.ipynb`

### 2.2 SPARQLWrapper (v2.0.0)

**Purpose**: Querying external SPARQL endpoints (Wikidata, DBpedia)

**Selection Justification:**
- **Simplicity**: Clean API for remote SPARQL queries
- **Format Handling**: Automatic JSON/XML result parsing
- **Wikidata Compatible**: Works seamlessly with Wikidata Query Service
- **Error Handling**: Robust timeout and retry mechanisms

**Usage in Project:**
- Entity linking via Wikidata SPARQL endpoint
- Fetching entity metadata (descriptions, types, relationships)
- Validating entity references

**Introductory Notebook**: `notebooks/01_tools_usage.ipynb`

### 2.3 Wikidata Knowledge Base

**Purpose**: Entity disambiguation and semantic grounding

**Selection Justification:**
- **Coverage**: 100M+ entities with multilingual labels
- **Open Access**: Free SPARQL endpoint with generous rate limits
- **Structured Data**: Rich property graph with types, relationships
- **Community Maintained**: Continuously updated and validated

**Usage in Project:**
- Linking named entities (persons, organizations, locations) to canonical IDs
- Enriching entity information with Wikidata properties
- Disambiguating entities with common names

---

## 3. NLP and Machine Learning Tools

### 3.1 spaCy (v3.7.2)

**Purpose**: Named Entity Recognition (NER) and text preprocessing

**Selection Justification:**
- **Speed**: Industrial-strength, optimized for production use
- **Accuracy**: Pre-trained models with 85%+ F1 on standard NER benchmarks
- **Pipeline**: Integrated tokenization, POS tagging, dependency parsing
- **Customizable**: Fine-tuning capability for domain-specific entities

**Model Used**: `en_core_web_sm` (small English model for efficiency)

**Usage in Project:**
- Extracting named entities (PERSON, ORG, GPE, etc.)
- Text tokenization and sentence splitting
- Part-of-speech tagging for linguistic analysis

**Introductory Notebook**: `notebooks/02_nlp_llm_tools_intro.ipynb`

### 3.2 OpenRouter API Gateway

**Purpose**: Unified access to multiple LLM providers

**Selection Justification:**
- **Model Variety**: Access to OpenAI, Google, Anthropic, and open-source models
- **OpenAI-Compatible**: Uses standard OpenAI SDK, easy integration
- **Cost Optimization**: Choose models based on cost/performance tradeoffs
- **Fallback Options**: Switch models without code changes

**Primary Model**: `google/gemini-2.5-flash-lite`
- Fast inference for development and testing
- Strong reasoning capabilities
- Cost-effective for batch processing

**Usage in Project:**
- Stage 1: Claim extraction from social media posts
- Stage 2: Persuasion technique detection and classification
- Stage 4: Fact-checking assistance and evidence assessment

**Introductory Notebook**: `notebooks/02_nlp_llm_tools_intro.ipynb`

### 3.3 Alternative LLM Providers

**Available via OpenRouter:**
- **OpenAI GPT-4**: Best for complex reasoning tasks
- **Anthropic Claude**: Strong content filtering, long context
- **Google Gemini**: Fast, multimodal capabilities
- **Open-source models**: Llama, Mistral for local deployment

**Usage in Project:**
- Model comparison experiments
- Fallback providers for redundancy

---

## 4. Data Processing Tools

### 4.1 Pandas (v2.1.4+)

**Purpose**: Tabular data manipulation and analysis

**Selection Justification:**
- **Standard**: De facto standard for Python data analysis
- **Performance**: Optimized for large datasets
- **Integration**: Seamless with visualization and ML libraries

**Usage in Project:**
- Loading and preprocessing CSV datasets (FALCON, JMBX, MUSE)
- Computing dataset statistics
- Creating unified dataset schema

### 4.2 NumPy (v1.26.0+)

**Purpose**: Numerical computing and array operations

**Selection Justification:**
- **Foundation**: Underlying library for Pandas, spaCy, etc.
- **Performance**: C-optimized array operations
- **Compatibility**: Python 3.12 compatible version

**Usage in Project:**
- Statistical computations
- Confidence score aggregation
- Numerical data transformations

### 4.3 Loguru (v0.7.2)

**Purpose**: Logging and monitoring

**Selection Justification:**
- **Simplicity**: Zero-configuration logging with sensible defaults
- **Features**: Colored output, file rotation, exception handling
- **Performance**: Minimal overhead

**Usage in Project:**
- Pipeline execution logging
- Error tracking and debugging
- Progress monitoring

---

## 5. Development and Collaboration Tools

### 5.1 Git / GitHub

**Purpose**: Version control and collaboration

**Selection Justification:**
- **Standard**: Industry-standard version control
- **Collaboration**: Pull requests, issues, code review
- **CI/CD**: Integration with automated testing

**Usage in Project:**
- Source code version control
- Documentation hosting
- Issue tracking for tasks

### 5.2 Jupyter Notebooks

**Purpose**: Interactive development and documentation

**Selection Justification:**
- **Exploration**: Ideal for data exploration and prototyping
- **Documentation**: Combines code, output, and markdown
- **Reproducibility**: Shareable analysis workflows

**Usage in Project:**
- Tool introduction notebooks
- Data preprocessing documentation
- Experimental result visualization

### 5.3 Project Management (GitHub Projects / Kanban)

**Purpose**: Task tracking and project timeline

**Selection Justification:**
- **Integration**: Native GitHub integration
- **Simplicity**: Kanban boards for visual task management
- **Collaboration**: Assignees, due dates, labels

**Usage in Project:**
- Milestone tracking
- Task assignment among team members
- Sprint planning

---

## 6. Tool-Dataset-Method Alignment

### Dataset-Tool Mapping

| Dataset | Size | Primary Tools | Purpose |
|---------|------|---------------|---------|
| **FALCON** | 2,916 tweets | Pandas, spaCy | Fallacy-labeled tweets for training/evaluation |
| **JMBX** | 1,877 tweets | Pandas, Twitter API | Propaganda detection with bias labels |
| **MUSE** | 988 entries | Pandas, OpenAI | Misinformation with human corrections |

### Method-Tool Mapping

| Pipeline Stage | Method | Tools |
|----------------|--------|-------|
| **Claim Extraction** | LLM prompting | OpenAI GPT-4, JSON mode |
| **Persuasion Detection** | LLM classification | OpenAI GPT-4, taxonomy prompt |
| **Entity Recognition** | NER | spaCy en_core_web_sm |
| **Entity Linking** | Knowledge base lookup | SPARQLWrapper, Wikidata |
| **RDF Generation** | Triple construction | RDFLib, custom ontology |
| **Fact-Checking** | Evidence retrieval + LLM | Requests, OpenAI |

### Tool Suitability Matrix

| Requirement | Selected Tool | Suitability Score | Justification |
|-------------|---------------|-------------------|---------------|
| RDF manipulation | RDFLib | ★★★★★ | Best Python RDF library |
| External KG queries | SPARQLWrapper | ★★★★★ | Clean Wikidata integration |
| Named entity extraction | spaCy | ★★★★☆ | Fast, accurate for standard entities |
| Claim extraction | Gemini (OpenRouter) | ★★★★★ | Fast, cost-effective semantic understanding |
| Persuasion classification | Gemini (OpenRouter) | ★★★★★ | Nuanced rhetorical analysis |
| Data preprocessing | Pandas | ★★★★★ | Standard, efficient |

---

## Summary

The selected tool stack provides:

1. **Complete Semantic Web Support**: RDFLib + SPARQLWrapper + Wikidata
2. **State-of-the-art NLP**: spaCy + Gemini (via OpenRouter)
3. **Robust Data Processing**: Pandas + NumPy
4. **Professional Development**: Git + Jupyter + GitHub Projects

All tools are:
- Open-source or have free tiers for academic use
- Well-documented with active communities
- Compatible with Python 3.10+
- Proven in production environments

---

## References

- RDFLib Documentation: https://rdflib.readthedocs.io/
- spaCy Documentation: https://spacy.io/usage
- OpenRouter API: https://openrouter.ai/docs
- Google Gemini: https://ai.google.dev/
- Wikidata Query Service: https://query.wikidata.org/
- SPARQLWrapper: https://sparqlwrapper.readthedocs.io/

---

**Last Updated**: December 2024
