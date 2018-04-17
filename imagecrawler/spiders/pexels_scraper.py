import scrapy
import re
from scrapy.linkextractor import LinkExtractor
from scrapy.selector import Selector
import requests
import os

class Global(object):
    img_path = "/mnt/c/Users/kimhe/Desktop/for-photos/downloaded_images/"
    img_name = "img"
    img_count = 1

class PexelsScraper(scrapy.Spider, Global):
    name = "pexels"    # Define spider

    # Define the regex we'll need to filter the returned links
    url_matcher = re.compile('^https:\/\/www\.pexels\.com\/photo\/')
    src_extractor = re.compile('src="([^"]*)"')
    tags_extractor = re.compile('alt="([^"]*)"')

    # Create a set that we'll keep track of ids we've crawled
    crawled_ids = set()

    # Bring a repeat section to execute
    def start_requests(self):   
        # Count the number of image files in selected directory and set the vaule
        Global.img_count = len(os.listdir(Global.img_path)) + 1

        url = "https://www.pexels.com/search/guys/"
        yield scrapy.Request(url, self.parse)

    # After Parsing the response, extract scrapted data and create a new request.
    def parse(self, response): 
        body = Selector(text=response.body)
        images = body.css('img.image-section__image').extract()
        # images is lists included of all tags of a class named 'img.image-section__image'

        # body.css().extract returns a list which might be empty
        for image in images:
            img_url = PexelsScraper.src_extractor.findall(image)[0]
            tags = [tag.replace(',', '').lower() for tag
                    in PexelsScraper.tags_extractor.findall(image)[0].split(' ')]
            img_type = str(img_url.split('/')[-1].split('.')[1].split('?')[0])

            # Set the full_path of a image file
            img_fullname = Global.img_name + str(Global.img_count) + img_type
            img_fullpath = Global.img_path + img_fullname
            # Download the image
            response = requests.get(img_url)
            with open(img_fullpath +'.'+ img_type, 'wb') as f:
                f.write(response.content)
            del response

            # Print the result to the console
            print(img_fullname, img_url, tags)
            Global.img_count = Global.img_count + 1

        link_extractor = LinkExtractor(allow=PexelsScraper.url_matcher)
        next_links = [link.url for link in link_extractor.extract_links(response)
                     if not self.is_extracted(link.url)]
        
        # Crawl the filtered links
        for link  in next_links:
            yield scrapy.Request(link, self.parse)

    def is_extracted(self, url):
        # Image urls are of type: https://www.pexels.com/photo/starry-sky-over-silhouette-of-trees-186599/
        id = int (url.split('/')[-2].split('-')[-1])

        if id not in PexelsScraper.crawled_ids:
            PexelsScraper.crawled_ids.add(id)
            return False
        return True