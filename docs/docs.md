# Documentation:
Are are given some words about the architecture.

### Orchestration
The orchestration is designed between a set Remote devices and a centralized Django web server, through a REST API.


#### States
Each device internally tracks a state, which can be:

- Free;
The device is ready to execute the next task, is going to do so by asking the list of the next tasks and calling the begin endpoint.
- Execution;
The execution of the task is happening right now, it can success or fail.
If success, the success endpoint is called, the task is set in the complete state. 
If fails, instead, the fail endpoint is called, the task is set to available. In both cases the device state is set to free.
- Offline;
The device is allowed to go offline, and then go back online. In any case the backend sets a timeout, which is considered by both parties, and once passed, sets the device to free and the task to available.

Instead, each task have a state between: 

- Available;
The task is ready to be requested by a device.
- Executing;
A device already requested the task and is in charge for its execution; if the timeout spires, the task is set to available.
- Completed;
The task was completed and its results are available.

Here is drawn a simple orchestration workflow through the use of the Petri Nets formalism:
![](/docs/pnet_v3.1.png)

In order to represent a Petri net as a workflow, the places START and END are added, and also two transactions, respectively, this is usual during the design phase and is needed in order to apply the verification tools which guarantees no deadlocks. Here was used [WoPeD 3.6.0](http://woped.dhbw-karlsruhe.de/woped/?page_id=22) as a verification tool.

### Queue management
The django_q library is used to implement the feature for the task timeouts. This library allows to configure separate (django_q) tasks that will be executed separately and asynchronously with regard to the http responses.
In particular the issued task is to change the (rbroker) task's state in the database once the 20 seconds timeout spires, by doing so its state is set to available.