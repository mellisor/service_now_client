#!/usr/bin/env python
"""
Author: Mitchell Ellisor
:desc: Client for the service now api
"""
__author__ = 'Mitchell Ellisor <evanmellisor@gmail.com>'

import requests
import json

def serialize_dict(j):
    return '&'.join([ '{}={}'.format(k,v) for k,v in j.items() ])

class ServiceNowClient():

    def __init__(self,username,password,api_url='https://yourdomain.service-now.com/api/now/v2/',response_format='json'):
        """
        username:        service now username
        password:        service now password
        api_url:         url of your service now api
        response_format: format for responses (json/xml)
        """
        self.auth = (username,password)
        self.url = api_url
        self.set_response_headers(response_format)
        self.kwargs = { 'auth' : self.auth, 'headers' : self.headers }
        self.response_format = response_format

    def set_response_headers(self,response_format):
        """
        Sets respone headers according to response_format argument
        response_format: string that represents response format.  Only json and xml are recognized
        """
        if response_format == 'json' or response_format == 'xml':
            self.headers = { "Accept" : "application/{FORMAT}".format(FORMAT=response_format) }
        else:
            raise ValueError("Response format {FORMAT} not recognized".format(FORMAT=response_format))

    def __return_content(self,content):
        """
        Determines what type of content to return based on chosen response_format
        content: string, either xml or json. If json, a dictionary will be returned
        """
        if self.response_format == 'json':
            return json.loads(content)
        else:
            return content

    def get_table(self,table,num=None):
        """
        Returns a dictionary that represents the contents of the requested table
        table: string, table name
        num:   number of results to return
        """
        print(self.url + 'table/{TABLE}?sysparm_limit={NUM}'.format(TABLE=table,NUM=num))
        response = requests.get(self.url + 'table/{TABLE}?sysparm_limit={NUM}'.format(TABLE=table,NUM=num),**self.kwargs)
        return self.__return_content(response.content)

    def query_table(self,table,query,num=None):
        """
        Returns the contents of a table that match the specified query
        table: string, table name
        query: string, query to perform
        num:   number of results to return
        """
        response = requests.get(self.url + 'table/{TABLE}?sysparm_limit={NUM}&sysparm_query={QUERY}'.format(NUM=num,QUERY=query),**self.kwargs)
        return self.__return_content(response.content)

    def dict_query_table(self,table,query_dict):
        """
        Returns the contents of a table that matches a given query
        query_dict: dict representation of a query where the keys represent attributes and the values represent data values
        NOTE: sysparm_limit must be specified to limit number of results
        """
        params = serialize_dict(query_dict)
        response = requests.get(self.url + 'table/{TABLE}?{PARAMS}'.format(TABLE=table,PARAMS=params),**self.kwargs)
        return self.__return_content(response.content)

    def get_table_item(self,table,id,query_dict={}):
        """
        Returns a specific item from a table
        table:      string, table name
        id:         string, item sys_id
        query_dict: dict, additional api search parameters
        """
        response = requests.get(self.url + 'table/{TABLE}/{ID}?{PARAMS}'.format(TABLE=table,ID=id,PARAMS=serialize_dict(query_dict)),**self.kwargs)
        return self.__return_content(response.content)
    
    def custom_query(self,query):
        """
        Returns the result of a custom query
        query: string, query to perform, base url is the api root
        """
        response = requests.get(self.url + query,**self.kwargs)
        return self.__return_content(response.content)

    def update_table_item(self,table,id,query_dict):
        """
        Updates item elements according to query_dict
        table: string, table to update
        id: sys_id to update
        query_dict: dict, keys represent attributes to modify, values represent new values
        """
        response = requests.patch(self.url + 'table/{TABLE}/{ID}'.format(TABLE=table,ID=id),json=query_dict,**self.kwargs)
        return self.__return_content(response.content) 
