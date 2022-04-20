# SmartJar

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![version](https://img.shields.io/badge/version-1.0-blue)](https://github.com/sak007/SmartJar/releases/tag/v1.0)
[![DOI](https://zenodo.org/badge/469118048.svg)](https://zenodo.org/badge/latestdoi/469118048)
[![GitHub issues](https://img.shields.io/github/issues/sak007/SmartJar)](https://github.com/sak007/SmartJar/issues?q=is%3Aopen+is%3Aissue)
[![GitHub closed issues](https://img.shields.io/github/issues-closed/sak007/SmartJar)](https://github.com/sak007/SmartJar/issues?q=is%3Aissue+is%3Aclosed)
[![Github pull requests](https://img.shields.io/github/issues-pr/sak007/SmartJar)](https://github.com/sak007/SmartJar/pulls)
[![Github closed pull requests](https://img.shields.io/github/issues-pr-closed/sak007/SmartJar)](https://github.com/sak007/SmartJar/pulls?q=is%3Apr+is%3Aclosed)

# Setup Instructions

## Hardware Setup

### What You’ll Need For This Project 

1. Jar with a non-conductive body and a conductive lid
2. 5 Kg Load Cell - Used in the scale to measure load
3. SparkFun Load Cell Amplifier - Amplifies the load cell signal and communicates with the Pi
4. 2 Wooden Plates for the Scale - Connect with the load cell to produce a scale
5. 2 5V 50N Hold Strength Magnets - Holds the jar lid in contact with the jar when powered
6. 5V Power Adaptor - Powers the magnets through the relay
7. Relay - Controlled by Pi to connect 5V supply to the magnets
8. Raspberry Pi 
9. Aluminum Foil and Wire Contact sensors for the Lid on Jar and Jar on Scale
10. Alarm/LED - Activated by Pi when the lid is forcibly opened or the child took more than the approved quantity.

### BOM

1) Jar - [link](https://www.amazon.com/dp/B0969WVW8M?ref=ppx_yo2ov_dt_b_product_details&th=1)
2) Alamscn 5 Kg Load Cell - [link](https://www.amazon.com/dp/B08KRWY43Y?ref=ppx_yo2ov_dt_b_product_details&th=1)
3) SparkFun HX711 Load Cell Amplifier - [link](https://www.amazon.com/dp/B079LVMC6X?psc=1&ref=ppx_yo2ov_dt_b_product_details)
4) 50N 5V Magnet - [link](https://www.amazon.com/dp/B01CYB0G24?psc=1&ref=ppx_yo2ov_dt_b_product_details)
5) 5V Power DC Power Adaptor - [link](https://www.amazon.com/dp/B078RXZM4C?psc=1&ref=ppx_yo2ov_dt_b_product_details)
6) KeeYees Relay - [link](https://www.amazon.com/gp/product/B07L6J6FHH/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1)

### Alternates:

7) 250N 24V Magnet - [link](https://www.amazon.com/dp/B01N21QDQC?psc=1&ref=ppx_yo2ov_dt_b_product_details)
8) 24V DC Power Adaptor - [link](https://www.amazon.com/dp/B08MQ2KM2N?ref=ppx_yo2ov_dt_b_product_details&th=1)

### Schematic
![image](https://user-images.githubusercontent.com/46975667/164135086-226d8538-8a4b-4966-9674-841a2dd3733a.png)

## Software Setup
### Bot
 - Create an account in IBM Watson IoT platform and register your device ([ibmcloudpi](https://github.com/usmanwardag/ibmcloudpi)).
 - Generate api_token for bot.
   + Download and install the Telegram mobile application or desktop application for your system from the following site: https://desktop.telegram.org/
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
