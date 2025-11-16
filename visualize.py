"""
Simple Knowledge Graph Visualizer
Run: python visualize.py
Opens an interactive HTML visualization in your browser
"""

from pyvis.network import Network
from rdflib import Graph, Namespace, RDF
import webbrowser
from pathlib import Path

# Configuration
INPUT_FILE = "data/output/example_annotated.ttl"
OUTPUT_FILE = "graph_visualization.html"

# Define namespaces
PERSUASION = Namespace("http://example.org/persuasion#")

# Node colors by type
COLORS = {
    "Post": "#FF6B6B",
    "Claim": "#4ECDC4",
    "FearAppeal": "#FFE66D",
    "LoadedLanguage": "#FFE66D",
    "Scapegoating": "#FFE66D",
    "AppealToAuthority": "#FFE66D",
    "Exaggeration": "#FFE66D",
    "Entity": "#95E1D3",
    "Evidence": "#A8E6CF",
    "False": "#FFB6C1",
    "Misleading": "#FFB6C1",
    "True": "#90EE90",
}

def clean_label(uri):
    """Extract clean label from URI"""
    label = str(uri).split('#')[-1].split('/')[-1]
    # Truncate long labels
    if len(label) > 30:
        label = label[:27] + "..."
    return label

def get_node_color(uri, rdf_graph):
    """Determine node color based on type"""
    # Check if it's a typed node
    for _, _, type_node in rdf_graph.triples((uri, RDF.type, None)):
        type_label = clean_label(type_node)
        if type_label in COLORS:
            return COLORS[type_label]
    
    # Fallback: check the label itself
    label = clean_label(uri)
    return COLORS.get(label, "#CCCCCC")

def get_node_size(uri, rdf_graph):
    """Determine node size based on type"""
    for _, _, type_node in rdf_graph.triples((uri, RDF.type, None)):
        type_label = clean_label(type_node)
        if type_label == "Post":
            return 30
        elif type_label == "Claim":
            return 25
        elif type_label in ["FearAppeal", "LoadedLanguage", "Scapegoating", "AppealToAuthority", "Exaggeration"]:
            return 20
    return 15

def create_visualization():
    """Main visualization function"""
    
    print("🔄 Loading RDF data...")
    
    # Load the RDF graph
    g = Graph()
    try:
        g.parse(INPUT_FILE, format="turtle")
        print(f"✅ Loaded {len(g)} triples from {INPUT_FILE}")
    except Exception as e:
        print(f"❌ Error loading file: {e}")
        print(f"Make sure {INPUT_FILE} exists!")
        return
    
    print("🎨 Creating interactive visualization...")
    
    # Create network
    net = Network(
        height="900px",
        width="100%",
        bgcolor="#f8f9fa",
        font_color="#2c3e50",
        directed=True,
        notebook=False
    )
    
    # Configure physics for better layout
    net.set_options("""
    {
        "physics": {
            "barnesHut": {
                "gravitationalConstant": -30000,
                "centralGravity": 0.3,
                "springLength": 200,
                "springConstant": 0.04
            },
            "minVelocity": 0.75
        },
        "edges": {
            "arrows": {
                "to": {
                    "enabled": true,
                    "scaleFactor": 0.5
                }
            },
            "smooth": {
                "type": "continuous"
            }
        }
    }
    """)
    
    # Track added nodes
    added_nodes = set()
    
    # Add nodes and edges
    for s, p, o in g:
        subject = clean_label(s)
        predicate = clean_label(p)
        obj = clean_label(o)
        
        # Skip literal values (text content)
        if not str(o).startswith("http"):
            continue
        
        # Add subject node
        if subject not in added_nodes:
            color = get_node_color(s, g)
            size = get_node_size(s, g)
            net.add_node(
                subject,
                label=subject,
                color=color,
                size=size,
                title=f"<b>{subject}</b><br>Click to highlight connections"
            )
            added_nodes.add(subject)
        
        # Add object node
        if obj not in added_nodes:
            color = get_node_color(o, g)
            size = get_node_size(o, g)
            net.add_node(
                obj,
                label=obj,
                color=color,
                size=size,
                title=f"<b>{obj}</b><br>Click to highlight connections"
            )
            added_nodes.add(obj)
        
        # Add edge with label for important predicates
        important_predicates = ['containsClaim', 'usesTechnique', 'targetsEntity', 'refutedBy', 'hasVerificationStatus']
        edge_label = predicate if predicate in important_predicates else ""
        
        net.add_edge(
            subject,
            obj,
            title=predicate,
            label=edge_label,
            color="#95a5a6" if not edge_label else "#34495e",
            width=2 if edge_label else 1
        )
    
    print(f"📊 Graph contains {len(added_nodes)} nodes and {len(g)} relationships")
    
    # Save the visualization
    net.save_graph(OUTPUT_FILE)
    
    # Add custom legend
    add_legend_to_html(OUTPUT_FILE)
    
    print(f"✅ Visualization saved to {OUTPUT_FILE}")
    
    # Open in browser
    print("🌐 Opening in browser...")
    file_path = Path(OUTPUT_FILE).absolute()
    webbrowser.open(f"file://{file_path}")
    print("\n✨ Done! Your knowledge graph is now visualized.")
    print("   You can drag nodes, zoom, and click on them to explore!")

def add_legend_to_html(html_file):
    """Add a legend to the HTML file"""
    
    legend_html = """
    <div style="position: fixed; top: 10px; right: 10px; background: white; 
                padding: 20px; border: 2px solid #ddd; border-radius: 10px; 
                font-family: 'Segoe UI', Arial, sans-serif; z-index: 1000;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1); max-width: 250px;">
        <h3 style="margin-top: 0; color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 8px;">
            📊 Legend
        </h3>
        <div style="margin: 8px 0;">
            <span style="display:inline-block; width:18px; height:18px; 
                 background:#FF6B6B; margin-right:8px; border-radius:3px;"></span>
            <b>Post</b> - Social media post
        </div>
        <div style="margin: 8px 0;">
            <span style="display:inline-block; width:18px; height:18px; 
                 background:#4ECDC4; margin-right:8px; border-radius:3px;"></span>
            <b>Claim</b> - Factual assertion
        </div>
        <div style="margin: 8px 0;">
            <span style="display:inline-block; width:18px; height:18px; 
                 background:#FFE66D; margin-right:8px; border-radius:3px;"></span>
            <b>Technique</b> - Persuasion method
        </div>
        <div style="margin: 8px 0;">
            <span style="display:inline-block; width:18px; height:18px; 
                 background:#95E1D3; margin-right:8px; border-radius:3px;"></span>
            <b>Entity</b> - Target/subject
        </div>
        <div style="margin: 8px 0;">
            <span style="display:inline-block; width:18px; height:18px; 
                 background:#A8E6CF; margin-right:8px; border-radius:3px;"></span>
            <b>Evidence</b> - Fact-check source
        </div>
        <div style="margin: 8px 0;">
            <span style="display:inline-block; width:18px; height:18px; 
                 background:#FFB6C1; margin-right:8px; border-radius:3px;"></span>
            <b>False/Misleading</b> - Verification
        </div>
        <hr style="margin: 12px 0; border: none; border-top: 1px solid #ddd;">
        <div style="font-size: 11px; color: #7f8c8d;">
            💡 <b>Tip:</b> Drag nodes to rearrange<br>
            🔍 Scroll to zoom<br>
            👆 Click nodes for details
        </div>
    </div>
    """
    
    # Read the HTML file
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Add legend before closing body tag
    html_content = html_content.replace('</body>', f'{legend_html}</body>')
    
    # Write back
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

if __name__ == "__main__":
    print("=" * 60)
    print("  PERSUASION KNOWLEDGE GRAPH VISUALIZER")
    print("=" * 60)
    print()
    
    create_visualization()
    
    print()
    print("=" * 60)
