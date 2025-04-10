import * as Location from 'expo-location';
import { Alert } from 'react-native';
import { getAgencyIdByCity } from '../constants/agency_data';

export interface LocationResult {
  city: string | null;
  town: string | null;
  isSupported: boolean;
}

export const getCurrentLocation = async (): Promise<LocationResult> => {
  try {

    const { status } = await Location.requestForegroundPermissionsAsync();
    
    if (status !== 'granted') {
      Alert.alert('Permission Denied', 'Location permission is required to show routes in your area.');
      return { city: null, town: null, isSupported: false };
    }

    const location = await Location.getCurrentPositionAsync({});
    const { latitude, longitude } = location.coords;

    const addressInfo = await Location.reverseGeocodeAsync({ latitude, longitude });
    
    if (addressInfo && addressInfo.length > 0) {
      const { city, subregion } = addressInfo[0];
      const town = subregion || city || '';
      

      const isSupported = city ? !!getAgencyIdByCity(city) : false;
      
      return { city: city || null, town, isSupported };
    }
    
    return { city: null, town: null, isSupported: false };
  } catch (error) {
    console.error('Error getting location:', error);
    return { city: null, town: null, isSupported: false };
  }
};