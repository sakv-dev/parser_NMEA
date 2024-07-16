import requests
import json

class NMEAParser:
    def __init__(self, nmea_sentence):
        self.sentence = nmea_sentence
        self.data = {}
        self.parse_sentence()

    def parse_sentence(self):
        if self.sentence.startswith('$GPGGA'):
            self.parse_gpgga()
        elif self.sentence.startswith('$GPGLL'):
            self.parse_gpgll()
        elif self.sentence.startswith('$GPGSA'):
            self.parse_gpgsa()
        elif self.sentence.startswith('$GPGSV'):
            self.parse_gpgsv()
        elif self.sentence.startswith('$GPVTG'):
            self.parse_gpvtg()
        elif self.sentence.startswith('$GPRMC'):
            self.parse_gprmc()
        else:
            print(f"Unsupported sentence type: {self.sentence}")

    def parse_gpgga(self):
        parts = self.sentence.split(',')
        if len(parts) < 15:
            print("Invalid GPGGA sentence")
            return

        self.data['type'] = 'GPGGA'
        self.data['time'] = self.convert_time(parts[1])
        self.data['latitude'] = self.convert_latitude(parts[2], parts[3])
        self.data['longitude'] = self.convert_longitude(parts[4], parts[5])
        self.data['fix_quality'] = parts[6]
        self.data['num_satellites'] = parts[7]
        self.data['horizontal_dilution'] = parts[8]
        self.data['altitude'] = parts[9] + ' ' + parts[10]
        self.data['geoid_height'] = parts[11] + ' ' + parts[12]
        self.data['what3words'] = self.convert_to_what3words(self.data['latitude'], self.data['longitude'])

    def parse_gpgll(self):
        parts = self.sentence.split(',')
        if len(parts) < 7:
            print("Invalid GPGLL sentence")
            return

        self.data['type'] = 'GPGLL'
        self.data['latitude'] = self.convert_latitude(parts[1], parts[2])
        self.data['longitude'] = self.convert_longitude(parts[3], parts[4])
        self.data['time'] = self.convert_time(parts[5])
        self.data['status'] = parts[6]

    def parse_gpgsa(self):
        parts = self.sentence.split(',')
        if len(parts) < 18:
            print("Invalid GPGSA sentence")
            return

        self.data['type'] = 'GPGSA'
        self.data['mode'] = parts[1]
        self.data['fix_type'] = parts[2]
        self.data['satellites'] = parts[3:15]
        self.data['pdop'] = parts[15]
        self.data['hdop'] = parts[16]
        self.data['vdop'] = parts[17]

    def parse_gpgsv(self):
        parts = self.sentence.split(',')
        if len(parts) < 8:
            print("Invalid GPGSV sentence")
            return

        self.data['type'] = 'GPGSV'
        self.data['num_sentences'] = parts[1]
        self.data['sentence_num'] = parts[2]
        self.data['num_satellites'] = parts[3]
        self.data['satellite_info'] = []

        for i in range(4, len(parts) - 1, 4):
            satellite = {
                'satellite_id': parts[i],
                'elevation': parts[i + 1],
                'azimuth': parts[i + 2],
                'snr': parts[i + 3]
            }
            self.data['satellite_info'].append(satellite)

    def parse_gpvtg(self):
        parts = self.sentence.split(',')
        if len(parts) < 9:
            print("Invalid GPVTG sentence")
            return

        self.data['type'] = 'GPVTG'
        self.data['true_track'] = parts[1] + ' T'
        self.data['magnetic_track'] = parts[3] + ' M'
        self.data['ground_speed_knots'] = parts[5] + ' N'
        self.data['ground_speed_kmph'] = parts[7] + ' K'

    def parse_gprmc(self):
        parts = self.sentence.split(',')
        if len(parts) < 12:
            print("Invalid GPRMC sentence")
            return

        self.data['type'] = 'GPRMC'
        self.data['time'] = self.convert_time(parts[1])
        self.data['status'] = parts[2]
        self.data['latitude'] = self.convert_latitude(parts[3], parts[4])
        self.data['longitude'] = self.convert_longitude(parts[5], parts[6])
        self.data['speed'] = parts[7]
        self.data['track_angle'] = parts[8]
        self.data['date'] = self.convert_date(parts[9])
        self.data['magnetic_variation'] = parts[10] + ' ' + parts[11] if parts[10] and parts[11] else 'N/A'

    def convert_time(self, raw_time):
        if len(raw_time) < 6:
            return "Invalid time"
        hours = raw_time[0:2]
        minutes = raw_time[2:4]
        seconds = raw_time[4:6]
        return f"{hours}:{minutes}:{seconds} UTC"

    def convert_latitude(self, raw_latitude, direction):
        if not raw_latitude or not direction:
            return "Invalid latitude"
        degrees = float(raw_latitude[0:2])
        minutes = float(raw_latitude[2:])
        latitude = degrees + (minutes / 60)
        if direction == 'S':
            latitude = -latitude
        return latitude

    def convert_longitude(self, raw_longitude, direction):
        if not raw_longitude or not direction:
            return "Invalid longitude"
        degrees = float(raw_longitude[0:3])
        minutes = float(raw_longitude[3:])
        longitude = degrees + (minutes / 60)
        if direction == 'W':
            longitude = -longitude
        return longitude

    def convert_date(self, raw_date):
        if len(raw_date) != 6:
            return "Invalid date"
        day = raw_date[0:2]
        month = raw_date[2:4]
        year = raw_date[4:6]
        return f"{day}/{month}/20{year}"

    def convert_to_what3words(self, lat, lon):
        api_key = 'YOUR_WHAT3WORDS_API_KEY'
        url = f"https://api.what3words.com/v3/convert-to-3wa?coordinates={lat}%2C{lon}&key={api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()['words']
        else:
            return "Erreur API what3words"

    def get_data(self):
        return self.data

    def output_data(self):
        output = json.dumps(self.data, indent=4)
        print(output)
        save_to_file = input("Do you want to save the results to a file? (yes/no): ").strip().lower()
        if save_to_file in ['yes', 'y', 'oui']:
            with open(self.output_filename, 'a') as f:
                f.write(output + '\n')

# Exemple d'utilisation / Example of usage
nmea_sentences = [
    "$GPGGA,123519,4807.038,N,01131.324,E,1,08,0.9,545.4,M,46.9,M,,*42",
    "$GPGLL,4916.45,N,12311.12,W,225444,A",
    "$GPGSA,A,3,04,05,,09,12,,,24,,,,,2.5,1.3,2.1*39",
    "$GPGSV,2,1,08,01,40,083,46,02,17,308,41,12,07,344,39,14,22,228,45*75",
    "$GPVTG,054.7,T,034.4,M,005.5,N,010.2,K",
    "$GPRMC,225446,A,4916.45,N,12311.12,W,000.5,054.7,191194,020.3,E*68"
]

all_data = []

for sentence in nmea_sentences:
    parser = NMEAParser(sentence)
    parser.parse_sentence()
    all_data.append(parser.get_data())

output = json.dumps(all_data, indent=4)
print(output)
save_to_file = input("Do you want to save the results to a file? (yes/no): ").strip().lower()
if save_to_file in ['yes', 'y', 'oui']:
    with open("output.json", 'w') as f:
        f.write(output + '\n')
