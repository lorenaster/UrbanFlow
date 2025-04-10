import axios from 'axios';
import { getAgencyIdByCity } from '../constants/agency_data';
const API_BASE_URL = 'http://192.168.0.153:8000';

export interface Route {
    route_id: string;
    short_name: string;
    long_name: string;
    type: number;
    color?: string;
    text_color?: string;
  }
  
  export interface Trip {
    trip_id: string;
    shape_id: string;
    stops: {
      stop_id: string;
      name: string;
      sequence: number;
      arrival?: string;
      departure?: string;
    }[];
  }
  
  export interface RouteShape {
    shape_id: string;
    points: {
      lat: number;
      lng: number;
      sequence: number;
    }[];
    stops?: {
      stop_id: string;
      name: string;
      lat: number;
      lng: number;
      sequence: number;
    }[];
  }

  export const fetchRoutesByTown = async (town: string, city: string): Promise<Route[]> => {
    try {
      const agencyId = getAgencyIdByCity(city);
      if (!agencyId) {
        throw new Error(`City ${city} is not supported`);
      }
  
      const response = await fetch(`${API_BASE_URL}/agencies/${agencyId}/routes?town=${encodeURIComponent(town)}`);
      
      if (!response.ok) {
        throw new Error(`API request failed with status ${response.status}`);
      }
      
      const data = await response.json();
      return data.routes;
    } catch (error) {
      console.error('Error fetching routes:', error);
      throw error;
    }
  };
  export const fetchRouteDetails = async (routeId: string, city: string): Promise<Trip[]> => {
    try {
      const agencyId = getAgencyIdByCity(city);
      if (!agencyId) {
        throw new Error(`City ${city} is not supported`);
      }
  
      const response = await fetch(`${API_BASE_URL}/agencies/${agencyId}/routes/${routeId}/trips`);
      
      if (!response.ok) {
        throw new Error(`API request failed with status ${response.status}`);
      }
      
      const data = await response.json();
      return data.trips;
    } catch (error) {
      console.error('Error fetching route details:', error);
      throw error;
    }
  };

  export const fetchRouteShape = async (shapeId: string, city: string): Promise<RouteShape> => {
    try {
      const agencyId = getAgencyIdByCity(city);
      if (!agencyId) {
        throw new Error(`City ${city} is not supported`);
      }
  
      const response = await fetch(`${API_BASE_URL}/agencies/${agencyId}/shapes/${shapeId}`);
      
      if (!response.ok) {
        throw new Error(`API request failed with status ${response.status}`);
      }
      
      const data = await response.json();
      return data.shape;
    } catch (error) {
      console.error('Error fetching route shape:', error);
      throw error;
    }
  };