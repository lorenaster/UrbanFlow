import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import { RootStackParamList } from './navigation/types';

// Import screens
import HomeScreen from './screens/homeScreen';
import RoutesScreen from './screens/routeScreen';
import RouteDetailScreen from './screens/routeDetailScreen';
import RouteMapScreen from './screens/routeMapScreen';

const Stack = createStackNavigator<RootStackParamList>();

const AppNavigator = () => {
  return (
    <NavigationContainer>
      <Stack.Navigator
        initialRouteName="Home"
        screenOptions={{
          headerShown: false,
          cardStyle: { backgroundColor: '#f5f5f5' }
        }}
      >
        <Stack.Screen name="Home" component={HomeScreen} />
        <Stack.Screen name="Routes" component={RoutesScreen} />
        <Stack.Screen name="RouteDetail" component={RouteDetailScreen} />
        <Stack.Screen name="RouteMap" component={RouteMapScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
};

export default AppNavigator;