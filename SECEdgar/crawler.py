# -*- coding:utf-8 -*-
# This script will download all the 10-K, 10-Q and 8-K
# provided that of company symbol and its cik code.
from __future__ import print_function  # Compatibility with Python 2

import requests
import os
import errno
from bs4 import BeautifulSoup
from config import DEFAULT_DATA_PATH


class SecCrawler():

    def __init__(self):
        self.hello = "Welcome to SEC Cralwer!"
        print("Path of the directory where data will be saved: " + DEFAULT_DATA_PATH)

    @staticmethod
    def make_directory(company_code, cik, priorto, filing_type):
        # Making the directory to save comapny filings
        path = os.path.join(DEFAULT_DATA_PATH, company_code, cik, filing_type)

        if not os.path.exists(path):
            try:
                os.makedirs(path)
            except OSError as exception:
                if exception.errno != errno.EEXIST:
                    raise

    @staticmethod
    def save_in_directory(company_code, cik, priorto, doc_list,
                          doc_name_list, filing_type):
        # Save every text document into its respective folder
        for j in range(len(doc_list)):
            base_url = doc_list[j]
            r = requests.get(base_url)
            data = r.text
            path = os.path.join(DEFAULT_DATA_PATH, company_code, cik,
                                filing_type, doc_name_list[j])

            with open(path, "ab") as f:
                f.write(data.encode('ascii', 'ignore'))

    @staticmethod
    def create_document_list(data):
        # parse fetched data using beatifulsoup
        soup = BeautifulSoup(data)
        # store the link in the list
        link_list = list()

        # If the link is .htm convert it to .html
        for link in soup.find_all('filinghref'):
            url = link.string
            if link.string.split(".")[len(link.string.split("."))-1] == "htm":
                url += "l"
            link_list.append(url)
        link_list_final = link_list

        print("Number of files to download: {0}".format(len(link_list_final)))
        print("Starting download...")

        # List of url to the text documents
        doc_list = list()
        # List of document names
        doc_name_list = list()

        # Get all the doc
        for k in range(len(link_list_final)):
            required_url = link_list_final[k].replace('-index.html', '')
            txtdoc = required_url + ".txt"
            docname = txtdoc.split("/")[-1]
            doc_list.append(txtdoc)
            doc_name_list.append(docname)
        return doc_list, doc_name_list

    def fetch_report(self, company_code, cik, priorto, count, filing_type):
        self.make_directory(company_code, cik, priorto, filing_type)

        # generate the url to crawl
        base_url = "http://www.sec.gov/cgi-bin/browse-edgar?action=getcompany"
        url = "{base}&CIK={cik}&type={filing_type}&dateb={priorto}&owner=exclude&output=xml&count={count}".format(
            base=base_url, cik=cik, filing_type=filing_type, priorto=priorto, count=count)
        print("started {filing_type} {company_code}".format(
            filing_type=filing_type, company_code=company_code))
        r = requests.get(url)
        data = r.text

        # get doc list data
        doc_list, doc_name_list = self.create_document_list(data)

        try:
            self.save_in_directory(
                company_code, cik, priorto, doc_list, doc_name_list, filing_type)
        except Exception as e:
            print(str(e))

        print("Successfully downloaded all the files")

    def filing_10Q(self, company_code, cik, priorto, count):
        self.fetch_report(company_code, cik, priorto, count, '10-Q')

    def filing_10K(self, company_code, cik, priorto, count):
        self.fetch_report(company_code, cik, priorto, count, '10-K')

    def filing_8K(self, company_code, cik, priorto, count):
        self.fetch_report(company_code, cik, priorto, count, '8-K')

    def filing_13F(self, company_code, cik, priorto, count):
        self.fetch_report(company_code, cik, priorto, count, '13-F')

    def filing_SD(self, company_code, cik, priorto, count):
        self.fetch_report(company_code, cik, priorto, count, 'SD')