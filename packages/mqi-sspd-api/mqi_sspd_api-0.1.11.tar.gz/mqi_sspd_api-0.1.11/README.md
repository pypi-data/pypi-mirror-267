# MQI Managing Module API

This is the official API made for the MQI biasing box. It allows you to interface
with the biasing box to set/read/update biases.

## Quickstart 

### Install pip package
Start of by installing the pip package write the following in your terminal window:

```
pip install mqi-sspd-api
```

Make sure you have python version higher than 3.0 installed (type python --version in 
a terminal window to make sure what version you have and updated it if needed).


Once you have the package installed you can start using the API! 

### Connecting to the bias box
Start by importing the api into your project. You will usually just work with the MQI
object.

```
from mqi.v1.api import MQI
m = MQI("ws://mqicontroller.local", "8080")
m.connect()
```

The biasing box and your local machine will communicate through a websocket served from the
biasing box. To intiate this connection
you will need to know the hostname of the bias box (this will usually be indicated by 
a sticker on the box itself). 

In example the above we have connected to the websocket at "mqicontroller.local" on port
"8080". The `m.connect() command will simply ping the server to make sure that the
connection is established correctly.

If you can run this without getting any error you have successfully connected and 
can start sending messages.

### Set a biasing current
To set a current you use the `setBias` function

```
m.setCurrent("3", "2")
```

This will set the bias on channel **3** to **2 mA**.

### Get a bias current
You can either get all the channels at once or just the channel that you request

```
# Get the bias of channel 3
m.getBias("3")

# Get all biases of arduino 0
m.getAllBias(0)
```

## Author
Filip Zlatoidsky

## License
MIT
