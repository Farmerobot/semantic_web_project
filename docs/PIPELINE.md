# Persuasion-Aware MUSE Pipeline
## LLM Annotation and RDF Generation

This document describes the pseudocode pipeline for annotating social media posts with persuasion techniques and generating structured RDF knowledge graphs.

---

## Overview

```
Input: Social media posts (JSON)
Process: LLM-based persuasion detection + Entity linking + Evidence retrieval
Output: RDF triples (Turtle/RDF-XML) for semantic querying
```

---

## Pipeline Architecture

```
┌─────────────────┐
│  Input Posts    │
│  (data/input)   │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│  Stage 1: Claim Extraction              │
│  - Parse post text                      │
│  - Identify factual claims              │
│  - Extract text fragments               │
└────────┬────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│  Stage 2: Persuasion Detection          │
│  - Classify persuasion techniques       │
│  - Identify loaded language             │
│  - Detect emotional triggers            │
└────────┬────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│  Stage 3: Entity Recognition & Linking  │
│  - Extract named entities               │
│  - Link to Wikidata IDs                 │
│  - Map entity relationships             │
└────────┬────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│  Stage 4: Fact-Checking                 │
│  - Query knowledge bases                │
│  - Retrieve evidence                    │
│  - Assign verification status           │
└────────┬────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│  Stage 5: RDF Triple Generation         │
│  - Create structured annotations        │
│  - Link to ontology classes             │
│  - Add provenance metadata              │
└────────┬────────────────────────────────┘
         │
         ▼
┌─────────────────┐
│  Output RDF     │
│  (data/output)  │
└─────────────────┘
```

---

## Detailed Pseudocode

### Stage 1: Claim Extraction

```pseudocode
FUNCTION extract_claims(post):
    INPUT: post = {post_id, text, author, timestamp, platform}
    OUTPUT: claims = List[Claim]
    
    // Initialize LLM with prompt
    prompt = """
    Analyze the following social media post and extract all factual claims.
    For each claim, identify:
    - The exact text fragment containing the claim
    - Start and end positions in the original text
    - A brief description of the claim
    
    Post: {post.text}
    
    Return as JSON:
    {
      "claims": [
        {
          "claim_id": "claim_1",
          "text": "extracted claim text",
          "fragment_start": int,
          "fragment_end": int,
          "description": "brief description"
        }
      ]
    }
    """
    
    // Call LLM API
    response = call_llm_api(prompt, model="gpt-4", temperature=0.2)
    claims = parse_json(response)
    
    // Create claim objects
    FOR EACH claim_data IN claims:
        claim = Claim(
            id = generate_claim_id(post.post_id, claim_data.claim_id),
            text = claim_data.text,
            fragment_start = claim_data.fragment_start,
            fragment_end = claim_data.fragment_end,
            source_post = post.post_id
        )
        ADD claim TO claims_list
    
    RETURN claims_list
END FUNCTION
```

### Stage 2: Persuasion Technique Detection

```pseudocode
FUNCTION detect_persuasion(claim, post):
    INPUT: claim = Claim object, post = Post object
    OUTPUT: techniques = List[PersuasionAnnotation]
    
    // Define persuasion taxonomy
    persuasion_taxonomy = {
        "FearAppeal": "Using fear to influence behavior",
        "LoadedLanguage": "Emotionally charged words",
        "AppealToAuthority": "Citing authority without evidence",
        "Scapegoating": "Blaming a group unfairly",
        "FlagWaving": "Appeal to nationalism",
        "Exaggeration": "Overstating facts",
        "AppealToEmotion": "Bypassing logic with emotion",
        "CausalOversimplification": "Simple cause for complex issue",
        "StrawMan": "Misrepresenting an argument",
        "RedHerring": "Introducing irrelevant material"
    }
    
    // Create detection prompt
    prompt = """
    Analyze this claim for persuasion techniques.
    
    Claim: {claim.text}
    Full Post: {post.text}
    
    Available techniques:
    {format_taxonomy(persuasion_taxonomy)}
    
    For each technique detected:
    1. Identify the technique type
    2. Provide confidence score (0-1)
    3. Explain why it applies
    4. Identify emotions invoked
    5. List specific loaded words/phrases
    
    Return as JSON:
    {
      "techniques": [
        {
          "type": "FearAppeal",
          "confidence": 0.92,
          "explanation": "Uses threatening language about safety",
          "emotions": ["Fear", "Anxiety"],
          "loaded_phrases": ["NEVER be safe", "destroying our way"]
        }
      ]
    }
    """
    
    response = call_llm_api(prompt, model="gpt-4", temperature=0.1)
    techniques_data = parse_json(response)
    
    techniques_list = []
    FOR EACH tech IN techniques_data.techniques:
        IF tech.confidence >= 0.6:  // Confidence threshold
            technique_annotation = PersuasionAnnotation(
                technique_type = tech.type,
                confidence = tech.confidence,
                explanation = tech.explanation,
                emotions = tech.emotions,
                loaded_phrases = tech.loaded_phrases,
                claim_id = claim.id
            )
            ADD technique_annotation TO techniques_list
    
    RETURN techniques_list
END FUNCTION
```

### Stage 3: Entity Recognition and Linking

```pseudocode
FUNCTION extract_and_link_entities(claim, post):
    INPUT: claim, post
    OUTPUT: entities = List[Entity]
    
    // Named Entity Recognition
    prompt = """
    Extract all named entities from this claim and post.
    Identify: persons, organizations, locations, events.
    
    Claim: {claim.text}
    Context: {post.text}
    
    Return as JSON:
    {
      "entities": [
        {
          "text": "European Union",
          "type": "Organization",
          "role": "target"  // target, source, or mentioned
        }
      ]
    }
    """
    
    ner_response = call_llm_api(prompt, model="gpt-4")
    entities_data = parse_json(ner_response)
    
    entities_list = []
    FOR EACH entity_data IN entities_data.entities:
        // Wikidata linking
        wikidata_id = query_wikidata(entity_data.text, entity_data.type)
        
        entity = Entity(
            name = entity_data.text,
            type = entity_data.type,
            role = entity_data.role,
            wikidata_id = wikidata_id,
            claim_id = claim.id
        )
        ADD entity TO entities_list
    
    RETURN entities_list
END FUNCTION


FUNCTION query_wikidata(entity_name, entity_type):
    // SPARQL query to Wikidata endpoint
    sparql_query = """
    SELECT ?item ?itemLabel WHERE {
      ?item rdfs:label "{entity_name}"@en .
      ?item wdt:P31 ?type .
      FILTER(CONTAINS(?type, "{entity_type}"))
      SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
    }
    LIMIT 1
    """
    
    result = execute_sparql(WIKIDATA_ENDPOINT, sparql_query)
    
    IF result IS NOT EMPTY:
        wikidata_id = extract_id_from_uri(result[0].item)
        RETURN wikidata_id
    ELSE:
        RETURN null
END FUNCTION
```

### Stage 4: Fact-Checking and Evidence Retrieval

```pseudocode
FUNCTION verify_claim(claim):
    INPUT: claim = Claim object
    OUTPUT: verification = VerificationResult
    
    // Search for evidence
    search_query = construct_search_query(claim.text)
    search_results = web_search(search_query, num_results=10)
    
    // Filter for reliable sources
    reliable_sources = filter_by_reliability(search_results)
    
    // LLM-based verification
    prompt = """
    Verify this claim using the provided evidence sources.
    
    Claim: {claim.text}
    
    Evidence sources:
    {format_sources(reliable_sources)}
    
    Determine:
    1. Verification status: True, False, Mostly True, Mostly False, Misleading, Unverified
    2. Supporting evidence (with URLs)
    3. Refuting evidence (with URLs)
    4. Explanation of verdict
    5. Confidence score
    
    Return as JSON:
    {
      "status": "False",
      "confidence": 0.88,
      "explanation": "The claim is factually incorrect because...",
      "supporting_evidence": [],
      "refuting_evidence": [
        {
          "text": "According to the EU official report...",
          "source_url": "https://example.com/report"
        }
      ]
    }
    """
    
    response = call_llm_api(prompt, model="gpt-4")
    verification_data = parse_json(response)
    
    verification = VerificationResult(
        claim_id = claim.id,
        status = verification_data.status,
        confidence = verification_data.confidence,
        explanation = verification_data.explanation,
        supporting_evidence = verification_data.supporting_evidence,
        refuting_evidence = verification_data.refuting_evidence,
        timestamp = current_timestamp()
    )
    
    RETURN verification
END FUNCTION


FUNCTION filter_by_reliability(search_results):
    // Whitelist of trusted sources
    trusted_domains = [
        "who.int", "cdc.gov", "nih.gov",
        "reuters.com", "apnews.com", "bbc.com",
        "nature.com", "sciencedirect.com",
        "gov", "edu"
    ]
    
    reliable_results = []
    FOR EACH result IN search_results:
        domain = extract_domain(result.url)
        IF any_match(domain, trusted_domains):
            ADD result TO reliable_results
    
    RETURN reliable_results
END FUNCTION
```

### Stage 5: RDF Triple Generation

```pseudocode
FUNCTION generate_rdf_triples(post, claims, techniques, entities, verifications):
    INPUT: All annotation data
    OUTPUT: rdf_graph = RDF Graph
    
    // Initialize RDF graph
    graph = RDFGraph()
    graph.bind("persuasion", "http://example.org/persuasion#")
    graph.bind("wd", "http://www.wikidata.org/entity/")
    graph.bind("prov", "http://www.w3.org/ns/prov#")
    
    // Generate post node
    post_uri = URIRef(f"http://example.org/post#{post.post_id}")
    graph.add((post_uri, RDF.type, persuasion.Post))
    graph.add((post_uri, persuasion.postId, Literal(post.post_id)))
    graph.add((post_uri, persuasion.textContent, Literal(post.text)))
    graph.add((post_uri, persuasion.author, Literal(post.author)))
    graph.add((post_uri, persuasion.platform, Literal(post.platform)))
    graph.add((post_uri, persuasion.timestamp, Literal(post.timestamp, datatype=XSD.dateTime)))
    
    // Generate claim nodes
    FOR EACH claim IN claims:
        claim_uri = URIRef(f"http://example.org/claim#{claim.id}")
        graph.add((claim_uri, RDF.type, persuasion.Claim))
        graph.add((claim_uri, persuasion.claimText, Literal(claim.text)))
        graph.add((claim_uri, persuasion.fragmentStart, Literal(claim.fragment_start, datatype=XSD.integer)))
        graph.add((claim_uri, persuasion.fragmentEnd, Literal(claim.fragment_end, datatype=XSD.integer)))
        
        // Link claim to post
        graph.add((post_uri, persuasion.containsClaim, claim_uri))
        
        // Add persuasion techniques
        techniques_for_claim = filter(techniques, lambda t: t.claim_id == claim.id)
        FOR EACH technique IN techniques_for_claim:
            technique_uri = URIRef(f"http://example.org/persuasion#{technique.technique_type}")
            graph.add((claim_uri, persuasion.usesTechnique, technique_uri))
            graph.add((claim_uri, persuasion.confidenceScore, Literal(technique.confidence, datatype=XSD.float)))
            
            // Add emotions
            FOR EACH emotion IN technique.emotions:
                emotion_uri = URIRef(f"http://example.org/persuasion#{emotion}")
                graph.add((technique_uri, persuasion.invokesEmotion, emotion_uri))
        
        // Add entities
        entities_for_claim = filter(entities, lambda e: e.claim_id == claim.id)
        FOR EACH entity IN entities_for_claim:
            entity_uri = URIRef(f"http://example.org/entity#{sanitize(entity.name)}")
            graph.add((entity_uri, RDF.type, persuasion.Entity))
            graph.add((entity_uri, persuasion.entityName, Literal(entity.name)))
            
            IF entity.wikidata_id IS NOT NULL:
                wikidata_uri = URIRef(f"http://www.wikidata.org/entity/{entity.wikidata_id}")
                graph.add((entity_uri, persuasion.linkedToWikidata, wikidata_uri))
            
            graph.add((claim_uri, persuasion.targetsEntity, entity_uri))
        
        // Add verification
        verification = get_verification_for_claim(verifications, claim.id)
        IF verification IS NOT NULL:
            status_uri = URIRef(f"http://example.org/persuasion#{verification.status}")
            graph.add((claim_uri, persuasion.hasVerificationStatus, status_uri))
            
            // Add evidence
            FOR EACH evidence IN verification.refuting_evidence:
                evidence_uri = URIRef(f"http://example.org/evidence#{generate_id()}")
                graph.add((evidence_uri, RDF.type, persuasion.Evidence))
                graph.add((evidence_uri, persuasion.evidenceText, Literal(evidence.text)))
                graph.add((evidence_uri, persuasion.evidenceSource, Literal(evidence.source_url, datatype=XSD.anyURI)))
                graph.add((claim_uri, persuasion.refutedBy, evidence_uri))
    
    // Add provenance
    agent_uri = URIRef("http://example.org/agent#MUSE_LLM_Run_1")
    graph.add((agent_uri, RDF.type, persuasion.LLMAgent))
    graph.add((agent_uri, persuasion.modelName, Literal("gpt-4")))
    graph.add((agent_uri, persuasion.modelVersion, Literal("2024-11-01")))
    graph.add((post_uri, persuasion.wasGeneratedBy, agent_uri))
    
    RETURN graph
END FUNCTION


FUNCTION serialize_rdf(graph, format="turtle"):
    // Serialize to file
    output_file = f"data/output/annotated_posts.{format}"
    
    IF format == "turtle":
        serialized = graph.serialize(format="turtle")
    ELSE IF format == "xml":
        serialized = graph.serialize(format="xml")
    ELSE IF format == "json-ld":
        serialized = graph.serialize(format="json-ld")
    
    write_file(output_file, serialized)
    RETURN output_file
END FUNCTION
```

---

## Main Orchestration Pipeline

```pseudocode
FUNCTION main_pipeline():
    // Configuration
    CONFIG = {
        "input_file": "data/input/processed/falcon_processed.json",
        "output_dir": "data/output",
        "ontology_file": "persuasion_ontology.ttl",
        "llm_model": "gpt-4",
        "confidence_threshold": 0.6,
        "batch_size": 5
    }
    
    // Load ontology
    ontology = load_ontology(CONFIG.ontology_file)
    
    // Load input posts
    posts = load_json(CONFIG.input_file)
    
    // Initialize RDF graph
    master_graph = RDFGraph()
    
    // Process posts in batches
    FOR EACH batch IN chunk(posts, CONFIG.batch_size):
        FOR EACH post IN batch:
            LOG(f"Processing post: {post.post_id}")
            
            // Stage 1: Extract claims
            claims = extract_claims(post)
            LOG(f"  Extracted {len(claims)} claims")
            
            // Stage 2: Detect persuasion techniques
            all_techniques = []
            FOR EACH claim IN claims:
                techniques = detect_persuasion(claim, post)
                all_techniques.extend(techniques)
            LOG(f"  Detected {len(all_techniques)} persuasion techniques")
            
            // Stage 3: Extract and link entities
            all_entities = []
            FOR EACH claim IN claims:
                entities = extract_and_link_entities(claim, post)
                all_entities.extend(entities)
            LOG(f"  Linked {len(all_entities)} entities")
            
            // Stage 4: Verify claims
            verifications = []
            FOR EACH claim IN claims:
                verification = verify_claim(claim)
                verifications.append(verification)
            LOG(f"  Verified {len(verifications)} claims")
            
            // Stage 5: Generate RDF triples
            post_graph = generate_rdf_triples(
                post, claims, all_techniques, all_entities, verifications
            )
            
            // Merge into master graph
            master_graph += post_graph
            
            LOG(f"  Generated {len(post_graph)} RDF triples")
    
    // Serialize output
    output_file_turtle = serialize_rdf(master_graph, format="turtle")
    output_file_json = serialize_rdf(master_graph, format="json-ld")
    
    LOG(f"Pipeline complete!")
    LOG(f"  Turtle output: {output_file_turtle}")
    LOG(f"  JSON-LD output: {output_file_json}")
    LOG(f"  Total triples: {len(master_graph)}")
    
    // Generate summary statistics
    generate_statistics(master_graph)
    
    RETURN master_graph
END FUNCTION


FUNCTION generate_statistics(graph):
    stats = {
        "total_posts": count_instances(graph, persuasion.Post),
        "total_claims": count_instances(graph, persuasion.Claim),
        "techniques_by_type": count_techniques_by_type(graph),
        "verification_status_distribution": count_verification_statuses(graph),
        "most_targeted_entities": get_most_targeted_entities(graph, top_n=10)
    }
    
    // Save statistics
    write_json("data/output/statistics.json", stats)
    LOG("Statistics saved to data/output/statistics.json")
    
    RETURN stats
END FUNCTION
```

---

## Example Execution

```pseudocode
// Run the pipeline
IF __name__ == "__main__":
    TRY:
        graph = main_pipeline()
        
        // Optional: Load into triple store
        triplestore_endpoint = "http://localhost:7200/repositories/persuasion"
        upload_to_triplestore(graph, triplestore_endpoint)
        
        LOG("Data successfully loaded into triple store")
        LOG("SPARQL endpoint available at: {triplestore_endpoint}")
        
    CATCH Exception AS e:
        LOG_ERROR(f"Pipeline failed: {e}")
        RAISE e
END
```

---

## Output Example

For the post:
```
"BREAKING: The EU is forcing member states to accept unlimited migrants! 
Your neighborhoods will NEVER be safe again. They're destroying our way of life!"
```

Generated RDF triples:
```turtle
:Post_001 rdf:type :Post ;
    :textContent "BREAKING: The EU is forcing..." ;
    :containsClaim :Claim_001_1 .

:Claim_001_1 rdf:type :Claim ;
    :claimText "The EU is forcing member states to accept unlimited migrants" ;
    :usesTechnique :FearAppeal ;
    :usesTechnique :LoadedLanguage ;
    :targetsEntity wd:Q458 ;  # European Union
    :invokesEmotion :Fear ;
    :invokesEmotion :Anxiety ;
    :hasVerificationStatus :False ;
    :refutedBy :Evidence_789 ;
    :confidenceScore 0.92 .

:FearAppeal :invokesEmotion :Fear .

:Evidence_789 rdf:type :Evidence ;
    :evidenceText "EU migration policy requires unanimous consent..." ;
    :evidenceSource <https://ec.europa.eu/home-affairs/policy/migration> .

:Post_001 prov:wasGeneratedBy :MUSE_LLM_Run_1 .
```

---

## Implementation Notes

### LLM Configuration
- **Model**: GPT-4 or equivalent (Claude, Gemini)
- **Temperature**: 0.1-0.2 for consistent classification
- **Max tokens**: 2000-4000 per request
- **Retry logic**: Implement exponential backoff for API failures

### Performance Optimization
- **Batch processing**: Process 5-10 posts at a time
- **Caching**: Cache Wikidata lookups
- **Parallel processing**: Use async calls for independent operations
- **Rate limiting**: Respect LLM API rate limits (e.g., 10 req/min)

### Quality Assurance
- **Confidence thresholds**: Only include annotations with confidence >= 0.6
- **Human validation**: Sample 10% of results for manual review
- **Inter-annotator agreement**: Compare multiple LLM runs
- **Ontology validation**: Use OWL reasoner to check consistency

### Error Handling
- **Missing entities**: Create entity node without Wikidata ID
- **Verification failures**: Mark as "Unverified"
- **LLM timeout**: Retry with reduced context window
- **Invalid JSON**: Log error and skip to next claim

---

## Next Steps

1. **Implementation**: Convert pseudocode to Python using `rdflib`, `openai`, `requests`
2. **Evaluation**: Run on test dataset and measure precision/recall
3. **Deployment**: Set up GraphDB/Fuseki triple store
4. **Querying**: Create SPARQL queries for common analysis tasks
5. **Visualization**: Build dashboard for exploring results

---

## Dependencies

```
Python 3.10+
rdflib==7.0.0
openai==1.3.0
requests==2.31.0
spacy==3.7.0
beautifulsoup4==4.12.0
numpy==1.24.0
```

---

## References

- Zhou et al., "Correcting Misinformation on Social Media with a Large Language Model (MUSE)", 2024
- Da San Martino et al., "Fine-grained Propaganda Detection in News Articles", ACL 2019
- Idziejczak et al., "Among Them: A Game-Based Framework for Assessing Persuasion Capabilities of LLMs", 2025
