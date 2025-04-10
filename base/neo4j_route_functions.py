from neo4j import GraphDatabase

#PUBLIC TRANSPORT ROUTES WITH NEO4J

uri = "bolt://localhost:7687" 
user = "neo4j"  
password = "password"

driver = GraphDatabase.driver(uri, auth=(user, password))

def find_closest_stops(lat, lon):
        with driver.session(database="neo4j") as session:
            # Run the Cypher query to find the closest stops
            query = """
            WITH point({latitude: $lat, longitude: $lon }) AS user_location
            MATCH (s:Stop)
            WHERE s.lat IS NOT NULL AND s.lon IS NOT NULL
            WITH s, point.distance(user_location, point({latitude: s.lat, longitude: s.lon})) AS dist
            ORDER BY dist ASC
            LIMIT 10
            RETURN s.name AS name, s.lat AS lat, s.lon AS lon, dist;
            """
            result = session.run(query, lat=lat, lon=lon)
            closest_stops = []
            for record in result:
                closest_stops.append({
                    'name': record['name'],
                    'lat': record['lat'],
                    'lon': record['lon'],
                    'distance': record['dist']
                })
            return closest_stops

def is_valid(lat, lon, is_at_start, const_lat, const_lon):
    with driver.session(database="neo4j") as session:
        # Query to find the next stations
        query = """
        MATCH (start:Stop {lat: $lat, lon: $lon})-[:NEXT]->(next:Stop)
        RETURN DISTINCT next
        """
        
        # Query to calculate the distance between two points
        query1 = """
        RETURN point.distance(
            point({latitude: $lat1, longitude: $lon1}),
            point({latitude: $lat2, longitude: $lon2})
        ) AS distance
        """
        
        # Get the next stops
        result = session.run(query, lat=lat, lon=lon)
        next_stops = []
        for record in result:
            next_stops.append({
                'id': record['next']['id'],
                'name': record['next']['name'],
                'lat': record['next']['lat'],
                'lon': record['next']['lon']
            })

        # Check if next_stops is empty
        if not next_stops:
            return 0
        
        # If checking for start stop
        distance_station_next = session.run(query1, lat1=const_lat, lon1=const_lon, lat2=next_stops[0]['lat'], lon2=next_stops[0]['lon']).single()['distance']
        distance_station = session.run(query1, lat1=const_lat, lon1=const_lon, lat2=lat, lon2=lon).single()['distance']

        if is_at_start:
            if distance_station_next < distance_station:
                return 1
            else:
                return 0
        
        # If checking for end stop
        else:
            if distance_station_next > distance_station:
                return 1
            else:
                return 0

def calculate_routes(start_name, end_name):
    with driver.session(database="neo4j") as session:
        # First shortest path
        query_1 = """
        MATCH (a:Stop {name: $start_name }), (c:Stop {name: $end_name})
        MATCH p = allShortestPaths((a)-[:STOPS_AT*]-(c))
        RETURN [node IN nodes(p) | node.name] AS itinerary
        LIMIT 1
        """
        result_1 = session.run(query_1, {"start_name": start_name, "end_name": end_name})
        first_route = []
        for record in result_1:
            first_route = record["itinerary"]

        # Second shortest path (exclude the nodes from the first path except for the start and end nodes)
        query_2 = """
        MATCH (a:Stop {name: $start_name }), (c:Stop {name: $end_name})
        MATCH p = allShortestPaths((a)-[:STOPS_AT*]-(c))
        WHERE NONE (n IN nodes(p) WHERE n.name IN $first_route AND n.name <> $start_name AND n.name <> $end_name)
        RETURN [node IN nodes(p) | node.name] AS itinerary
        LIMIT 1
        """
        result_2 = session.run(query_2, {"start_name": start_name, "end_name": end_name, "first_route": first_route})
        second_route = []
        for record in result_2:
            second_route = record["itinerary"]

        # Third shortest path (exclude the nodes from both the first and second paths except for the start and end nodes)
        query_3 = """
        MATCH (a:Stop {name: $start_name }), (c:Stop {name: $end_name})
        MATCH p = allShortestPaths((a)-[:STOPS_AT*]-(c))
        WHERE NONE (n IN nodes(p) WHERE n.name IN $all_previous_routes AND n.name <> $start_name AND n.name <> $end_name)
        RETURN [node IN nodes(p) | node.name] AS itinerary
        LIMIT 1
        """
        # Combine the first and second routes to avoid repetition in the third path
        all_previous_routes = first_route + second_route
        result_3 = session.run(query_3, {"start_name": start_name, "end_name": end_name, "all_previous_routes": all_previous_routes})
        third_route = []
        for record in result_3:
            third_route = record["itinerary"]

        return first_route, second_route, third_route
    return [], [], []

start_lat = 47.145561
start_lon = 27.594237 

end_lat= 47.184455
end_lon= 27.561124

def get_public_transport_routes(start_lat, start_lon, end_lat, end_lon):
    
    #find valid stops at the start location 
    closest_stops_start =find_closest_stops(start_lat, start_lon)
    valid_closest_stops_start=[]

    for close_station_start in closest_stops_start:
        if(is_valid(close_station_start["lat"], close_station_start["lon"],1, end_lat, end_lon)):
            valid_closest_stops_start.append(close_station_start)


    #find valid stops at the end location
    closest_stops_end=find_closest_stops(end_lat, end_lon)
    valid_closest_stops_end=[]

    for close_station_end in closest_stops_end:
        if(is_valid(close_station_end["lat"], close_station_end["lon"],0 , start_lat, start_lon)):
            valid_closest_stops_end.append(close_station_end)

    #print(closest_stops_start)
    #print("===========")
    #print(valid_closest_stops_end)

    routes=[]
    for start_stop in valid_closest_stops_start[:2]:
        for end_stop in valid_closest_stops_end[:2]:
            route=calculate_routes(start_stop['name'], end_stop['name'])
            routes.append(route)

    return routes

routes=get_public_transport_routes(start_lat, start_lon, end_lat, end_lon)
print(routes)


driver.close()