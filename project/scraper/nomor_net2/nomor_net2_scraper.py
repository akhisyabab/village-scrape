from flask import Blueprint
import requests
from bs4 import BeautifulSoup

from project import db
from project.utils.standardize import standardize
from project.models.models import ReportSource


scraper_blueprint = Blueprint('scraper', __name__, template_folder='templates')

class Nomornet2Scraper:
    source_name = 'nomornet2'
    reports = []

    @staticmethod
    def scrape():
        payload = {
            '_i': 'desa-kodepos',
            'daerah': '',
            'jobs': '',
            'perhal': '10',
            'urut': '6',
            'asc': '000100',
            'sby': '000000'
        }

        response = requests.get('https://www.nomor.net/_kodepos.php', params=payload)
        # 'https://www.nomor.net/_kodepos.php?_i=desa-kodepos&daerah=&jobs=&perhal=100&urut=6&asc=000100&sby=000000'
        # 'https://www.nomor.net/_kodepos.php?_i=desa-kodepos&daerah=&jobs=&perhal=100&urut=6&asc=000100&sby=000000&no1=1&no2=100&kk=2'
        # 'https://www.nomor.net/_kodepos.php?_i=desa-kodepos&daerah=&jobs=&perhal=100&urut=6&asc=000100&sby=000000&no1=101&no2=200&kk=3'
        # 'https://www.nomor.net/_kodepos.php?_i=desa-kodepos&daerah=&jobs=&perhal=40&urut=6&asc=000100&sby=000000&no1=81&no2=120&kk=4'

        soup = BeautifulSoup(response.text, 'html.parser')
        rows = soup.find_all(attrs={'bgcolor': '#ccffff'})

        kode_pos = []
        desa = []
        kode = []
        kecamatan = []
        dt2 = []
        kota = []
        provinsi = []

        for row in rows:
            columns = row.find_all('td')
            parsed_data = [column.text for column in columns[1:]]
            kode_pos.append(parsed_data[0])
            desa.append(parsed_data[1])
            kode.append(parsed_data[2])
            kecamatan.append(parsed_data[3])
            dt2.append(parsed_data[4])
            kota.append(parsed_data[5])
            provinsi.append(parsed_data[6])

        raw_data = [kode_pos, desa, kode, kecamatan, dt2, kota, provinsi]
        return raw_data

    @classmethod
    def parse(cls, raw_data):
        zipped_data = [list(x) for x in zip(*raw_data)]
        for data in zipped_data:
            new_dict = dict(zip(standardize().keys(), data))
            cls.reports.append(new_dict)
        return cls.reports

    @classmethod
    def store(cls):
        db_json = {
            'data_source': cls.source_name
        }
        for data in cls.reports:
            db_json.update(data)
            report_row = ReportSource.find_by_desa(data_source=db_json['data_source'],
                                                   desa=db_json['desa'],
                                                   kecamatan=db_json['kecamatan'],
                                                   kota=db_json['kota'])
            if report_row:
                continue
            try:
                db.session.bulk_insert_mappings(ReportSource, [db_json])
            except Exception:
                print('DB store error')
                db.session.rollback()
                db.session.commit()
                raise

        db.session.commit()

    @classmethod
    def scraper(cls):
        try:
           raw_data = cls.scrape()
           cls.parse(raw_data)
           cls.store()
        except Exception:
            raise

