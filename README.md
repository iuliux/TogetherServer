Together Server
===============

Server part of a collaborative editing system.

Destined for Sublime Text 2


The big picture
---------------

The system is designed to work around a central server which manages all the
files and sessions.

Clients are instances of the Sublime plugin. They only communicate with the
server.

This is nice because there is no need for getting the address of the owner of
the file, you can still work on some file even if the owner is not online.
Configs are done only on the first use.


Consistency Model
-----------------

The system guarantees *sequential consistency*. This means that all clients
will commit edits in the same order, although this order may vary from the
absolute cronological order of edits, due to different message propagation
times.


Current implementation
----------------------

The server runs on CherryPy, exposing a REST interface to the clients. This
seemed nice at first, but it turned out it doesn't play well for the 'realtime'
type of app.


The plan
--------

The plan now is to completely replace the server and change the communication
protocol from HTTP to (probably) WebSockets. Options are Node.js (which needs
complete reimplementation) or Tornado.
