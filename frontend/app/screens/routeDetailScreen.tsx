// screens/RouteDetailScreen.tsx
import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet, FlatList, TouchableOpacity, ActivityIndicator, SafeAreaView } from 'react-native';
import { RouteProp } from '@react-navigation/native';
import { StackNavigationProp } from '@react-navigation/stack';
import { RootStackParamList } from '../navigation/types';
import { fetchRouteDetails, Trip } from '../services/apiService';

type RouteDetailScreenProps = {
  navigation: StackNavigationProp<RootStackParamList, 'RouteDetail'>;
  route: RouteProp<RootStackParamList, 'RouteDetail'>;
};

const RouteDetailScreen: React.FC<RouteDetailScreenProps> = ({ navigation, route }) => {
  const { city, routeId, routeName } = route.params;
  const [loading, setLoading] = useState(true);
  const [trips, setTrips] = useState<Trip[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [selectedTrip, setSelectedTrip] = useState<string | null>(null);

  useEffect(() => {
    loadRouteDetails();
  }, []);

  const loadRouteDetails = async () => {
    setLoading(true);
    setError(null);
    try {
      const routeDetails = await fetchRouteDetails(routeId, city);
      setTrips(routeDetails);
      if (routeDetails.length > 0) {
        setSelectedTrip(routeDetails[0].trip_id);
      }
    } catch (err) {
      console.error('Error loading route details:', err);
      setError('Failed to load route details. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleViewOnMap = () => {
    const trip = trips.find(t => t.trip_id === selectedTrip);
    if (trip && trip.shape_id) {
      navigation.navigate('RouteMap', {
        city,
        shapeId: trip.shape_id,
        routeName
      });
    }
  };

  const renderStopItem = ({ item, index }: { item: any; index: number }) => (
    <View style={styles.stopItem}>
      <View style={styles.stopSequence}>
        <Text style={styles.stopSequenceText}>{item.sequence}</Text>
      </View>
      <View style={styles.stopContent}>
        <Text style={styles.stopName}>{item.name}</Text>
        <Text style={styles.stopTime}>
          {item.arrival ? `Arrival: ${item.arrival}` : ''}
          {item.arrival && item.departure ? ' | ' : ''}
          {item.departure ? `Departure: ${item.departure}` : ''}
        </Text>
      </View>
    </View>
  );

  const selectedTripData = trips.find(trip => trip.trip_id === selectedTrip);

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.headerTitle}>Route {routeName} Details</Text>
      </View>
      
      {loading ? (
        <View style={styles.loadingContainer}>
          <ActivityIndicator size="large" color="#0066cc" />
          <Text style={styles.loadingText}>Loading route details...</Text>
        </View>
      ) : error ? (
        <View style={styles.errorContainer}>
          <Text style={styles.errorText}>{error}</Text>
          <TouchableOpacity style={styles.button} onPress={loadRouteDetails}>
            <Text style={styles.buttonText}>Retry</Text>
          </TouchableOpacity>
        </View>
      ) : trips.length === 0 ? (
        <View style={styles.emptyContainer}>
          <Text style={styles.emptyText}>No details found for this route.</Text>
        </View>
      ) : (
        <View style={styles.contentContainer}>
          {trips.length > 1 && (
            <View style={styles.tripSelector}>
              <Text style={styles.selectorLabel}>Select Trip:</Text>
              <FlatList
                data={trips}
                horizontal
                showsHorizontalScrollIndicator={false}
                renderItem={({ item }) => (
                  <TouchableOpacity
                    style={[
                      styles.tripItem,
                      selectedTrip === item.trip_id && styles.selectedTripItem
                    ]}
                    onPress={() => setSelectedTrip(item.trip_id)}
                  >
                    <Text 
                      style={[
                        styles.tripItemText,
                        selectedTrip === item.trip_id && styles.selectedTripItemText
                      ]}
                    >
                      Trip {item.trip_id.slice(-4)}
                    </Text>
                  </TouchableOpacity>
                )}
                keyExtractor={(item) => item.trip_id}
              />
            </View>
          )}
          
          {selectedTripData && selectedTripData.shape_id && (
            <TouchableOpacity 
              style={styles.mapButton}
              onPress={handleViewOnMap}
            >
              <Text style={styles.mapButtonText}>View Route on Map</Text>
            </TouchableOpacity>
          )}
          
          <Text style={styles.stopsTitle}>Stops</Text>
          
          {selectedTripData && (
            <FlatList
              data={selectedTripData.stops}
              renderItem={renderStopItem}
              keyExtractor={(item, index) => `${item.stop_id}-${index}`}
              contentContainerStyle={styles.stopsList}
            />
          )}
        </View>
      )}
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  header: {
    backgroundColor: '#0066cc',
    padding: 16,
    alignItems: 'center',
  },
  headerTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: 'white',
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  loadingText: {
    marginTop: 16,
    fontSize: 16,
  },
  errorContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 16,
  },
  errorText: {
    fontSize: 16,
    color: 'red',
    marginBottom: 16,
    textAlign: 'center',
  },
  emptyContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 16,
  },
  emptyText: {
    fontSize: 16,
    color: '#666',
    textAlign: 'center',
  },
  contentContainer: {
    flex: 1,
    padding: 16,
  },
  tripSelector: {
    marginBottom: 16,
  },
  selectorLabel: {
    fontSize: 16,
    fontWeight: '600',
    marginBottom: 8,
  },
  tripItem: {
    backgroundColor: '#e0e0e0',
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderRadius: 16,
    marginRight: 8,
  },
  selectedTripItem: {
    backgroundColor: '#0066cc',
  },
  tripItemText: {
    fontSize: 14,
    color: '#333',
  },
  selectedTripItemText: {
    color: 'white',
  },
  mapButton: {
    backgroundColor: '#4CAF50',
    paddingVertical: 12,
    borderRadius: 8,
    alignItems: 'center',
    marginBottom: 16,
  },
  mapButtonText: {
    color: 'white',
    fontSize: 16,
    fontWeight: 'bold',
  },
  stopsTitle: {
    fontSize: 18, 
    fontWeight: 'bold',
    marginBottom: 8,
  },
  stopsList: {
    paddingBottom: 16,
  },
  stopItem: {
    flexDirection: 'row',
    backgroundColor: 'white',
    borderRadius: 8,
    marginBottom: 8,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.1,
    shadowRadius: 2,
    elevation: 1,
    overflow: 'hidden',
  },
  stopSequence: {
    backgroundColor: '#0066cc',
    width: 40,
    alignItems: 'center',
    justifyContent: 'center',
  },
  stopSequenceText: {
    color: 'white',
    fontWeight: 'bold',
  },
  stopContent: {
    flex: 1,
    padding: 12,
  },
  stopName: {
    fontSize: 16,
    fontWeight: '500',
  },
  stopTime: {
    fontSize: 14,
    color: '#666',
    marginTop: 4,
  },
  button: {
    backgroundColor: '#0066cc',
    paddingHorizontal: 24,
    paddingVertical: 12,
    borderRadius: 8,
  },
  buttonText: {
    color: 'white',
    fontSize: 16,
    fontWeight: 'bold',
  },
});

export default RouteDetailScreen;