# crypto-currency
The intention of this repository is to display abilities for Full Stack Python developer job positions,
The topic of the repository is Crypto-currency as is a topic that everyone is familiarize nowadays, the
repository uses Kraken API to load Open-High-Low-Close data from Kraken top 6 coins (by market capitalization).
is not intended to be used on a live server, the main objective is for possible companies to inspect 
the code with the following guidelines and certify that the candidate has enough abilities to start the 
abilities assessment process. 

Please follow recommendations below to assess abilities.

1 - KraKen-frontend: this directory contains a react app developed by TDD methodology.
It uses Jest and React hooks to implement component that fetches data and displays it on a table and 
a form component to upload data, note it uses eslint-config-airbnb.

2 - crypto_rest: this directory contains a Django app intended to show abilities for
django/django rest framework, TDD, developed with design patters, Abstract base classes,
Object Oriented Programming.

2.1 - crypto_data: Django rest framework Design with generic views and Serializers.

2.2 - crypto_rest: Django settings directory.

2.3 - data_display: Develop script with command line options to display crypto currency data.

2.4 - data_loader: Load data from Kraken API and save it into a Postgresql database, uses TDD, Abstract
base classes, design patterns.