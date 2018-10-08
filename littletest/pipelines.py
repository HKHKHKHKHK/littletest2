
import json

class Pipeline_ToJson(object):

        
    def open_spider(self, spider):
        self.file = open('data.json', 'w',encoding='utf-8')


    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item

    def close_spider(self, spider):
        self.file.close()