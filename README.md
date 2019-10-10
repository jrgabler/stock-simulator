
# Stock Simulator Proposal
## Summary
A simulated stock trading application implementing the multiple realtime and historical stock APIs to execute simulated user trades versus the NYSE and NASDAQ in real time. Users are able to set a starting amount of virtual money and execute trades as if it was the actual Stock Market.

## Goals
To create a web application that allows users to simulate real-time stock trading with virtual money.  The application will have the following features:


* A login system that will store and track the user’s information as well as their trades.

* Enable the buying and selling of stocks with virtual money, and track the profits / losses made through trading. Users are able to set a starting amount and track their losses and gains over time.

* Allow users to add a limited amount of stocks to a watchlist. This list will show up on the homepage with a chart depicting the changes at a glance in the stock over time. A user also may add or remove stocks to the watchlist at anytime.

* Generate a report that analyzes the user’s trading habits, investments and owned assets. 

## Stakeholders
Stakeholders include:

* Individuals interested in learning how the stock market operates and how to execute a trade.


* Individuals interested in experimenting with stocks without real consequences since Virtual Money is used


* The team itself as we are juggling this project in addition to additional classes, work, and extracurriculars.


* Professor McQuaid since he assigned the project to the team members and will have to provide a grade. He will also need to understand how to successfully run our project on his local machine in order to correctly grade the project.

* Our team manager will have the additional responsibility of ensuring that all team members are contributing equally to the project while managing his other classes and extracurriculars.


* Individuals who may want to provide financial advice to their clients or customers by  using the program to explain the ins and outs of the Stock Market. These individuals may refer additional stakeholders to the project for experimentation and learning.


## Scope
The scope of this project involves creating a polished and responsive website, a system where users can buy and sell stocks with virtual money, and generate a report that will analyze the user’s overall position. 

The project will not aim to provide financial advice or predict the changes in the Stock Market. The application is essentially a tool to simulate the Stock Market and allow users to experiment on their own. The application will not serve as an accurate source of information in regards to finances, but will strive to mimic the market as much as humanly possible.

## Input
We will be pulling from various finance and stock APIs to get the realtime and historical price of the stocks, the index, the stock symbol, and the time bought.

* User data from database
* Generated report data pulled from database
* Dynamic interaction with API


## Processing
Database queries will be run against historical user data, as well as searchable historical report data.

* Account total history
* Order history by order type
* Dividend history
* Historical data on orders, owned assets, and account valuation and dividends will be processed and displayed

* Stock Watchlist for individual users that will display changes over time.


## Output 
The program should simulate the process of performing basic market, limit, and stop orders, as well as sales, while tracking user’s total valuation. It should also generate and display some basic, high level reports, such as the most recent performance of any owned assets, as well as common stock market indices.

## Data Sources
1. Alpha Vantage - An API that allows users to pull real-time and historical stock data (5 API requests per minute and 500 requests per day)

2. Investor Exchange Trading API - unlimited real time stock API to enable automated trading (over 100 requests per second.)

3. Tradier API (60 request per minute.)

## Technology Stack
#### Front End
* Vanilla JavaScript
  * Our focus is mainly on the Database and Backend portion of the application since the project is for Database Application Development. We decided to stick with Vanilla JS in order to keep it simple as well as make sure any member can easily contribute.
* SASS
 * SASS is relatively  easy to learn and most members are comfortable with SASS 
* D3.js 
	* D3 is being used to help with data visualization on the front end
* Mobile first approach
	* In order to allow users to "trade on the go" like a game, the application will be designed and developed with a mobile first mindset and scaled to desktop

#### Back End
* Python
  * Developers on the team are comfortable programming in Python. Python provides a range of libraries that allow the team to meet the needs of the project.
  
#### Database
* PostgreSQL
  * PostgreSQL is a great open source option that provides features to protect data integrity, extensible, and a chance to explore a new type of relational database for most team members.

-------
Please refer to the project's Wiki in the upcoming weeks for up to date documentation. The Wiki will contain in-depth details of design patterns, architecture, roles, expectations, and more.
