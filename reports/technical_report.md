# Persuasion-Aware MUSE: Technical Report (Draft)

**Project:** Semantic Web Methods for Detecting Persuasion Techniques in Social Media  
**Authors:** [Team Name]  
**Date:** December 2025  
**Repository:** https://github.com/Farmerobot/semantic_web_project

---

## 1. Introduction

### 1.1 Problem Statement

Social media has become a primary vector for the spread of misinformation and manipulative content. Detecting persuasion techniques—such as fear appeals, loaded language, and scapegoating—is critical for combating disinformation. However, current approaches often lack:

1. **Structured representations** that enable reasoning over detected patterns
2. **Entity linking** to external knowledge bases for contextualization
3. **Explainability** in the form of semantic justifications

### 1.2 Proposed Approach

We present **Persuasion-Aware MUSE**, a semantic web pipeline that:

- Extracts factual claims from social media posts using LLMs
- Detects persuasion techniques with confidence scores
- Links named entities to Wikidata for enrichment
- Generates RDF knowledge graphs following a custom ontology
- Enables SPARQL-based querying for analysis

---

## 2. Related Work

### 2.1 Propaganda and Persuasion Detection

- **Da San Martino et al. (2019)** introduced fine-grained propaganda detection with 18 technique categories [1]
- **FALCON dataset** provides fallacy annotations for COVID-19 tweets [2]
- **PTC corpus** offers sentence-level propaganda labels

### 2.2 Misinformation Correction

- **MUSE framework (Zhou et al., 2024)** generates structured explanations for misinformation [3]
- Community Notes on X (Twitter) provide crowdsourced corrections

### 2.3 Semantic Web for Misinformation

- **ClaimReview schema** standardizes fact-check metadata
- **Wikidata** provides linked open data for entity enrichment
- **PROV-O** ontology enables provenance tracking

---

## 3. Dataset Description

We use the **FALCON** (Fallacies in COVID-19 Network-based) dataset as our primary corpus.

### 3.1 Dataset Statistics

| Metric | Value |
|--------|-------|
| Total tweets | 2,916 |
| Train split | 1,811 |
| Validation split | 550 |
| Test split | 555 |
| Tweets with ≥1 fallacy | 1,009 (34.6%) |

### 3.2 Fallacy Distribution

| Fallacy Type | Count | Percentage |
|--------------|-------|------------|
| Loaded Language | 457 | 15.7% |
| Ad Hominem | 259 | 8.9% |
| Appeal to Ridicule | 238 | 8.2% |
| False Dilemma | 168 | 5.8% |
| Appeal to Fear | 157 | 5.4% |
| Hasty Generalization | 91 | 3.1% |

### 3.3 Ontology Mapping

FALCON fallacies are mapped to our persuasion ontology classes:

```
Ad Hominem          → AdHominem
Appeal to Fear      → FearAppeal
Appeal to Ridicule  → AppealToRidicule
False Dilemma       → FalseDilemma
Hasty Generalization → HastyGeneralization
Loaded Language     → LoadedLanguage
```

---

## 4. Method

### 4.1 Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                          INPUT LAYER                            │
│                    FALCON Dataset (JSON)                        │
└───────────────────────────┬─────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                    PROCESSING PIPELINE                          │
│                                                                 │
│  Stage 1: Claim Extraction (LLM - Gemini)                      │
│           ↓                                                     │
│  Stage 2: Persuasion Detection (LLM + Ground Truth)            │
│           ↓                                                     │
│  Stage 3: Entity Recognition (spaCy) + Wikidata Linking        │
│           ↓                                                     │
│  Stage 4: Verification Status (Placeholder)                    │
│           ↓                                                     │
│  Stage 5: RDF Generation (RDFLib)                              │
└───────────────────────────┬─────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                        OUTPUT LAYER                             │
│                                                                 │
│  ├── annotated_posts.ttl (Turtle format)                       │
│  ├── annotated_posts.json-ld (JSON-LD format)                  │
│  └── pipeline_stats.json (Summary metrics)                     │
└─────────────────────────────────────────────────────────────────┘
```

### 4.2 Ontology Design

Our custom ontology (`persuasion_ontology.ttl`) defines:

**Core Classes:**
- `Post` - Social media post container
- `Claim` - Verifiable factual assertion
- `Entity` - Named entity with optional Wikidata link
- `Evidence` - Supporting/refuting source

**Persuasion Techniques (subclasses of PersuasionTechnique):**
- `FearAppeal`, `LoadedLanguage`, `Scapegoating`
- `AppealToAuthority`, `Exaggeration`, `AdHominem`
- `FalseDilemma`, `HastyGeneralization`, `AppealToRidicule`

**Key Properties:**
- `containsClaim` - Links Post to Claims
- `usesTechnique` - Associates technique with Claim
- `targetsEntity` - Links Claim to mentioned Entity
- `linkedToWikidata` - External entity reference
- `hasVerificationStatus` - Fact-check result

### 4.3 Technology Stack

| Component | Technology |
|-----------|------------|
| LLM Backend | Google Gemini 2.5 Flash (via OpenRouter) |
| NER | spaCy (en_core_web_sm) |
| Entity Linking | Wikidata SPARQL |
| RDF Library | RDFLib 7.0 |
| Ontology | OWL 2 + PROV-O |

---

## 5. Experimental Setup

### 5.1 Configuration

```python
LLM_MODEL = "google/gemini-2.5-flash-lite"
CONFIDENCE_THRESHOLD = 0.6
BATCH_SIZE = 5
MAX_POSTS = 15  # For demo run
```

### 5.2 Execution Environment

- Python 3.12
- macOS environment
- OpenRouter API for LLM access

### 5.3 Evaluation Metrics

For posts with FALCON ground-truth labels, we use:
- Technique detection accuracy
- Entity linking precision
- RDF triple count

---

## 6. Results

### 6.1 Pipeline Execution Summary

| Metric | Value |
|--------|-------|
| Posts processed | 15 |
| Claims extracted | 36 |
| Techniques detected | 64 |
| Entities linked | 20 |
| RDF triples generated | ~492 |

### 6.2 Technique Distribution (LLM + Ground Truth)

| Technique | Count |
|-----------|-------|
| LoadedLanguage | 26 |
| FalseDilemma | 14 |
| HastyGeneralization | 9 |
| Scapegoating | 8 |
| FearAppeal | 3 |
| AdHominem | 2 |
| AppealToRidicule | 1 |
| Exaggeration | 1 |

### 6.3 Entity Linking Results

Example entities successfully linked to Wikidata:

| Entity | Type | Wikidata ID |
|--------|------|-------------|
| George Floyd | Person | Q5539328 |
| Milwaukee Bucks | Organization | Q169637 |
| Trump | Organization | Q2643970 |

### 6.4 Sample RDF Output

```turtle
<http://example.org/post#falcon_9> a ns1:Post ;
    ns1:containsClaim <http://example.org/claim#falcon_9_1> ;
    ns1:platform "Twitter" ;
    ns1:postId "falcon_9" ;
    prov:wasGeneratedBy <http://example.org/agent#MUSE_Pipeline> .

<http://example.org/claim#falcon_9_1> a ns1:Claim ;
    ns1:claimText "No one could have watched that George Floyd video..." ;
    ns1:confidenceScore "1.0"^^xsd:float ;
    ns1:targetsEntity <http://example.org/entity#George_Floyd> ;
    ns1:usesTechnique ns1:FalseDilemma .

<http://example.org/entity#George_Floyd> a ns1:Entity ;
    ns1:entityName "George Floyd" ;
    ns1:entityType "Person" ;
    ns1:linkedToWikidata <http://www.wikidata.org/entity/Q5539328> .
```

---

## 7. Conclusions

### 7.1 Contributions

1. **Semantic Pipeline**: End-to-end system for persuasion detection with RDF output
2. **Ontology Design**: Custom vocabulary integrating PROV-O and Wikidata
3. **LLM Integration**: Demonstrated use of Gemini for claim/technique extraction
4. **Entity Linking**: Automated linking to Wikidata knowledge base

### 7.2 Advantages over Baseline

Compared to the original MUSE framework:

| Aspect | MUSE | Our Approach |
|--------|------|--------------|
| Output format | Text explanations | RDF knowledge graph |
| Entity linking | None | Wikidata integration |
| Queryability | None | SPARQL endpoint ready |
| Provenance | Limited | Full PROV-O tracking |

### 7.3 Limitations and Future Work

- **Verification**: Fact-checking module is placeholder (requires web search API)
- **Scale**: Demo limited to 15 posts; full dataset would require API budget
- **Evaluation**: Need human evaluation of LLM-extracted claims
- **Visualization**: Graph visualization component is separate

### 7.4 Next Steps

1. Integrate web search for evidence retrieval
2. Deploy to triple store (GraphDB/Fuseki)
3. Build SPARQL-powered dashboard
4. Evaluate on full FALCON test set

---

## References

[1] Da San Martino, G., et al. (2019). "Fine-Grained Analysis of Propaganda in News Articles." EMNLP.

[2] Ulasik, M., Stieglitz, S., et al. (2023). "FALCON: A Fallacy Annotated COVID-19 Corpus." arXiv.

[3] Zhou, Y., et al. (2024). "MUSE: Machine Unlearning Six-Way Evaluation." arXiv.

[4] W3C. (2013). "PROV-O: The PROV Ontology." W3C Recommendation.

[5] Vrandečić, D., & Krötzsch, M. (2014). "Wikidata: A free collaborative knowledge base." CACM.

---

## Appendix

### A. Repository Structure

```
semantic_web_project/
├── pipeline_implementation.py   # Main pipeline
├── persuasion_ontology.ttl      # OWL ontology
├── notebooks/
│   ├── 01_tools_usage.ipynb     # RDF + Wikidata demo
│   ├── 02_nlp_llm_tools_intro.ipynb  # LLM + spaCy demo
│   └── 03_data_preprocessing.ipynb   # FALCON preprocessing
├── data/
│   ├── input/processed/         # Preprocessed FALCON
│   └── output/                  # Generated RDF + stats
└── reports/
    └── technical_report.md      # This document
```

### B. Example SPARQL Queries

**Find all posts using FearAppeal:**
```sparql
PREFIX persuasion: <http://example.org/persuasion#>

SELECT ?post ?claimText
WHERE {
    ?post persuasion:containsClaim ?claim .
    ?claim persuasion:usesTechnique persuasion:FearAppeal ;
           persuasion:claimText ?claimText .
}
```

**Count techniques by type:**
```sparql
PREFIX persuasion: <http://example.org/persuasion#>

SELECT ?technique (COUNT(?claim) as ?count)
WHERE {
    ?claim persuasion:usesTechnique ?technique .
}
GROUP BY ?technique
ORDER BY DESC(?count)
```
