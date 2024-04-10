# coding: utf-8

"""
    Intrinio API

    Welcome to the Intrinio API! Through our Financial Data Marketplace, we offer a wide selection of financial data feed APIs sourced by our own proprietary processes as well as from many data vendors. For a complete API request / response reference please view the [Intrinio API documentation](https://docs.intrinio.com/documentation/api_v2). If you need additional help in using the API, please visit the [Intrinio website](https://intrinio.com) and click on the chat icon in the lower right corner.  # noqa: E501

    OpenAPI spec version: 2.56.5
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from intrinio_sdk.models.bulk_download_summary import BulkDownloadSummary  # noqa: F401,E501


class ApiResponseBulkDownloadLinks(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'bulk_downloads': 'list[BulkDownloadSummary]'
    }

    attribute_map = {
        'bulk_downloads': 'bulk_downloads'
    }

    def __init__(self, bulk_downloads=None):  # noqa: E501
        """ApiResponseBulkDownloadLinks - a model defined in Swagger"""  # noqa: E501

        self._bulk_downloads = None
        self.discriminator = None

        if bulk_downloads is not None:
            self.bulk_downloads = bulk_downloads

    @property
    def bulk_downloads(self):
        """Gets the bulk_downloads of this ApiResponseBulkDownloadLinks.  # noqa: E501


        :return: The bulk_downloads of this ApiResponseBulkDownloadLinks.  # noqa: E501
        :rtype: list[BulkDownloadSummary]
        """
        return self._bulk_downloads
        
    @property
    def bulk_downloads_dict(self):
        """Gets the bulk_downloads of this ApiResponseBulkDownloadLinks.  # noqa: E501


        :return: The bulk_downloads of this ApiResponseBulkDownloadLinks.  # noqa: E501
        :rtype: list[BulkDownloadSummary]
        """

        result = None

        value = self.bulk_downloads
        if isinstance(value, list):
            result = list(map(
                lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                value
            ))
        elif hasattr(value, "to_dict"):
            result = value.to_dict()
        elif isinstance(value, dict):
            result = dict(map(
                lambda item: (item[0], item[1].to_dict())
                if hasattr(item[1], "to_dict") else item,
                value.items()
            ))
        else:
            result = { 'bulk_downloads': value }

        
        return result
        

    @bulk_downloads.setter
    def bulk_downloads(self, bulk_downloads):
        """Sets the bulk_downloads of this ApiResponseBulkDownloadLinks.


        :param bulk_downloads: The bulk_downloads of this ApiResponseBulkDownloadLinks.  # noqa: E501
        :type: list[BulkDownloadSummary]
        """

        self._bulk_downloads = bulk_downloads

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, ApiResponseBulkDownloadLinks):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
