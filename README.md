## Safety Culture Data Visualization
This project is used to better visualize the massive amount of data that Safety Culture generates every day. 
It is a dashboard that will display useful insights about templates and audits. It is going to use differents
graphs, charts, and maps.

## Motivation
**why?** We started this project as an internship project, with the original problem given being...
> Seeking a team of smart and motivated JCU students to help us make sense of our data.
We have tens of thousands of inspections in our SafetyCulture iAuditor account, but no idea how to make sense of them all. We know we have interesting business insights in our data, but we have no idea where to start.
Jimmy down in accounts has an Excel spreadsheet, but he's on leave and no one knows how it works. The company CEO is coming in four weeks time and we need to wow her with something special.
If you have what it takes to extract, analyse and visualise large amounts of data and turn them into interesting business insights, apply right now, we need you!
>

It took some time and a few failed ideas before we finally settled on an idea that we believed would work best.

## Build status
Very early stages of development. no versions or releases 

## Code
- python
- dash 
- dash html
 
## Screenshots
The main dashboard once logged into an account
![Dashboard](static/dashboard.PNG?raw=true "Optional Title")
The login page
![Login page](static/login.PNG?raw=true "Optional Title")

## Tech/framework used
<b>Built with</b>
- [Flask](https://www.fullstackpython.com/flask.html)
- [Pycharm](https://www.jetbrains.com/pycharm/)
- [AWS](https://aws.amazon.com/getting-started/tutorials/launch-an-app/)
- [Dash](https://dash.plot.ly/)
- [iAuditorAPI](https://developer.safetyculture.io/#inspection-items)

<b>With help from</b>
- [Github](https://github.com/)
- [Postman](https://www.getpostman.com/)
- [Trello](https://trello.com/)
- [Slack](https://slack.com/intl/en-au/)
- [PyCharm](https://www.jetbrains.com/pycharm/)


## Features
- actively updates as new audits are created (under development)
- only calls to the API for new audits, for faster responses (under development)
- displays a map with each audit as a point, that is colored to its percentage completed (under development)
- will display other graphs and charts with relevant data, that can be personalised (under development)

## Code Example
We have our code properly layered, to where all that is in the main application is this
```ruby
from flaskr import create_app

application = create_app()

if __name__ == "__main__":
    application.run()
```
We have 1 dash application, that has multiple layouts that it builds into one dashboard
```ruby
layout = html.Div([
    header, map_health_bar, average_scores_percentages, audit_duration_failed_audits
])
```
We use aggregate functions to get specific information from our database, like so.
```ruby
pipeline = [
        {
            '$project': {
                'score_percentage': "$audit_data.score_percentage",
                'within_start_date': {'$gte': [{'$dateFromString': {'dateString': '$modified_at'}}, start_datetime]},
                'within_end_date': {'$lte': [{'$dateFromString': {'dateString': '$modified_at'}}, end_datetime]}
            }

        },
        {
            '$match': {
                'within_start_date': True,
                'within_end_date': True
            }
        },
        {
            "$group": {
                '_id': None,
                'avg_score_percentage': {
                    '$avg': "$score_percentage"
                }
            }
        },
        {
            '$project': {
                '_id': 0,
                'avg_score_percentage': 1
            }

        }
    ]
```
## Installation
pip install (all of the packages in the requirements.txt)
Then you are ready to run

## How to use?
Once packages have been installed, run from application.py.
This will open a new local server for you to open in your browser.
If running on something like AWS ( elastic beanstalk ), it will automatically recognise which folder to run.
create an account and use an API token from iAuditor API, referenced above.

## Credits
[Matthew Lewandowski](https://www.linkedin.com/in/matthew-lewandowski93/)  
[Nathan Marson](https://www.linkedin.com/in/nathan-marson/)  
[Joshua Gale](https://www.linkedin.com/in/joshua-j-gale/)
