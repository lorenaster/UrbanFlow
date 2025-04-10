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
    def get_towns_by_city(self, city):
        """
        Get all towns from a specific city
        """
        with self.driver.session() as session:
            result = session.read_transaction(self._get_towns_by_city, city)
            return result

    def _get_towns_by_city(self, tx, city):
        query = """
        MATCH (s:Stop)
        WHERE s.city = $city AND s.town IS NOT NULL
        RETURN DISTINCT s.town AS town
        ORDER BY town
        """
        result = tx.run(query, city=city)
        return [record["town"] for record in result]

    def get_routes_by_town(self, town, agency_id):
        """
        Get all routes that have stops in a specific town
        """
        with self.driver.session() as session:
            result = session.read_transaction(self._get_routes_by_town, town, agency_id)
            return result

    def _get_routes_by_town(self, tx, town, agency_id):
        query = """
        MATCH (r:Route)<-[:BELONGS_TO]-(t:Trip)-[:STOPS_AT]->(s:Stop)
        WHERE s.town = $town AND r.agency_id = $agency_id
        RETURN DISTINCT r.route_id AS route_id, 
            r.short_name AS short_name, 
            r.long_name AS long_name,
            r.type AS type,
            r.color AS color,
            r.text_color AS text_color
        ORDER BY r.short_name
        """
        result = tx.run(query, town=town, agency_id=agency_id)
        return [dict(record) for record in result]

    def get_route_details(self, route_id, agency_id):
        """
        Get detailed information about a specific route including its stops
        """
        with self.driver.session() as session:
            route_info = session.read_transaction(self._get_route_info, route_id, agency_id)
            if not route_info:
                return None
            
            # Get stops for each direction
            outbound_stops = session.read_transaction(
                self._get_route_stops, route_id, "0", agency_id
            )
            inbound_stops = session.read_transaction(
                self._get_route_stops, route_id, "1", agency_id
            )
            
            # Get shape IDs for this route
            shape_ids = session.read_transaction(self._get_route_shape_ids, route_id, agency_id)
            
            return {
                "route_info": route_info,
                "outbound_stops": outbound_stops,
                "inbound_stops": inbound_stops,
                "shape_ids": shape_ids
            }

    def _get_route_info(self, tx, route_id, agency_id):
        query = """
        MATCH (r:Route {route_id: $route_id, agency_id: $agency_id})
        RETURN r.route_id AS route_id, 
            r.short_name AS short_name, 
            r.long_name AS long_name,
            r.type AS type,
            r.color AS color,
            r.text_color AS text_color,
            r.city AS city
        """
        result = tx.run(query, route_id=route_id, agency_id=agency_id)
        record = result.single()
        return dict(record) if record else None

    def _get_route_stops(self, tx, route_id, direction_id, agency_id):
        query = """
        MATCH (r:Route {route_id: $route_id, agency_id: $agency_id})<-[:BELONGS_TO]-(t:Trip {direction_id: $direction_id})-[st:STOPS_AT]->(s:Stop)
        RETURN DISTINCT s.stop_id AS stop_id,
            s.name AS name,
            s.lat AS lat,
            s.lon AS lon,
            s.town AS town
        ORDER BY st.stop_sequence
        """
        result = tx.run(query, route_id=route_id, direction_id=direction_id, agency_id=agency_id)
        return [dict(record) for record in result]

    def _get_route_shape_ids(self, tx, route_id, agency_id):
        query = """
        MATCH (r:Route {route_id: $route_id, agency_id: $agency_id})<-[:BELONGS_TO]-(t:Trip)
        WHERE t.shape_id IS NOT NULL
        RETURN DISTINCT t.shape_id AS shape_id
        """
        result = tx.run(query, route_id=route_id, agency_id=agency_id)
        return [record["shape_id"] for record in result]

    def get_shape_points(self, shape_id):
        """
        Get all shape points for a specific shape
        """
        with self.driver.session() as session:
            result = session.read_transaction(self._get_shape_points, shape_id)
            return result

    def _get_shape_points(self, tx, shape_id):
        query = """
        MATCH (sp:ShapePoint {shape_id: $shape_id})
        RETURN sp.lat AS lat, sp.lon AS lon, sp.sequence AS sequence
        ORDER BY sp.sequence
        """
        result = tx.run(query, shape_id=shape_id)
        return [dict(record) for record in result]
