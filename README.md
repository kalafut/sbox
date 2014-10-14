sbox allows you to use


Goals
=====

* Secure
* Works on port 80
* Portable

Assumptions
===========
* A hash will be the SHA256 hash of the data
* All data will be binary (i.e. not converted to hex or other more readable formats)

Theory
======

* Client and Server have a shared key ("Server Key")
* All data between client and server is encrypted with shared key
* Clients have a key that is common to all clients, but isn't stored on the server ("Client Key").
* All file contents and path names will be encrypted with the Client Key prior to transmission

Server Operations
=================
* `get_object`
* `put_object`
* `delete_object`
* `get_object_list`

Objects
=======
An object consists of:

Unencrypted Elements:
* ID
* Data Hash ("Hash")

Encrypted Elements:
* Path
* Data

ID
--
Object IDs are the hash of the full path and filename. Leading and trailing white-space will be trimmed. Path separators will be converted to forward slashes on Windows systems. Case is significant.

Data Hash
----------------
The Data Hash or "Hash" of an object will the the hash of the uncompressed and unencrypted file's contents.

Path
----
Path will be the full path and filename. This string is identical to the one used to generated ID.

Data
----
Data will be the compressed file data.

Sync logic
==========
The client must store the last Hash ("common hash") for each file that was common with the server.  At the start of sync, a the hash of every client file is computed and the object list is requested from the server.

* If an object ID exists only on the server, the client will `get` it.
* If an object ID exists only on the client, the client will `put` it.
* If an object ID exists on both the client and server and it will be resolved so:

break

    if server_hash != client_hash:
        if client_hash != common_hash && server_hash == common_hash:
            put client object
        if client_hash == common_hash && server_hash != common_hash:
            get server object
        if client_hash != common_hash && server_hash != common_hash:
            get server object and mark as duplicate
