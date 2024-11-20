# Minimal Example: Use Dask from a Jupyter Notebook

This is a minimal example of how to use Dask from a Jupyter Notebook making use
of the Dask Operator.

## Access the Dask Dashboard

The [Dask dashboard](https://docs.dask.org/en/latest/dashboard.html) can be
very helpful for debugging Dask code. This web UI is provided by the scheduler
pod of the Dask cluster. To view the dashboard in a web browser, a port
forwarding connection must first be established from the scheduler pod to your
local machine.

### Steps to Access the Dashboard:

1. **Identify the Scheduler Pod:**  
   First, find the scheduler pod. For example, you can use the following
   command:  

   ```sh
   kubectl get pods -n <your-namespace> | grep scheduler
   ```
2. Start Port Forwarding:
   Use the pod name obtained from the previous step to
   start port forwarding. Run the following command, replacing
   <scheduler-pod-name> with the actual name of the scheduler pod:

   ```sh
   kubectl port-forward <scheduler-pod-name> 8787:8787
   ```
3. Access the Dashboard:
   Once port forwarding is active, the Dask dashboard will be accessible in
   your browser at: [http://localhost:8787](http://localhost:8787)
