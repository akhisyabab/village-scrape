from flask import Blueprint, render_template, request, flash, redirect, url_for

from project.scraper.nomor_net.nomor_net_scraper import NomornetScraper
from project.scraper.nomor_net2.nomor_net2_scraper import Nomornet2Scraper

scraper_blueprint = Blueprint('scraper', __name__)

get_class_source = {
    'nomornet': NomornetScraper,
    'nomornet2': Nomornet2Scraper,
}

@scraper_blueprint.route('/fetch', methods=['GET', 'POST'])
def fetch():
    try:
        if 'fetcher' not in request.args:
            return 'Fetcher not found'
        fetcher = request.args['fetcher']
        if fetcher not in get_class_source:
            return 'fetcher unlisted'

        get_class_source[fetcher].scraper()

        return {
            'message': '{} fetched'.format(fetcher),
            'status': 'success',
        }, 200
        
    except Exception:
        raise

 # df = DataFrame(datas, columns=datas.keys())
 # df.to_csv('data_desa.csv', index=None, header=True)     