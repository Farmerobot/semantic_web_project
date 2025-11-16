# Persuasion-Aware MUSE: Semantic Web Project

**Semantic-Web Explanations of Manipulation in Social Media Posts**

This project extends the MUSE (Misinformation correction Using Structured Explanations) framework with semantic web technologies to detect, annotate, and explain persuasion techniques in social media posts.

---

## 📋 Project Overview

Traditional misinformation detection systems identify **what is false** but fail to explain **how persuasion is achieved**. This project combines:

- **LLM-based annotation** for detecting persuasion techniques
- **Knowledge graphs (RDF)** for structured representation
- **Entity linking (Wikidata)** for semantic grounding
- **Evidence retrieval** for fact-checking
- **SPARQL querying** for analytical insights

### Key Features

✅ Detects 5 core persuasion techniques (Fear Appeal, Loaded Language, Scapegoating, etc.)  
✅ Links entities to Wikidata for disambiguation  
✅ Provides evidence-based fact-checking  
✅ Generates queryable RDF knowledge graphs  
✅ Includes provenance metadata (PROV-O)  

---

## 📁 Project Structure

```
semantic_web/
│
├── README.md                           # This file
├── PIPELINE.md                         # Pseudocode for LLM annotation pipeline
├── SPARQL_QUERIES.md                   # Example SPARQL queries
│
├── persuasion_ontology.ttl             # RDF ontology definition
│
├── data/
│   ├── input/
│   │   └── posts.json                  # Sample social media posts (15 examples)
│   │
│   └── output/
│       └── example_annotated.ttl       # Example annotated RDF output
│
└── (future: implementation scripts)
```

---

## 🧬 Ontology Structure

The `persuasion_ontology.ttl` defines:

### Core Classes
- **Post**: Social media post
- **Claim**: Factual assertion that can be verified
- **Evidence**: Source supporting/refuting a claim
- **Entity**: Real-world entity (linked to Wikidata)
- **Correction**: Structured misinformation correction

### Persuasion Techniques (5 Core)
- **FearAppeal**: Using fear to influence behavior
- **LoadedLanguage**: Emotionally charged words
- **AppealToAuthority**: Citing authority without evidence
- **Scapegoating**: Unfairly blaming a group
- **Exaggeration**: Overstating/understating facts

### Verification Status
- True, False, Mostly True, Mostly False, Misleading, Unverified

---

## 🔄 Pipeline Overview

```
Input Posts (JSON) 
    ↓
Stage 1: Claim Extraction (LLM)
    ↓
Stage 2: Persuasion Detection (LLM)
    ↓
Stage 3: Entity Recognition & Wikidata Linking
    ↓
Stage 4: Fact-Checking & Evidence Retrieval
    ↓
Stage 5: RDF Triple Generation
    ↓
Output RDF (Turtle/JSON-LD)
```

See [`PIPELINE.md`](PIPELINE.md) for detailed pseudocode.

---

## 📊 Sample Data

### Input: Social Media Posts

The `data/input/posts.json` contains 15 example posts covering:

- **Migration/Immigration** misinformation
- **Health** misinformation (COVID-19, alternative medicine)
- **Climate change** denial
- **Economic** oversimplifications
- **Technology** conspiracy theories
- **Political** scapegoating

Each post includes:
```json
{
  "post_id": "post_001",
  "platform": "Twitter",
  "author": "@username",
  "timestamp": "2025-01-02T14:30:00Z",
  "text": "Post content...",
  "metadata": {
    "retweets": 1523,
    "likes": 4210
  }
}
```

### Output: RDF Triples

Example annotation for a post about EU migration:

```turtle
:Post_001 a :Post ;
    :textContent "BREAKING: The EU is forcing member states..." ;
    :containsClaim :Claim_001_1 .

:Claim_001_1 a :Claim ;
    :claimText "The EU is forcing member states to accept unlimited migrants" ;
    :usesTechnique :FearAppeal, :LoadedLanguage ;
    :targetsEntity wd:Q458 ;  # European Union
    :hasVerificationStatus :False ;
    :refutedBy :Evidence_001_1 ;
    :confidenceScore 0.92 .

:Evidence_001_1 a :Evidence ;
    :evidenceText "EU migration policy requires unanimous consent..." ;
    :evidenceSource <https://ec.europa.eu/home-affairs/...> .
```

See [`data/output/example_annotated.ttl`](data/output/example_annotated.ttl) for complete examples.

---

## 🔍 SPARQL Queries

The [`SPARQL_QUERIES.md`](SPARQL_QUERIES.md) file contains 40+ example queries, including:

### Basic Queries
- Find all posts and claims
- Count posts by platform
- List all persuasion techniques

### Analytical Queries
- Find most targeted entities
- Detect coordinated manipulation patterns
- Temporal analysis of techniques
- Author manipulation scores

### Fact-Checking Queries
- Find all false claims with evidence
- Count claims by verification status
- Find misleading claims with specific techniques

### Example Query: Find Fear Appeal Posts

```sparql
PREFIX : <http://example.org/persuasion#>

SELECT ?post ?text ?claim ?claimText
WHERE {
    ?post rdf:type :Post ;
          :textContent ?text ;
          :containsClaim ?claim .
    ?claim :claimText ?claimText ;
           :usesTechnique :FearAppeal .
}
```

---

## 🚀 Implementation Roadmap

### Phase 1: Ontology & Data (✅ Complete)
- [x] Define RDF ontology
- [x] Create sample social media posts
- [x] Document pipeline pseudocode
- [x] Write SPARQL queries

### Phase 2: Pipeline Implementation (🔜 Next)
- [ ] Implement Python scripts for pipeline
- [ ] Integrate LLM API (OpenAI/Anthropic)
- [ ] Add Wikidata entity linking
- [ ] Implement evidence retrieval
- [ ] Generate RDF triples programmatically

### Phase 3: Deployment (📅 Future)
- [ ] Set up triple store (GraphDB/Fuseki)
- [ ] Create web interface for querying
- [ ] Build visualization dashboard
- [ ] Deploy fact-checking API

### Phase 4: Evaluation (📅 Future)
- [ ] Human annotation for ground truth
- [ ] Measure precision/recall
- [ ] Compare with BERT-based models
- [ ] Publish results

---

## 🛠️ Technologies

### Current (Ontology & Data)
- **RDF/OWL**: Ontology definition
- **Turtle**: RDF serialization
- **SPARQL**: Querying language
- **JSON**: Input data format

### Future (Implementation)
- **Python 3.10+**
- **RDFLib**: RDF manipulation
- **OpenAI API / Anthropic Claude**: LLM annotation
- **SPARQLWrapper**: SPARQL queries
- **spaCy**: NLP preprocessing
- **Requests**: Web scraping for evidence

### Optional (Deployment)
- **GraphDB** or **Apache Jena Fuseki**: Triple store
- **Streamlit** or **Flask**: Web interface
- **Plotly/D3.js**: Visualization

---

## 📖 Usage

### 1. Explore the Ontology

```bash
# View ontology structure
cat persuasion_ontology.ttl
```

### 2. Examine Sample Data

```bash
# View input posts
cat data/input/posts.json

# View example annotations
cat data/output/example_annotated.ttl
```

### 3. Review Pipeline

```bash
# Read pseudocode pipeline
cat PIPELINE.md
```

### 4. Try SPARQL Queries

```bash
# Load example annotations into a triple store
# Then execute queries from SPARQL_QUERIES.md
```

---

## 🎯 Research Contributions

This project addresses limitations in prior work:

| Dimension | Previous Work | Our Contribution |
|-----------|---------------|------------------|
| **Modeling** | Text classification | Hybrid LLM + knowledge graph |
| **Output** | Flat labels | RDF triples with semantic relationships |
| **Reasoning** | None | Ontology-based logical validation |
| **Application** | Either persuasion OR misinformation | Unified framework for both |
| **Explainability** | Natural language only | Structured + linguistic + factual |

---

## 📚 References

1. **Zhou et al.** (2024). *Correcting Misinformation on Social Media with a Large Language Model (MUSE)*
2. **Da San Martino et al.** (2019). *Fine-grained Propaganda Detection in News Articles*, ACL
3. **Idziejczak et al.** (2025). *Among Them: A Game-Based Framework for Assessing Persuasion Capabilities of LLMs*

---

## 🤝 Contributors

- **Mateusz Idziejczak** - Poznań University of Technology
- **Mateusz Stawicki** - Poznań University of Technology
- **Anastasiya Serdioukova** - Poznań University of Technology

**Institute of Computing Science**  
Poznań University of Technology

---

## 📝 License

This project is for academic research purposes. Data sources and LLM APIs may have their own terms of service.

---

## 🔗 Related Resources

- **Wikidata**: https://www.wikidata.org/
- **SPARQL Tutorial**: https://www.w3.org/TR/sparql11-query/
- **RDF Primer**: https://www.w3.org/TR/rdf11-primer/
- **PROV-O**: https://www.w3.org/TR/prov-o/
- **MUSE Paper**: (Add link when available)

---

## 📞 Contact

For questions or collaboration:
- GitHub Issues: (Add repository link)
- Email: (Add contact email)

---

## 🌟 Acknowledgments

This project builds upon:
- The MUSE framework for misinformation correction
- Propaganda detection taxonomy from Da San Martino et al.
- LLM persuasion assessment from Idziejczak et al.

---

**Last Updated**: January 2025  
**Version**: 1.0
