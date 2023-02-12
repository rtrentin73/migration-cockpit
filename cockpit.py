from flask import Flask, request, render_template, redirect, url_for
import google.auth
from googleapiclient.discovery import build
from oauth2client.client import OAuth2WebServerFlow

credential = None

# Create a Flask app
app = Flask(__name__)

# Option 1: Setup Identity
def get_federated_credentials():
    global credential
    credential, project = google.auth.default()
    return credential

# Option 2: Setup Project
def list_projects():
    service = build('cloudresourcemanager', 'v1', credentials=credential)
    request = service.projects().list()
    projects = {}
    while request is not None:
        response = request.execute()
        for project in response['projects']:
            projects[project['projectId']] = project['name']
        request = service.projects().list_next(previous_request=request, previous_response=response)
    return projects

# # Option 3: Setup Network
def list_networks(project_id):
    service = build('compute', 'v1', credentials=credential)
    request = service.networks().list(project=project_id)
    response = request.execute()
    networks = response.get("items", [])
    return networks

# Option 4: Discover Routes
def get_routes(service, project_id, network_url):
    result = service.routes().list(project=project_id, filter="network eq '{}'".format(network_url)).execute()
    routes = [{'name': route['name'], 'destination': route['destRange'], 'priority': route['priority'],
               'nextHopInstance': route.get('nextHopInstance'), 'nextHopIp': route.get('nextHopIp'),
               'nextHopNetwork': route.get('nextHopNetwork'), 'nextHopVpnTunnel': route.get('nextHopVpnTunnel'),
               'nextHopGateway': route.get('nextHopGateway'),
               'tags': route.get('tags', [])} for route in result['items']]
    return routes

# Route for the main menu
@app.route('/')
def index():
    return render_template('index.html')

# Route for option 1: Setup Identity
@app.route('/option1')
def option1():
    return render_template('option1.html')

# Route for option 2: Setup Project
@app.route("/option2", methods=["GET", "POST"])
def option2():
    if request.method == "POST":
        project_id = request.form["project_id"]
        return redirect(url_for("option3", project_id=project_id))
    else:
        projects = list_projects()
        return render_template("option2.html", projects=projects)

# Route for option 3: Setup Network
@app.route("/option3/<project_id>", methods=["GET", "POST"])
def option3(project_id):
    if request.method == "GET":
        networks = list_networks(project_id)
        return render_template("option3.html", project_id=project_id, networks=networks)
    elif request.method == "POST":
        network = request.form.get("network")
        return redirect(url_for("option4", project_id=project_id, network_url=network))

# Route for option 4: Discover Routes
@app.route("/option4")
def option4():
    project_id = request.args.get("project_id")
    network_url = request.args.get("network_url")
    service = build('compute', 'v1', credentials=credential)
    routes = get_routes(service, project_id, network_url)
    return render_template('option4.html', project_id=project_id, network_url=network_url, routes=routes)

@app.route('/option5', methods=['GET', 'POST'])
def option5():
    if request.method == 'POST':
        target = request.form['target']
        return redirect(url_for('index'))
    else:
        return render_template('option5.html')

@app.route('/option6')
def option6():
    return render_template('option6.html')

if __name__ == "__main__":
    app.run(debug=True)

