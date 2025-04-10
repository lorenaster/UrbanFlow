// screens/HomeScreen.tsx
import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, ActivityIndicator, SafeAreaView, Image } from 'react-native';
import { getCurrentLocation } from '../services/locationService';
import { StackNavigationProp } from '@react-navigation/stack';
import { RootStackParamList } from '../navigation/types';
import { getAllCities } from '../constants/agency_data';

type HomeScreenProps = {
  navigation: StackNavigationProp<RootStackParamList, 'Home'>;
};

const HomeScreen: React.FC<HomeScreenProps> = ({ navigation }) => {
  const [loading, setLoading] = useState(true);
  const [city, setCity] = useState<string | null>(null);
  const [town, setTown] = useState<string | null>(null);
  const [isSupported, setIsSupported] = useState(false);

  useEffect(() => {
    detectLocation();
  }, []);

  const detectLocation = async () => {
    setLoading(true);
    try {
      const { city, town, isSupported } = await getCurrentLocation();
      setCity(city);
      setTown(town);
      setIsSupported(isSupported);
    } catch (error) {
      console.error('Failed to get location:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleViewRoutes = () => {
    if (city && town) {
      navigation.navigate('Routes', { city, town });
    }
  };

  if (loading) {
    return (
      <SafeAreaView style={styles.container}>
        <View style={styles.loadingContainer}>
          <ActivityIndicator size="large" color="#0000ff" />
          <Text style={styles.loadingText}>Detecting your location...</Text>
        </View>
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.headerContainer}>
        <Text style={styles.title}>UrbanFlow</Text>
        <Text style={styles.subtitle}>Your Public Transit Companion</Text>
      </View>

      <View style={styles.locationContainer}>
        <Text style={styles.locationLabel}>Current Location:</Text>
        <Text style={styles.locationText}>
          {town ? town : 'Unknown'}{city ? `, ${city}` : ''}
        </Text>

        {isSupported ? (
          <Text style={styles.supportedText}>✓ Your city is supported!</Text>
        ) : (
          <Text style={styles.unsupportedText}>✗ Your city is not supported</Text>
        )}

        {!isSupported && (
          <Text style={styles.supportedCitiesText}>
            Supported cities: {getAllCities().join(', ')}
          </Text>
        )}
      </View>

      <View style={styles.buttonContainer}>
        <TouchableOpacity
          style={[styles.button, !isSupported && styles.buttonDisabled]}
          onPress={handleViewRoutes}
          disabled={!isSupported}
        >
          <Text style={styles.buttonText}>View Routes</Text>
        </TouchableOpacity>

        <TouchableOpacity
          style={styles.refreshButton}
          onPress={detectLocation}
        >
          <Text style={styles.refreshButtonText}>Refresh Location</Text>
        </TouchableOpacity>
      </View>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
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
  headerContainer: {
    alignItems: 'center',
    padding: 24,
    backgroundColor: '#0066cc',
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: 'white',
  },
  subtitle: {
    fontSize: 16,
    color: 'rgba(255, 255, 255, 0.8)',
    marginTop: 4,
  },
  locationContainer: {
    padding: 16,
    margin: 16,
    backgroundColor: 'white',
    borderRadius: 8,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 2,
  },
  locationLabel: {
    fontSize: 16,
    fontWeight: '600',
    marginBottom: 8,
  },
  locationText: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 8,
  },
  supportedText: {
    fontSize: 16,
    color: 'green',
    marginTop: 8,
  },
  unsupportedText: {
    fontSize: 16,
    color: 'red',
    marginTop: 8,
  },
  supportedCitiesText: {
    fontSize: 14,
    color: '#666',
    marginTop: 8,
  },
  buttonContainer: {
    padding: 16,
    marginHorizontal: 16,
  },
  button: {
    backgroundColor: '#0066cc',
    paddingVertical: 12,
    borderRadius: 8,
    alignItems: 'center',
  },
  buttonDisabled: {
    backgroundColor: '#cccccc',
  },
  buttonText: {
    color: 'white',
    fontSize: 18,
    fontWeight: 'bold',
  },
  refreshButton: {
    marginTop: 16,
    paddingVertical: 12,
    alignItems: 'center',
  },
  refreshButtonText: {
    color: '#0066cc',
    fontSize: 16,
  },
});

export default HomeScreen;