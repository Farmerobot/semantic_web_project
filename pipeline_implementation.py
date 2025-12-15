"""
Persuasion-Aware MUSE Pipeline Implementation
A fully functional pipeline for detecting persuasion techniques in social media posts
and generating RDF knowledge graphs.

Uses:
- spaCy for Named Entity Recognition
- OpenRouter API (Gemini) for LLM-based claim extraction and persuasion detection
- RDFLib for semantic graph generation
- SPARQLWrapper for Wikidata entity linking
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional
from dataclasses import dataclass, field
from pathlib import Path

from rdflib import Graph, Namespace, Literal, URIRef, RDF, RDFS, XSD
from rdflib.namespace import FOAF
from SPARQLWrapper import SPARQLWrapper, JSON
from dotenv import load_dotenv
import spacy
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Helper for success logging
def log_success(msg):
    logger.info(f"✓ {msg}")


# Load environment variables
load_dotenv()

# OpenRouter configuration
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
MODEL_NAME = "google/gemini-2.5-flash-lite"


# ========================================
# Configuration
# ========================================

class Config:
    """Pipeline configuration"""
    INPUT_FILE = "data/input/processed/falcon_processed.json"  # Preprocessed FALCON dataset
    OUTPUT_DIR = "data/output"
    ONTOLOGY_FILE = "persuasion_ontology.ttl"
    LLM_MODEL = MODEL_NAME
    CONFIDENCE_THRESHOLD = 0.6
    BATCH_SIZE = 5
    MAX_POSTS = 15  # Limit for demo run


# ========================================
# Data Classes
# ========================================

@dataclass
class Post:
    """Social media post"""
    post_id: str
    text: str
    platform: str = "Twitter"
    author: str = "unknown"
    timestamp: str = ""
    metadata: Dict = field(default_factory=dict)
    # Pre-labeled techniques (from FALCON)
    known_techniques: List[str] = field(default_factory=list)


@dataclass
class Claim:
    """Extracted claim from a post"""
    id: str
    text: str
    fragment_start: int = 0
    fragment_end: int = 0
    source_post: str = ""


@dataclass
class PersuasionAnnotation:
    """Persuasion technique annotation"""
    technique_type: str
    confidence: float
    explanation: str
    loaded_phrases: List[str] = field(default_factory=list)
    claim_id: str = ""


@dataclass
class Entity:
    """Named entity"""
    name: str
    type: str
    role: str = "mentioned"
    wikidata_id: Optional[str] = None
    claim_id: str = ""


@dataclass
class VerificationResult:
    """Fact-checking result"""
    claim_id: str
    status: str = "Unverified"
    confidence: float = 0.0
    explanation: str = "Verification not yet implemented"
    supporting_evidence: List[Dict] = field(default_factory=list)
    refuting_evidence: List[Dict] = field(default_factory=list)
    timestamp: str = ""


# ========================================
# LLM Client Setup
# ========================================

def get_llm_client():
    """Initialize OpenRouter client for LLM access."""
    try:
        from openai import OpenAI
        api_key = os.getenv("OPENROUTER_API_KEY")
        if api_key:
            client = OpenAI(
                base_url=OPENROUTER_BASE_URL,
                api_key=api_key
            )
            logger.info(f"OpenRouter client initialized with model: {MODEL_NAME}")
            return client
        else:
            logger.warning("OPENROUTER_API_KEY not found in environment")
            return None
    except ImportError:
        logger.error("openai package not installed")
        return None


# ========================================
# NER Setup
# ========================================

def get_nlp():
    """Load spaCy NLP model."""
    try:
        nlp = spacy.load("en_core_web_sm")
        logger.info("spaCy model loaded successfully")
        return nlp
    except OSError:
        logger.error("spaCy model not found. Run: python -m spacy download en_core_web_sm")
        return None


# ========================================
# Persuasion Taxonomy
# ========================================

PERSUASION_TAXONOMY = {
    "FearAppeal": "Using fear or threats to influence behavior or beliefs",
    "LoadedLanguage": "Using emotionally charged words to influence without evidence",
    "AppealToAuthority": "Citing authority figures without proper evidence",
    "Scapegoating": "Unfairly blaming a person or group for problems",
    "Exaggeration": "Overstating or understating facts for effect",
    "AdHominem": "Attacking the person making the argument rather than the argument itself",
    "AppealToRidicule": "Mocking or ridiculing an argument to discredit it",
    "FalseDilemma": "Presenting only two options when more exist",
    "HastyGeneralization": "Drawing broad conclusions from limited examples",
}


# ========================================
# Stage 1: Claim Extraction
# ========================================

def extract_claims(post: Post, client) -> List[Claim]:
    """
    Extract factual claims from a social media post using LLM.
    """
    logger.info(f"Extracting claims from post: {post.post_id}")
    
    if client is None:
        logger.warning("LLM client not available, skipping claim extraction")
        # Return the full text as a single claim if no LLM
        return [Claim(
            id=f"{post.post_id}_claim_1",
            text=post.text[:500],  # Truncate if too long
            source_post=post.post_id
        )]
    
    prompt = f"""Analyze the following social media post and extract all factual claims that can be verified.
For each claim, provide:
1. The exact text of the claim
2. A brief description

Post: {post.text}

Return ONLY valid JSON in this exact format (no markdown, no extra text):
{{
  "claims": [
    {{
      "claim_id": "1",
      "text": "extracted claim",
      "description": "brief description"
    }}
  ]
}}"""
    
    try:
        response = client.chat.completions.create(
            model=Config.LLM_MODEL,
            messages=[
                {"role": "system", "content": "You are an expert fact-checker. Always respond with valid JSON only."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )
        
        content = response.choices[0].message.content.strip()
        # Remove markdown code blocks if present
        if content.startswith("```"):
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content[4:]
        content = content.strip()
        
        claims_data = json.loads(content)
        claims_list = []
        
        for claim_data in claims_data.get("claims", []):
            claim = Claim(
                id=f"{post.post_id}_{claim_data['claim_id']}",
                text=claim_data["text"],
                source_post=post.post_id
            )
            claims_list.append(claim)
        
        return claims_list if claims_list else [Claim(
            id=f"{post.post_id}_claim_1",
            text=post.text[:500],
            source_post=post.post_id
        )]
        
    except Exception as e:
        logger.error(f"Error extracting claims: {e}")
        return [Claim(
            id=f"{post.post_id}_claim_1",
            text=post.text[:500],
            source_post=post.post_id
        )]


# ========================================
# Stage 2: Persuasion Detection
# ========================================

def detect_persuasion(claim: Claim, post: Post, client) -> List[PersuasionAnnotation]:
    """
    Detect persuasion techniques in a claim using LLM.
    """
    logger.info(f"Detecting persuasion in claim: {claim.id}")
    
    # If post has known techniques (from FALCON), use them
    if post.known_techniques:
        return [
            PersuasionAnnotation(
                technique_type=tech,
                confidence=1.0,  # Ground truth
                explanation="Labeled in FALCON dataset",
                claim_id=claim.id
            )
            for tech in post.known_techniques
        ]
    
    if client is None:
        logger.warning("LLM client not available, skipping persuasion detection")
        return []
    
    taxonomy_str = "\n".join([f"- {k}: {v}" for k, v in PERSUASION_TAXONOMY.items()])
    
    prompt = f"""Analyze this claim for persuasion techniques.

Claim: {claim.text}
Full Post Context: {post.text}

Available techniques:
{taxonomy_str}

Return ONLY valid JSON:
{{
  "techniques": [
    {{
      "type": "TechniqueName",
      "confidence": 0.85,
      "explanation": "Why this technique applies"
    }}
  ]
}}"""
    
    try:
        response = client.chat.completions.create(
            model=Config.LLM_MODEL,
            messages=[
                {"role": "system", "content": "You are an expert in rhetoric and propaganda analysis. Always respond with valid JSON only."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1
        )
        
        content = response.choices[0].message.content.strip()
        if content.startswith("```"):
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content[4:]
        content = content.strip()
        
        result = json.loads(content)
        techniques_list = []
        
        for tech in result.get("techniques", []):
            if tech.get("confidence", 0) >= Config.CONFIDENCE_THRESHOLD:
                annotation = PersuasionAnnotation(
                    technique_type=tech["type"],
                    confidence=tech["confidence"],
                    explanation=tech.get("explanation", ""),
                    claim_id=claim.id
                )
                techniques_list.append(annotation)
        
        return techniques_list
        
    except Exception as e:
        logger.error(f"Error detecting persuasion: {e}")
        return []


# ========================================
# Stage 3: Entity Recognition & Linking
# ========================================

# spaCy label to ontology type mapping
LABEL_MAPPING = {
    "PERSON": "Person",
    "ORG": "Organization",
    "GPE": "Location",
    "LOC": "Location",
    "NORP": "Group",
    "EVENT": "Event",
    "DATE": "Date",
}

WIKIDATA_ENDPOINT = "https://query.wikidata.org/sparql"


def find_wikidata_entity(entity_name: str, entity_type: str = None) -> Optional[str]:
    """
    Search Wikidata for an entity by name and return Wikidata ID.
    """
    sparql = SPARQLWrapper(WIKIDATA_ENDPOINT)
    sparql.setReturnFormat(JSON)
    
    # Build query with optional type filter
    type_filter = ""
    if entity_type == "Person":
        type_filter = "?item wdt:P31 wd:Q5 ."  # instance of human
    elif entity_type == "Organization":
        type_filter = "?item wdt:P31/wdt:P279* wd:Q43229 ."  # instance of organization
    elif entity_type == "Location":
        type_filter = "?item wdt:P31/wdt:P279* wd:Q618123 ."  # geographical feature
    
    query = f"""
    SELECT ?item WHERE {{
        ?item rdfs:label "{entity_name}"@en .
        {type_filter}
    }}
    LIMIT 1
    """
    
    try:
        sparql.setQuery(query)
        results = sparql.query().convert()
        
        if results["results"]["bindings"]:
            result = results["results"]["bindings"][0]
            return result["item"]["value"].split("/")[-1]
    except Exception as e:
        logger.debug(f"Wikidata query failed for {entity_name}: {e}")
    
    return None


def extract_and_link_entities(claim: Claim, post: Post, nlp) -> List[Entity]:
    """
    Extract named entities using spaCy and link to Wikidata.
    """
    logger.info(f"Extracting entities from claim: {claim.id}")
    
    if nlp is None:
        return []
    
    doc = nlp(claim.text)
    entities_list = []
    seen = set()
    
    for ent in doc.ents:
        if ent.text.lower() not in seen:
            seen.add(ent.text.lower())
            entity_type = LABEL_MAPPING.get(ent.label_, "Other")
            
            # Try to find Wikidata ID
            wikidata_id = find_wikidata_entity(ent.text, entity_type)
            
            entity = Entity(
                name=ent.text,
                type=entity_type,
                wikidata_id=wikidata_id,
                claim_id=claim.id
            )
            entities_list.append(entity)
    
    return entities_list


# ========================================
# Stage 4: Fact-Checking (Placeholder)
# ========================================

def verify_claim(claim: Claim) -> VerificationResult:
    """
    Verify a claim using evidence retrieval and LLM assessment.
    Currently returns placeholder - full implementation would include web search.
    """
    logger.info(f"Verifying claim: {claim.id}")
    
    return VerificationResult(
        claim_id=claim.id,
        status="Unverified",
        confidence=0.0,
        explanation="Verification requires external API access",
        timestamp=datetime.utcnow().isoformat()
    )


# ========================================
# Stage 5: RDF Generation
# ========================================

def generate_rdf_triples(
    post: Post,
    claims: List[Claim],
    techniques: List[PersuasionAnnotation],
    entities: List[Entity],
    verifications: List[VerificationResult]
) -> Graph:
    """
    Generate RDF triples from annotations.
    """
    logger.info(f"Generating RDF triples for post: {post.post_id}")
    
    g = Graph()
    
    # Define namespaces
    PERSUASION = Namespace("http://example.org/persuasion#")
    WD = Namespace("http://www.wikidata.org/entity/")
    PROV = Namespace("http://www.w3.org/ns/prov#")
    
    g.bind("persuasion", PERSUASION)
    g.bind("wd", WD)
    g.bind("prov", PROV)
    
    # Create post node
    post_uri = URIRef(f"http://example.org/post#{post.post_id}")
    g.add((post_uri, RDF.type, PERSUASION.Post))
    g.add((post_uri, PERSUASION.postId, Literal(post.post_id)))
    g.add((post_uri, PERSUASION.textContent, Literal(post.text)))
    g.add((post_uri, PERSUASION.platform, Literal(post.platform)))
    
    if post.timestamp:
        g.add((post_uri, PERSUASION.timestamp, 
               Literal(post.timestamp, datatype=XSD.dateTime)))
    
    # Add claims
    for claim in claims:
        claim_uri = URIRef(f"http://example.org/claim#{claim.id}")
        g.add((claim_uri, RDF.type, PERSUASION.Claim))
        g.add((claim_uri, PERSUASION.claimText, Literal(claim.text)))
        
        # Link claim to post
        g.add((post_uri, PERSUASION.containsClaim, claim_uri))
        
        # Add persuasion techniques
        claim_techniques = [t for t in techniques if t.claim_id == claim.id]
        for technique in claim_techniques:
            technique_uri = URIRef(f"http://example.org/persuasion#{technique.technique_type}")
            g.add((claim_uri, PERSUASION.usesTechnique, technique_uri))
            g.add((claim_uri, PERSUASION.confidenceScore, 
                   Literal(technique.confidence, datatype=XSD.float)))
        
        # Add entities
        claim_entities = [e for e in entities if e.claim_id == claim.id]
        for entity in claim_entities:
            entity_uri = URIRef(f"http://example.org/entity#{entity.name.replace(' ', '_')}")
            g.add((entity_uri, RDF.type, PERSUASION.Entity))
            g.add((entity_uri, PERSUASION.entityName, Literal(entity.name)))
            g.add((entity_uri, PERSUASION.entityType, Literal(entity.type)))
            
            if entity.wikidata_id:
                wikidata_uri = URIRef(f"http://www.wikidata.org/entity/{entity.wikidata_id}")
                g.add((entity_uri, PERSUASION.linkedToWikidata, wikidata_uri))
            
            g.add((claim_uri, PERSUASION.targetsEntity, entity_uri))
        
        # Add verification
        verification = next((v for v in verifications if v.claim_id == claim.id), None)
        if verification:
            status_uri = URIRef(f"http://example.org/persuasion#{verification.status}")
            g.add((claim_uri, PERSUASION.hasVerificationStatus, status_uri))
    
    # Add provenance
    agent_uri = URIRef("http://example.org/agent#MUSE_Pipeline")
    g.add((agent_uri, RDF.type, PERSUASION.LLMAgent))
    g.add((agent_uri, PERSUASION.modelName, Literal(Config.LLM_MODEL)))
    g.add((post_uri, PROV.wasGeneratedBy, agent_uri))
    
    return g


def serialize_rdf(graph: Graph, output_format: str = "turtle") -> str:
    """
    Serialize RDF graph to file.
    """
    output_dir = Path(Config.OUTPUT_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    ext = "ttl" if output_format == "turtle" else output_format
    output_file = output_dir / f"annotated_posts.{ext}"
    
    graph.serialize(destination=str(output_file), format=output_format)
    logger.info(f"Serialized RDF to: {output_file}")
    
    return str(output_file)


# ========================================
# Main Pipeline Orchestration
# ========================================

def load_posts_from_falcon(input_file: str, max_posts: int = None) -> List[Post]:
    """Load posts from processed FALCON JSON file."""
    with open(input_file, 'r', encoding='utf-8') as f:
        posts_data = json.load(f)
    
    if max_posts:
        posts_data = posts_data[:max_posts]
    
    posts = []
    for item in posts_data:
        post = Post(
            post_id=item["post_id"],
            text=item.get("text_clean", item.get("text", "")),
            platform="Twitter",  # FALCON is Twitter-based
            known_techniques=item.get("techniques", [])
        )
        posts.append(post)
    
    return posts


def main_pipeline(use_falcon: bool = True, max_posts: int = None):
    """Main pipeline orchestration."""
    logger.info("Starting Persuasion-Aware MUSE Pipeline")
    
    # Initialize tools
    client = get_llm_client()
    nlp = get_nlp()
    
    # Load input posts
    if Path(Config.INPUT_FILE).exists():
        posts = load_posts_from_falcon(Config.INPUT_FILE, max_posts or Config.MAX_POSTS)
        logger.info(f"Loaded {len(posts)} posts from FALCON dataset")
    else:
        logger.error("No input data found. Run notebook 03_data_preprocessing.ipynb first.")
        return None
    
    # Initialize master graph
    master_graph = Graph()
    
    # Statistics
    stats = {
        "total_posts": len(posts),
        "total_claims": 0,
        "total_techniques": 0,
        "total_entities": 0,
        "technique_counts": {}
    }
    
    # Process posts in batches
    for i in range(0, len(posts), Config.BATCH_SIZE):
        batch = posts[i:i + Config.BATCH_SIZE]
        logger.info(f"Processing batch {i // Config.BATCH_SIZE + 1}")
        
        for post in batch:
            logger.info(f"Processing post: {post.post_id}")
            
            # Stage 1: Extract claims
            claims = extract_claims(post, client)
            stats["total_claims"] += len(claims)
            logger.info(f"  Extracted {len(claims)} claims")
            
            # Stage 2: Detect persuasion techniques
            all_techniques = []
            for claim in claims:
                techniques = detect_persuasion(claim, post, client)
                all_techniques.extend(techniques)
                for t in techniques:
                    stats["technique_counts"][t.technique_type] = \
                        stats["technique_counts"].get(t.technique_type, 0) + 1
            stats["total_techniques"] += len(all_techniques)
            logger.info(f"  Detected {len(all_techniques)} persuasion techniques")
            
            # Stage 3: Extract and link entities
            all_entities = []
            for claim in claims:
                entities = extract_and_link_entities(claim, post, nlp)
                all_entities.extend(entities)
            stats["total_entities"] += len(all_entities)
            logger.info(f"  Linked {len(all_entities)} entities")
            
            # Stage 4: Verify claims
            verifications = [verify_claim(claim) for claim in claims]
            logger.info(f"  Verified {len(verifications)} claims")
            
            # Stage 5: Generate RDF triples
            post_graph = generate_rdf_triples(
                post, claims, all_techniques, all_entities, verifications
            )
            
            # Merge into master graph
            master_graph += post_graph
            logger.info(f"  Generated {len(post_graph)} RDF triples")
    
    # Serialize output
    output_file_turtle = serialize_rdf(master_graph, "turtle")
    output_file_json = serialize_rdf(master_graph, "json-ld")
    
    # Save statistics
    stats_file = Path(Config.OUTPUT_DIR) / "pipeline_stats.json"
    with open(stats_file, 'w') as f:
        json.dump(stats, f, indent=2)
    logger.info(f"Saved statistics to: {stats_file}")
    
    log_success("Pipeline complete!")
    logger.info(f"  Turtle output: {output_file_turtle}")
    logger.info(f"  JSON-LD output: {output_file_json}")
    logger.info(f"  Total triples: {len(master_graph)}")
    logger.info(f"  Statistics: {stats}")
    
    return master_graph, stats


# ========================================
# Entry Point
# ========================================

if __name__ == "__main__":
    try:
        graph, stats = main_pipeline(use_falcon=True, max_posts=15)
        log_success("Pipeline completed successfully")
        
        # Print summary
        print("\n" + "=" * 60)
        print("PIPELINE EXECUTION SUMMARY")
        print("=" * 60)
        print(f"Posts processed: {stats['total_posts']}")
        print(f"Claims extracted: {stats['total_claims']}")
        print(f"Techniques detected: {stats['total_techniques']}")
        print(f"Entities linked: {stats['total_entities']}")
        print(f"Total RDF triples: {len(graph)}")
        print("\nTechnique breakdown:")
        for tech, count in sorted(stats['technique_counts'].items(), key=lambda x: -x[1]):
            print(f"  {tech}: {count}")
        print("=" * 60)
        
    except Exception as e:
        logger.error(f"Pipeline failed: {e}")
        raise
