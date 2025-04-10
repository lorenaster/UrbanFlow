export type RootStackParamList = {
    Home: undefined;
    Routes: { city: string; town: string };
    RouteDetail: { city: string; routeId: string; routeName: string };
    RouteMap: { city: string; shapeId: string; routeName: string };
  };