# Project Structure
## Persuasion-Aware MUSE: Complete Overview

---

## 📂 Directory Tree

```
semantic_web/
│
├── 📄 README.md                          # Main project documentation
├── 📄 QUICKSTART.md                      # 5-minute getting started guide
├── 📄 PIPELINE.md                        # Detailed pseudocode pipeline
├── 📄 SPARQL_QUERIES.md                  # 40+ example SPARQL queries
├── 📄 PROJECT_STRUCTURE.md               # This file
│
├── 🧬 persuasion_ontology.ttl            # RDF/OWL ontology definition
│
├── 🐍 pipeline_implementation.py         # Python starter code
├── 📦 requirements.txt                   # Python dependencies
├── 🔐 .env.example                       # Environment variables template
│
└── 📁 data/
    ├── 📁 input/
    │   └── 📄 posts.json                 # 15 sample social media posts
    │
    └── 📁 output/
        └── 📄 example_annotated.ttl      # Example RDF annotations (4 posts)
```

---

## 📊 File Summary

| File | Size | Type | Purpose |
|------|------|------|---------|
| `README.md` | ~7 KB | Docs | Project overview, features, references |
| `QUICKSTART.md` | ~8 KB | Docs | 5-minute tutorial and FAQ |
| `PIPELINE.md` | ~20 KB | Docs | Detailed pseudocode for all 5 stages |
| `SPARQL_QUERIES.md` | ~15 KB | Docs | 40+ example queries with explanations |
| `PROJECT_STRUCTURE.md` | ~3 KB | Docs | This file |
| `persuasion_ontology.ttl` | ~8 KB | RDF | Ontology: 30+ classes, 20+ properties |
| `pipeline_implementation.py` | ~15 KB | Code | Python starter with data classes |
| `requirements.txt` | ~500 B | Config | Dependencies (rdflib, openai, etc.) |
| `.env.example` | ~600 B | Config | API keys and settings template |
| `posts.json` | ~5 KB | Data | 15 sample posts with metadata |
| `example_annotated.ttl` | ~7 KB | RDF | Annotated output for 4 posts |

**Total:** ~90 KB of documentation, code, and data

---

## 🎯 Core Components

### 1. Ontology (`persuasion_ontology.ttl`)

**Classes (30+):**
```
Core:
  - Post, Claim, Evidence, Entity, Correction

Persuasion Techniques (10):
  - FearAppeal, LoadedLanguage, Scapegoating
  - AppealToAuthority, FlagWaving, Exaggeration
  - AppealToEmotion, CausalOversimplification
  - StrawMan, RedHerring

Emotions (7):
  - Fear, Anger, Disgust, Anxiety, Outrage, Pride, Hope

Verification Status (6):
  - True, False, MostlyTrue, MostlyFalse, Misleading, Unverified
```

**Properties (20+):**
```
Object Properties:
  - containsClaim, usesTechnique, targetsEntity
  - invokesEmotion, supportedBy, refutedBy
  - hasVerificationStatus, hasCorrection

Data Properties:
  - postId, textContent, claimText
  - evidenceText, evidenceSource, entityName
  - confidenceScore, timestamp
```

---

### 2. Sample Data (`posts.json`)

**15 Posts Covering:**

| Topic | Count | Example |
|-------|-------|---------|
| Migration | 2 | "EU forcing unlimited migrants" |
| Health | 3 | "Vitamin C cures COVID-19" |
| Climate | 2 | "Climate change is a hoax" |
| Economy | 2 | "Inflation caused by unemployed" |
| Technology | 2 | "5G towers control thoughts" |
| Politics | 2 | "Teachers indoctrinating kids" |
| Other | 2 | "EVs worse than gas cars" |

**Platforms:** Twitter (8), Facebook (5), Instagram (2)

**Metadata per post:**
- Retweets/shares
- Likes/reactions
- Author verification status
- Timestamp

---

### 3. Pipeline (`PIPELINE.md`)

**5 Stages:**

```
Stage 1: Claim Extraction
  Input: Post text
  Process: LLM identifies factual claims
  Output: Claim objects with text fragments

Stage 2: Persuasion Detection
  Input: Claims + context
  Process: LLM classifies techniques
  Output: Technique annotations with confidence

Stage 3: Entity Linking
  Input: Claims
  Process: NER + Wikidata SPARQL
  Output: Entities with Wikidata IDs

Stage 4: Fact-Checking
  Input: Claims
  Process: Web search + LLM verification
  Output: Verification status + evidence

Stage 5: RDF Generation
  Input: All annotations
  Process: Convert to RDF triples
  Output: Turtle/JSON-LD files
```

**Functions (11):**
- `extract_claims()`
- `detect_persuasion()`
- `extract_and_link_entities()`
- `query_wikidata()`
- `verify_claim()`
- `filter_by_reliability()`
- `generate_rdf_triples()`
- `serialize_rdf()`
- `load_posts()`
- `main_pipeline()`
- `generate_statistics()`

---

### 4. SPARQL Queries (`SPARQL_QUERIES.md`)

**10 Categories, 40+ Queries:**

1. **Basic Queries** (3)
   - Find all posts
   - Find all claims
   - Count posts by platform

2. **Persuasion Techniques** (5)
   - Find posts using Fear Appeal
   - Count techniques by type
   - Find claims with multiple techniques
   - High-confidence detections
   - Loaded language posts

3. **Emotions** (3)
   - Find claims invoking fear
   - Count emotions invoked
   - Posts with multiple emotions

4. **Entities** (4)
   - Most targeted entities
   - Claims about specific entity
   - Entities with Wikidata links
   - Scapegoating by entity

5. **Fact-Checking** (4)
   - All false claims
   - Count by verification status
   - Misleading claims with evidence
   - Unverified claims with fear appeal

6. **Combined Analysis** (4)
   - False claims + fear + entities
   - High manipulation score posts
   - Temporal analysis
   - Author analysis

7. **Provenance** (2)
   - Find all LLM agents
   - Count annotations by agent

8. **Advanced Patterns** (4)
   - Coordinated manipulation
   - Technique combinations
   - Appeal to authority in false claims
   - Red herring + loaded language

9. **Explanatory** (2)
   - Full annotation for single post
   - Generate explanation text

10. **Statistics** (3)
    - Overall statistics
    - Platform-specific analysis
    - Technique co-occurrence matrix

---

### 5. Example Output (`example_annotated.ttl`)

**4 Fully Annotated Posts:**

1. **Post_001**: EU migration (Fear Appeal + Loaded Language)
2. **Post_002**: COVID-19 vitamin C (Appeal to Authority + Scapegoating)
3. **Post_003**: Inflation blame (Scapegoating + Oversimplification)
4. **Post_004**: Climate denial (Flag Waving + Straw Man)

**RDF Triples Generated:**
- ~150 triples total
- 4 Post nodes
- 6 Claim nodes
- 12 Technique instances
- 5 Entity nodes (with Wikidata links)
- 6 Evidence nodes
- 8 Emotion instances

---

## 🔄 Data Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                          INPUT LAYER                                │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                    posts.json (15 samples)
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      PROCESSING LAYER                               │
│                                                                     │
│  Stage 1: extract_claims()                                          │
│           ↓                                                         │
│  Stage 2: detect_persuasion()                                       │
│           ↓                                                         │
│  Stage 3: extract_and_link_entities()                               │
│           ↓                                                         │
│  Stage 4: verify_claim()                                            │
│           ↓                                                         │
│  Stage 5: generate_rdf_triples()                                    │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         OUTPUT LAYER                                │
│                                                                     │
│  ├── annotated_posts.ttl (Turtle format)                            │
│  ├── annotated_posts.json-ld (JSON-LD format)                       │
│  └── statistics.json (Summary metrics)                              │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      QUERY & ANALYSIS                               │
│                                                                     │
│  ├── SPARQL Queries → Patterns, statistics, insights                │
│  ├── Triple Store → GraphDB / Fuseki                                │
│  └── Visualization → Networks, timelines, dashboards                │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🧩 Technology Stack

### Current Implementation
```
Layer          Technology           Purpose
─────────────────────────────────────────────────────────────────
Ontology       RDF/OWL             Schema definition
Serialization  Turtle, JSON-LD     RDF formats
Querying       SPARQL 1.1          Graph queries
Vocabulary     PROV-O, Wikidata    Provenance, entities
Documentation  Markdown            Guides, examples
```

### Planned Implementation
```
Layer          Technology           Purpose
─────────────────────────────────────────────────────────────────
Language       Python 3.10+        Pipeline implementation
RDF Library    rdflib 7.0          Graph manipulation
LLM API        OpenAI GPT-4        Annotation
NLP            spaCy 3.7           Entity recognition
Web Scraping   requests, BS4       Evidence retrieval
Triple Store   GraphDB/Fuseki      RDF storage
Web Interface  Streamlit/Flask     User interface
Visualization  Plotly, D3.js       Data visualization
```

---

## 📈 Metrics & Statistics

### Ontology Complexity
- **Classes**: 30+
- **Object Properties**: 13
- **Data Properties**: 15
- **Depth**: 3 levels (e.g., Emotion → Fear → invokesEmotion)
- **Expressivity**: RDFS + OWL 2

### Dataset Size
- **Posts**: 15 samples
- **Topics**: 7 categories
- **Platforms**: 3 (Twitter, Facebook, Instagram)
- **Time span**: ~1 week (simulated)

### Documentation
- **Total words**: ~25,000
- **Code lines**: ~500 (Python starter)
- **SPARQL queries**: 40+
- **Examples**: 4 fully annotated posts

---

## 🎓 Learning Path

### For Beginners
1. ✅ Read `QUICKSTART.md` (5 min)
2. ✅ Explore `posts.json` (5 min)
3. ✅ View `example_annotated.ttl` (10 min)
4. ✅ Try 3-5 SPARQL queries (15 min)
5. ✅ Read `README.md` overview (10 min)

**Total: ~45 minutes to understand the project**

### For Developers
1. ✅ Complete beginner path
2. ✅ Study `persuasion_ontology.ttl` (20 min)
3. ✅ Read `PIPELINE.md` pseudocode (30 min)
4. ✅ Review `pipeline_implementation.py` (20 min)
5. 🔨 Implement LLM API calls (2-4 hours)
6. 🔨 Test on sample data (1 hour)
7. 🔨 Deploy to triple store (1 hour)

**Total: ~6-8 hours to implement**

### For Researchers
1. ✅ Complete beginner path
2. ✅ Review related papers (2 hours)
3. ✅ Analyze ontology design choices (30 min)
4. 📝 Annotate test dataset (4-8 hours)
5. 📊 Evaluate accuracy (2-4 hours)
6. 📈 Generate visualizations (2 hours)
7. 📄 Write paper (20-40 hours)

**Total: ~30-50 hours for research paper**

---

## ✅ Completeness Checklist

### Documentation
- [x] README with overview
- [x] Quick start guide
- [x] Detailed pipeline pseudocode
- [x] SPARQL query examples
- [x] Project structure documentation
- [x] Environment configuration template

### Ontology
- [x] Core classes defined
- [x] Persuasion technique taxonomy
- [x] Emotion classes
- [x] Verification statuses
- [x] Object properties
- [x] Data properties
- [x] Provenance integration (PROV-O)
- [x] Wikidata linking

### Data
- [x] 15 sample posts (JSON)
- [x] Multiple topics covered
- [x] Multiple platforms
- [x] Metadata included
- [x] 4 example annotations (TTL)

### Code
- [x] Python starter implementation
- [x] Data classes defined
- [x] Pipeline functions outlined
- [x] RDF generation logic
- [x] Dependencies listed

### Queries
- [x] Basic queries
- [x] Technique queries
- [x] Entity queries
- [x] Fact-checking queries
- [x] Statistical queries
- [x] Advanced pattern queries

---

## 🚀 Deployment Checklist

### Development
- [ ] Clone/copy project files
- [ ] Install Python dependencies
- [ ] Set up API keys (.env)
- [ ] Test data loading
- [ ] Implement LLM calls
- [ ] Test pipeline on 1 post
- [ ] Validate RDF output

### Testing
- [ ] Annotate test dataset (20+ posts)
- [ ] Compare LLM vs human annotations
- [ ] Measure precision/recall
- [ ] Check Wikidata linking accuracy
- [ ] Validate fact-checking results
- [ ] Test SPARQL queries

### Production
- [ ] Set up triple store (GraphDB/Fuseki)
- [ ] Load ontology
- [ ] Load annotated data
- [ ] Configure SPARQL endpoint
- [ ] Build web interface
- [ ] Add monitoring/logging
- [ ] Deploy to server

---

## 📞 Support Resources

**Documentation:**
- `README.md` - Start here
- `QUICKSTART.md` - Fast tutorial
- `PIPELINE.md` - Implementation guide
- `SPARQL_QUERIES.md` - Query examples

**External Resources:**
- [RDF Tutorial](https://www.w3.org/TR/rdf11-primer/)
- [SPARQL Tutorial](https://www.w3.org/TR/sparql11-query/)
- [Wikidata Query Service](https://query.wikidata.org/)
- [PROV-O Documentation](https://www.w3.org/TR/prov-o/)

**Papers:**
- Zhou et al. (2024) - MUSE framework
- Da San Martino et al. (2019) - Propaganda detection
- Idziejczak et al. (2025) - LLM persuasion assessment

---

## 🎉 Project Status

**Phase 1: Ontology & Data** ✅ COMPLETE
- [x] RDF ontology designed
- [x] Sample data generated
- [x] Pipeline documented
- [x] SPARQL queries written
- [x] Example output created

**Phase 2: Implementation** 🚧 STARTER CODE PROVIDED
- [ ] LLM integration
- [ ] Entity linking
- [ ] Evidence retrieval
- [ ] End-to-end testing

**Phase 3: Deployment** 📅 PLANNED
- [ ] Triple store setup
- [ ] Web interface
- [ ] API endpoints
- [ ] Production deployment

**Phase 4: Evaluation** 📅 PLANNED
- [ ] Human annotation
- [ ] Accuracy metrics
- [ ] Comparative evaluation
- [ ] Publication

---

**Last Updated**: January 2025  
**Version**: 1.0  
**Status**: Phase 1 Complete ✅
