# Queenroxxanes
The Auction House System provides an interface for handling auction house functions from item acquisition to completion of an auction to storing auction history for retroactive reflection. Managers supervise the approval, addition, and removal of items and employees. Curators oversee the acquisition of new items. Auctioneers lead the starting, managing, and ending of auctions. Bidders are able to place bids on items of open auctions.


# Setup
 * first run ```python3 -m venv ./auctionhouse``` from the root folder to set up the appropriate files in that folder
 * Run the appropriate startup script for your system - https://docs.python.org/3/library/venv.html#creating-virtual-environments for reference
 * After starting it, run ```pip install -r requirements.txt``` in the auctionhouse directory to install the prerequisites
 * Set your FLASK_APP environment variable to auctionhouse/app.py if you are running the app from the root directory

This is the backend and will be used for Flask, pymongo, etc.

Start the React app by navigating into auctionhouse-frontend
 * run npm install to install the prerequisite packages
 * run npm start to launch the React frontend
