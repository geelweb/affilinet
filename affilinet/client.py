#!/usr/bin/env python
# -*- coding: utf-8 -*-

from suds.client import Client as SudsClient
from suds.xsd.doctor import Import, ImportDoctor
from datetime import datetime

class PublisherClient():
    url = "https://api.affili.net/V2.0"
    credential_token = None

    username = None
    password = None
    sandbox_publisher_id = None

    def __init__(self, username=None, password=None,  sandbox_publisher_id=None):
        self.username = username
        self.password = password
        self.sandbox_publisher_id=sandbox_publisher_id

    def _get_product_client(self):
        self.logon(self.username, self.password, 'Product')

        wsdl_url = self.url + '/ProductServices.svc?wsdl'

        client = SudsClient(url=wsdl_url)
        return client

    def _get_inbox_client(self):
        self.logon(self.username, self.password, 'Publisher')

        wsdl_url = self.url + '/PublisherInbox.svc?wsdl'

        client = SudsClient(url=wsdl_url)
        return client

    def _get_program_client(self):
        self.logon(self.username, self.password, 'Publisher')

        wsdl_url = self.url + '/PublisherProgram.svc?wsdl'

        schema_url = 'http://affilinet.framework.webservices/types/PublisherProgram'
        schema_import = Import(schema_url)
        schema_doctor = ImportDoctor(schema_import)

        client = SudsClient(url=wsdl_url, doctor=schema_doctor)
        return client

    def _get_creatives_client(self):
        self.logon(self.username, self.password, 'Publisher')

        wsdl_url = self.url + '/PublisherCreative.svc?wsdl'

        schema_url = 'http://affilinet.framework.webservices/Svc'
        schema_import = Import(schema_url)
        schema_doctor = ImportDoctor(schema_import)

        schema_doctor.add(Import('http://affilinet.framework.webservices/types/PublisherCreative'))
        schema_doctor.add(Import('http://schemas.microsoft.com/2003/10/Serialization/Arrays'))

        client = SudsClient(url=wsdl_url, doctor=schema_doctor)
        return client

    # Logon web service
    def logon(self, username, password, service_type, sandbox_publisher_id=None):
        wsdl_url = self.url + '/Logon.svc?wsdl'

        schema_url = 'http://affilinet.framework.webservices/types'
        schema_import = Import(schema_url)
        schema_doctor = ImportDoctor(schema_import)

        client = SudsClient(url=wsdl_url, doctor=schema_doctor)
        self.credential_token = client.service.Logon(
            username,
            password,
            service_type)

    # Creative web services
    def get_creative_categories(self, program_id):
        return self._get_creatives_client().service.GetCreativeCategories(
                self.credential_token,
                program_id)

    def search_creatives(self, current_page=1, page_size=10, category_ids=None,
            creative_types=None, html_link_types=None, max_height=1000,
            min_height=1, max_width=1000, min_width=None, program_ids=None,
            search_string=None, text_link_types=None):

        client = self._get_creatives_client()

        display_settings = client.factory.create('ns1:CreativeDisplaySettings')
        display_settings.CurrentPage = current_page,
        display_settings.PageSize = page_size

        search_query = client.factory.create('ns1:SearchCreativesQuery')
        search_query.ProgramIds.int = program_ids
        search_query.CategoryIds.int = category_ids
        search_query.CreativeTypes.CreativeTypeEnum = creative_types
        search_query.HTMLLinkTypes.HTMLLinkTypeEnum = html_link_types
        search_query.MaxHeight = max_height
        search_query.MaxWidth = max_width
        search_query.MinHeight = min_height
        search_query.MinWidth = min_width
        search_query.SearchString = search_string
        search_query.TextLinkTypes.TextLinkTypeEnum = text_link_types

        return client.service.SearchCreatives(
            self.credential_token,
            display_settings,
            search_query)

    # Inbox web services
    def get_voucher_codes(self, program_id=0, voucher_code=None, query=None,
            start_date=None, end_date=None):

        if start_date is None:
            start_date = datetime.today()

        if end_date is None:
            end_date = datetime.today()

        return self._get_inbox_client().service.GetVoucherCodes(self.credential_token, {
            'ProgramId': program_id,
            'VoucherCode': voucher_code,
            'Query': query,
            'StartDate': start_date,
            'EndDate': end_date
        })


    # Program list web service

    def get_all_programs(self, query=' '):
        return self._get_program_client().service.GetAllPrograms(self.credential_token, {'Query': query})

    def get_my_programs(self, query=' '):
        return self._get_program_client().service.GetMyPrograms(self.credential_token, {'Query': query})

    def get_new_programs(self):
        return self._get_program_client().service.GetNewPrograms(self.credential_token)

    def get_program_categories(self):
        return self._get_program_client().service.GetProgramCategories(self.credential_token)

    def get_program_list_by_category(self, category_id=None):
        return self._get_program_client().service.GetProgramListByCategory(self.credential_token, {
            'CategoryId': category_id
        })

