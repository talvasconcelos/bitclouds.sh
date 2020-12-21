from flask import Flask, jsonify, request, current_app
import pymongo
import requests
import os
import datetime

dbclient = pymongo.MongoClient('localhost')
mongo_db = "tickets"
mongo = dbclient[mongo_db]

app = Flask(__name__)

app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.url_map.strict_slashes = False


def html(bolt):
    return """
    <!DOCTYPE html>
<html lang="en">
<title>support.bitclouds.sh - cloud support portal</title>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
<link rel="stylesheet" href="https://www.w3schools.com/lib/w3-theme-black.css">
<link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Roboto">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
<style>
html,body,h1,h2,h3,h4,h5,h6 {font-family: "Roboto", sans-serif;}
.w3-sidebar {
  z-index: 3;
  width: 250px;
  top: 43px;
  bottom: 0;
  height: inherit;
}
</style>
<body>

<!-- Navbar -->
<div class="w3-top">
  <div class="w3-bar w3-theme w3-top w3-left-align w3-large">
    <a class="w3-bar-item w3-button w3-right w3-hide-large w3-hover-white w3-large w3-theme-l1" href="javascript:void(0)" onclick="w3_open()"><i class="fa fa-bars"></i></a>
    <a href="#" class="w3-bar-item w3-button w3-theme-l1">support.bitclouds.sh</a>
    <a href="#" class="w3-bar-item w3-button w3-hide-small w3-hover-white">create a support ticket online</a>
  </div>
</div>

<!-- Sidebar -->
<nav class="w3-sidebar w3-bar-block w3-collapse w3-large w3-theme-l5 w3-animate-left" id="mySidebar">
  <a href="javascript:void(0)" onclick="w3_close()" class="w3-right w3-xlarge w3-padding-large w3-hover-black w3-hide-large" title="Close Menu">
    <i class="fa fa-remove"></i>
  </a>
  <h4 class="w3-bar-item"><b>resources</b></h4>
  <a class="w3-bar-item w3-button w3-hover-black" href="https://www.bitclouds.sh">www</a>
  <a class="w3-bar-item w3-button w3-hover-black" href="https://twitter.com/bitcoinsoftwar1">twitter</a>
  <a class="w3-bar-item w3-button w3-hover-black" href="https://t.me/s/BitClouds">telegram</a>
  <a class="w3-bar-item w3-button w3-hover-black" href="https://app.element.io/?pk_vid=1608239257ed7273#/room/#chat:matrix.bitclouds.sh">#chat:matrix.bitclouds.sh</a>
</nav>

<!-- Overlay effect when opening sidebar on small screens -->
<div class="w3-overlay w3-hide-large" onclick="w3_close()" style="cursor:pointer" title="close side menu" id="myOverlay"></div>

<!-- Main content: shift it to the right by 250 pixels when the sidebar is visible -->
<div class="w3-main" style="margin-left:250px">

  <div class="w3-row w3-padding-64">
    <div class="w3-twothird w3-container">
      <h1 class="w3-text-teal">submitted!t</h1>

    </div>
    <div class="w3-third w3-container">
      <p class="w3-border w3-padding-large w3-padding-32 w3-center">invoice will appear here</p>
    </div>
  </div>

  <footer id="myFooter">
    <div class="w3-container w3-theme-l2 w3-padding-32">
    </div>

    <div class="w3-container w3-theme-l1">
      <p>Powered by <a href="https://www.w3schools.com/w3css/default.asp" target="_blank">w3.css</a></p>
    </div>
  </footer>

<!-- END MAIN -->
</div>

<script>
// Get the Sidebar
var mySidebar = document.getElementById("mySidebar");

// Get the DIV with overlay effect
var overlayBg = document.getElementById("myOverlay");

// Toggle between showing and hiding the sidebar, and add overlay effect
function w3_open() {
  if (mySidebar.style.display === 'block') {
    mySidebar.style.display = 'none';
    overlayBg.style.display = "none";
  } else {
    mySidebar.style.display = 'block';
    overlayBg.style.display = "block";
  }
}

// Close the sidebar with the close button
function w3_close() {
  mySidebar.style.display = "none";
  overlayBg.style.display = "none";
}
</script>

</body>
</html>
    """


def generate_invoice(amount_sats, desc):
    dtime = datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d-%H%M%S')

    headers = {
        'X-Access': os.environ['SPARKO_RO'],
    }

    data = '{"method": "invoice",' \
           ' "params": ["' + str(amount_sats*1000) + '", "' + dtime + '-' + desc + '", "' + desc + '@bitclouds"]}'

    response = requests.post(os.environ['SPARKO_ENDPOINT'] + '/rpc', headers=headers, data=data, verify=False)

    return response.json()


@app.route('/ticket')
def handle_data():
    invoice = generate_invoice(99, str(request.values.get('instance'))+"-support")['bolt11']
    params = {
        'instance': request.values.get('instance'),
        'email': request.values.get('email'),
        'msg': request.values.get('msg'),
        'invoice': invoice

    }

    #return jsonify(params)
    #return current_app.send_static_file('reply.html')
    return html("test")


if __name__ == '__main__':
    app.run(debug=False, port=6677)
