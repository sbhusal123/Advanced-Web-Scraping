# Debugging Scrapy Spider
- [Docs](https://docs.scrapy.org/en/latest/topics/debug.html)

## i. Parse Command

**Usage Scenario**

- ``scrapy parse --spider=<spider_name> -c <callback_method> -d <depth> <item_url>``.

```text
Link A ---meta--> Link B -----meta---> Link C
```

Suppose our spider crawles the deep nested pages with links as shown above. 
But we want to test the **Link B** parsed items with specific metapassed from the LinkA.

**Example in case of countries spider:**
```python
class CountriesSpider(scrapy.Spider):
    name = 'countries'
    ...
    def parse_country(self, response):
        """Crawl country page"""
        name = response.request.meta['country_name'] # we need to pass country_name explicitly
        rows = response.xpath('(//table[@class="table table-striped table-bordered table-hover table-condensed table-list"])[1]/tbody/tr')
        for row in rows:
            year = row.xpath(".//td[1]/text()").get()
            population = row.xpath(".//td[2]/strong/text()").get()

            yield {
                'country_name': name,
                'year': year,
                'population': population
            }
    ...
```

``scrapy parse --spider=countries -c parse_country --meta='{"country_name": "China"}' https://www.worldometers.info/world-population/china-population/``

**Output:**
```bash
>>> STATUS DEPTH LEVEL 1 <<<
# Scraped Items  ------------------------------------------------------------
[{'country_name': 'China', 'population': '1,439,323,776', 'year': '2020'},
 {'country_name': 'China', 'population': '1,433,783,686', 'year': '2019'},
 {'country_name': 'China', 'population': '1,427,647,786', 'year': '2018'},
 {'country_name': 'China', 'population': '1,421,021,791', 'year': '2017'},
 {'country_name': 'China', 'population': '1,414,049,351', 'year': '2016'},
 {'country_name': 'China', 'population': '1,406,847,870', 'year': '2015'},
 {'country_name': 'China', 'population': '1,368,810,615', 'year': '2010'},
 {'country_name': 'China', 'population': '1,330,776,380', 'year': '2005'},
 {'country_name': 'China', 'population': '1,290,550,765', 'year': '2000'},
 {'country_name': 'China', 'population': '1,240,920,535', 'year': '1995'},
 {'country_name': 'China', 'population': '1,176,883,674', 'year': '1990'},
 {'country_name': 'China', 'population': '1,075,589,361', 'year': '1985'},
 {'country_name': 'China', 'population': '1,000,089,235', 'year': '1980'},
 {'country_name': 'China', 'population': '926,240,885', 'year': '1975'},
 {'country_name': 'China', 'population': '827,601,394', 'year': '1970'},
 {'country_name': 'China', 'population': '724,218,968', 'year': '1965'},
 {'country_name': 'China', 'population': '660,408,056', 'year': '1960'},
 {'country_name': 'China', 'population': '612,241,554', 'year': '1955'}]

# Requests  -----------------------------------------------------------------
```

## ii. Scrapy Shell
- Drops the context into the shell.

> Debug the situation when parse_details sometimes receives no item

```python
import scrapy
from scrapy.shell import inspect_response

class FooSpider(scrapy.Spider):
    ....
    ....

    def parse_details(self, response, item=None):
        if item:
            # populate more `item` fields
            return item
        else:
            inspect_response(response, self)
```

## iii. Open in Browser
- Opens the response in browser.

```python
from scrapy.utils.response import open_in_browser

class FooSpider(scrapy.Spider):
    ....
    ....

    def parse_details(self, response):
        if "item name" not in response.body:
            open_in_browser(response)
```