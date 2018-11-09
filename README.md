### Instructions to setup
Project run on docker compose with docker file so dependencies are 
 - docker-compose
 - docker (only for base debugging)

Run the application : `docker-compose up --build -d` or use stack for file `docker-compose.yml`

Application consists of following architecture
1. Gunicorn Server - For handling 4 * `(2 * [no. of CPUs] + 1)` concurrent requests
2. Flask  - For RestAPI endpoints
3. Celery, Redis - For long-running tasks (database query, import and export in our example)
4. MySQL - For Data storage of csv files and teams

Following Docker containers are composed 
1. Gunicorn server (running on 8081)+ Celery
2. Redis (running on 6379)
3. MySQL - 5.7 (running on 3306)
 
## RestAPI endpoints

Following are the UI interaction URLs
1. Upload CSV (example 1) : `http://localhost:8081/upload`
2. Bulk Team Upload (example 2) : `http://localhost:8081/team`
3. Export of data from database (example 3): `http://localhost:8081/export`

In Example 3, instead of loading data to interface, it creates a CSV file of export request with having control over the process like revoking the export request

## Upload specification

Goal of fail-safe and controllable file upload in ex 1 & 3 is done through sending data in parts.

From client side it sends data into small chunks and backend combines the chunks from its metadata for an ongoing upload.

Because of chunking files, we can 
   - Upload multiple files at the same time
   - Cancel any on-going upload
   - Pause/Resume/Restart any on-going upload

## Export Specification

To export data from database (example 2), client side sends a trigger(request) to server side to run data export task which might be a long running job.

In response, it sends the UID of task for further uses.

Now the client side keep checking the status of task and update it on UI. If user want to terminate a specific task, it can be revoked by just a click on `Cancel`. Once the task has completed, data will be dumped to a csv file then client will be able to download the file from server on a single click of  `Download`.

(Try out here - http://localhost:8081/export )

## General
1. Sample dummy files for upload are in the `data-sample` folder, at the root of the project
    > `data-sample/upload` consists sample data of example 1
    > `data-sample/team` consists sample data for example 3
2. I have taken very sparse data set which consists dates around 2017 and 2016. So for testing export requests, it's better to export for a range of 2016 - 2017
3. Root folder mostly consists of configuration files and the overall code structure follows open source standards of Flask Web Apps.

 
## Scalability Assurance
1. Gunicorn - Running `(2 * [no. of CPUs] + 1)` workers with 4 worker thread in each worker
2. Supervisor - Assuring auto recovery of server down/fail
3. Celery - Scaling long running task in background, can handle 20 parallel tasks (as of our configurations)

## Potential Issues
1. Server down/termination - Create state restore mechanism for rescheduling long-running tasks
2. Resource overflow - Setting up monitoring scripts/tools for making server safe from case of overflow (like memory overflow)
3. 
