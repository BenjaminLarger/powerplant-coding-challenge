# powerplant-coding-challenge

## How to launch the program

1. Build the docker-compose from the root of the project using **`make`**.

2. Send a POST request to the productionplan endpoint via **`make send-request1`**, **`make send-request2`**, or **`make send-request3`**. These requests correspond to the data provided in the subject, but you can also personalize your own payload by editing those files and executing the corresponding command (**`make send-request<n>`** sends **`payload<n>`** POST request).