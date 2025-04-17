# Detailed Documentation: Related Authorities Processing in IsisCB JSON-LD Conversion

## Overview

The Related Authorities processing is a critical component of the IsisCB JSON-LD conversion that handles the relationships between citation records and authority records. This documentation explains how the system processes these relationships, the data flow, and the conversion logic.

## Data Format and Structure

### Original Related Authorities Field Format

The "Related Authorities" field in the IsisCB database contains structured relationship information with the following pattern:

```
ACR_ID ACR000606449 || ACRStatus Active || ACRType Author || ACRDisplayOrder 1.0 || 
ACRNameForDisplayInCitation Joseph W. Dauben || AuthorityID CBA000023541 || 
AuthorityStatus Active || AuthorityType Person || AuthorityName Dauben, Joseph Warren
```

Key components include:
- `ACR_ID`: Unique identifier for the authority-citation relationship
- `ACRStatus`: Status of the relationship (usually Active)
- `ACRType`: Type of relationship (Author, Subject, Editor, etc.)
- `ACRDisplayOrder`: Order for display in citations
- `ACRNameForDisplayInCitation`: Name to display in citations
- `AuthorityID`: ID of the authority record
- `AuthorityType`: Type of the authority (Person, Concept, etc.)
- `AuthorityName`: Name of the authority record

Multiple authority relationships are separated by a double slash (`//`).

## Processing Pipeline

### 1. Entry Point: `RelatedAuthoritiesConverter.convert()`

The processing begins in the `convert` method of the `RelatedAuthoritiesConverter` class, which:
1. Validates the input value
2. Calls `_convert_impl()` to perform the actual conversion

### 2. Core Conversion: `_convert_impl()`

This method:
1. Parses the raw field value
2. Organizes relationships by type
3. Generates appropriate JSON-LD representation
4. Returns a dictionary with both specific relationship properties and the complete relationship list

```python
def _convert_impl(self, value: str, record_id: str) -> Dict:
    # Parse entries and organize by type
    relationships_by_type = self._parse_and_organize_relationships(value, record_id)
    
    # Generate result dictionary
    result = {}
    
    # Add specialized relationship groups
    self._add_person_contributors(result, relationships_by_type)
    self._add_subjects(result, relationships_by_type)
    self._add_publication_relationships(result, relationships_by_type)
    self._add_institution_relationships(result, relationships_by_type)
    
    # Add generic/rare relationships
    self._add_generic_relationships(result, relationships_by_type)
    
    # Store the full structured representation for preservation
    if any(relationships_by_type.values()):
        all_relationships = []
        for type_relationships in relationships_by_type.values():
            all_relationships.extend(type_relationships)
            
        if all_relationships:
            result["isiscb:relatedAuthorities"] = all_relationships
    
    return result
```

### 3. Parsing and Organization: `_parse_and_organize_relationships()`

This function:
1. Splits the field value into individual relationships
2. Parses each relationship into a structured dictionary
3. Organizes relationships by type for specialized processing
4. Uses the schema mapping functions to get appropriate URIs

```python
def _parse_and_organize_relationships(self, value: str, record_id: str) -> Dict[str, List[Dict]]:
    # Split entries by double slash
    entries = value.split(" // ")
    
    # Dictionary to hold relationships by type
    relationships_by_type = {}
    
    for entry in entries:
        try:
            # Parse the entry into a dictionary
            entry_dict = self._parse_entry(entry)
            
            if not entry_dict or "ACRType" not in entry_dict or "AuthorityID" not in entry_dict:
                continue
                
            # Get relationship type and normalize
            relationship_type = entry_dict["ACRType"]
            normalized_type = self._normalize_type(relationship_type)
            
            # Create relationship object with proper type URI
            relationship = {
                "@type": get_relationship_uri(relationship_type),
                "isiscb:relationshipType": relationship_type,
                "isiscb:authority": {
                    "@id": f"https://data.isiscb.org/authority/{entry_dict.get('AuthorityID', '')}"
                }
            }
            
            # Add additional properties...
            
            # Add to appropriate category
            if normalized_type not in relationships_by_type:
                relationships_by_type[normalized_type] = []
                
            relationships_by_type[normalized_type].append(relationship)
            
        except Exception as e:
            logger.warning(f"Error parsing related authority entry for record {record_id}")
            
    return relationships_by_type
```

### 4. Schema Mapping: Relationship Type -> Standard Property

The converter uses two key functions from `schema_mappings.py`:

#### `get_relationship_property()`:
Converts a relationship type to a standard property URI:
```python
def get_relationship_property(relationship_type):
    """Get property URI for a relationship type."""
    relationship_type = relationship_type.upper()
    
    if relationship_type in AUTHORITY_RELATIONSHIP_TYPES:
        return AUTHORITY_RELATIONSHIP_TYPES[relationship_type]["primary"]
    elif relationship_type in CITATION_RELATIONSHIP_TYPES:
        return CITATION_RELATIONSHIP_TYPES[relationship_type]["primary"]
    else:
        return f"isiscb:{relationship_type.lower()}"
```

#### `get_relationship_uri()`:
Converts a relationship type to a type URI:
```python
def get_relationship_uri(relationship_type):
    """Get URI for a relationship type."""
    relationship_type = relationship_type.upper()
    
    if relationship_type in AUTHORITY_RELATIONSHIP_TYPES:
        return AUTHORITY_RELATIONSHIP_TYPES[relationship_type]["uri"]
    elif relationship_type in CITATION_RELATIONSHIP_TYPES:
        return CITATION_RELATIONSHIP_TYPES[relationship_type]["uri"]
    else:
        return f"isiscb:{relationship_type.lower()}"
```

### 5. Specialized Processing by Relationship Type

The converter uses specialized methods to process different types of relationships:

#### Person Contributors: `_add_person_contributors()`
Processes authors, editors, translators, etc. and adds them to the result:
```python
def _add_person_contributors(self, result: Dict, relationships_by_type: Dict) -> None:
    # Process authors
    if "AUTHOR" in relationships_by_type:
        authors = self._process_authors(relationships_by_type["AUTHOR"])
        if authors:
            result["dc:creator"] = authors
            result["schema:author"] = authors
    
    # Process editors, translators, etc.
    # ...
```

#### Subjects: `_add_subjects()`
Processes subject and category relationships:
```python
def _add_subjects(self, result: Dict, relationships_by_type: Dict) -> None:
    all_subjects = []
    
    # Process subjects
    if "SUBJECT" in relationships_by_type:
        subjects = self._process_subjects(relationships_by_type["SUBJECT"])
        all_subjects.extend(subjects)
        
    # Process categories
    if "CATEGORY" in relationships_by_type:
        categories = self._process_subjects(relationships_by_type["CATEGORY"])
        all_subjects.extend(categories)
        
    if all_subjects:
        result["dc:subject"] = all_subjects
        result["schema:about"] = all_subjects
```

#### Publications: `_add_publication_relationships()`
Processes periodicals and book series:
```python
def _add_publication_relationships(self, result: Dict, relationships_by_type: Dict) -> None:
    # Process periodicals
    if "PERIODICAL" in relationships_by_type:
        periodical = self._process_periodical(relationships_by_type["PERIODICAL"])
        if periodical:
            result["schema:isPartOf"] = periodical
            result["dcterms:isPartOf"] = periodical
    
    # Process book series
    # ...
```

#### Institutions: `_add_institution_relationships()`
Processes publishers, schools, and other institutions:
```python
def _add_institution_relationships(self, result: Dict, relationships_by_type: Dict) -> None:
    # Process publishers
    if "PUBLISHER" in relationships_by_type:
        publisher = self._process_institution(relationships_by_type["PUBLISHER"], "publisher")
        if publisher:
            result["dc:publisher"] = publisher
            result["schema:publisher"] = publisher
    
    # Process schools, institutions, meetings, etc.
    # ...
```

## Entity Processing

For each relationship type, specialized processing functions create structured objects:

### Author Processing: `_process_authors()`

This function:
1. Sorts authors by display order
2. Creates structured author objects with appropriate types
3. Handles name display (prioritizing display name over authority name)
4. Adds position and role information

```python
def _process_authors(self, author_relationships: List[Dict]) -> List[Dict]:
    # Sort by display order
    sorted_authors = sorted(
        author_relationships, 
        key=lambda p: float(p.get("isiscb:displayOrder", "1.0"))
    )
    
    author_objects = []
    for idx, author in enumerate(sorted_authors):
        # Create base author object with proper ID
        author_obj = {
            "@id": author["isiscb:authority"]["@id"]
        }
        
        # Set appropriate type based on authority type
        if "isiscb:authorityType" in author:
            authority_type = author["isiscb:authorityType"]
            if authority_type == "Institution" or authority_type == "Organization":
                author_obj["@type"] = ["schema:Organization", "foaf:Organization"]
            else:
                author_obj["@type"] = ["schema:Person", "foaf:Person"]
        else:
            # Default to Person
            author_obj["@type"] = ["schema:Person", "foaf:Person"]
        
        # Handle name (prioritize display name over authority name)
        if "isiscb:displayName" in author and author["isiscb:displayName"]:
            display_name = author["isiscb:displayName"].strip()
            author_obj["schema:name"] = display_name
            author_obj["name"] = display_name  # For compatibility
        elif "isiscb:authorityName" in author:
            authority_name = author["isiscb:authorityName"].strip()
            author_obj["schema:name"] = authority_name
            author_obj["name"] = authority_name  # For compatibility
        
        # Add position and role information
        position = author.get("isiscb:displayOrder", str(idx + 1))
        author_obj["schema:position"] = position
        author_obj["isiscb:position"] = position  # For compatibility
        author_obj["schema:roleName"] = "author"
        author_obj["isiscb:role"] = "author"  # For compatibility
        
        author_objects.append(author_obj)
    
    return author_objects
```

Similar specialized processing methods exist for other entity types.

## Relationship Schema Mappings

The schema mappings define how relationship types map to standard vocabularies:

```python
AUTHORITY_RELATIONSHIP_TYPES = {
    "AUTHOR": {
        "primary": "dc:creator",
        "equivalents": ["schema:author"],
        "uri": "isiscb:author"
    },
    "EDITOR": {
        "primary": "schema:editor",
        "equivalents": ["dc:contributor"],
        "uri": "isiscb:editor"
    },
    "SUBJECT": {
        "primary": "dc:subject",
        "equivalents": ["schema:about"],
        "uri": "isiscb:subject"
    },
    # ... more relationship types
}
```

These mappings ensure:
1. Consistent property usage across the application
2. Proper mapping to standard vocabularies
3. Preservation of IsisCB-specific information

## Output Format

The processed relationships are represented in two ways:

### 1. Standard Vocabulary Properties

Relationships are added using standard vocabulary properties:

```json
{
  "dc:creator": [
    {
      "@id": "https://data.isiscb.org/authority/CBA000023541",
      "name": "Joseph W. Dauben",
      "isiscb:role": "author",
      "isiscb:position": "1.0",
      "isiscb:authorityType": "Person"
    }
  ],
  "dc:subject": [
    {
      "@id": "https://data.isiscb.org/authority/CBA000067891",
      "name": "Mathematics",
      "@type": ["skos:Concept"]
    }
  ]
}
```

### 2. Complete Representation

The complete original data is preserved in the `isiscb:relatedAuthorities` property:

```json
{
  "isiscb:relatedAuthorities": [
    {
      "@type": "isiscb:author",
      "isiscb:relationshipType": "Author",
      "isiscb:displayOrder": "1.0",
      "isiscb:authority": {
        "@id": "https://data.isiscb.org/authority/CBA000023541"
      },
      "isiscb:authorityName": "Dauben, Joseph Warren",
      "isiscb:authorityType": "Person",
      "isiscb:displayName": "Joseph W. Dauben",
      "isiscb:authorityStatus": "Active"
    },
    // Additional relationships...
  ]
}
```

## Error Handling

The converter includes robust error handling:

1. Empty or null values return an empty dictionary
2. Malformed entries are caught and logged without failing the entire conversion
3. Missing critical fields (ACRType, AuthorityID) are skipped
4. Individual relationship parsing errors are logged with the record ID

This ensures that partial data is preserved even when some relationships have issues.

## Integration with the Pipeline

The `RelatedAuthoritiesConverter` is registered in the `CitationConverterPipeline` and applied to the "Related Authorities" field:

```python
# In pipeline initialization
self.converters = {
    # Other converters...
    'related_authorities': RelatedAuthoritiesConverter(),
}

# In convert_row method
if 'Related Authorities' in row:
    jsonld.update(self.converters['related_authorities'].convert(row['Related Authorities'], record_id))
```

This ensures that all citation records with related authorities are properly processed during conversion.