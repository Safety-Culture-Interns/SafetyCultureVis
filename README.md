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


## Tech/framework used
<b>Built with</b>
- [Pycharm](https://www.jetbrains.com/pycharm/)
- [AWS](https://aws.amazon.com/getting-started/tutorials/launch-an-app/)
- [Dash](https://dash.plot.ly/)
- [iAuditorAPI](https://developer.safetyculture.io/#inspection-items)

<b>With help from</b>
- [Github](https://github.com/)
- [Postman](https://www.getpostman.com/)
- [Trello](https://trello.com/)
- [Slack](https://slack.com/intl/en-au/)


## Features
- actively updates as new audits are created (under development)
- only calls to the API for new audits, for faster responses (under development)
- displays a map with each audit as a point, that is colored to its percentage completed (under development)
- will display other graphs and charts with relevant data, that can be personalised (under development)

## Code Example
One of the first things that needs to be done is making requests to the Safety Culture API, done like so...
```ruby
URL = "https://sandpit-api.safetyculture.io"  
HEADER = {'Authorization': 'Bearer *"this would be your access token"*'}
value == "audits" or value == "templates":  
request = requests.get(url="{}/{}/search".format(URL, value), headers=HEADER)
```
More to come
## Installation
still in development

## API Reference
still in development

## Tests
still in development

## How to use?
still in development

## Credits
[Matthew Lewandowski](https://www.linkedin.com/in/matthew-lewandowski93/)  
[Nathan Marson](https://www.linkedin.com/in/nathan-marson/)  
[Joshua Gale](https://www.linkedin.com/in/joshua-j-gale/)
