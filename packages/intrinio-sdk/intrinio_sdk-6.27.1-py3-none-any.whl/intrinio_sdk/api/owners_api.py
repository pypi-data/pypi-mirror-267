# coding: utf-8

"""
    Intrinio API

    Welcome to the Intrinio API! Through our Financial Data Marketplace, we offer a wide selection of financial data feed APIs sourced by our own proprietary processes as well as from many data vendors. For a complete API request / response reference please view the [Intrinio API documentation](https://docs.intrinio.com/documentation/api_v2). If you need additional help in using the API, please visit the [Intrinio website](https://intrinio.com) and click on the chat icon in the lower right corner.  # noqa: E501

    OpenAPI spec version: 2.56.5
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from intrinio_sdk.api_client import ApiClient


class OwnersApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def get_all_owners(self, **kwargs):  # noqa: E501
        """All Owners  # noqa: E501

        Returns all owners and information for all insider and institutional owners of securities covered by Intrinio.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async=True
        >>> thread = api.get_all_owners(_async=True)
        >>> result = thread.get()

        :param async bool
        :param bool institutional: Returns insider owners who have filed forms 3, 4, or 5 with the SEC only. Possible values are true, false, or omit for both.
        :param int page_size: The number of results to return
        :param str next_page: Gets the next page of data from a previous API call
        :return: ApiResponseOwners
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async'):
            return self.get_all_owners_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.get_all_owners_with_http_info(**kwargs)  # noqa: E501
            return data

    def get_all_owners_with_http_info(self, **kwargs):  # noqa: E501
        """All Owners  # noqa: E501

        Returns all owners and information for all insider and institutional owners of securities covered by Intrinio.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async=True
        >>> thread = api.get_all_owners_with_http_info(_async=True)
        >>> result = thread.get()

        :param async bool
        :param bool institutional: Returns insider owners who have filed forms 3, 4, or 5 with the SEC only. Possible values are true, false, or omit for both.
        :param int page_size: The number of results to return
        :param str next_page: Gets the next page of data from a previous API call
        :return: ApiResponseOwners
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['institutional', 'page_size', 'next_page']  # noqa: E501
        all_params.append('async')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_all_owners" % key
                )
            params[key] = val
        del params['kwargs']

        if 'page_size' in params and params['page_size'] > 10000:  # noqa: E501
            raise ValueError("Invalid value for parameter `page_size` when calling `get_all_owners`, must be a value less than or equal to `10000`")  # noqa: E501
        collection_formats = {}

        path_params = {}

        query_params = []
        if 'institutional' in params:
            query_params.append(('institutional', params['institutional']))  # noqa: E501
        if 'page_size' in params:
            query_params.append(('page_size', params['page_size']))  # noqa: E501
        if 'next_page' in params:
            query_params.append(('next_page', params['next_page']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['ApiKeyAuth']  # noqa: E501

        return self.api_client.call_api(
            '/owners', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ApiResponseOwners',  # noqa: E501
            auth_settings=auth_settings,
            _async=params.get('async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_owner_by_id(self, identifier, **kwargs):  # noqa: E501
        """Owner by ID  # noqa: E501

        Returns the Owner with the given ID  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async=True
        >>> thread = api.get_owner_by_id(identifier, _async=True)
        >>> result = thread.get()

        :param async bool
        :param str identifier: An Intrinio ID or CIK of an Owner (required)
        :return: Owner
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async'):
            return self.get_owner_by_id_with_http_info(identifier, **kwargs)  # noqa: E501
        else:
            (data) = self.get_owner_by_id_with_http_info(identifier, **kwargs)  # noqa: E501
            return data

    def get_owner_by_id_with_http_info(self, identifier, **kwargs):  # noqa: E501
        """Owner by ID  # noqa: E501

        Returns the Owner with the given ID  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async=True
        >>> thread = api.get_owner_by_id_with_http_info(identifier, _async=True)
        >>> result = thread.get()

        :param async bool
        :param str identifier: An Intrinio ID or CIK of an Owner (required)
        :return: Owner
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['identifier']  # noqa: E501
        all_params.append('async')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_owner_by_id" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'identifier' is set
        if ('identifier' not in params or
                params['identifier'] is None):
            raise ValueError("Missing the required parameter `identifier` when calling `get_owner_by_id`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'identifier' in params:
            path_params['identifier'] = params['identifier']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['ApiKeyAuth']  # noqa: E501

        return self.api_client.call_api(
            '/owners/{identifier}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='Owner',  # noqa: E501
            auth_settings=auth_settings,
            _async=params.get('async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def insider_transaction_filings_by_owner(self, identifier, **kwargs):  # noqa: E501
        """Insider Transaction Filings by Owner  # noqa: E501

        Returns a list of all insider transaction filings by an owner in as many companies as the owner may be considered an insider. Criteria for being an insider include being a director, officer, or 10%+ owner in the company. Transactions are detailed for both non-derivative and derivative transactions by the insider.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async=True
        >>> thread = api.insider_transaction_filings_by_owner(identifier, _async=True)
        >>> result = thread.get()

        :param async bool
        :param str identifier: The Central Index Key issued by the SEC, which is the unique identifier all owner filings are issued under. (required)
        :param date start_date: Return Owner's insider transaction filings on or after this date
        :param date end_date: Return Owner's insider transaction filings on or before this date
        :param int page_size: The number of results to return
        :param str next_page: Gets the next page of data from a previous API call
        :return: ApiResponseOwnerInsiderTransactionFilings
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async'):
            return self.insider_transaction_filings_by_owner_with_http_info(identifier, **kwargs)  # noqa: E501
        else:
            (data) = self.insider_transaction_filings_by_owner_with_http_info(identifier, **kwargs)  # noqa: E501
            return data

    def insider_transaction_filings_by_owner_with_http_info(self, identifier, **kwargs):  # noqa: E501
        """Insider Transaction Filings by Owner  # noqa: E501

        Returns a list of all insider transaction filings by an owner in as many companies as the owner may be considered an insider. Criteria for being an insider include being a director, officer, or 10%+ owner in the company. Transactions are detailed for both non-derivative and derivative transactions by the insider.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async=True
        >>> thread = api.insider_transaction_filings_by_owner_with_http_info(identifier, _async=True)
        >>> result = thread.get()

        :param async bool
        :param str identifier: The Central Index Key issued by the SEC, which is the unique identifier all owner filings are issued under. (required)
        :param date start_date: Return Owner's insider transaction filings on or after this date
        :param date end_date: Return Owner's insider transaction filings on or before this date
        :param int page_size: The number of results to return
        :param str next_page: Gets the next page of data from a previous API call
        :return: ApiResponseOwnerInsiderTransactionFilings
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['identifier', 'start_date', 'end_date', 'page_size', 'next_page']  # noqa: E501
        all_params.append('async')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method insider_transaction_filings_by_owner" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'identifier' is set
        if ('identifier' not in params or
                params['identifier'] is None):
            raise ValueError("Missing the required parameter `identifier` when calling `insider_transaction_filings_by_owner`")  # noqa: E501

        if 'page_size' in params and params['page_size'] > 10000:  # noqa: E501
            raise ValueError("Invalid value for parameter `page_size` when calling `insider_transaction_filings_by_owner`, must be a value less than or equal to `10000`")  # noqa: E501
        collection_formats = {}

        path_params = {}
        if 'identifier' in params:
            path_params['identifier'] = params['identifier']  # noqa: E501

        query_params = []
        if 'start_date' in params:
            query_params.append(('start_date', params['start_date']))  # noqa: E501
        if 'end_date' in params:
            query_params.append(('end_date', params['end_date']))  # noqa: E501
        if 'page_size' in params:
            query_params.append(('page_size', params['page_size']))  # noqa: E501
        if 'next_page' in params:
            query_params.append(('next_page', params['next_page']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['ApiKeyAuth']  # noqa: E501

        return self.api_client.call_api(
            '/owners/{identifier}/insider_transaction_filings', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ApiResponseOwnerInsiderTransactionFilings',  # noqa: E501
            auth_settings=auth_settings,
            _async=params.get('async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def institutional_holdings_by_owner(self, identifier, **kwargs):  # noqa: E501
        """Institutional Holdings by Owner  # noqa: E501

        Returns a list of all ownership interests and the value of their interests by a single institutional owner.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async=True
        >>> thread = api.institutional_holdings_by_owner(identifier, _async=True)
        >>> result = thread.get()

        :param async bool
        :param str identifier: The Central Index Key issued by the SEC, which is the unique identifier all owner filings are issued under. (required)
        :param int page_size: The number of results to return
        :param date as_of_date: Return only holdings filed before this date.
        :param str next_page: Gets the next page of data from a previous API call
        :return: ApiResponseOwnerInstitutionalHoldings
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async'):
            return self.institutional_holdings_by_owner_with_http_info(identifier, **kwargs)  # noqa: E501
        else:
            (data) = self.institutional_holdings_by_owner_with_http_info(identifier, **kwargs)  # noqa: E501
            return data

    def institutional_holdings_by_owner_with_http_info(self, identifier, **kwargs):  # noqa: E501
        """Institutional Holdings by Owner  # noqa: E501

        Returns a list of all ownership interests and the value of their interests by a single institutional owner.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async=True
        >>> thread = api.institutional_holdings_by_owner_with_http_info(identifier, _async=True)
        >>> result = thread.get()

        :param async bool
        :param str identifier: The Central Index Key issued by the SEC, which is the unique identifier all owner filings are issued under. (required)
        :param int page_size: The number of results to return
        :param date as_of_date: Return only holdings filed before this date.
        :param str next_page: Gets the next page of data from a previous API call
        :return: ApiResponseOwnerInstitutionalHoldings
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['identifier', 'page_size', 'as_of_date', 'next_page']  # noqa: E501
        all_params.append('async')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method institutional_holdings_by_owner" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'identifier' is set
        if ('identifier' not in params or
                params['identifier'] is None):
            raise ValueError("Missing the required parameter `identifier` when calling `institutional_holdings_by_owner`")  # noqa: E501

        if 'page_size' in params and params['page_size'] > 10000:  # noqa: E501
            raise ValueError("Invalid value for parameter `page_size` when calling `institutional_holdings_by_owner`, must be a value less than or equal to `10000`")  # noqa: E501
        collection_formats = {}

        path_params = {}
        if 'identifier' in params:
            path_params['identifier'] = params['identifier']  # noqa: E501

        query_params = []
        if 'page_size' in params:
            query_params.append(('page_size', params['page_size']))  # noqa: E501
        if 'as_of_date' in params:
            query_params.append(('as_of_date', params['as_of_date']))  # noqa: E501
        if 'next_page' in params:
            query_params.append(('next_page', params['next_page']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['ApiKeyAuth']  # noqa: E501

        return self.api_client.call_api(
            '/owners/{identifier}/institutional_holdings', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ApiResponseOwnerInstitutionalHoldings',  # noqa: E501
            auth_settings=auth_settings,
            _async=params.get('async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def search_owners(self, query, **kwargs):  # noqa: E501
        """Search Owners  # noqa: E501

        Searches for Owners matching the text `query`  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async=True
        >>> thread = api.search_owners(query, _async=True)
        >>> result = thread.get()

        :param async bool
        :param str query: (required)
        :param bool institutional: Returns insider owners who have filed forms 3, 4, or 5 with the SEC only. Possible values are true, false, or omit for both.
        :param int page_size: The number of results to return
        :param str next_page: Gets the next page of data from a previous API call
        :return: ApiResponseOwners
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async'):
            return self.search_owners_with_http_info(query, **kwargs)  # noqa: E501
        else:
            (data) = self.search_owners_with_http_info(query, **kwargs)  # noqa: E501
            return data

    def search_owners_with_http_info(self, query, **kwargs):  # noqa: E501
        """Search Owners  # noqa: E501

        Searches for Owners matching the text `query`  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async=True
        >>> thread = api.search_owners_with_http_info(query, _async=True)
        >>> result = thread.get()

        :param async bool
        :param str query: (required)
        :param bool institutional: Returns insider owners who have filed forms 3, 4, or 5 with the SEC only. Possible values are true, false, or omit for both.
        :param int page_size: The number of results to return
        :param str next_page: Gets the next page of data from a previous API call
        :return: ApiResponseOwners
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['query', 'institutional', 'page_size', 'next_page']  # noqa: E501
        all_params.append('async')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method search_owners" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'query' is set
        if ('query' not in params or
                params['query'] is None):
            raise ValueError("Missing the required parameter `query` when calling `search_owners`")  # noqa: E501

        if 'page_size' in params and params['page_size'] > 10000:  # noqa: E501
            raise ValueError("Invalid value for parameter `page_size` when calling `search_owners`, must be a value less than or equal to `10000`")  # noqa: E501
        collection_formats = {}

        path_params = {}

        query_params = []
        if 'query' in params:
            query_params.append(('query', params['query']))  # noqa: E501
        if 'institutional' in params:
            query_params.append(('institutional', params['institutional']))  # noqa: E501
        if 'page_size' in params:
            query_params.append(('page_size', params['page_size']))  # noqa: E501
        if 'next_page' in params:
            query_params.append(('next_page', params['next_page']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['ApiKeyAuth']  # noqa: E501

        return self.api_client.call_api(
            '/owners/search', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ApiResponseOwners',  # noqa: E501
            auth_settings=auth_settings,
            _async=params.get('async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
