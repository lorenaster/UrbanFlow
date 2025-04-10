from django.core.management.base import BaseCommand
from base.tranzy_app.neo4j_client import Neo4jClient

class Command(BaseCommand):
    help = 'Test Neo4j database connection and query basic statistics'

    def handle(self, *args, **options):
        client = Neo4jClient()
        
        try:
            # Test connection
            with client.driver.session() as session:
                self.stdout.write("Testing connection...")
                session.run("MATCH (n) RETURN count(n) LIMIT 1")
                self.stdout.write(self.style.SUCCESS("✓ Connection successful"))
            
            # Count nodes by type
            with client.driver.session() as session:
                self.stdout.write("\nCounting nodes by type...")
                result = session.run("""
                    CALL apoc.meta.nodeTypeProperties()
                    YIELD nodeType, propertyName, propertyTypes
                    RETURN nodeType, count(propertyName) as properties
                    ORDER BY nodeType
                """)
                
                for record in result:
                    self.stdout.write(f"{record['nodeType']}: {record['properties']} properties")
            
            # Sample data for each entity type
            node_types = ["Stop", "Route", "Trip", "ShapePoint"]
            for node_type in node_types:
                with client.driver.session() as session:
                    self.stdout.write(f"\nSample {node_type}:")
                    result = session.run(f"MATCH (n:{node_type}) RETURN n LIMIT 1")
                    sample = result.single()
                    if sample:
                        self.stdout.write(str(dict(sample["n"].items())))
                    else:
                        self.stdout.write(f"No {node_type} nodes found")
            
            client.close()
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error: {str(e)}"))
            client.close()