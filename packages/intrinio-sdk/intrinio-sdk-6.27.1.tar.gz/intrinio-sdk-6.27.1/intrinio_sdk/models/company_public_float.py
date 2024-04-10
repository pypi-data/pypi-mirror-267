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


class CompanyPublicFloat(object):
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
        'date': 'date',
        'filing_date': 'date',
        'public_float_value': 'float',
        'public_float_shares': 'float'
    }

    attribute_map = {
        'date': 'date',
        'filing_date': 'filing_date',
        'public_float_value': 'public_float_value',
        'public_float_shares': 'public_float_shares'
    }

    def __init__(self, date=None, filing_date=None, public_float_value=None, public_float_shares=None):  # noqa: E501
        """CompanyPublicFloat - a model defined in Swagger"""  # noqa: E501

        self._date = None
        self._filing_date = None
        self._public_float_value = None
        self._public_float_shares = None
        self.discriminator = None

        if date is not None:
            self.date = date
        if filing_date is not None:
            self.filing_date = filing_date
        if public_float_value is not None:
            self.public_float_value = public_float_value
        if public_float_shares is not None:
            self.public_float_shares = public_float_shares

    @property
    def date(self):
        """Gets the date of this CompanyPublicFloat.  # noqa: E501

        The date of the public float.  # noqa: E501

        :return: The date of this CompanyPublicFloat.  # noqa: E501
        :rtype: date
        """
        return self._date
        
    @property
    def date_dict(self):
        """Gets the date of this CompanyPublicFloat.  # noqa: E501

        The date of the public float. as a dictionary. Useful for Panda Dataframes.  # noqa: E501

        :return: The date of this CompanyPublicFloat.  # noqa: E501
        :rtype: date
        """

        result = None

        value = self.date
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
            result = { 'date': value }

        
        return result
        

    @date.setter
    def date(self, date):
        """Sets the date of this CompanyPublicFloat.

        The date of the public float.  # noqa: E501

        :param date: The date of this CompanyPublicFloat.  # noqa: E501
        :type: date
        """

        self._date = date

    @property
    def filing_date(self):
        """Gets the filing_date of this CompanyPublicFloat.  # noqa: E501

        The filing date of the public float.  # noqa: E501

        :return: The filing_date of this CompanyPublicFloat.  # noqa: E501
        :rtype: date
        """
        return self._filing_date
        
    @property
    def filing_date_dict(self):
        """Gets the filing_date of this CompanyPublicFloat.  # noqa: E501

        The filing date of the public float. as a dictionary. Useful for Panda Dataframes.  # noqa: E501

        :return: The filing_date of this CompanyPublicFloat.  # noqa: E501
        :rtype: date
        """

        result = None

        value = self.filing_date
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
            result = { 'filing_date': value }

        
        return result
        

    @filing_date.setter
    def filing_date(self, filing_date):
        """Sets the filing_date of this CompanyPublicFloat.

        The filing date of the public float.  # noqa: E501

        :param filing_date: The filing_date of this CompanyPublicFloat.  # noqa: E501
        :type: date
        """

        self._filing_date = filing_date

    @property
    def public_float_value(self):
        """Gets the public_float_value of this CompanyPublicFloat.  # noqa: E501

        The dollar value for company float.  # noqa: E501

        :return: The public_float_value of this CompanyPublicFloat.  # noqa: E501
        :rtype: float
        """
        return self._public_float_value
        
    @property
    def public_float_value_dict(self):
        """Gets the public_float_value of this CompanyPublicFloat.  # noqa: E501

        The dollar value for company float. as a dictionary. Useful for Panda Dataframes.  # noqa: E501

        :return: The public_float_value of this CompanyPublicFloat.  # noqa: E501
        :rtype: float
        """

        result = None

        value = self.public_float_value
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
            result = { 'public_float_value': value }

        
        return result
        

    @public_float_value.setter
    def public_float_value(self, public_float_value):
        """Sets the public_float_value of this CompanyPublicFloat.

        The dollar value for company float.  # noqa: E501

        :param public_float_value: The public_float_value of this CompanyPublicFloat.  # noqa: E501
        :type: float
        """

        self._public_float_value = public_float_value

    @property
    def public_float_shares(self):
        """Gets the public_float_shares of this CompanyPublicFloat.  # noqa: E501

        The public shares for the company.  # noqa: E501

        :return: The public_float_shares of this CompanyPublicFloat.  # noqa: E501
        :rtype: float
        """
        return self._public_float_shares
        
    @property
    def public_float_shares_dict(self):
        """Gets the public_float_shares of this CompanyPublicFloat.  # noqa: E501

        The public shares for the company. as a dictionary. Useful for Panda Dataframes.  # noqa: E501

        :return: The public_float_shares of this CompanyPublicFloat.  # noqa: E501
        :rtype: float
        """

        result = None

        value = self.public_float_shares
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
            result = { 'public_float_shares': value }

        
        return result
        

    @public_float_shares.setter
    def public_float_shares(self, public_float_shares):
        """Sets the public_float_shares of this CompanyPublicFloat.

        The public shares for the company.  # noqa: E501

        :param public_float_shares: The public_float_shares of this CompanyPublicFloat.  # noqa: E501
        :type: float
        """

        self._public_float_shares = public_float_shares

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
        if not isinstance(other, CompanyPublicFloat):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
