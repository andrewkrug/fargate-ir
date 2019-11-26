import boto3
import os
import uuid
import pyarrow.parquet as pq
from lambda_handler import pcap
from moto import mock_s3


class TestGetDb(object):
    def test_get_database(self):
        object_key = "file://./tests/unit/pcaps/sample.pcap"
        p = pcap.Analyze(object_key)
        p.get_geoip_database()


@mock_s3
class TestPcap(object):
    def setup(self):
        self.bucket_name = f"forensics.{uuid.uuid4()}"
        self.conn = boto3.resource("s3", region_name="us-west-2")
        self.conn.create_bucket(Bucket=self.bucket_name)
        self.conn.Bucket(self.bucket_name).upload_file(
            "tests/unit/pcaps/sample.pcap", "case-001/sample.pcap"
        )

    def test_file_loader_system(self):
        object_key = "file://./tests/unit/pcaps/sample.pcap"
        p = pcap.Analyze(object_key)
        p.load_pcap()
        file_location = f"/tmp/{p.analysis_uuid}.pcap"
        assert os.path.isfile(file_location) is not None

    def test_file_loader_s3(self):
        object_key = f"s3://{self.bucket_name}/case-001/sample.pcap"
        p = pcap.Analyze(object_key)
        p.load_pcap()
        file_location = f"/tmp/{p.analysis_uuid}.pcap"
        assert os.path.isfile(file_location) is not None

    def test_ip_to_locations(self):
        object_key = f"s3://{self.bucket_name}/case-001/sample.pcap"
        p = pcap.Analyze(object_key)
        result = p._ip_to_locations("4.2.2.2")
        assert result["country"] != "unknown"

    def test_extraction_and_analysis(self):
        object_key = f"s3://{self.bucket_name}/case-001/sample.pcap"
        p = pcap.Analyze(object_key)
        p.load_pcap()
        file_location = f"/tmp/{p.analysis_uuid}.pcap"
        assert os.path.isfile(file_location) is not None

        extraction = p.get_extraction()

        json_result = p.extraction_to_json(extraction)
        assert json_result is not None

        for row in json_result:
            assert row["src_ip"] is not None
            assert row["dst_ip"] is not None

        parquet_result = p.json_to_parquet(json_result)
        assert parquet_result is not None
        assert os.path.isfile(parquet_result) is not None

        can_load_parquet = pq.read_pandas(
            parquet_result, columns=["src_ip"]
        ).to_pandas()
        assert can_load_parquet is not None

    def teardown(self):
        os.system("rm -f /tmp/*.pcap")
