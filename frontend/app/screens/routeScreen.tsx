// screens/RoutesScreen.tsx
import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet, FlatList, TouchableOpacity, ActivityIndicator, SafeAreaView } from 'react-native';
import { RouteProp } from '@react-navigation/native';
import { StackNavigationProp } from '@react-navigation/stack';
import { RootStackParamList } from '../navigation/types';
import { fetchRoutesByTown, Route } from '../services/apiService';

type RoutesScreenProps = {
  navigation: StackNavigationProp<RootStackParamList, 'Routes'>;
  route: RouteProp<RootStackParamList, 'Routes'>;
};

const RoutesScreen: React.FC<RoutesScreenProps> = ({ navigation, route }) => {
  const { city, town } = route.params;
  const [loading, setLoading] = useState(true);
  const [routes, setRoutes] = useState<Route[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadRoutes();
  }, []);

  const loadRoutes = async () => {
    setLoading(true);
    setError(null);
    try {
      const routesData = await fetchRoutesByTown(town, city);
      setRoutes(routesData);
    } catch (err) {
      console.error('Error loading routes:', err);
      setError('Failed to load routes. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleRoutePress = (route: Route) => {
    navigation.navigate('RouteDetail', { 
      city, 
      routeId: route.route_id,
      routeName: route.short_name
    });
  };

  const renderRouteItem = ({ item }: { item: Route }) => {
    // Convert hex color to a valid color string
    const routeColor = `#${item.color || 'FFFFFF'}`;
    const textColor = `#${item.text_color || '000000'}`;
    
    const getRouteTypeIcon = (type: number) => {
      switch (type) {
        case 0: return '🚆';
        case 1: return '🚇'; 
        case 2: return '🚄'; 
        case 3: return '🚌'; 
        case 4: return '⛴️'; 
        case 5: return '🚋'; 
        case 6: return '🚠'; 
        case 7: return '🚡'; 
        default: return '🚌';
      }
    };

    return (
      <TouchableOpacity 
        style={[styles.routeItem, { backgroundColor: routeColor }]}
        onPress={() => handleRoutePress(item)}
      >
        <View style={styles.routeIconContainer}>
          <Text style={styles.routeIcon}>{getRouteTypeIcon(item.type)}</Text>
        </View>
        <View style={styles.routeInfo}>
          <Text style={[styles.routeNumber, { color: textColor }]}>{item.short_name}</Text>
          <Text style={[styles.routeName, { color: textColor }]}>{item.long_name}</Text>
        </View>
      </TouchableOpacity>
    );
  };

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.headerTitle}>Routes in {town}</Text>
      </View>
      
      {loading ? (
        <View style={styles.loadingContainer}>
          <ActivityIndicator size="large" color="#0066cc" />
          <Text style={styles.loadingText}>Loading routes...</Text>
        </View>
      ) : error ? (
        <View style={styles.errorContainer}>
          <Text style={styles.errorText}>{error}</Text>
          <TouchableOpacity style={styles.retryButton} onPress={loadRoutes}>
            <Text style={styles.retryButtonText}>Retry</Text>
          </TouchableOpacity>
        </View>
      ) : routes.length === 0 ? (
        <View style={styles.emptyContainer}>
          <Text style={styles.emptyText}>No routes found for this location.</Text>
          <TouchableOpacity style={styles.retryButton} onPress={loadRoutes}>
            <Text style={styles.retryButtonText}>Refresh</Text>
          </TouchableOpacity>
        </View>
      ) : (
        <FlatList
          data={routes}
          renderItem={renderRouteItem}
          keyExtractor={(item) => item.route_id}
          contentContainerStyle={styles.listContainer}
        />
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
  retryButton: {
    backgroundColor: '#0066cc',
    paddingHorizontal: 24,
    paddingVertical: 12,
    borderRadius: 8,
  },
  retryButtonText: {
    color: 'white',
    fontSize: 16,
    fontWeight: 'bold',
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
    marginBottom: 16,
    textAlign: 'center',
  },
  listContainer: {
    padding: 16,
  },
  routeItem: {
    flexDirection: 'row',
    marginBottom: 12,
    borderRadius: 8,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 2,
    overflow: 'hidden',
  },
  routeIconContainer: {
    justifyContent: 'center',
    alignItems: 'center',
    width: 48,
    backgroundColor: 'rgba(0,0,0,0.1)',
    paddingVertical: 12,
  },
  routeIcon: {
    fontSize: 24,
  },
  routeInfo: {
    flex: 1,
    padding: 12,
  },
  routeNumber: {
    fontSize: 18,
    fontWeight: 'bold',
  },
  routeName: {
    fontSize: 14,
    marginTop: 4,
  },
});

export default RoutesScreen;