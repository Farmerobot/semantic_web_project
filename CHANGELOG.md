# Changelog

## Version 2.0 (Simplified Ontology)

### 🎯 Major Changes

**Simplified to 5 Core Persuasion Techniques:**
1. **FearAppeal** - Using fear to influence behavior
2. **LoadedLanguage** - Emotionally charged words
3. **AppealToAuthority** - Citing authority without evidence
4. **Scapegoating** - Blaming a person or group unfairly
5. **Exaggeration** - Overstating or understating facts

### ❌ Removed

**Techniques Removed:**
- FlagWaving (Appeal to nationalism)
- AppealToEmotion (Bypassing logic with emotion)
- CausalOversimplification (Simple cause for complex issue)
- StrawMan (Misrepresenting arguments)
- RedHerring (Introducing irrelevant material)

**Emotion Tracking Removed:**
- Removed all Emotion classes (Fear, Anger, Disgust, Anxiety, Outrage, Pride, Hope)
- Removed `invokesEmotion` property
- Simplified annotation pipeline

### 📝 Files Updated

1. **persuasion_ontology.ttl** (v2.0)
   - Reduced from 10 techniques to 5
   - Removed emotion classes
   - Removed `invokesEmotion` property
   - Cleaner, more focused ontology

2. **example_annotated.ttl**
   - Updated all technique references
   - Removed emotion triples
   - Replaced removed techniques with core 5

3. **pipeline_implementation.py**
   - Updated `persuasion_taxonomy` dictionary
   - Removed `emotions` field from `PersuasionAnnotation` dataclass
   - Simplified LLM prompts
   - Removed emotion RDF generation code

4. **README.md**
   - Updated feature list
   - Updated ontology structure section
   - Removed emotion references
   - Updated example RDF output

### ✅ Rationale

**Why Simplify?**
- **Focus**: Core 5 techniques cover ~80% of persuasion cases
- **Clarity**: Easier to understand and implement
- **Accuracy**: Fewer classes = better LLM classification accuracy
- **Performance**: Faster annotation with simpler taxonomy
- **Practical**: Most common manipulation strategies

**Why Remove Emotions?**
- **Overlap**: Emotions are implicit in technique definitions
  - FearAppeal → naturally invokes fear
  - Scapegoating → naturally invokes anger
- **Complexity**: Emotion detection adds annotation overhead
- **Subjectivity**: Emotion labels vary more than technique labels
- **Simplicity**: Focus on manipulation strategies, not psychological effects

### 🔄 Migration Guide

**If you were using the old ontology:**

1. **Technique Mapping:**
   ```
   Old Technique              → New Technique
   ─────────────────────────────────────────────
   FlagWaving                 → LoadedLanguage or Exaggeration
   AppealToEmotion            → LoadedLanguage
   CausalOversimplification   → Exaggeration
   StrawMan                   → Exaggeration
   RedHerring                 → LoadedLanguage
   ```

2. **Remove Emotion Queries:**
   - Delete SPARQL queries that use `invokesEmotion`
   - Remove emotion-based filters

3. **Update LLM Prompts:**
   - Use the simplified 5-technique taxonomy
   - Remove emotion detection instructions

### 📊 Impact

**Before (v1.0):**
- 10 persuasion techniques
- 7 emotion classes
- `invokesEmotion` property
- More complex annotations

**After (v2.0):**
- 5 persuasion techniques (50% reduction)
- 0 emotion classes (simplified)
- No emotion properties (cleaner model)
- Focused, practical annotations

### 🎓 Use Cases

**Version 2.0 is ideal for:**
- ✅ Rapid prototyping
- ✅ Educational purposes
- ✅ Production systems requiring high accuracy
- ✅ Limited annotation budget
- ✅ Real-time detection systems

**Version 1.0 might be better for:**
- 🔬 Detailed research on persuasion psychology
- 📊 Comprehensive emotion analysis
- 📚 Academic studies on propaganda techniques

---

## Version 1.0 (Original - Full Ontology)

### Features
- 10 persuasion techniques
- 7 emotion classes
- Comprehensive emotion tracking
- Detailed annotation framework

---

**Current Version**: 2.0 (Simplified)  
**Last Updated**: January 2025
