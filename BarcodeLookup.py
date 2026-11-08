import json
import urllib.error
import urllib.request

import zxingcpp
from PIL import Image, ImageOps

class BarcodeLookup:
    api_url = "https://world.openfoodfacts.org/api/v2/product/{barcode}.json?fields=product_name,product_name_ro,generic_name,nutriments"
    # Open Food Facts asks every client to identify itself
    user_agent = "calories_counter/1.0 (personal calorie tracker)"
    barcode_formats = zxingcpp.BarcodeFormat.EAN13 | zxingcpp.BarcodeFormat.EAN8 | zxingcpp.BarcodeFormat.UPCA | zxingcpp.BarcodeFormat.UPCE
    # phone photos are huge; this is plenty for a barcode and keeps decoding fast
    max_image_side = 2000

    @staticmethod
    def decode_barcode(image_file):
        image = Image.open(image_file)
        # phones store the rotation in EXIF instead of rotating the pixels
        image = ImageOps.exif_transpose(image).convert('L')
        image.thumbnail((BarcodeLookup.max_image_side, BarcodeLookup.max_image_side))

        results = zxingcpp.read_barcodes(image, formats=BarcodeLookup.barcode_formats)
        return results[0].text if results else None

    @staticmethod
    def lookup_product(barcode):
        """Returns a dict with the per 100g values from Open Food Facts (missing ones are None), or None if not found"""
        request = urllib.request.Request(BarcodeLookup.api_url.format(barcode=barcode),
                                         headers={'User-Agent': BarcodeLookup.user_agent})
        try:
            with urllib.request.urlopen(request, timeout=10) as response:
                data = json.load(response)
        except urllib.error.HTTPError as error:
            # the API answers 404 for unknown barcodes
            if error.code == 404:
                return None
            raise

        product = data.get('product')
        if data.get('status') != 1 or not product:
            return None

        nutriments = product.get('nutriments', {})

        calories = BarcodeLookup._get_value(nutriments, 'energy-kcal_100g')
        if calories is None:
            # some products only list the energy in kJ
            kilojoules = BarcodeLookup._get_value(nutriments, 'energy-kj_100g')
            calories = round(kilojoules / 4.184, 2) if kilojoules is not None else None

        return {'name': product.get('product_name_ro') or product.get('product_name') or product.get('generic_name') or '',
                'calories': calories,
                'protein': BarcodeLookup._get_value(nutriments, 'proteins_100g'),
                'fats': BarcodeLookup._get_value(nutriments, 'fat_100g'),
                'carbs': BarcodeLookup._get_value(nutriments, 'carbohydrates_100g')}

    @staticmethod
    def _get_value(nutriments, key):
        try:
            return round(float(nutriments[key]), 2)
        except (KeyError, TypeError, ValueError):
            return None
