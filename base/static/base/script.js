function showRouteDetails(routeName) {
    // Find the route by its short name
    var data = routesData.find(route => route.route_short_name === routeName);  

    if (data) {
        // Display route details
        document.getElementById("route-details").innerHTML =
            `<h1>Ruta: ${data.route_short_name} -- ${data.route_long_name}</h1>`;
    } else {
        console.error("Route not found.");
    }
}
