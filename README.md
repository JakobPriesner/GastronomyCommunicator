# GastronomyCommunicator
A communicator for catering establishments, where customers can call for service via a device at the table 

For starting, you have to start the server.py

After that, API calls can be made via the IP of the device on which the server was started.

<h1>GET</h1>

<h3>- /api/GET/_action_/_inf_</h3>
    _action_: until now only actions can be queried. Set the _action_ parameter to "action". <br />
        - _inf_: This parameter stands for the ID of the action to be queried. If you want to query all actions, set "*" for the parameter.

<h1>POST</h1>

<h3>- /api/POST/_action_</h3>
    _action_: either "addAction" or "completeAction", as the case may be <br />
        - _addAction_: expects a JSON format with the information "description" and "table_id". <br />
        - _completeAction_: expects a JSON format with the information "action_id".

<br /><br /><br /><br />
--> In the package client are sample clients for testing purposes