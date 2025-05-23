"""
This is the server file for the central server

It receives pings, and uses it with the location of nodes to calculate the location of the target.

This is the server file, it's a basic Flask server which creates an image

Functions:

    - ☑ Register | add a new or rebooted node to the network
        - Pings the dashboard and tells the user to add coordinates for the node. After coordinates are received adds node to the cache (timestamp 0) and nodes database (dont want nodes without coordinates being added to the math)

    - ☐ Target ping | a node tells the server it can ping the target
        - Takes the node id and the target_address from the node, and writes with the time to the cache

    - ☑ Config version | node requests the current config version
        - Returns the sha256 hash of the config file

    - ☐ Config | node requests the config file
        - Returns a file.read() of the config file

    - ☐ Config change | user changes the config file form the dashboard
        - Takes the new config parameters and writes them to the config file

    - ☐ Database change | user wants to change the coordinates of a node (submits the coordinates and ids for all nodes because I hate frontend)
        - Takes the ids and coordinates for the nodes and writes them to the database

"""

from flask import Flask, request, render_template, jsonify
import hashlib, csv, time

app = Flask(__name__)

global toAdd
toAdd=[]

# Destroy the existing node database and cache
#open('nodes.csv', 'w').close()
open('cache', 'w').close()

@app.route('/', methods=['GET'])
def index():
    # The index webpage with the real time map of the network
    number=1
    
    return render_template('index.html', number=number)

@app.route('/register', methods=['POST'])
def register():
    # For the nodes only, the form to actually register nodes on the is at /register_final

    global toAdd

    data = request.json
    id = data.get('id')

    # Add logic to make sure that submitted is a valid mac address here

    if id is not None and id not in toAdd:
        toAdd.append(id)
        return "Added"

    return "Failed"

@app.route('/register_final', methods=['POST'])
def register_final():
    # For the user submitted form

    global toAdd
    
    data = request.json

    id = data.get('id')
    data = data.get('data')

    x=data.split(",")[0].replace(" ", "")
    y=data.split(",")[0].replace(" ", "")

    """
    # This can be commented for debugging, but should be uncommented for production
    try:
        x=int(x)
        y=int(y)
    except:
        print("Not formatted correctly")
        return ''

    """

    toAdd.remove(id)

    print(id, x, y)

    # Write to the database

    with open("nodes.csv", mode='a', newline='') as file:
        writer = csv.writer(file)
        
        # Write the new row
        writer.writerow([id, x, y])

    # Write to the cache

    with open('cache', 'a') as file:
        file.write(f'{id} 0\n')

    return ''

@app.route('/ping', methods=['POST'])
def ping():

    # Test if the node is in the database, if not tell it to register

    # Node can ping the target
    data = request.get_json()

    id = data.get('id')
    ssid = data.get('ssid')  # This label should be changed so it can apply to bluetooth and wifi signals
    strength = data.get('strength')

    print(id, ssid, strength)

    # Add target filtering here, make nodes do this in the future but they need to load the config from the central server

    # Write to the cache

    with open("cache", "a") as file:
        file.write(f"{id} {strength} {time.time()}\n")
    
    return "Accepted"

@app.route('/config_version', methods=['GET'])
def config_version():
    # Returns the sha256sum of the config
    
    return hashlib.sha256(open('config', 'rb').read()).hexdigest()

@app.route('/config', methods=['GET'])
def config():
    # Returns the config

    return open('config').read()

@app.route('/config_change', methods=['POST'])
def config_change():
    # Changes the config

    # When the user clicks a button the current config is loaded into a form, and the user can edit stuff and hit submit, which sends the new config to this route

    target_address = request.args.get('target_address')
    le = request.args.get('le')
    config_update_wait = request.args.get('config_update_wait')
    clock_delay = request.args.get('clock_delay')

    # Load these new settings into the config

    return 

@app.route('/database_change', methods=['POST'])
def database_change():
    # Changes the config

    # When the user clicks a button the current database is loaded into a form, and the user can edit stuff and hit submit, which sends the new database to this route

    # Read the submitted list of nodes and coordinates

    # Load the new database into the database

    return 

@app.route('/check', methods=['GET'])
def check():

    global toAdd

    #print(toAdd)

    # I don't know whether the list of all of the nodes in toAdd should be returned or if toAdd[0] until toAdd is empty. I think the former would probably work better but I would need to change the frontend and I'm on a bus without internet access sp that's a future me promise

    response = []
    
    # The nodes aren't taking the title for title , so I need to 
    if len(toAdd) > 0:

        response = toAdd
        #toAdd.pop(0) #toAdd is all of the nodes which need to be added with coordinates
    
    return jsonify(response)

@app.route('/submit', methods=['POST'])
def submit():
    return "I don't think I need this method"


@app.route('/nt', methods=['GET'])
def notify():
    # The index webpage with the real time map of the network
    
    return render_template('notify.html')



if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")