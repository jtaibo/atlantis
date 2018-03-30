var xmlrpc_connection_ok = false;
var status_string;
var console;

function on_load() {
  console = document.getElementById("console");
  query_status();
}

function update_page_contents() {

  button_airpump = document.getElementById("button_airpump");

  status_obj = JSON.parse(status_string);

  if ( ! xmlrpc_connection_ok || ! status_obj || status_obj.faultCode ) {
    // Connection failure
    button_airpump.style.backgroundColor = "red"; 
  }
  else {
    if ( status_obj.relays[2] )
      button_airpump.style.backgroundColor = "green";
    else 
      button_airpump.style.backgroundColor = "gray";
  }
}

function query_status() {

  status_string = "";

  var connection = document.getElementById("connection");

  var request = new XmlRpcRequest("http://atlantis:8000/AtlantisRPC", "get_status");

  try {
    var response = request.send();
    var parsed_response = response.parseXML();

    if ( parsed_response.faultCode ) {
      connection.innerHTML = "CONNECTION ERROR";
      connection.style.backgroundColor = "red";
      console.innerHTML = parsed_response.faultString;
      xmlrpc_connection_ok = false;
    }
    else {
      connection.innerHTML = "CONNECTED";
      connection.style.backgroundColor = "green";
      status_string = JSON.stringify(parsed_response);
      xmlrpc_connection_ok = true;
    }
  }
  catch(err) {
    console.innerHTML = "ERROR contacting XMLRPC server : <br/>" + err.message;
    connection.innerHTML = "OFFLINE";
    connection.style.backgroundColor = "red";
    xmlrpc_connection_ok = false;
  }
  update_page_contents();
}


function toggleRelay(ch) {
  // To-Do
  if ( xmlrpc_connection_ok ) {
    console.innerHTML= "Sending XMLRPC request";
    var request = new XmlRpcRequest("http://atlantis:8000/AtlantisRPC", "toggle_relay");
    request.addParam( ch );
    var response = request.send();
  }
  query_status();
}


// Button callbacks

function toggle_filter() {
}

function toggle_fluorescent() {
}

function toggle_airpump() {
  toggleRelay(2);
}
