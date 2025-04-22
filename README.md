# IsisCB JSON-LD Conversion

A framework for converting IsisCB Explore Database records to JSON-LD format, preserving the rich context of history of science, technology, and medicine data while ensuring interoperability with standard semantic web vocabularies.

## Overview

This project implements a hybrid approach to JSON-LD conversion that leverages standard bibliographic vocabularies (Dublin Core, Schema.org, SKOS) while maintaining IsisCB's domain-specific attributes through custom vocabulary extensions.

The conversion process transforms:
- Citation records (books, articles, theses, etc.)
- Authority records (people, institutions, concepts, etc.)
- Relationships between records
- External authority links (VIAF, DNB, etc.)

## Features

- **Standardized Conversion**: Maps IsisCB fields to established vocabularies
- **Hybrid Approach**: Preserves specialized scholarly context while ensuring broad interoperability
- **Validation**: Built-in JSON-LD validation with custom schemas
- **Modular Architecture**: Field-specific converters for maximum flexibility
- **Comprehensive Documentation**: Detailed mapping documentation and guides

## Usage

Consult the files in the doc directory for more detailed documentation. 