from neo4j import GraphDatabase
from django.conf import settings

class Neo4jClient:
    def __init__(self):
        self.driver = GraphDatabase.driver(
            settings.NEO4J_URI,
            auth=(settings.NEO4J_USERNAME, settings.NEO4J_PASSWORD)
        )
    def test_connection(self):
        try:
            with self.driver.session() as session:
                result = session.run("MATCH (n) RETURN count(n) as count")
                count = result.single()["count"]
                return True, f"Connected successfully. Database contains {count} nodes."
        except Exception as e:
            return False, f"Connection failed: {str(e)}"
    
    def close(self):
        self.driver.close()

    def insert_stop(self, stop_id, name, lat, lon, town=None, city=None, agency_id=None):
        with self.driver.session() as session:
            session.write_transaction(self._insert_stop, stop_id, name, lat, lon, town, city, agency_id)

    def _insert_stop(self, tx, stop_id, name, lat, lon, town, city, agency_id):
        query = """
        MERGE (s:Stop {stop_id: $stop_id})
        SET s.name = $name, 
            s.lat = $lat, 
            s.lon = $lon, 
            s.town = $town,
            s.city = $city,
            s.agency_id = $agency_id
        """
        tx.run(query, stop_id=stop_id, name=name, lat=lat, lon=lon, town=town, city=city, agency_id=agency_id)

    def insert_route(self, route_id, short_name, long_name, route_type, route_color="FFFFFF", route_text_color="000000", agency_id=None, city=None):
        with self.driver.session() as session:
            session.write_transaction(
                self._insert_route, 
                route_id, short_name, long_name, route_type, route_color, route_text_color, agency_id, city
            )

    def _insert_route(self, tx, route_id, short_name, long_name, route_type, route_color, route_text_color, agency_id, city):
        query = """
        MERGE (r:Route {route_id: $route_id})
        SET r.short_name = $short_name,
            r.long_name = $long_name,
            r.type = $route_type,
            r.color = $route_color,
            r.text_color = $route_text_color,
            r.agency_id = $agency_id,
            r.city = $city
        """
        tx.run(query, route_id=route_id, short_name=short_name, long_name=long_name, route_type=route_type,
               route_color=route_color, route_text_color=route_text_color, agency_id=agency_id, city=city)

    def insert_trip(self, trip_id, route_id, direction_id, shape_id=None, agency_id=None):
        with self.driver.session() as session:
            session.write_transaction(self._insert_trip, trip_id, route_id, direction_id, shape_id, agency_id)

    def _insert_trip(self, tx, trip_id, route_id, direction_id, shape_id, agency_id):
        query = """
        MATCH (r:Route {route_id: $route_id})
        MERGE (t:Trip {trip_id: $trip_id})
        SET t.direction_id = $direction_id,
            t.shape_id = $shape_id,
            t.agency_id = $agency_id
        MERGE (t)-[:BELONGS_TO]->(r)
        """
        tx.run(query, trip_id=trip_id, route_id=route_id, direction_id=direction_id, shape_id=shape_id, agency_id=agency_id)

    def insert_stop_time(self, trip_id, stop_id, arrival_time, departure_time, stop_sequence, agency_id=None):
        with self.driver.session() as session:
            session.write_transaction(
                self._insert_stop_time,
                trip_id, stop_id, arrival_time, departure_time, stop_sequence, agency_id
            )

    def _insert_stop_time(self, tx, trip_id, stop_id, arrival_time, departure_time, stop_sequence, agency_id):
        query = """
        MATCH (t:Trip {trip_id: $trip_id}), (s:Stop {stop_id: $stop_id})
        MERGE (t)-[r:STOPS_AT]->(s)
        SET r.arrival_time = $arrival_time,
            r.departure_time = $departure_time,
            r.stop_sequence = $stop_sequence,
            r.agency_id = $agency_id
        """
        tx.run(query, trip_id=trip_id, stop_id=stop_id, arrival_time=arrival_time,
               departure_time=departure_time, stop_sequence=stop_sequence, agency_id=agency_id)

    def insert_shape_point(self, shape_id, lat, lon, sequence, agency_id=None):
        with self.driver.session() as session:
            session.write_transaction(self._insert_shape_point, shape_id, lat, lon, sequence, agency_id)

    def _insert_shape_point(self, tx, shape_id, lat, lon, sequence, agency_id):
        query = """
        MERGE (s:ShapePoint {shape_id: $shape_id, sequence: $sequence})
        SET s.lat = $lat, s.lon = $lon, s.agency_id = $agency_id
        """
        tx.run(query, shape_id=shape_id, lat=lat, lon=lon, sequence=sequence, agency_id=agency_id)
