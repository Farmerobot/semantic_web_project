# 📊 Knowledge Graph Visualization

Quick guide to visualize your persuasion knowledge graph.

---

## 🚀 Quick Start (3 Steps)

### Option 1: Automated (Windows)
**Just double-click:** `run_visualization.bat`

That's it! It will:
1. Install dependencies
2. Generate the visualization
3. Open it in your browser

---

### Option 2: Manual

**Step 1: Install dependencies**
```bash
pip install pyvis rdflib
```

**Step 2: Run the script**
```bash
python visualize.py
```

**Step 3: View**
Opens automatically in your browser, or open `graph_visualization.html`

---

## 🎨 What You'll See

An **interactive HTML graph** showing:

- 🔴 **Red nodes** = Posts
- 🔵 **Teal nodes** = Claims
- 🟡 **Yellow nodes** = Persuasion Techniques
- 🟢 **Green nodes** = Entities (EU, China, etc.)
- 🟢 **Light green nodes** = Evidence sources
- 🩷 **Pink nodes** = Verification status

**Edges (arrows)** show relationships:
- `containsClaim` → Post contains this claim
- `usesTechnique` → Claim uses this persuasion method
- `targetsEntity` → Claim targets this entity
- `refutedBy` → Claim refuted by this evidence
- `hasVerificationStatus` → Claim verification status

---

## 💡 How to Use

**🖱️ Interact with the graph:**
- **Drag nodes** to rearrange
- **Scroll** to zoom in/out
- **Click nodes** to see details
- **Hover over edges** to see relationship types

**🎯 Explore patterns:**
- Follow arrows from Post → Claims → Techniques
- See which entities are targeted most
- Trace evidence back to claims
- Identify verification statuses

---

## 📁 What Gets Generated

**Output file:** `graph_visualization.html`
- Self-contained HTML file
- Works offline
- Share with others
- No server needed

---

## 🔧 Customization

Edit `visualize.py` to change:
- **Colors:** Modify the `COLORS` dictionary
- **Node sizes:** Edit `get_node_size()` function
- **Layout:** Adjust physics parameters in `net.set_options()`
- **Input file:** Change `INPUT_FILE` variable

---

## ❓ Troubleshooting

### "Module not found: pyvis"
```bash
pip install pyvis
```

### "Module not found: rdflib"
```bash
pip install rdflib
```

### "File not found: data/output/example_annotated.ttl"
Make sure you have the example RDF file. Run the pipeline first or create it manually.

### Graph looks messy
- Drag nodes to organize them
- Adjust physics settings in the script
- Reload the page to reset layout

---

## 📊 Example View

Your graph will show connections like:

```
Post_001
    ↓ containsClaim
Claim_001_1
    ↓ usesTechnique
FearAppeal
    
Claim_001_1
    ↓ targetsEntity
Entity_EU (Wikidata: Q458)

Claim_001_1
    ↓ hasVerificationStatus
False
    
Claim_001_1
    ↓ refutedBy
Evidence_001_1
```

---

## 🎓 Next Steps

1. ✅ Visualize the example data
2. 📝 Add your own posts to `data/input/posts.json`
3. 🔄 Run the annotation pipeline
4. 🔍 Visualize your new data
5. 📊 Analyze patterns in persuasion techniques

---

**Enjoy exploring your knowledge graph! 🎉**
