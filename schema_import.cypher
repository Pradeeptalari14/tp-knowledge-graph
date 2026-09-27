// Neo4j Graph Database Schema Constraints & Relationship Importer

CREATE CONSTRAINT unique_entity_name IF NOT EXISTS
FOR (e:Entity) REQUIRE e.name IS UNIQUE;

CREATE INDEX entity_label_idx IF NOT EXISTS
FOR (e:Entity) ON (e.label);

UNWIND $relations AS rel
MERGE (source:Entity {name: rel.source})
SET source.label = rel.source_label
MERGE (target:Entity {name: rel.target})
SET target.label = rel.target_label
MERGE (source)-[r:RELATES_TO {type: rel.relation}]->(target)
RETURN count(r) AS imported_relationships;
