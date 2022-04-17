# SmartJar

## Setup Instructions

### Bot
 - Generate api_token for bot.
   + Download and install the Telegram desktop application for your system from the following site: https://desktop.telegram.org/
   + Once you login to your Telegram account, search for "BotFather" in Telegram. Click on \"Start\" --> enter the following command: ```/newbot```
   + Follow the instructions on screen and choose a name for your bot. Post this, select a username for your bot that ends with "bot" (as per the instructions on your Telegram screen)
   + BotFather will now confirm the creation of your bot and provide a TOKEN to access the HTTP API - copy this token.

 - Update the ```api_token``` in ```properties.json```
 - Update Device info in ```properties.json```
 - Add ```orgId```, ```typeId```, ```deviceId``` and ```token``` in ```device.yaml```
 - Add ```appId```, ```key``` and ```token``` in ```application.yaml```
 - Run ```bash setup.sh``` or ```./setup.sh``` to install prerequisites.
 - For Windows, follow this [link](http://wkhtmltopdf.org/) to install wkhtmltopdf.
 - Run ```bash startBot.sh``` or ```./startBot.sh``` from root directory to start the bot.

### Jar
 - Update Device info in ```properties.json```
 - Add ```orgId```, ```typeId```, ```deviceId``` and ```token``` in ```device.yaml```
 - Run ```bash setup.sh``` or ```./setup.sh``` to install prerequisites.
 - For Windows, follow this [link](http://wkhtmltopdf.org/) to install wkhtmltopdf.
 - Run ```bash startJar.sh``` or ```./startJar.sh``` from root directory to start the jar.
