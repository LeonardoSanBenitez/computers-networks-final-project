// console.log("hello world");

function updateMeasures() {
    var url = window.location.href + '/measures';
    var params = {
        method: "POST"
    };

    // src: https://stackabuse.com/using-fetch-to-send-http-requests-in-javascript/
    fetch(url, params)
    .then(res => res.json())
    .then(json => {
        console.log(json);
        
        // TODO: specify the measures units 
        document.getElementById('temperature').innerHTML = json.temperature + " ºC";
        document.getElementById('pressure').innerHTML    = json.pressure + " p";
        document.getElementById('humidity').innerHTML    = json.humidity;

    });
}

updateMeasures();
setInterval(updateMeasures, 1000 * 60); // in miliseconds