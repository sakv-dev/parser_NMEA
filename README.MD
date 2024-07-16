
# NMEA Sentence Parser

This Python project is designed to parse NMEA sentences, which are data formats used by marine and GPS navigation systems to transmit information such as location, speed, and time.

## What is NMEA?

NMEA (National Marine Electronics Association) is a standard data format supported by all GPS manufacturers for interfacing between various marine electronic devices. The NMEA-0183 standard defines the electrical signal and data format of an ASCII serial data stream that enables GPS receivers to communicate with other electronic devices.

## Prerequisites

To run this project, you need:
- Python 3.x
- Requests library for Python

You can install the required library using pip:
```bash
pip install requests
```

## Usage

1. Clone the repository to your local machine:
```bash
git clone https://github.com/yourusername/nmea-parser.git
cd nmea-parser
```

2. Replace `YOUR_WHAT3WORDS_API_KEY` in the `NMEAParser` class with your actual what3words API key.

3. Run the script:
```bash
python nmea_parser.py
```

4. Input the NMEA sentences you want to parse. The parsed data will be displayed in JSON format in the console.

5. You will be asked if you want to save the results to a file. Type `yes` to save or `no` to skip.

Example of usage:
```python
nmea_sentences = [
    "$GPGGA,123519,4807.038,N,01131.324,E,1,08,0.9,545.4,M,46.9,M,,*42",
    "$GPGLL,4916.45,N,12311.12,W,225444,A",
    "$GPGSA,A,3,04,05,,09,12,,,24,,,,,2.5,1.3,2.1*39",
    "$GPGSV,2,1,08,01,40,083,46,02,17,308,41,12,07,344,39,14,22,228,45*75",
    "$GPVTG,054.7,T,034.4,M,005.5,N,010.2,K",
    "$GPRMC,225446,A,4916.45,N,12311.12,W,000.5,054.7,191194,020.3,E*68"
]

for sentence in nmea_sentences:
    parser = NMEAParser(sentence)
    parser.output_data()
```
