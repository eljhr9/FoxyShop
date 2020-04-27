# FoxyShop
View website: https://foxyshop.herokuapp.com/

# Description
FoxyShop is a Django online store created for portfolio.


# Screenshot
![FoxyShop](https://i.imgur.com/7t1FJOF.png)

## Features
This store is based on Django version 2.2.10 and the PostgreSQL database. Here is a list of all the features and technologies used in this project:
- To work with registered users and register new ones, the built-in django authentication system is used
- Third-party APIs (Google, Facebook) are used to authenticate the user
- Product search is carried out by solr search platform
- Shopping cart and product comparison made using django sessions
- A coupon system has also been introduced, a сoupon «foxy» gives a 30% discount on order
- Celery and RabbytMQ are used to send email messages asynchronously
- AWS is used to store media files
- There is a bonus system, for each purchase, registered users receive bonuses depending on the amount of the order
- Configured internationalization and localization using GNU gettext
- The project has 2 translations (Russian and English), you can change the language in "..." menu [Change Language](https://i.imgur.com/AlccuXi.png)

## Author

(C) 2020 Illya Redkolis.
illyaredkolis@gmail.com
