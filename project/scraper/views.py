from flask import Blueprint

from project.scraper.nomor_net.nomor_net_scraper import NomornetScraper


scraper_blueprint = Blueprint('scraper', __name__, template_folder='templates')


@scraper_blueprint.route('/', methods=['GET', 'POST'])
def scraper():
    return NomornetScraper.scraper()

