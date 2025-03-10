# Original Database Structure

The data in the cvs files is exported from the orignal database that contains the follwoing tables

- Citations (CBB records)
- Authorities (CBA records)
- ACR records which is many-to-many relationship between authorities and citations
- CCR record which is a many-to-many relationship between ciation records

The cvs files are created by an automated epxport therefor we can assume that the data is handled in a consisten way. We can also assume that where the data is presented in multiple places (eg Author field, and the Related Authority field) the data is consistent.

In the cvs the field 'Related Authorites' and 'Reclated Citations' is the export of the ACR and CCR records. The individual records as seperated by '//' Fields within a record are seperated by '||' with a field name being followed by value. 

There is an additional field 'Linked Data' that containes links to outside resources. This are seperated by '||'