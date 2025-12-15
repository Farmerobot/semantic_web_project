# Milestone 4: First Iteration Experimental Results

**Project:** Semantic Web Methods for Detecting Persuasion Techniques in Social Media  
**Authors:** Mateusz Idziejczak, Mateusz Stawicki  
**Date:** December 2025  
**Repository:** https://github.com/Farmerobot/semantic_web_project

---

## 1. Experimental Setup

### 1.1 Dataset
- **FALCON** (Fallacies in COVID-19 Network-based)
- 2,916 tweets annotated for 6 fallacy types
- Sample size for this iteration: **15 posts**

### 1.2 Pipeline Configuration
| Parameter | Value |
|-----------|-------|
| Input File | `data/input/processed/falcon_processed.json` |
| LLM Model | `google/gemini-2.5-flash-lite` (via OpenRouter) |
| Confidence Threshold | 0.6 |
| NER Model | spaCy `en_core_web_sm` |

---

## 2. Experimental Results

### 2.1 Pipeline Output Statistics

| Metric | Value |
|--------|-------|
| Posts Processed | 15 |
| Claims Extracted | 34 |
| Persuasion Techniques Detected | 57 |
| Entities Linked to Wikidata | 18 |
| RDF Triples Generated | 390 |

**Averages:**
- Claims per post: 2.27
- Techniques per post: 3.80

### 2.2 Detected Persuasion Techniques

| Technique | Count | Percentage |
|-----------|-------|------------|
| LoadedLanguage | 23 | 40.4% |
| FalseDilemma | 13 | 22.8% |
| HastyGeneralization | 7 | 12.3% |
| Scapegoating | 6 | 10.5% |
| FearAppeal | 3 | 5.3% |
| AdHominem | 2 | 3.5% |
| Exaggeration | 2 | 3.5% |
| AppealToRidicule | 1 | 1.8% |

### 2.3 Ground Truth vs Detected Comparison

| Technique | Ground Truth | Detected |
|-----------|--------------|----------|
| AdHominem | 1 | 2 |
| AppealToRidicule | 0 | 1 |
| Exaggeration | 0 | 2 |
| FalseDilemma | 3 | 13 |
| FearAppeal | 0 | 3 |
| HastyGeneralization | 2 | 7 |
| LoadedLanguage | 5 | 23 |
| Scapegoating | 0 | 6 |
| **TOTAL** | **11** | **57** |

**Observation:** LLM-based detection identifies significantly more techniques than human-labeled ground truth. This indicates:
1. Richer annotation capability
2. Potential over-detection (hallucination risk)
3. Human labels may be conservative

### 2.4 Entity Linking Results

Sample entities successfully linked to Wikidata:

| Entity | Wikidata ID |
|--------|-------------|
| George Floyd | Q5539328 |
| Milwaukee Bucks | Q169637 |
| Trump | Q2643970 |
| Supermax | Q7643958 |

### 2.5 SPARQL Query Results

**Posts with >2 persuasion techniques:**
| Post ID | Technique Count |
|---------|-----------------|
| falcon_2 | 5 |
| falcon_0 | 4 |
| falcon_1 | 4 |
| falcon_13 | 4 |
| falcon_4 | 3 |
| falcon_7 | 3 |

---

## 3. Comparison with Baseline (MUSE Framework)

We compare our approach with **MUSE** (Zhou et al., 2024), the baseline framework for persuasion-aware misinformation correction.

| Feature | MUSE (Baseline) | Our Approach |
|---------|-----------------|--------------|
| Output Format | Plain text corrections | RDF Knowledge Graph |
| Queryable Knowledge Graph | No | **Yes** |
| Entity Linking (Wikidata) | No | **Yes** |
| Provenance Tracking (PROV-O) | No | **Yes** |
| Persuasion Technique Types | 4 types | **8+ types (extensible)** |
| Claim Extraction | Yes (LLM) | Yes (LLM) |
| Structured Explanations | Text-based | **Semantic (RDF)** |
| SPARQL Querying | No | **Yes** |
| Multi-format Export | No | **Yes (TTL, JSON-LD)** |

### 3.1 Key Advantages Over Baseline

1. **Structured Knowledge Representation**
   - RDF enables machine reasoning and inference
   - Knowledge graph can be extended and linked to other datasets

2. **Entity Disambiguation**
   - Wikidata linking provides unambiguous entity references
   - Enables cross-referencing with external knowledge bases

3. **Queryability**
   - SPARQL allows complex analytical queries
   - Pattern detection across multiple posts

4. **Provenance**
   - PROV-O tracks annotation generation metadata
   - Supports reproducibility and auditing

5. **Interoperability**
   - Standard formats (Turtle, JSON-LD)
   - Compatible with existing semantic web tools

---

## 4. Initial Insights and Conclusions

### 4.1 Key Findings

1. **LoadedLanguage dominates** - Most frequently detected technique (40.4%), consistent with FALCON's COVID-19 discourse focus

2. **LLM detection is more aggressive** - Detects ~5x more techniques than ground truth labels, suggesting either richer annotation or over-detection

3. **Entity linking successful** - 18 entities linked to Wikidata from 15 posts, enabling knowledge graph enrichment

4. **RDF representation works** - 390 triples generated, queryable via SPARQL

### 4.2 Limitations Identified

1. **Fact-checking placeholder** - Currently returns "Unverified" for all claims
2. **Potential hallucination** - LLM may detect techniques not actually present
3. **API rate limits** - Processing speed constrained by OpenRouter limits
4. **Non-deterministic LLM outputs** - Cloud LLM APIs (OpenRouter, OpenAI, etc.) do not guarantee reproducible results even with temperature=0, due to GPU parallelism and mixture-of-experts batching. We use temperature=0.1-0.2 for simplicity and cost efficiency. For strict reproducibility, users can swap to self-hosted solutions like **vLLM** or **Ollama** with fixed random seeds, which guarantee deterministic outputs.

### 4.3 Next Steps

1. Increase sample size for more robust statistics
2. Implement precision/recall metrics against ground truth
3. Add fact-checking integration with external APIs
4. Fine-tune detection prompts to reduce hallucination

---

## 5. Output Artifacts

| File | Description |
|------|-------------|
| `data/output/annotated_posts.ttl` | RDF in Turtle format |
| `data/output/annotated_posts.json-ld` | RDF in JSON-LD format |
| `data/output/pipeline_stats.json` | Execution statistics |

---

## References

1. Zhou et al. (2024). *Correcting Misinformation on Social Media with a Large Language Model (MUSE)*
2. FALCON Dataset - Fallacies in COVID-19 Network-based dataset
3. Wikidata - https://www.wikidata.org/
