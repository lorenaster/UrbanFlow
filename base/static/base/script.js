//VIZUALIZARE RUTE

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


//CONFIGURARE TRASEU

//set timer for autocomplete
function debounce(fn, delay) {
    let timeoutId;
    return function (...args) {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => fn.apply(this, args), delay);
    };
}

//autocomplete function
document.addEventListener("DOMContentLoaded", () => {
    const geocodeUrl = "/configurare-trasee/autocomplete/";

    function setupAutocomplete(inputId, listId) {
        const input = document.getElementById(inputId);
        const list = document.getElementById(listId);

        input.addEventListener('input', debounce( async () => {
            const query = input.value;
            if (query.length < 3) {
                list.innerHTML = '';
                return;
            }

            try {
                const response = await fetch(`${geocodeUrl}?text=${encodeURIComponent(query)}`);
                const data = await response.json();
                console.log(data); // for debugging

                list.innerHTML = '';
                if (data.features) {
                    data.features.forEach(feature => {
                        const li = document.createElement('li');
                        li.textContent = feature.properties.label;
                        li.addEventListener('click', () => {
                            input.value = feature.properties.label;
                            input.setAttribute("data-coords", feature.geometry.coordinates.join(','));
                            list.innerHTML = '';
                        });
                        list.appendChild(li);
                    });
                }
            } catch (err) {
                console.error("Autocomplete error:", err);
            }
        }, 500));
    }

    setupAutocomplete("start-location", "autocomplete-start");
    setupAutocomplete("end-location", "autocomplete-end");
});

document.getElementById('route-form').addEventListener('submit', (event) => {
    console.log('Form submitted!');
});