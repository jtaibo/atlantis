var buttons = ["filter", "fluorescent", "airpump", "heater"];
var refresh_period = 5000; // Refresh period in milliseconds

$(document).ready(
  function() {
    // Button events' functions  
    for( i=0 ; i < buttons.length ; i++ ) {
      $("#relays").append("<li><button class=\"relay\" id=\"button_" + buttons[i] + "\">" + buttons[i].toUpperCase() + "</button></li>");
      var function_body = "toggle_device(\"" + buttons[i] + "\");";
      $("#button_" + buttons[i]).click( Function(function_body) );
    }
    $("#button_stream").click( toggle_stream );
    {
      var ledstrip_id = 0;
      var function_body = "set_ledstrip_color(" + ledstrip_id + ");";
      $("#ledstrip_" + ledstrip_id + "_color").change( Function(function_body) );
    }
    query_status();
    setTimeout(refresh, refresh_period);
  }
);

function refresh() {
  query_status();
  setTimeout(refresh, refresh_period);
}

function update_page_contents(status) {
  $("#console").html(" status: " + JSON.stringify(status));
  if ( ! status ) {
    // Connection failure
    for( i=0 ; i < buttons.length ; i++ ) {
      $("#button_" + buttons[i]).css("background-color", "darkred");
    }
    $("#button_stream").css("background-color", "darkred");
  }
  else {
    for( i=0 ; i < buttons.length ; i++ ) {
      if ( status.relays[buttons[i]] ) {
        $("#button_" + buttons[i]).css("background-color", "green");
      }
      else {
        $("#button_" + buttons[i]).css("background-color", "gray");
      }
    }
    if ( status.streaming ) {
      $("#button_stream").css("background-color", "green");
    }
    else {
      $("#button_stream").css("background-color", "gray");
    }
    $("#air_temperature").html(status.sensors.air_temperature + " ºC");
    $("#air_humidity").html(status.sensors.air_humidity + " %");
    $("#water_temperature").html(status.sensors.water_temperature + " ºC");
    $("#water_ph").html(status.sensors.water_ph);
  }
}

function query_status() {
  try {
    $.xmlrpc({
      url: "http://atlantis:8000/AtlantisRPC",
      methodName: "get_status",
//      params: [],
      success: function(response, status, jqXHR) {
        connection_ok();
        update_page_contents(response[0]);
      },
      error: function(jqXHR, status, error) {
        $("#console").html("Error contacting XML-RPC server: " + error);
        connection_error();
        update_page_contents();
      }
    });
  }
  catch(err) {
    $("#console").html("ERROR contacting XMLRPC server");
    connection_error();
    update_page_contents();
  }
}

function connection_ok() {
  $("#connection").html("CONNECTED");
  $("#connection").css("background-color", "green");
}

function connection_error() {
  $("#connection").html("OFFLINE");
  $("#connection").css("background-color", "red");
}

function toggle_device(id) {
  try {
    $.xmlrpc({
      url: "http://atlantis:8000/AtlantisRPC",
      methodName: "toggle_device",
      params: [id],
      success: function(response, status, jqXHR) {
        update_page_contents(response[0]);
      },
      error: function(jqXHR, status, error) {
        $("#console").html("Error contacting XML-RPC server: " + error);
        connection_error();
        update_page_contents();
      }
    });
  }
  catch(err) {
    $("#console").html("ERROR contacting XMLRPC server");
    connection_error();
    update_page_contents();
  }
}

function toggle_stream() {
  try {
    $.xmlrpc({
      url: "http://atlantis:8000/AtlantisRPC",
      methodName: "toggle_stream",
      params: [],
      success: function(response, status, jqXHR) {
        update_page_contents(response[0]);
      },
      error: function(jqXHR, status, error) {
        $("#console").html("Error contacting XML-RPC server: " + error);
        connection_error();
        update_page_contents();
      }
    });
  }
  catch(err) {
    $("#console").html("ERROR contacting XMLRPC server");
    connection_error();
    update_page_contents();
  }
}

function hexToRgb(hex) {
  var bigint = parseInt(hex.replace("#", ""), 16);
  var color = {};
  color.r = (bigint >> 16) & 255;
  color.g = (bigint >> 8) & 255;
  color.b = bigint & 255;

  color.r /= 255.0;
  color.g /= 255.0;
  color.b /= 255.0;

  return color;
}

function set_ledstrip_color( id ) {
  rgb_color = hexToRgb( $("#ledstrip_" + id + "_color").val() );
  try {
    $.xmlrpc({
      url: "http://atlantis:8000/AtlantisRPC",
      methodName: "set_leds_color",
      params: [id, rgb_color],
      success: function(response, status, jqXHR) {
        update_page_contents(response[0]);
      },
      error: function(jqXHR, status, error) {
        $("#console").html("Error contacting XML-RPC server: " + error);
        connection_error();
        update_page_contents();
      }
    });
  }
  catch(err) {
    $("#console").html("ERROR contacting XMLRPC server");
    connection_error();
    update_page_contents();
  }
}
