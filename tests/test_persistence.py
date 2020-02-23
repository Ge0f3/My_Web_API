import manage
import unittest
import json
import os
from services.config import RequiredConstants

base_url = 'v1/persistence/'
RequiredConstants.BUCKET_NAME = 'bitbucket-pipeline-tests'

class TestMethods(unittest.TestCase):
    """docstring for TestMethods"""
    x = ''

    def setUp(self):
        # self.app = create_app(testing=True)
        manage.app.testing = True
        # self.app.testing = True
        print('self')
        self.app = manage.app.test_client()

    def create_file(self):
        f = open("guru.txt", "w+")
        result = os.path.realpath(f.name)
        f.close()
        return result

    def test_health(self):
        response = self.app.get('/v1/health', content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_1_upload_200(self):
        path = TestMethods.create_file(self)
        response = self.app.post(
            base_url + 'upload',
            data=json.dumps(dict(
                s3_file_path="testing-account/testing-algorith/",
                file_path=path,
                s3_file_name="guru.txt"
            )),
            headers={'Content-Type': 'application/json'}
        )

        self.assertEqual(response.status_code, 200)

    def test_2_upload_404(self):
        response = self.app.post(
            base_url + 'upload',
            data=json.dumps(dict(
                s3_file_path="testing-account/testing-algorith/",
                file_path="./persistence_files/upload_files/testing12345.docx",
                s3_file_name="testing12345.docx"
                )),
            headers={'Content-Type': 'application/json'}
        )
        print(response)
        self.assertEqual(response.status_code, 404)

    def test_3_download_200(self):

        response = self.app.post(
            base_url + 'download',
            data=json.dumps(dict(
                s3_file_path="testing-account/testing-algorith/",
                s3_file_name="guru.txt"
            )),
            headers={'Content-Type': 'application/json'}
        )
        result = json.loads(response.get_data())
        self.__class__.x = result['response']['file_path']
        self.assertEqual(response.status_code, 200)

    def test_4_download_404(self):
        response = self.app.post(
            base_url + 'download',
            data=json.dumps(dict(
                s3_file_path="testing-account/testing-algorith/",
                s3_file_name="testing12345665.docx"
            )),
            headers={'Content-Type': 'application/json'}
        )

        self.assertEqual(response.status_code, 404)

    def test_5_delete_one_200(self):
        response = self.app.post(
            base_url + 'cleanup',
            data=json.dumps(dict(
                file_path=self.__class__.x
            )),
            headers={'Content-Type': 'application/json'}
        )
        result = json.loads((response.get_data()))
        self.assertEqual(response.status_code, 200)

    def test_delete_one_500(self):
        response = self.app.post(
            base_url + 'cleanup',
            data=json.dumps(dict(
                file_path="./persistence_files/delete_files/testing123.docx"
            )),
            headers={'Content-Type': 'application/json'}
        )
        self.assertEqual(response.status_code, 500)

    def test_delete_all_200(self):
        response = self.app.post(
            base_url + 'cleanup_all',
            headers={'Content-Type': 'application/json'}
        )
        self.assertEqual(response.status_code, 200)

    def test_delete_all_500(self):
        response = self.app.post(
            base_url + 'cleanup_all',
            headers={'Content-Type': 'application/json'}
        )
        self.assertEqual(response.status_code, 500)


if __name__ == '__main__':
    unittest.main()
