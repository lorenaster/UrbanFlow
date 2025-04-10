// screens/RouteMapScreen.tsx
import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet, ActivityIndicator, SafeAreaView, TouchableOpacity } from 'react-native';
import { RouteProp } from '@react-navigation/native';
import { StackNavigationProp } from '@react-navigation/stack';
import { RootStackParamList } from '../navigation/types';
import MapView, { Polyline, Marker, PROVIDER_GOOGLE } from 'react-native-maps';
import { fetchRouteShape, RouteShape } from '../services/apiService';

type RouteMapScreenProps = {
  navigation: StackNavigationProp<RootStackParamList, 'RouteMap'>;
  route: RouteProp<RootStackParamList, 'RouteMap'>;
};

const RouteMapScreen: React.FC<RouteMapScreenProps> = ({ navigation, route }) => {
  const { city, shapeId, routeName } = route.params;
  const [loading, setLoading] = useState(true);
  const [routeShape, setRouteShape] = useState<RouteShape | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadRouteShape();
  }, []);

  const loadRouteShape = async () => {
    setLoading(true);
    setError(null);
    try {
      const shapeData = await fetchRouteShape(shapeId, city);
      setRouteShape(shapeData);
    } catch (err) {
      console.error('Error loading route shape:', err);
      setError('Failed to load route map. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const getInitialRegion = () => {
    if (!routeShape || !routeShape.points || routeShape.points.length === 0) {
      return {
        latitude: 47.1585, 
        longitude: 27.6014,
        latitudeDelta: 0.05,
        longitudeDelta: 0.05,
      };
    }
    let minLat = routeShape.points[0].lat;
    let maxLat = routeShape.points[0].lat;
    let minLng = routeShape.points[0].lng;
    let maxLng = routeShape.points[0].lng;

    routeShape.points.forEach(point => {
      minLat = Math.min(minLat, point.lat);
      maxLat = Math.max(maxLat, point.lat);
      minLng = Math.min(minLng, point.lng);
      maxLng = Math.max(maxLng, point.lng);
    });

    const centerLat = (minLat + maxLat) / 2;
    const centerLng = (minLng + maxLng) / 2;
    

    const latDelta = (maxLat - minLat) * 1.2;
    const lngDelta = (maxLng - minLng) * 1.2;

    return {
      latitude: centerLat,
      longitude: centerLng,
      latitudeDelta: Math.max(latDelta, 0.02),
      longitudeDelta: Math.max(lngDelta, 0.02),
    };
  };

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <TouchableOpacity style={styles.backButton} onPress={() => navigation.goBack()}>
          <Text style={styles.backButtonText}>← Back</Text>
        </TouchableOpacity>
        <Text style={styles.headerTitle}>Route {routeName} Map</Text>
        <View style={styles.placeholder} />
      </View>
      
      {loading ? (
        <View style={styles.loadingContainer}>
          <ActivityIndicator size="large" color="#0066cc" />
          <Text style={styles.loadingText}>Loading route map...</Text>
        </View>
      ) : error ? (
        <View style={styles.errorContainer}>
          <Text style={styles.errorText}>{error}</Text>
          <TouchableOpacity style={styles.button} onPress={loadRouteShape}>
            <Text style={styles.buttonText}>Retry</Text>
          </TouchableOpacity>
        </View>
      ) : !routeShape || !routeShape.points || routeShape.points.length === 0 ? (
        <View style={styles.emptyContainer}>
          <Text style={styles.emptyText}>No route data available to display on map.</Text>
        </View>
      ) : (
        <View style={styles.mapContainer}>
          <MapView
            style={styles.map}
            provider={PROVIDER_GOOGLE}
            initialRegion={getInitialRegion()}
          >
            <Polyline
              coordinates={routeShape.points.map(point => ({
                latitude: point.lat,
                longitude: point.lng,
              }))}
              strokeColor="#0066cc"
              strokeWidth={4}
            />
            
            {routeShape.stops?.map((stop, index) => (
                <Marker
                    key={`stop-${index}`}
                    coordinate={{ latitude: stop.lat, longitude: stop.lng }}
                    title={stop.name}
                    description={`Stop #${stop.sequence}`}
                    pinColor={index === 0 ? 'green' : index === (routeShape.stops?.length || 0) - 1 ? 'red' : 'blue'}
                />
                ))}
          </MapView>
          
          <View style={styles.legend}>
            <View style={styles.legendItem}>
              <View style={[styles.legendColor, { backgroundColor: 'green' }]} />
              <Text style={styles.legendText}>Start</Text>
            </View>
            <View style={styles.legendItem}>
              <View style={[styles.legendColor, { backgroundColor: 'blue' }]} />
              <Text style={styles.legendText}>Stop</Text>
            </View>
            <View style={styles.legendItem}>
              <View style={[styles.legendColor, { backgroundColor: 'red' }]} />
              <Text style={styles.legendText}>End</Text>
            </View>
          </View>
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
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    padding: 16,
  },
  headerTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: 'white',
  },
  backButton: {
    paddingVertical: 4,
    paddingHorizontal: 8,
  },
  backButtonText: {
    color: 'white',
    fontSize: 16,
  },
  placeholder: {
    width: 40, 
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
  mapContainer: {
    flex: 1,
    position: 'relative',
  },
  map: {
    ...StyleSheet.absoluteFillObject,
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
  legend: {
    position: 'absolute',
    bottom: 16,
    right: 16,
    backgroundColor: 'white',
    padding: 8,
    borderRadius: 8,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.2,
    shadowRadius: 4,
    elevation: 4,
  },
  legendItem: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 4,
  },
  legendColor: {
    width: 16,
    height: 16,
    borderRadius: 8,
    marginRight: 8,
  },
  legendText: {
    fontSize: 14,
  },
});

export default RouteMapScreen;