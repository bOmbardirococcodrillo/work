from neo4j import GraphDatabase
import csv

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "pass123456"))

def add_data(tx, type_name, name, prop1, prop2):
    query = f"CREATE (n:{type_name} {{name: $name, prop1: $prop1, prop2: $prop2}})"
    tx.run(query, name=name, prop1=prop1, prop2=prop2)

with driver.session() as session:
    with open("sample_data.csv", "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            session.execute_write(add_data, row["type"], row["name"], row["property1"], row["property2"])

driver.close()