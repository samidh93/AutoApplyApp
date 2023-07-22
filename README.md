# soft_linkedin_easyAutoApply_Api
web app to automate search and apply for jobs. 

## What Is This App About?
The web application aims to help users (candidate looking for jobs) to automate the job search and send applications in one place.
The goal of the app is to automate the job application process on most common platforms such linkedin, indeed and stepstone ...
The vision is to relief humans from repeting the same tasks such filling forms, writing emails to each and every job to apply for. the automation of this process will help reduce the time consumed on this task and organise the following processes such as interview meeting, resume enhancement, matching quotation and skills aquirements ..

## Architecture:

      +------------------------+
      |       UI Frontend      |
      +------------------------+
                    |
             REST API Requests/responses
                    |
      +------------------------+
      |     Django Backend     |
      +------------------------+
                    |
            Interacts with (core direct integration or via grpc)
                    |
      +------------------------+
      |     Core Backend       |
      +------------------------+

## Core Backend
the core backend is where the algorithmic part is defined. it is based on a microservice architecture. 
The microservices are listed below:

1- job Link microservice: the role of this service is to collect all links based on user search keywords and store then in a database. example storage is under data/links.csv

2- job build microservice: the role of this service is to create  job database links based on the links from the first service. example file is under data/jobs.csv

3- email apply microservice: the role of this service is to send email application to jobs from the jobs database.

4- direct apply microservice: the role of this service is to fill extern form application to jobs from the jobs database.

5- easy apply microservice: the role of this service is to fill easy apply form  application from the jobs database.

## Django Backend
the Django backend define where the interaction between the core backend and the frontend requests happens. it is based on a django framework. main tasks is data handling (databases), requests handling etc..
To handle respt api, django rest is also needed.

## UI Frontend
the UI Frontend define client side of the app, basicly where the interaction happens with user.
main tasks are ui routing, displaying content and user interaction, requests forwarding etc..
the ui is created via online tool like .bubble, flutterflow, webflow to generate the necessary html, css and javascripts files.


## Features and AI
### AI 

one of the major feature is to integrate AI to increase candidate chance for application process.
- AI Resume creator: using AI, the candidate resume can be most adapted to the job requirements. A suitable resume can help pass the prescreening Tool used by company select candidates. This feature will generate automaticly a new Resume based on job requirement and current Resume. If the candidate current resume is not suitable for a job or list of jobs, the candidate will be notified about the missing skills across the jobs. 
- AI Email generator: 

- AI Interview Manager: 
## Free and Premium Plans
The first goal of this App is to help around the world find their dream job and relief them from a repetetive annoying tasks such as sending email and filling forms for each and every job.
Therefore a Free plan to use the App is mandatory.

### Free Plan 
The Free plan considers max 20 applications per day.
The Free plan's duration is 7 days. 
To extend the free plan, either the user is required to select one of the premium plans (described below) or by succefully inviting a new candidate to register on the App using his secret code.

### Premium Plans
The Free plan is itself good enough to get applications sent and potentially land a good interview followed by a job offer. 
The premium plans exist to offer upgrades to the free plan. If the user wishes extra number of applications per day, AI integration and skills enhancement, the premium plans shall accomplish it.
- premium silver: up to 50 applications per day
- premium platinium: up to 100 applic per day, AI resume creator, AI Email generator
- premium gold: up to 500 applic per day, AI resume creator, AI Email generator,  AI Interview Manager

The pricing in general depends on the user region. 