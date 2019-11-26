import json

fh = open("tests/integration/fixtures/evidence.json")
EVENT_FIXTURE = json.loads(fh.read())
fh.close()


class TestEvidenceProcessor(object):
    def test_processing_evidence(self):
        from lambda_handler.pcap import Analyze

        if EVENT_FIXTURE["detail"]["remediation"]["evidence"]["objects"] != []:
            for object_key in EVENT_FIXTURE["detail"]["remediation"]["evidence"][
                "objects"
            ]:
                full_path = f"s3://public.demo.reinvent2019/{object_key}"
                a = Analyze(full_path)
                a.get_geoip_database()
                a.load_pcap()
                extraction = a.get_extraction()
                result = a.extraction_to_json(extraction)
                a.json_to_parquet(result)
                a.upload_all_processed()
