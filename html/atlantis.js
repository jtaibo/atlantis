
function on_load() {
  var console = document.getElementById("console");
  console.innerHTML = "on_load()";
  query_status();  
}

function query_status() {

  var console = document.getElementById("console");

  console.innerHTML = "1";
  var request = new XmlRpcRequest("http://atlantis:8000/AtlantisRPC", "get_status");
  var response;
  try {
    response = request.send();
    var connection = document.getElementById("connection");
    connection.innerHTML = "CONNECTED";
    connection.style.backgroundColor = "green";
  }
  catch(err) {
    console.innerHTML = "ERROR contacting XMLRPC server : \n" + err.message;
    var connection = document.getElementById("connection");
    connection.innerHTML = "DISCONNECTED";
    connection.style.backgroundColor = "red";
  }
}


function toggleRelay(ch) {
  // To-Do
  console.innerHTML= "Sending XMLRPC request";

  var request = new XmlRpcRequest("http://atlantis:8000/AtlantisRPC", "toggle_relay");
  request.addParam( ch );
  var response = request.send();
  var answer = document.getElementById("response");
//  answer.innerHTML = response.xmlData;
  answer.innerHTML = response.parseXML();
}


// Button callbacks

function button_filter() {
}

function button_fluorescent() {
}

function button_air() {
}
