# Prlmro_spider
## Web scrapper used to extract information about the deputies and senators from the Romanian Parliament website.


To run the spider, run the following commands:

```
virtualenv env

source ./env/bin/activate

pip install -r requirements.txt 

scrapy crawl prlmro_spider

deactivate

```