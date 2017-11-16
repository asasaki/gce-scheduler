# GCE Scheduler

Start and stop GCE instances using App Engine's cron service

## Prerequisites

* python 2.7
* virtualenv
* Google Cloud SDK

## How to Deploy

1. Replace YOUR_PROJECT with your project id in app.yaml
2. Edit [cron.yaml](https://cloud.google.com/appengine/docs/standard/python/config/cronref) to set schedule to start and stop GCE instances.
3. Add labels (`gce-scheduler=startstop`) to the instances you want to start and stop on schedule
  * You can change key/value in app.yaml
4. Deploy App engine application

  ```
  virtualenv env
  source env/bin/activate
  pip install -t lib -U -r requirements.txt
  gcloud app deploy --version 1 app.yaml cron.yaml
  ```
