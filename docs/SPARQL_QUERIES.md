# SPARQL Query Examples
## Querying the Persuasion-Aware RDF Knowledge Graph

This document contains example SPARQL queries for analyzing persuasion techniques and misinformation in social media posts.

---

## Setup

```sparql
PREFIX : <http://example.org/persuasion#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX prov: <http://www.w3.org/ns/prov#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
```

---

## 1. Basic Queries

### 1.1 Find All Posts
```sparql
SELECT ?post ?text ?author ?platform ?timestamp
WHERE {
    ?post rdf:type :Post ;
          :textContent ?text ;
          :author ?author ;
          :platform ?platform ;
          :timestamp ?timestamp .
}
ORDER BY DESC(?timestamp)
```

### 1.2 Find All Claims
```sparql
SELECT ?post ?claim ?claimText
WHERE {
    ?post rdf:type :Post ;
          :containsClaim ?claim .
    ?claim :claimText ?claimText .
}
```

### 1.3 Count Posts by Platform
```sparql
SELECT ?platform (COUNT(?post) AS ?count)
WHERE {
    ?post rdf:type :Post ;
          :platform ?platform .
}
GROUP BY ?platform
ORDER BY DESC(?count)
```

---

## 2. Persuasion Technique Queries

### 2.1 Find All Posts Using Fear Appeal
```sparql
SELECT ?post ?text ?claim ?claimText
WHERE {
    ?post rdf:type :Post ;
          :textContent ?text ;
          :containsClaim ?claim .
    ?claim :claimText ?claimText ;
           :usesTechnique :FearAppeal .
}
```

### 2.2 Count Persuasion Techniques by Type
```sparql
SELECT ?technique (COUNT(?claim) AS ?frequency)
WHERE {
    ?claim :usesTechnique ?technique .
}
GROUP BY ?technique
ORDER BY DESC(?frequency)
```

### 2.3 Find Claims Using Multiple Techniques
```sparql
SELECT ?claim ?claimText (COUNT(?technique) AS ?techniqueCount)
WHERE {
    ?post :containsClaim ?claim .
    ?claim :claimText ?claimText ;
           :usesTechnique ?technique .
}
GROUP BY ?claim ?claimText
HAVING (COUNT(?technique) > 1)
ORDER BY DESC(?techniqueCount)
```

### 2.4 Find High-Confidence Persuasion Detection
```sparql
SELECT ?post ?claim ?claimText ?technique ?confidence
WHERE {
    ?post :containsClaim ?claim .
    ?claim :claimText ?claimText ;
           :usesTechnique ?technique ;
           :confidenceScore ?confidence .
    FILTER(?confidence >= 0.85)
}
ORDER BY DESC(?confidence)
```

### 2.5 Find Posts Using Loaded Language
```sparql
SELECT ?post ?text ?claim ?claimText
WHERE {
    ?post rdf:type :Post ;
          :textContent ?text ;
          :containsClaim ?claim .
    ?claim :claimText ?claimText ;
           :usesTechnique :LoadedLanguage .
}
```

---

## 3. Emotion and Sentiment Queries

### 3.1 Find Claims Invoking Fear
```sparql
SELECT ?post ?claim ?claimText ?technique
WHERE {
    ?post :containsClaim ?claim .
    ?claim :claimText ?claimText ;
           :usesTechnique ?technique .
    ?technique :invokesEmotion :Fear .
}
```

### 3.2 Count Emotions Invoked
```sparql
SELECT ?emotion (COUNT(?technique) AS ?count)
WHERE {
    ?technique :invokesEmotion ?emotion .
}
GROUP BY ?emotion
ORDER BY DESC(?count)
```

### 3.3 Find Posts Invoking Multiple Emotions
```sparql
SELECT ?post ?text (GROUP_CONCAT(DISTINCT ?emotion; separator=", ") AS ?emotions)
WHERE {
    ?post rdf:type :Post ;
          :textContent ?text ;
          :containsClaim ?claim .
    ?claim :usesTechnique ?technique .
    ?technique :invokesEmotion ?emotion .
}
GROUP BY ?post ?text
HAVING (COUNT(DISTINCT ?emotion) > 1)
```

---

## 4. Entity-Based Queries

### 4.1 Find Most Targeted Entities
```sparql
SELECT ?entity ?entityName (COUNT(?claim) AS ?targetCount)
WHERE {
    ?claim :targetsEntity ?entity .
    ?entity :entityName ?entityName .
}
GROUP BY ?entity ?entityName
ORDER BY DESC(?targetCount)
LIMIT 10
```

### 4.2 Find Claims About Specific Entity (e.g., European Union)
```sparql
SELECT ?post ?claim ?claimText ?technique
WHERE {
    ?post :containsClaim ?claim .
    ?claim :claimText ?claimText ;
           :targetsEntity ?entity ;
           :usesTechnique ?technique .
    ?entity :linkedToWikidata wd:Q458 .  # Q458 = European Union
}
```

### 4.3 Find Entities with Wikidata Links
```sparql
SELECT ?entity ?entityName ?wikidataId
WHERE {
    ?entity :entityName ?entityName ;
            :linkedToWikidata ?wikidataUri .
    BIND(REPLACE(STR(?wikidataUri), "http://www.wikidata.org/entity/", "") AS ?wikidataId)
}
ORDER BY ?entityName
```

### 4.4 Find Scapegoating Techniques by Targeted Entity
```sparql
SELECT ?entity ?entityName (COUNT(?claim) AS ?scapegoatingCount)
WHERE {
    ?claim :targetsEntity ?entity ;
           :usesTechnique :Scapegoating .
    ?entity :entityName ?entityName .
}
GROUP BY ?entity ?entityName
ORDER BY DESC(?scapegoatingCount)
```

---

## 5. Fact-Checking Queries

### 5.1 Find All False Claims
```sparql
SELECT ?post ?claim ?claimText ?evidence ?evidenceSource
WHERE {
    ?post :containsClaim ?claim .
    ?claim :claimText ?claimText ;
           :hasVerificationStatus :False ;
           :refutedBy ?evidenceNode .
    ?evidenceNode :evidenceText ?evidence ;
                  :evidenceSource ?evidenceSource .
}
```

### 5.2 Count Claims by Verification Status
```sparql
SELECT ?status (COUNT(?claim) AS ?count)
WHERE {
    ?claim :hasVerificationStatus ?status .
}
GROUP BY ?status
ORDER BY DESC(?count)
```

### 5.3 Find Misleading Claims with Evidence
```sparql
SELECT ?claim ?claimText ?evidence ?source
WHERE {
    ?claim :claimText ?claimText ;
           :hasVerificationStatus :Misleading ;
           :refutedBy ?evidenceNode .
    ?evidenceNode :evidenceText ?evidence ;
                  :evidenceSource ?source .
}
```

### 5.4 Find Unverified Claims Using Fear Appeal
```sparql
SELECT ?post ?claim ?claimText
WHERE {
    ?post :containsClaim ?claim .
    ?claim :claimText ?claimText ;
           :usesTechnique :FearAppeal ;
           :hasVerificationStatus :Unverified .
}
```

---

## 6. Combined Analysis Queries

### 6.1 Find False Claims Using Fear + Targeting Specific Entities
```sparql
SELECT ?post ?claim ?claimText ?entity ?entityName
WHERE {
    ?post :containsClaim ?claim .
    ?claim :claimText ?claimText ;
           :usesTechnique :FearAppeal ;
           :hasVerificationStatus :False ;
           :targetsEntity ?entity .
    ?entity :entityName ?entityName .
}
```

### 6.2 Find Posts with High Manipulation Score
```sparql
# Posts with multiple persuasion techniques + false claims
SELECT ?post ?text 
       (COUNT(DISTINCT ?technique) AS ?techniqueCount)
       (COUNT(DISTINCT ?falseClaim) AS ?falseClaimCount)
WHERE {
    ?post rdf:type :Post ;
          :textContent ?text ;
          :containsClaim ?claim .
    ?claim :usesTechnique ?technique .
    
    OPTIONAL {
        ?post :containsClaim ?falseClaim .
        ?falseClaim :hasVerificationStatus :False .
    }
}
GROUP BY ?post ?text
HAVING (?techniqueCount >= 2 && ?falseClaimCount >= 1)
ORDER BY DESC(?techniqueCount + ?falseClaimCount)
```

### 6.3 Temporal Analysis: Techniques Over Time
```sparql
SELECT ?date (COUNT(?technique) AS ?techniqueCount)
WHERE {
    ?post :timestamp ?timestamp ;
          :containsClaim ?claim .
    ?claim :usesTechnique ?technique .
    
    BIND(xsd:date(?timestamp) AS ?date)
}
GROUP BY ?date
ORDER BY ?date
```

### 6.4 Author Analysis: Most Manipulative Authors
```sparql
SELECT ?author 
       (COUNT(DISTINCT ?post) AS ?postCount)
       (COUNT(DISTINCT ?technique) AS ?techniqueCount)
       (COUNT(DISTINCT ?falseClaim) AS ?falseClaimCount)
WHERE {
    ?post :author ?author ;
          :containsClaim ?claim .
    ?claim :usesTechnique ?technique .
    
    OPTIONAL {
        ?post :containsClaim ?falseClaim .
        ?falseClaim :hasVerificationStatus :False .
    }
}
GROUP BY ?author
ORDER BY DESC(?techniqueCount + ?falseClaimCount)
LIMIT 10
```

---

## 7. Provenance Queries

### 7.1 Find All LLM Agents Used
```sparql
SELECT DISTINCT ?agent ?modelName ?modelVersion
WHERE {
    ?post prov:wasGeneratedBy ?agent .
    ?agent rdf:type :LLMAgent ;
           :modelName ?modelName ;
           :modelVersion ?modelVersion .
}
```

### 7.2 Count Annotations by LLM Agent
```sparql
SELECT ?agent ?modelName (COUNT(?post) AS ?annotationCount)
WHERE {
    ?post prov:wasGeneratedBy ?agent .
    ?agent :modelName ?modelName .
}
GROUP BY ?agent ?modelName
ORDER BY DESC(?annotationCount)
```

---

## 8. Advanced Pattern Detection

### 8.1 Find Coordinated Manipulation Patterns
```sparql
# Find posts by different authors using similar techniques about same entity
SELECT ?entity ?entityName ?technique 
       (COUNT(DISTINCT ?author) AS ?authorCount)
       (COUNT(DISTINCT ?post) AS ?postCount)
WHERE {
    ?post :author ?author ;
          :containsClaim ?claim .
    ?claim :usesTechnique ?technique ;
           :targetsEntity ?entity .
    ?entity :entityName ?entityName .
}
GROUP BY ?entity ?entityName ?technique
HAVING (COUNT(DISTINCT ?author) >= 3)
ORDER BY DESC(?postCount)
```

### 8.2 Find Causal Oversimplification with Scapegoating
```sparql
SELECT ?post ?claim ?claimText ?entity ?entityName
WHERE {
    ?post :containsClaim ?claim .
    ?claim :claimText ?claimText ;
           :usesTechnique :CausalOversimplification ;
           :usesTechnique :Scapegoating ;
           :targetsEntity ?entity .
    ?entity :entityName ?entityName .
}
```

### 8.3 Find Appeal to Authority in False Claims
```sparql
SELECT ?post ?claim ?claimText ?evidence
WHERE {
    ?post :containsClaim ?claim .
    ?claim :claimText ?claimText ;
           :usesTechnique :AppealToAuthority ;
           :hasVerificationStatus :False ;
           :refutedBy ?evidenceNode .
    ?evidenceNode :evidenceText ?evidence .
}
```

### 8.4 Find Red Herring with Loaded Language
```sparql
SELECT ?post ?text ?claim ?claimText
WHERE {
    ?post rdf:type :Post ;
          :textContent ?text ;
          :containsClaim ?claim .
    ?claim :claimText ?claimText ;
           :usesTechnique :RedHerring ;
           :usesTechnique :LoadedLanguage .
}
```

---

## 9. Explanatory Queries for MUSE Interface

### 9.1 Full Annotation for a Single Post
```sparql
SELECT ?post ?text ?claim ?claimText ?technique ?emotion 
       ?entity ?entityName ?status ?evidence
WHERE {
    ?post :postId "post_001" ;
          :textContent ?text ;
          :containsClaim ?claim .
    
    ?claim :claimText ?claimText .
    
    OPTIONAL {
        ?claim :usesTechnique ?technique .
        ?technique :invokesEmotion ?emotion .
    }
    
    OPTIONAL {
        ?claim :targetsEntity ?entity .
        ?entity :entityName ?entityName .
    }
    
    OPTIONAL {
        ?claim :hasVerificationStatus ?status .
    }
    
    OPTIONAL {
        ?claim :refutedBy ?evidenceNode .
        ?evidenceNode :evidenceText ?evidence .
    }
}
```

### 9.2 Generate Explanation Text for Claim
```sparql
CONSTRUCT {
    ?claim :hasExplanation ?explanation .
}
WHERE {
    ?claim :claimText ?claimText ;
           :usesTechnique ?technique ;
           :hasVerificationStatus :False .
    
    BIND(CONCAT(
        "This claim uses ", STR(?technique), 
        " to manipulate opinion. Fact-checking shows this claim is false."
    ) AS ?explanation)
}
```

---

## 10. Statistical Queries

### 10.1 Overall Statistics
```sparql
SELECT 
    (COUNT(DISTINCT ?post) AS ?totalPosts)
    (COUNT(DISTINCT ?claim) AS ?totalClaims)
    (COUNT(DISTINCT ?technique) AS ?totalTechniques)
    (AVG(?confidence) AS ?avgConfidence)
WHERE {
    ?post rdf:type :Post ;
          :containsClaim ?claim .
    ?claim :usesTechnique ?technique ;
           :confidenceScore ?confidence .
}
```

### 10.2 Platform-Specific Analysis
```sparql
SELECT ?platform
       (COUNT(DISTINCT ?post) AS ?postCount)
       (COUNT(DISTINCT ?falseClaim) AS ?falseClaimCount)
       (COUNT(?technique) AS ?techniqueCount)
WHERE {
    ?post :platform ?platform ;
          :containsClaim ?claim .
    ?claim :usesTechnique ?technique .
    
    OPTIONAL {
        ?post :containsClaim ?falseClaim .
        ?falseClaim :hasVerificationStatus :False .
    }
}
GROUP BY ?platform
ORDER BY DESC(?techniqueCount)
```

### 10.3 Technique Co-occurrence Matrix
```sparql
SELECT ?technique1 ?technique2 (COUNT(?claim) AS ?cooccurrence)
WHERE {
    ?claim :usesTechnique ?technique1 ;
           :usesTechnique ?technique2 .
    FILTER(?technique1 != ?technique2)
}
GROUP BY ?technique1 ?technique2
ORDER BY DESC(?cooccurrence)
```

---

## Usage Examples

### Using with GraphDB / Fuseki
```bash
# Upload RDF data
curl -X POST http://localhost:7200/repositories/persuasion/statements \
  -H "Content-Type: application/x-turtle" \
  --data-binary @data/output/annotated_posts.ttl

# Execute SPARQL query
curl -X POST http://localhost:7200/repositories/persuasion \
  -H "Content-Type: application/sparql-query" \
  -H "Accept: application/sparql-results+json" \
  --data-binary @query.sparql
```

### Using with RDFLib (Python)
```python
from rdflib import Graph

# Load RDF data
g = Graph()
g.parse("data/output/annotated_posts.ttl", format="turtle")

# Execute SPARQL query
query = """
    PREFIX : <http://example.org/persuasion#>
    SELECT ?post ?technique (COUNT(?technique) AS ?count)
    WHERE {
        ?post :containsClaim ?claim .
        ?claim :usesTechnique ?technique .
    }
    GROUP BY ?post ?technique
"""

results = g.query(query)
for row in results:
    print(f"Post: {row.post}, Technique: {row.technique}, Count: {row.count}")
```

---

## Visualization Queries

### For Network Graphs
```sparql
# Entity-Technique Network
SELECT ?entity ?entityName ?technique
WHERE {
    ?claim :targetsEntity ?entity ;
           :usesTechnique ?technique .
    ?entity :entityName ?entityName .
}
```

### For Timeline Visualization
```sparql
# Technique Frequency Over Time
SELECT ?date ?technique (COUNT(?claim) AS ?count)
WHERE {
    ?post :timestamp ?timestamp ;
          :containsClaim ?claim .
    ?claim :usesTechnique ?technique .
    BIND(xsd:date(?timestamp) AS ?date)
}
GROUP BY ?date ?technique
ORDER BY ?date
```

---

## Performance Tips

1. **Use LIMIT**: Add `LIMIT 100` for exploratory queries
2. **Index entities**: Ensure entity URIs are properly indexed
3. **Filter early**: Place FILTER clauses as early as possible
4. **Use OPTIONAL wisely**: OPTIONAL clauses can be expensive
5. **Aggregate efficiently**: Use GROUP BY with appropriate variables

---

## References

- SPARQL 1.1 Query Language: https://www.w3.org/TR/sparql11-query/
- RDF Primer: https://www.w3.org/TR/rdf11-primer/
- PROV-O: https://www.w3.org/TR/prov-o/
