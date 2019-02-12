from django.test import TestCase, Client

class TestUploadView(TestCase):

    def setUp(self):
        self.client = Client()

    def test_upload_form(self):
        '''testando se o formulario esta funcionando'''
        response = self.client.get('/upload/')
        self.assertEquals(response.status_code, 200)

    def test_upload_process(self):
        '''testando se o submit de arquivos esta funcionando'''
        with open('example_input.tab') as file_to_upload:
            response = self.client.post('/upload/', {'spreadsheet_file': file_to_upload})
            self.assertEquals(response.status_code, 200)

    def test_upload_revenue_total(self):
        '''testando se o submit de arquivos esta funcionando'''
        with open('example_input.tab') as file_to_upload:
            response = self.client.post('/upload/', {'spreadsheet_file': file_to_upload})
            self.assertContains(response, 'Value of total revenue :')

    def test_upload_only_tab_file(self):
        '''testando se o arquivo é .tab, se não for retorna status 415'''
        with open('example_input.txt') as file_to_upload:
            response = self.client.post('/upload/', {'spreadsheet_file': file_to_upload})
            self.assertEquals(response.status_code, 415)