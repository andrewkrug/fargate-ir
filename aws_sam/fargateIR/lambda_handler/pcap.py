import boto3
import json
import pcapkit
import os
import requests
import shutil
import geoip2.database

from fastparquet import write
import pandas as pd
from pandas.io.json import json_normalize

from logging import getLogger
from shutil import copyfile
from uuid import uuid4


logger = getLogger(__name__)


class Analyze(object):
    def __init__(self, object_key):
        self.object_key = object_key
        self.analysis_uuid = uuid4().hex

    def _get_object_from_s3(self):
        logger.debug("Attempting to fetch ")
        conn = boto3.resource(
            "s3", region_name=os.getenv("AWS_DEFAULT_REGION", "us-west-2")
        )
        bucket_name = self.object_key.strip("s3://").split("/")[0]
        print(self.object_key.split(f"s3://{bucket_name}/"))
        path = self.object_key.split(f"s3://{bucket_name}/")[1]
        bucket = conn.Bucket(bucket_name)
        bucket.download_file(path, f"/tmp/{self.analysis_uuid}.pcap")

    def _get_object_from_file(self):
        logger.debug("Moving our file from the location on disk to tmp for analysis.")
        copyfile(self.object_key, f"/tmp/{self.analysis_uuid}.pcap")

    def _upload_file(self, local_file_path):
        logger.debug("Attempting to fetch ")
        conn = boto3.resource(
            "s3", region_name=os.getenv("AWS_DEFAULT_REGION", "us-west-2")
        )
        bucket_name = self.object_key.strip("s3://").split("/")[0]
        bucket = conn.Bucket(bucket_name)
        path = self.object_key.split(f"s3://{bucket_name}/")[1]
        folder = path.split("/")[0]
        file_name = local_file_path.split("/")[-1]
        bucket.upload_file(local_file_path, f"{folder}/{file_name}")

    def load_pcap(self):
        if self.object_key.startswith("s3://"):
            self._get_object_from_s3()
        elif self.object_key.startswith("file://"):
            self.object_key = self.object_key.split("file://")[1]
            self._get_object_from_file()
        else:
            self._get_object_from_file

    def upload_all_processed(self):
        self._upload_file(f"/tmp/{self.analysis_uuid}.json")
        self._upload_file(f"/tmp/{self.analysis_uuid}.parquet")

    def get_extraction(self):
        pcap_path = f"/tmp/{self.analysis_uuid}.pcap"
        extraction = pcapkit.extract(
            fin=pcap_path, store=True, nofile=True, ip=True, tcp=True, strict=True
        )
        return extraction

    def packet_to_timestamps(self, extraction, packet):
        try:
            first_frame_id = list(packet["index"])[0]
            last_frame_id = list(packet["index"])[-1]

            start_time = extraction.frame[first_frame_id]["time"]
            end_time = extraction.frame[last_frame_id]["time"]
            duration = (start_time - end_time).seconds
        except Exception as e:
            logger.error(f"Problem parsing timestamps due to: {e}.")
            start_time = None
            end_time = None
            duration = None

        return dict(
            start_time=str(start_time), end_time=str(end_time), duration=duration
        )

    def _ip_to_locations(self, ip):
        this_path = "/tmp/GeoLite2-City/"
        geolite_path = os.path.join(this_path, "GeoLite2-City.mmdb")

        if os.path.isfile(geolite_path):
            reader = geoip2.database.Reader(geolite_path)
        else:
            this_path = "/tmp/GeoLite2-City/"
            geolite_path = os.path.join(this_path, "GeoLite2-City.mmdb")
            reader = geoip2.database.Reader(geolite_path)

        try:
            resp = reader.city(ip)
            country = resp.country.name
            city = resp.city.name
            latitude = resp.location.latitude
            longitude = resp.location.longitude
        except Exception as e:
            logger.error(f"Error geolocating due to: {e}")
            country = "unknown"
            city = "unknown"
            latitude = "unknown"
            longitude = "unknown"
        return dict(
            city=city, country=country, latitude=str(latitude), longitude=str(longitude)
        )

    def extraction_to_json(self, extraction):
        result = []
        for packet in extraction.reassembly.tcp:
            timestamps = self.packet_to_timestamps(extraction, packet)
            source_ip = packet["id"]["src"][0].exploded
            destination_ip = packet["id"]["dst"][0].exploded
            source_geodata = self._ip_to_locations(source_ip)
            destination_geodata = self._ip_to_locations(destination_ip)

            result.append(
                dict(
                    ack=packet["id"]["ack"],
                    src_ip=source_ip,
                    dst_ip=destination_ip,
                    src_country=source_geodata["country"],
                    src_city=source_geodata["city"],
                    src_lat=source_geodata["latitude"],
                    src_long=source_geodata["longitude"],
                    dst_country=destination_geodata["country"],
                    dst_city=destination_geodata["city"],
                    dst_lat=destination_geodata["latitude"],
                    dst_long=destination_geodata["longitude"],
                    src_port=packet["id"]["src"][1],
                    dst_port=packet["id"]["dst"][1],
                    bytes=len(packet["payload"]),
                    start_time=timestamps["start_time"],
                    end_time=timestamps["end_time"],
                    duration=timestamps["duration"],
                    proto="tcp",
                )
            )

        fh = open(f"/tmp/{self.analysis_uuid}.json", "w")
        fh.write(json.dumps(result))
        fh.close()
        return result

    def json_to_parquet(self, json_extraction_result):
        normalize_data = json_normalize(json_extraction_result)
        df = pd.DataFrame(normalize_data)
        file_path = f"/tmp/{self.analysis_uuid}.parquet"
        write(file_path, df)
        return file_path

    def get_geoip_database(self):
        geolite_location = "/tmp/GeoLite2-City.tar.gz"
        if not os.path.exists("/tmp/GeoLite2-City.tar.gz"):
            server_endpoint = "https://geolite.maxmind.com/download/geoip/database/GeoLite2-City.tar.gz"
            response = requests.get(server_endpoint)
            local_file_path = geolite_location
            # If the HTTP GET request can be served
            if response.status_code == 200:

                # Write the file contents in the response to a file specified by local_file_path
                with open(local_file_path, "wb") as local_file:
                    for chunk in response.iter_content(chunk_size=128):
                        local_file.write(chunk)

                filename = "/tmp/GeoLite2-City.tar.gz"
                extract_path = "/tmp"
                shutil.unpack_archive(filename, extract_path)
                os.popen("mv /tmp/GeoLite2-City_* /tmp/GeoLite2-City")
