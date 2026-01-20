# Persuasion-Aware MUSE: Final Report

**Project:** Semantic Web Methods for Detecting Persuasion Techniques in Social Media  
**Authors:** Mateusz Idziejczak, Mateusz Stawicki  
**Repository:** https://github.com/Farmerobot/semantic_web_project

---

## Abstract

This report presents **Persuasion-Aware MUSE**, a semantic web pipeline for detecting persuasion techniques in social media posts. Our system extracts factual claims using Large Language Models (LLMs), detects rhetorical manipulation patterns, links named entities to Wikidata, performs sentiment analysis, and generates RDF knowledge graphs following a custom OWL 2 ontology. We demonstrate the pipeline on the FALCON dataset of COVID-19 related tweets, producing queryable semantic representations that enable reasoning over misinformation patterns.

---

## 1. Introduction

### 1.1 Problem Statement

Social media has become a primary vector for the spread of misinformation and manipulative content. Persuasion techniques-such as fear appeals, loaded language, ad hominem attacks, and false dilemmas-are frequently employed to influence public opinion without logical argumentation. Detecting these techniques is critical for:

1. **Media literacy** - Helping users recognize manipulation
2. **Content moderation** - Assisting platforms in identifying harmful content
3. **Research** - Enabling systematic analysis of disinformation campaigns

However, current approaches often lack:
- **Structured representations** that enable reasoning over detected patterns
- **Entity linking** to external knowledge bases for contextualization
- **Explainability** in the form of semantic justifications
- **Interoperability** with other semantic web resources

### 1.2 Proposed Approach

We present **Persuasion-Aware MUSE**, a semantic web pipeline that addresses these limitations by:

- Extracting factual claims from social media posts using LLMs (Gemini 2.5 Flash)
- Detecting persuasion techniques with confidence scores and explanations
- Linking named entities to Wikidata for knowledge enrichment
- Performing sentiment analysis using TextBlob
- Generating RDF knowledge graphs following a custom OWL 2 ontology
- Enabling SPARQL-based querying for downstream analysis

### 1.3 Contributions

1. **Custom Ontology**: A comprehensive OWL 2 ontology for modeling persuasion techniques, claims, entities, and sentiment with proper class hierarchies
2. **End-to-End Pipeline**: Fully functional Python implementation processing raw social media posts to RDF
3. **Reification Pattern**: Novel use of `PersuasionAnnotation` class to properly associate confidence scores with specific technique detections
4. **Multi-modal Analysis**: Integration of NER, sentiment analysis, and LLM-based reasoning
5. **Knowledge Graph Output**: SPARQL-queryable RDF in Turtle and JSON-LD formats

---

## 2. Related Work

### 2.1 Propaganda and Persuasion Detection

| Work | Contribution | Limitation |
|------|--------------|------------|
| Da San Martino et al. (2019) [1] | Fine-grained propaganda detection with 18 technique categories | No semantic output |
| FALCON dataset (Ulasik et al., 2023) [2] | Fallacy annotations for COVID-19 tweets | Classification only, no knowledge graph |
| PTC corpus | Sentence-level propaganda labels | Limited to news articles |

### 2.2 Misinformation Correction Systems

| System | Approach | Output |
|--------|----------|--------|
| MUSE (Zhou et al., 2024) [3] | LLM-generated structured explanations | Text/JSON |
| Community Notes (X/Twitter) | Crowdsourced corrections | Unstructured text |
| ClaimBuster | Automated claim detection | Binary classification |

### 2.3 Semantic Web for Misinformation

- **ClaimReview schema**: Schema.org vocabulary for fact-check metadata, used by Google Search
- **Wikidata**: Collaborative knowledge base with 100M+ entities, ideal for entity linking
- **PROV-O ontology**: W3C standard for provenance tracking, enabling transparency in automated annotations

### 2.4 Gap Analysis

No existing system combines:
- LLM-based persuasion detection
- Semantic web output (RDF/OWL)
- Entity linking to Wikidata
- Sentiment analysis integration
- Queryable knowledge graph generation

Our work fills this gap.

---

## 3. Dataset Description

### 3.1 FALCON Dataset

We use the **FALCON** (Fallacies in COVID-19 Network-based) dataset [2] as our primary corpus. FALCON contains Twitter conversations annotated with logical fallacy and persuasion technique labels.

**Dataset Characteristics:**

| Metric | Value |
|--------|-------|
| Total tweets | 2,916 |
| Train split | 1,811 (62.1%) |
| Validation split | 550 (18.9%) |
| Test split | 555 (19.0%) |
| Tweets with ≥1 fallacy | 1,009 (34.6%) |
| Average tweet length | 187 characters |
| Time period | 2020-2021 (COVID-19) |

### 3.2 Fallacy Type Distribution

| Fallacy Type | Count | Percentage | Ontology Mapping |
|--------------|-------|------------|------------------|
| Loaded Language | 457 | 15.7% | `LoadedLanguage` |
| Ad Hominem | 259 | 8.9% | `AdHominem` |
| Appeal to Ridicule | 238 | 8.2% | `AppealToRidicule` |
| False Dilemma | 168 | 5.8% | `FalseDilemma` |
| Appeal to Fear | 157 | 5.4% | `FearAppeal` |
| Hasty Generalization | 91 | 3.1% | `HastyGeneralization` |
| Scapegoating | 84 | 2.9% | `Scapegoating` |
| Exaggeration | 72 | 2.5% | `Exaggeration` |

### 3.3 Data Preprocessing

The FALCON dataset was preprocessed using the following steps:

1. **Text cleaning**: Removal of URLs, normalization of whitespace
2. **User anonymization**: Replacement of @mentions with `[userXXXX]` tokens
3. **Technique mapping**: Conversion of FALCON labels to ontology class names
4. **JSON export**: Structured format with `post_id`, `text_clean`, and `techniques` fields

---

## 4. Method

### 4.1 System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                           INPUT LAYER                                │
│                     FALCON Dataset (JSON)                            │
│              [post_id, text_clean, techniques]                       │
└─────────────────────────────┬───────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      PROCESSING PIPELINE                             │
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │ Stage 1: CLAIM EXTRACTION                                    │    │
│  │ • LLM: Google Gemini 2.5 Flash (via OpenRouter)             │    │
│  │ • Extracts verifiable factual assertions from post text      │    │
│  │ • Output: List[Claim] with claim_id, text, source_post       │    │
│  └─────────────────────────────┬───────────────────────────────┘    │
│                                ▼                                     │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │ Stage 2: PERSUASION DETECTION                                │    │
│  │ • Uses FALCON ground-truth labels when available             │    │
│  │ • LLM-based detection for unlabeled posts                    │    │
│  │ • Output: PersuasionAnnotation with technique, confidence,   │    │
│  │           and explanation                                     │    │
│  └─────────────────────────────┬───────────────────────────────┘    │
│                                ▼                                     │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │ Stage 3: ENTITY RECOGNITION & LINKING                        │    │
│  │ • NER: spaCy (en_core_web_sm)                                │    │
│  │ • Entity types: Person, Organization, Location, Event        │    │
│  │ • Wikidata linking via SPARQL endpoint                       │    │
│  └─────────────────────────────┬───────────────────────────────┘    │
│                                ▼                                     │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │ Stage 4: SENTIMENT ANALYSIS                                  │    │
│  │ • TextBlob polarity scoring (-1 to +1)                       │    │
│  │ • Classification: Positive/Negative/Neutral                  │    │
│  └─────────────────────────────┬───────────────────────────────┘    │
│                                ▼                                     │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │ Stage 5: RDF GENERATION                                      │    │
│  │ • RDFLib graph construction                                  │    │
│  │ • Ontology import for property declarations                  │    │
│  │ • Provenance tracking with PROV-O                            │    │
│  └─────────────────────────────┬───────────────────────────────┘    │
│                                                                      │
└─────────────────────────────────┬───────────────────────────────────┘
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                          OUTPUT LAYER                                │
│                                                                      │
│  ├── annotated_posts.ttl      (Turtle RDF format)                   │
│  ├── annotated_posts.json-ld  (JSON-LD format)                      │
└─────────────────────────────────────────────────────────────────────┘
```

### 4.2 Ontology Design

Our custom ontology (`persuasion_ontology.ttl`) is designed following OWL 2 DL principles with proper class hierarchies and property declarations.

#### 4.2.1 Class Hierarchy

```
owl:Thing
├── InformationUnit (abstract base)
│   ├── Post
│   └── Claim
├── Entity
│   ├── Person
│   ├── Organization
│   ├── Location
│   └── Event
├── PersuasionTechnique
│   ├── FearAppeal
│   ├── LoadedLanguage
│   ├── AdHominem
│   ├── Scapegoating
│   ├── Exaggeration
│   ├── FalseDilemma
│   ├── HastyGeneralization
│   ├── AppealToRidicule
│   ├── Whataboutism
│   ├── Bandwagon
│   └── AppealToEmotion
├── PersuasionAnnotation (reification)
├── Sentiment
│   ├── PositiveSentiment
│   ├── NegativeSentiment
│   └── NeutralSentiment
├── VerificationStatus
│   ├── True / False / Unverified
│   ├── MostlyTrue / MostlyFalse
│   └── Misleading
├── Evidence
├── Correction
└── Source
```

#### 4.2.2 Property Definitions

**Object Properties:**

| Property | Domain | Range | Description |
|----------|--------|-------|-------------|
| `containsClaim` | Post | Claim | Links post to extracted claims |
| `hasAnnotation` | Claim | PersuasionAnnotation | Links claim to technique annotation |
| `annotatesTechnique` | PersuasionAnnotation | PersuasionTechnique | The detected technique |
| `targetsEntity` | Claim | Entity | Entity mentioned in claim |
| `linkedToWikidata` | Entity | (external) | Wikidata entity reference |
| `hasSentiment` | InformationUnit | Sentiment | Emotional tone |
| `hasVerificationStatus` | Claim | VerificationStatus | Fact-check result |
| `replyTo` | Post | Post | Thread structure |
| `contradicts` | Claim | Claim | Symmetric contradiction |

**Data Properties:**

| Property | Domain | Range | Description |
|----------|--------|-------|-------------|
| `postId` | Post | xsd:string | Unique identifier |
| `hasText` | Post | xsd:string | Textual content (subproperty of `hasContent`) |
| `hasImage` | Post | xsd:anyURI | Image reference (subproperty of `hasContent`) |
| `confidenceScore` | PersuasionAnnotation | xsd:float | Detection confidence (0-1) |
| `explanation` | PersuasionAnnotation | xsd:string | Justification text |
| `sentimentScore` | InformationUnit | xsd:float | Polarity (-1 to +1) |
| `entityName` | Entity | xsd:string | Entity label |

#### 4.2.3 Property Characteristics

OWL 2 property characteristics enable reasoning and constraint enforcement:

| Property | Characteristics | Rationale |
|----------|-----------------|-----------|
| `wasGeneratedBy` | Functional | Each post/claim generated by exactly one agent |
| `hasVerificationStatus` | Functional | Each claim has exactly one verification status |
| `hasSentiment` | Functional | Each content unit has exactly one sentiment |
| `linkedToWikidata` | Functional | Each entity links to at most one Wikidata ID |
| `annotatesTechnique` | Functional | Each annotation identifies exactly one technique |
| `replyTo` | Functional, Asymmetric, Irreflexive | A post replies to exactly one post; cannot reply to itself |
| `quotes` | Asymmetric, Irreflexive | Quoting is directional; cannot quote itself |
| `correctsClaim` | Asymmetric, Irreflexive | Corrections are directional |
| `contradicts` | Symmetric, Irreflexive | Contradiction is mutual; a claim cannot contradict itself |
| `relatedTo` | Symmetric | Topic relatedness is mutual |

#### 4.2.4 Design Decisions

1. **InformationUnit base class**: Both `Post` and `Claim` inherit from this abstract class, enabling shared properties like `hasSentiment` and `mentions`

2. **Reification via PersuasionAnnotation**: Instead of directly linking claims to techniques, we use an intermediate class that bundles:
   - The technique type
   - Confidence score
   - Explanation text
   
   This solves the problem of associating multiple confidence scores with multiple techniques per claim.

3. **Entity subclasses**: `Person`, `Organization`, `Location`, `Event` enable type-specific reasoning and Wikidata query optimization

4. **Content property hierarchy**: `hasText` and `hasImage` are subproperties of `hasContent`, enabling future multi-modal support

### 4.3 Technology Stack

| Component | Technology | Version |
|-----------|------------|---------|
| Language | Python | 3.12 |
| LLM Backend | Google Gemini 2.5 Flash | via OpenRouter API |
| NER | spaCy | en_core_web_sm |
| Sentiment Analysis | TextBlob | 0.18.0 |
| Entity Linking | Wikidata | SPARQL endpoint |
| RDF Library | RDFLib | 7.0 |
| Ontology Language | OWL 2 DL | + PROV-O |

---

## 5. Evaluation Strategy

### 5.1 Experimental Configuration

```python
Config:
    LLM_MODEL = "google/gemini-2.5-flash-lite"
    CONFIDENCE_THRESHOLD = 0.6
    BATCH_SIZE = 5
    MAX_POSTS = 100  # Demo run limitation
```

### 5.2 Evaluation Dimensions

| Dimension | Metric | Method |
|-----------|--------|--------|
| Claim extraction | Quality | Manual inspection of extracted claims |
| Technique detection | Accuracy | Comparison with FALCON ground truth |
| Entity linking | Precision | Validation of Wikidata matches |
| Sentiment analysis | Correlation | TextBlob vs. manual assessment |
| RDF validity | Syntactic | Protégé ontology validation |
| Queryability | Functional | SPARQL query execution |

### 5.3 Limitations

- **Demo scale**: Full evaluation limited to 100 posts due to API costs
- **Ground truth dependency**: Technique detection uses FALCON labels when available
- **Verification placeholder**: Fact-checking module not fully implemented
- **LLM non-determinism**: Cloud APIs do not guarantee reproducible results

---

## 6. Results

### 6.1 Pipeline Execution Summary

| Metric | Value |
|--------|-------|
| Posts processed | 100 |
| Claims extracted | 247 |
| Techniques detected | 401 |
| Entities linked | 145 |
| RDF triples generated | 4,456 |

### 6.2 Technique Detection Results

| Technique | Count | Percentage |
|-----------|-------|------------|
| LoadedLanguage | 157 | 39.2% |
| FalseDilemma | 59 | 14.7% |
| AdHominem | 35 | 8.7% |
| Exaggeration | 34 | 8.5% |
| HastyGeneralization | 30 | 7.5% |
| Scapegoating | 30 | 7.5% |
| AppealToRidicule | 30 | 7.5% |
| AppealToAuthority | 17 | 4.2% |
| FearAppeal | 9 | 2.2% |

### 6.3 Sentiment Analysis Results

| Sentiment Class | Count | Example Score Range |
|-----------------|-------|---------------------|
| NegativeSentiment | 6 | -0.7 to -0.1 |
| NeutralSentiment | 5 | -0.05 to +0.05 |
| PositiveSentiment | 4 | +0.1 to +0.375 |

### 6.4 Entity Recognition Results

Entities are now typed using ontology subclasses:

| Entity | Type | Wikidata ID |
|--------|------|-------------|
| George Floyd | Person | Q5539328 |
| Milwaukee Bucks | Organization | Q169637 |
| BLM | Organization | - |
| Trump | Person | Q22686 |

### 6.5 Sample RDF Output

```turtle
@prefix : <http://example.org/persuasion#> .
@prefix prov: <http://www.w3.org/ns/prov#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<http://example.org/post#falcon_9> a :Post ;
    :postId "falcon_9"^^xsd:string ;
    :hasText "Why must we always be combative?..."^^xsd:string ;
    :platform "Twitter"^^xsd:string ;
    :containsClaim <http://example.org/claim#falcon_9_1> ;
    :hasSentiment :NegativeSentiment ;
    :sentimentScore "-0.7"^^xsd:float ;
    prov:wasGeneratedBy <http://example.org/agent#MUSE_Pipeline> .

<http://example.org/claim#falcon_9_1> a :Claim ;
    :claimText "No one could have watched that George Floyd video..." ;
    :hasAnnotation <http://example.org/annotation#falcon_9_1_tech_0> ;
    :targetsEntity <http://example.org/entity#George_Floyd> ;
    :hasVerificationStatus :Unverified .

<http://example.org/annotation#falcon_9_1_tech_0> a :PersuasionAnnotation ;
    :annotatesTechnique :FalseDilemma ;
    :confidenceScore "1.0"^^xsd:float ;
    :explanation "Labeled in FALCON dataset"^^xsd:string .

<http://example.org/entity#George_Floyd> a :Person ;
    :entityName "George Floyd"^^xsd:string ;
    :linkedToWikidata <http://www.wikidata.org/entity/Q5539328> .
```

### 6.6 SPARQL Query Examples

**Query 1: Find all posts using FearAppeal technique**
```sparql
PREFIX : <http://example.org/persuasion#>

SELECT ?post ?claimText ?confidence
WHERE {
    ?post :containsClaim ?claim .
    ?claim :claimText ?claimText ;
           :hasAnnotation ?annotation .
    ?annotation :annotatesTechnique :FearAppeal ;
                :confidenceScore ?confidence .
}
```

**Query 2: Count techniques by type with explanations**
```sparql
PREFIX : <http://example.org/persuasion#>

SELECT ?technique (COUNT(?annotation) as ?count)
WHERE {
    ?annotation :annotatesTechnique ?technique .
}
GROUP BY ?technique
ORDER BY DESC(?count)
```

**Query 3: Find negative sentiment posts with scapegoating**
```sparql
PREFIX : <http://example.org/persuasion#>

SELECT ?post ?text ?score
WHERE {
    ?post :hasSentiment :NegativeSentiment ;
          :sentimentScore ?score ;
          :hasText ?text ;
          :containsClaim ?claim .
    ?claim :hasAnnotation ?ann .
    ?ann :annotatesTechnique :Scapegoating .
}
```

---

## 7. Conclusions

### 7.1 Achievements

1. **Complete Semantic Pipeline**: End-to-end system from raw social media posts to queryable RDF knowledge graphs

2. **Rich Ontology**: OWL 2 DL ontology with proper class hierarchies, data/object property distinctions, and extensibility for future features

3. **Reification Pattern**: Novel `PersuasionAnnotation` class that correctly associates confidence scores and explanations with specific technique detections

4. **Multi-modal Analysis**: Integration of LLM reasoning, NER, sentiment analysis, and entity linking in a unified pipeline

5. **Wikidata Integration**: Automated linking of named entities to the Wikidata knowledge base

6. **Provenance Tracking**: Full PROV-O compliance for transparency in automated annotations

### 7.2 Comparison with Baseline

| Aspect | Original MUSE | Persuasion-Aware MUSE |
|--------|---------------|----------------------|
| Output format | Text explanations | RDF knowledge graph |
| Entity linking | None | Wikidata integration |
| Queryability | None | SPARQL-ready |
| Provenance | Limited | Full PROV-O |
| Sentiment | None | TextBlob integration |
| Ontology | None | Custom OWL 2 DL |
| Extensibility | Low | High (semantic web) |

### 7.3 Limitations

1. **Scale**: Demo limited to 100 posts; full dataset processing requires significant API budget
2. **Verification**: Fact-checking module is a placeholder (requires web search API integration)
3. **LLM Reproducibility**: Cloud LLM APIs do not guarantee deterministic outputs
4. **Entity Linking Coverage**: Not all entities have Wikidata matches
5. **Evaluation**: Comprehensive human evaluation of LLM-extracted claims not performed

### 7.4 Future Work

1. **Web Search Integration**: Implement evidence retrieval for fact-checking
2. **Triple Store Deployment**: Deploy to GraphDB or Apache Jena Fuseki for production use
3. **SPARQL Dashboard**: Build interactive visualization of knowledge graph
4. **Full Dataset Evaluation**: Process complete FALCON test set with proper metrics
5. **Multi-lingual Support**: Extend to non-English social media content
6. **Image Analysis**: Leverage `hasImage` property for multi-modal persuasion detection

---

## References

[1] Da San Martino, G., Yu, S., Barrón-Cedeño, A., Petrov, R., & Nakov, P. (2019). "Fine-Grained Analysis of Propaganda in News Articles." *Proceedings of EMNLP-IJCNLP 2019*, pp. 5636-5646.

[2] Ulasik, M., Stieglitz, S., Widjaja, T., & Giese, J. (2023). "FALCON: A Fallacy Annotated Corpus of COVID-19 Related Tweets." *arXiv preprint arXiv:2308.15816*.

[3] Zhou, X., Sharma, Y., Peng, H., & Choi, Y. (2024). "Correcting Misinformation on Social Media with a Large Language Model." *arXiv preprint arXiv:2403.11169*.

[4] W3C. (2013). "PROV-O: The PROV Ontology." *W3C Recommendation*. https://www.w3.org/TR/prov-o/

[5] Vrandečić, D., & Krötzsch, M. (2014). "Wikidata: A Free Collaborative Knowledgebase." *Communications of the ACM*, 57(10), pp. 78-85.

[6] Schema.org. (2017). "ClaimReview." https://schema.org/ClaimReview

[7] Loper, E., & Bird, S. (2002). "NLTK: The Natural Language Toolkit." *Proceedings of the ACL-02 Workshop on Effective Tools and Methodologies for Teaching NLP*.

---

## Appendix

### A. Repository Structure

```
semantic_web_project/
├── pipeline_implementation.py      # Main pipeline (749 lines)
├── persuasion_ontology.ttl         # OWL 2 ontology (454 lines)
├── requirements.txt                # Python dependencies
├── .env                            # API keys (not committed)
├── notebooks/
│   ├── 01_tools_usage.ipynb        # RDF + Wikidata demo
│   ├── 02_nlp_llm_tools_intro.ipynb # LLM + spaCy demo
│   ├── 03_data_preprocessing.ipynb  # FALCON preprocessing
│   └── 04_experimental_results.ipynb # Pipeline execution
├── data/
│   ├── input/
│   │   ├── raw/                    # Original FALCON dataset
│   │   └── processed/              # Preprocessed JSON
│   └── output/
│       ├── annotated_posts.ttl     # RDF output (Turtle)
│       ├── annotated_posts.json-ld # RDF output (JSON-LD)
│       └── pipeline_stats.json     # Execution statistics
└── reports/
    ├── presentation_milestone_4.md
    ├── presentation_milestone_5.md
    └── presentation_milestone_6.md  # This document
```

### B. Ontology Namespace Prefixes

| Prefix | URI | Description |
|--------|-----|-------------|
| `:` | `http://example.org/persuasion#` | Custom ontology |
| `prov:` | `http://www.w3.org/ns/prov#` | Provenance |
| `wd:` | `http://www.wikidata.org/entity/` | Wikidata entities |
| `owl:` | `http://www.w3.org/2002/07/owl#` | OWL 2 |
| `xsd:` | `http://www.w3.org/2001/XMLSchema#` | XML Schema datatypes |
| `dc:` | `http://purl.org/dc/elements/1.1/` | Dublin Core |

### C. Installation Instructions

```bash
# Clone repository
git clone https://github.com/Farmerobot/semantic_web_project.git
cd semantic_web_project

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or: .\venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
python -m spacy download en_core_web_sm

# Configure API key
echo "OPENROUTER_API_KEY=your_key_here" > .env

# Run pipeline
python pipeline_implementation.py
```

### D. Dependencies

```
rdflib>=7.0.0
spacy>=3.7.0
SPARQLWrapper>=2.0.0
python-dotenv>=1.0.0
openai>=1.0.0
textblob>=0.18.0
```

---