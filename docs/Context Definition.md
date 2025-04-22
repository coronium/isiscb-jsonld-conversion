{
  "@context": {
    "dc": "http://purl.org/dc/elements/1.1/",
    "dcterms": "http://purl.org/dc/terms/",
    "schema": "http://schema.org/",
    "bibo": "http://purl.org/ontology/bibo/",
    "foaf": "http://xmlns.com/foaf/0.1/",
    "skos": "http://www.w3.org/2004/02/skos/core#",
    "prism": "http://prismstandard.org/namespaces/basic/2.0/",
    "vivo": "http://vivoweb.org/ontology/core#",
    "isiscb": "https://ontology.isiscb.org/vocabulary/",
    
    "title": "dc:title",
    "name": "schema:name",
    "creator": "dc:creator",
    "contributor": "dc:contributor",
    "editor": "schema:editor",
    "date": "dc:date",
    "datePublished": "schema:datePublished",
    "publisher": "dc:publisher",
    "subject": "dc:subject",
    "language": "dc:language",
    "description": "schema:description",
    "abstract": "dc:abstract",
    "identifier": "dc:identifier",
    
    "recordID": "isiscb:recordID",
    "recordType": "isiscb:recordType",
    "recordStatus": "isiscb:recordStatus",
    "recordNature": "isiscb:recordNature",
    "mainTitle": "isiscb:mainTitle",
    "subtitle": "isiscb:subtitle",
    "yearNormalized": "isiscb:yearNormalized",
    "publisherLocation": "isiscb:publisherLocation",
    "extent": "isiscb:extent",
    "physicalDetails": "isiscb:physicalDetails",
    "pagesFreeText": "isiscb:pagesFreeText",
    "completeCitation": "isiscb:completeCitation",
    "staffNotes": "isiscb:staffNotes",
    "recordHistory": "isiscb:recordHistory",
    "namePreferred": "isiscb:namePreferred",
    "flourishedDate": "isiscb:flourishedDate",
    "classificationSystem": "isiscb:classificationSystem",
    "classificationCode": "isiscb:classificationCode",
    "classificationScheme": "isiscb:classificationScheme",
    "mainCategory": "isiscb:mainCategory",
    "subCategory": "isiscb:subCategory",
    "redirectsTo": "isiscb:redirectsTo",
    
    "familyName": "schema:familyName",
    "givenName": "schema:givenName",
    "nameSuffix": "schema:nameSuffix",
    "birthDate": "schema:birthDate",
    "deathDate": "schema:deathDate",
    "placeName": "schema:placeName",
    "addressCountry": "schema:addressCountry",
    "numberOfPages": "schema:numberOfPages",
    "position": "schema:position",
    "isPartOf": "schema:isPartOf",
    "about": "schema:about",
    "sameAs": "schema:sameAs",
    
    "prefLabel": "skos:prefLabel",
    "altLabel": "skos:altLabel",
    "broader": "skos:broader",
    "narrower": "skos:narrower",
    "related": "skos:related",
    "inScheme": "skos:inScheme",
    "notation": "skos:notation",
    
    "edition": "bibo:edition",
    "pages": "bibo:pages",
    "pageStart": "bibo:pageStart",
    "pageEnd": "bibo:pageEnd",
    "volume": "bibo:volume",
    "issue": "bibo:issue",
    "isbn": "bibo:isbn",
    "issn": "bibo:issn",
    "shortTitle": "bibo:shortTitle",
    
    "isReviewedBy": {
      "@id": "isiscb:isReviewedBy",
      "@type": "@id"
    },
    "reviews": {
      "@id": "isiscb:reviews",
      "@type": "@id"
    },
    "includesSeriesArticle": {
      "@id": "isiscb:includesSeriesArticle",
      "@type": "@id"
    },
    "isPartOf": {
      "@id": "dcterms:isPartOf",
      "@type": "@id"
    },
    "hasPart": {
      "@id": "dcterms:hasPart",
      "@type": "@id"
    },
    "references": {
      "@id": "dcterms:references",
      "@type": "@id"
    },
    "isReferencedBy": {
      "@id": "dcterms:isReferencedBy",
      "@type": "@id"
    },
    
    "relatedAuthorities": "isiscb:relatedAuthorities",
    "relatedCitations": "isiscb:relatedCitations",
    "linkedData": "isiscb:linkedData",
    "attributes": "isiscb:attributes",
    
    "Person": "schema:Person",
    "Organization": "schema:Organization",
    "Place": "schema:Place",
    "CreativeWork": "schema:CreativeWork",
    "Book": "bibo:Book",
    "Article": "bibo:Article",
    "Chapter": "bibo:Chapter",
    "Thesis": "bibo:Thesis",
    "Periodical": "bibo:Periodical",
    "Concept": "skos:Concept",
    "Collection": "skos:Collection",
    "PeriodOfTime": "dcterms:PeriodOfTime",
    
    "author": {
      "@id": "isiscb:author",
      "@subPropertyOf": "dc:creator"
    },
    "editor": {
      "@id": "schema:editor",
      "@subPropertyOf": "dc:contributor"
    },
    "translator": {
      "@id": "schema:translator",
      "@subPropertyOf": "dc:contributor"
    },
    "advisor": {
      "@id": "vivo:advisorIn",
      "@subPropertyOf": "dc:contributor"
    },
    "institution": {
      "@id": "isiscb:institution",
      "@type": "@id"
    },
    "school": {
      "@id": "bibo:degreeGrantor",
      "@type": "@id"
    },
    "subject": {
      "@id": "dc:subject",
      "@type": "@id"
    },
    "category": {
      "@id": "isiscb:category",
      "@subPropertyOf": "dc:subject"
    },
    "periodical": {
      "@id": "isiscb:periodical",
      "@subPropertyOf": "schema:isPartOf"
    }
  }
}