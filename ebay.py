import requests
import urllib.request
import urllib.parse
import PIL
import re
import configparser
import json
from PIL import Image
from ebaysdk.trading import Connection as Trading
from ebaysdk.exception import ConnectionError
from yaml import load
from PyQt5.QtWidgets import QMessageBox


class EbaySeller:

    def __init__(self):
        self.api = Trading()
        config = configparser.ConfigParser()
        config.read('config.ini')
        with open('details.yaml', 'r') as file:
            self.yaml_config = load(file)

    def upload_card(self, card_name, eu_card_price, us_card_price, card_id):
        if us_card_price != 0:
            card_price = us_card_price * 0.8
        else:
            card_price = eu_card_price
        if card_price < 1:
            card_price = 1
        card_price = str(round(card_price, 2))
        try:
            card_image = 'http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid=' + card_id + '&type=card'
        except:
            self.msg = QMessageBox()
            self.msg.setWindowTitle("Upload Failed")
            self.msg.setText("Upload Failed, wizards gatherer error")
            self.msg.setStandardButtons(QMessageBox.Ok)
            self.msg.exec()
        urllib.request.urlretrieve(card_image, 'temp.jpg')
        # Resize card
        base_height = 500
        img = Image.open('temp.jpg')
        height_percent = (base_height / float(img.size[1]))
        wsize = int((float(img.size[0]) * float(height_percent)))
        img = img.resize((wsize, base_height), PIL.Image.ANTIALIAS)
        img.save('temp.png')
        # Upload to PictShare
        files = {'file': open('temp.png', 'rb')}
        try:
            r = requests.post('https://pictshare.net/api/upload.php', files=files)
        except:
            self.msg = QMessageBox()
            self.msg.setWindowTitle("Upload Failed")
            self.msg.setText("Upload Failed, PictShare error")
            self.msg.setStandardButtons(QMessageBox.Ok)
            self.msg.exec()
        print(r)
        r = r.text
        r = json.loads(r)
        print(r)
        r = r['url']
        # Fix using regular expression, may not be needed at a later date
        r = re.sub('\\.net', '.net/', r)
        r = re.sub('\\.net//', '.net/', r)
        print(r)
        try:
            image = self.api.execute('UploadSiteHostedPictures', {'ExternalPictureURL': r})
            image = image.dict()
            image = image['SiteHostedPictureDetails']['FullURL']

            print(image)
            # Upload to ebay
            response = self.api.execute('AddFixedPriceItem', {
                'Item': {'Title': card_name + ' MTG - NM/M', 'Description': card_name + ' MTG - NM/M',
                         'Quantity': '1', 'PictureDetails': {'PictureURL': image},
                         'ReturnPolicy': {'ReturnsAcceptedOption': 'ReturnsNotAccepted'}, 'DispatchTimeMax': '3',
                         'ConditionID': '1000', 'StartPrice': card_price, 'PostalCode': self.yaml_config["PostalCode"],
                         'Currency': self.yaml_config["Currency"],
                         'Country': 'GB', 'ListingDuration': 'Days_30', 'PaymentMethods': 'PayPal',
                         'PayPalEmailAddress': self.yaml_config["PayPalEmailAddress"],
                         'PrimaryCategory': {'CategoryID': '38292'},
                         'ShippingDetails': {'ShippingType': 'Flat',
                                             'ShippingServiceOptions': {'ShippingServicePriority': '1',
                                                                        'ShippingService': self.yaml_config[
                                                                            "ShippingService"],
                                                                        'ShippingServiceCost': '1'}}}})
            print(response.dict())
            print(response.reply)

            self.msg = QMessageBox()

            if response.reply.Ack == 'Failure':
                self.msg.setWindowTitle("Upload Failed")
                self.msg.setText("Upload Complete, please check log.txt")
                self.msg.setStandardButtons(QMessageBox.Ok)
                with open('log.txt', 'a+') as log_file:
                    log_file.write(response.reply)
            else:
                self.msg.setWindowTitle("Upload Complete")
                self.msg.setText("Upload Complete, please check your ebay account to confirm")
                self.msg.setStandardButtons(QMessageBox.Ok)

            self.msg.exec()
        except ConnectionError as e:
            print(e)
            print(e.response.dict())

    def get_multiverse_id(self, name):
        try:
            name = re.sub(' ', '%20', name)
            r = requests.get('https://api.scryfall.com/cards/named?exact=' + name)
            r = json.loads(r.text)
            return r['multiverse_ids'][0]
        except:
            self.msg = QMessageBox()
            self.msg.setWindowTitle("Upload Failed")
            self.msg.setText("Upload Failed, scryfall error")
            self.msg.setStandardButtons(QMessageBox.Ok)
            self.msg.exec()



    def get_card_info_and_sell(self, name):
        try:
            multiverse_id = self.get_multiverse_id(name)
            r = requests.get('http://api.cardsearch.nl/v1/prices?key=W00dw0rk$&mids[]=' + str(multiverse_id))
            r = json.loads(r.text)
            r = r[0]
            card_name = r.get('name')
            eu_card_price = r.get('price_normal')
            us_card_price = r.get('us_normal')
            card_set = r.get('set_id')
            card_set_name = r.get('set_name')
            card_id = r.get('multiverse_id')

            # Display card info in CLI
            print('Name: ' + card_name)
            print('Set: ' + card_set)
            print('Set name: ' + card_set_name)
            print('Card ID: ' + str(card_id))
            self.upload_card(card_name, eu_card_price, us_card_price, card_id)
        except:
            self.msg = QMessageBox()
            self.msg.setWindowTitle("Upload Failed")
            self.msg.setText("Upload Failed, card name not valid")
            self.msg.setStandardButtons(QMessageBox.Ok)
            self.msg.exec()
