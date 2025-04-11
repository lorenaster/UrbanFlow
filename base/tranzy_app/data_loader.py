import pandas as pd
import re
import logging
from .neo4j_client import Neo4jClient
from .tranzy_client import TranzyClient
from django.conf import settings


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def extract_town(stop_name, city):
    """Extract town name from stop_name or return city as default."""
    town_match = re.search(r',\s*([^,]+)$', stop_name)
    if town_match:
        return town_match.group(1).strip()
    return city

def load_transit_data(city=None):
    """
    Load transit data from Tranzy API to Neo4j database.
    If city is specified, load data only for that city.
    Otherwise, load data for all cities in TRANZY_AGENCY_MAPPING.
    """
    if city:
        cities = [city]
    else:
        cities = settings.TRANZY_AGENCY_MAPPING.keys()

    total_stats = {
        'stops': 0,
        'routes': 0,
        'trips': 0,
        'stop_times': 0,
        'shape_points': 0
    }


    neo4j_client = Neo4jClient()

    success, message = neo4j_client.test_connection()
    if not success:
        logger.error(f"Neo4j connection failed: {message}")
        return False
    logger.info(f"Neo4j connection successful: {message}")

    try:
        for current_city in cities:
            agency_id = settings.TRANZY_AGENCY_MAPPING.get(current_city)
            if isinstance(agency_id, dict):
                agency_id = agency_id.get('agency_id')
            
            if not agency_id:
                logger.warning(f"No agency ID found for city: {current_city}")
                continue

            logger.info(f"Loading data for {current_city} (Agency ID: {agency_id})...")

            tranzy_client = TranzyClient(agency_id=agency_id)

            routes = tranzy_client.get_routes()
            trips = tranzy_client.get_trips()
            stops = tranzy_client.get_stops()
            stop_times = tranzy_client.get_stop_times()
            shapes = tranzy_client.get_shapes()


            logger.info(f"Fetched data for {current_city}:")
            logger.info(f"  - Stops: {len(stops) if not stops.empty else 0} records")
            logger.info(f"  - Routes: {len(routes) if not routes.empty else 0} records")
            logger.info(f"  - Trips: {len(trips) if not trips.empty else 0} records")
            logger.info(f"  - Stop times: {len(stop_times) if not stop_times.empty else 0} records")
            logger.info(f"  - Shape points: {len(shapes) if not shapes.empty else 0} records")
            
            city_stats = {
                'stops': 0,
                'routes': 0,
                'trips': 0,
                'stop_times': 0,
                'shape_points': 0
            }

            if not stops.empty:
                stops['city'] = current_city
                stops['town'] = stops['stop_name'].apply(lambda x: extract_town(x, current_city))

                for _, stop in stops.iterrows():
                    try:
                        neo4j_client.insert_stop(
                            stop['stop_id'],
                            stop['stop_name'],
                            float(stop['stop_lat']),
                            float(stop['stop_lon']),
                            stop['town'],
                            current_city,
                            agency_id
                        )
                        city_stats['stops'] += 1
                    except Exception as e:
                        logger.error(f"Error inserting stop {stop['stop_id']}: {str(e)}")


            if not routes.empty:
                for _, route in routes.iterrows():
                    try:
                        neo4j_client.insert_route(
                            route['route_id'],
                            route.get('route_short_name', ''),
                            route.get('route_long_name', ''),
                            int(route.get('route_type', 3)),
                            route.get('route_color', 'FFFFFF'),
                            route.get('route_text_color', '000000'),
                            agency_id,
                            current_city
                        )
                        city_stats['routes'] += 1
                    except Exception as e:
                        logger.error(f"Error inserting route {route['route_id']}: {str(e)}")


            if not trips.empty:
                for _, trip in trips.iterrows():
                    try:
                        neo4j_client.insert_trip(
                            trip['trip_id'],
                            trip['route_id'],
                            int(trip.get('direction_id', 0)),
                            trip.get('shape_id', None),
                            agency_id
                        )
                        city_stats['trips'] += 1
                    except Exception as e:
                        logger.error(f"Error inserting trip {trip['trip_id']}: {str(e)}")

            if not stop_times.empty:
                batch_size = 1000
                for i in range(0, len(stop_times), batch_size):
                    batch = stop_times.iloc[i:i+batch_size]
                    for _, stop_time in batch.iterrows():
                        try:
                            neo4j_client.insert_stop_time(
                                stop_time['trip_id'],
                                stop_time['stop_id'],
                                stop_time.get('arrival_time', ''),
                                stop_time.get('departure_time', ''),
                                int(stop_time.get('stop_sequence', 0)),
                                agency_id
                            )
                            city_stats['stop_times'] += 1
                        except Exception as e:
                            logger.error(f"Error inserting stop time for trip {stop_time['trip_id']}, stop {stop_time['stop_id']}: {str(e)}")
                    logger.info(f"Processed {min(i+batch_size, len(stop_times))} of {len(stop_times)} stop times for {current_city}")

            if not shapes.empty:
                batch_size = 1000
                for i in range(0, len(shapes), batch_size):
                    batch = shapes.iloc[i:i+batch_size]
                    for _, shape in batch.iterrows():
                        try:
                            neo4j_client.insert_shape_point(
                                shape['shape_id'],
                                float(shape['shape_pt_lat']),
                                float(shape['shape_pt_lon']),
                                int(shape['shape_pt_sequence']),
                                agency_id
                            )
                            city_stats['shape_points'] += 1
                        except Exception as e:
                            logger.error(f"Error inserting shape point {shape['shape_id']}-{shape['shape_pt_sequence']}: {str(e)}")
                    logger.info(f"Processed {min(i+batch_size, len(shapes))} of {len(shapes)} shape points for {current_city}")

            for key in total_stats:
                total_stats[key] += city_stats[key]
                
            logger.info(f"Completed loading data for {current_city}:")
            logger.info(f"  - Inserted {city_stats['stops']} stops")
            logger.info(f"  - Inserted {city_stats['routes']} routes")
            logger.info(f"  - Inserted {city_stats['trips']} trips")
            logger.info(f"  - Inserted {city_stats['stop_times']} stop times")
            logger.info(f"  - Inserted {city_stats['shape_points']} shape points")


        neo4j_client.close()

        logger.info("Overall import statistics:")
        logger.info(f"  - Total stops: {total_stats['stops']}")
        logger.info(f"  - Total routes: {total_stats['routes']}")
        logger.info(f"  - Total trips: {total_stats['trips']}")
        logger.info(f"  - Total stop times: {total_stats['stop_times']}")
        logger.info(f"  - Total shape points: {total_stats['shape_points']}")
        
        return True
        
    except Exception as e:
        logger.error(f"Error in data loading process: {str(e)}")
        neo4j_client.close()
        return False