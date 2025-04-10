from neo4j import GraphDatabase
import csv

# Connect to Neo4j
driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "pass123456"))

def add_relationship(tx, start_type, start_name, end_type, end_name, relationship):
    query = f"""
    MATCH (start:{start_type} {{name: $start_name}})
    MATCH (end:{end_type} {{name: $end_name}})
    CREATE (start)-[:{relationship}]->(end)
    """
    tx.run(query, start_name=start_name, end_name=end_name)

with driver.session() as session:
    with open("relationships.csv", "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            session.execute_write(add_relationship, 
                                      row["start_type"], row["start_name"],
                                      row["end_type"], row["end_name"],
                                      row["relationship"])

driver.close()
print("Relationships added!")