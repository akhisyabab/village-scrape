from flask import Blueprint, render_template
import requests
from bs4 import BeautifulSoup
from pandas import DataFrame

scraper_blueprint = Blueprint('scraper', __name__, template_folder='templates')

class NomornetScraper:
    datas = []
    main_datas = []

    @staticmethod
    def scrape():
        payload = {
            '_i': 'desa-kodepos',
            'daerah': '',
            'jobs': '',
            'perhal': '100',
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

        all_data = [kode_pos, desa, kode, kecamatan, dt2, kota, provinsi]
        main_datas = [list(x) for x in zip(*all_data)]

        datas = {
            'Kode Pos': kode_pos,
            'Desa/Kelurahan': desa,
            'Kode Wilayah': kode,
            'Kecamatan': kecamatan,
            'DT2': dt2,
            'Kota/Kabupaten': kota,
            'Provinsi': provinsi
        }


        # df = DataFrame(datas, columns=datas.keys())
        # df.to_csv('data_desa.csv', index=None, header=True)
        return (datas, main_datas)

    @classmethod
    def scraper(cls):
        if cls.main_datas == []:
            cls.datas, cls.main_datas = cls.scrape()
            return 'Data kosong'

        return render_template('index.html', datas=cls.datas, main_datas=cls.main_datas)
