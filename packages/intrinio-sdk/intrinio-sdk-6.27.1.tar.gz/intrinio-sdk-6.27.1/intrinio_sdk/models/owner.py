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


class Owner(object):
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
        'id': 'str',
        'company_id': 'str',
        'owner_cik': 'str',
        'name': 'str',
        'state': 'str',
        'state_inc': 'str',
        'country_inc': 'str',
        'business_address': 'str',
        'business_phone_no': 'str',
        'mailing_address': 'str',
        'institutional': 'bool',
        'updated_on': 'datetime',
        'created_on': 'datetime'
    }

    attribute_map = {
        'id': 'id',
        'company_id': 'company_id',
        'owner_cik': 'owner_cik',
        'name': 'name',
        'state': 'state',
        'state_inc': 'state_inc',
        'country_inc': 'country_inc',
        'business_address': 'business_address',
        'business_phone_no': 'business_phone_no',
        'mailing_address': 'mailing_address',
        'institutional': 'institutional',
        'updated_on': 'updated_on',
        'created_on': 'created_on'
    }

    def __init__(self, id=None, company_id=None, owner_cik=None, name=None, state=None, state_inc=None, country_inc=None, business_address=None, business_phone_no=None, mailing_address=None, institutional=None, updated_on=None, created_on=None):  # noqa: E501
        """Owner - a model defined in Swagger"""  # noqa: E501

        self._id = None
        self._company_id = None
        self._owner_cik = None
        self._name = None
        self._state = None
        self._state_inc = None
        self._country_inc = None
        self._business_address = None
        self._business_phone_no = None
        self._mailing_address = None
        self._institutional = None
        self._updated_on = None
        self._created_on = None
        self.discriminator = None

        if id is not None:
            self.id = id
        if company_id is not None:
            self.company_id = company_id
        if owner_cik is not None:
            self.owner_cik = owner_cik
        if name is not None:
            self.name = name
        if state is not None:
            self.state = state
        if state_inc is not None:
            self.state_inc = state_inc
        if country_inc is not None:
            self.country_inc = country_inc
        if business_address is not None:
            self.business_address = business_address
        if business_phone_no is not None:
            self.business_phone_no = business_phone_no
        if mailing_address is not None:
            self.mailing_address = mailing_address
        if institutional is not None:
            self.institutional = institutional
        if updated_on is not None:
            self.updated_on = updated_on
        if created_on is not None:
            self.created_on = created_on

    @property
    def id(self):
        """Gets the id of this Owner.  # noqa: E501

        The Intrinio ID for the Owner  # noqa: E501

        :return: The id of this Owner.  # noqa: E501
        :rtype: str
        """
        return self._id
        
    @property
    def id_dict(self):
        """Gets the id of this Owner.  # noqa: E501

        The Intrinio ID for the Owner as a dictionary. Useful for Panda Dataframes.  # noqa: E501

        :return: The id of this Owner.  # noqa: E501
        :rtype: str
        """

        result = None

        value = self.id
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
            result = { 'id': value }

        
        return result
        

    @id.setter
    def id(self, id):
        """Sets the id of this Owner.

        The Intrinio ID for the Owner  # noqa: E501

        :param id: The id of this Owner.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def company_id(self):
        """Gets the company_id of this Owner.  # noqa: E501

        The Intrinio ID for the company for which the Security is issued  # noqa: E501

        :return: The company_id of this Owner.  # noqa: E501
        :rtype: str
        """
        return self._company_id
        
    @property
    def company_id_dict(self):
        """Gets the company_id of this Owner.  # noqa: E501

        The Intrinio ID for the company for which the Security is issued as a dictionary. Useful for Panda Dataframes.  # noqa: E501

        :return: The company_id of this Owner.  # noqa: E501
        :rtype: str
        """

        result = None

        value = self.company_id
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
            result = { 'company_id': value }

        
        return result
        

    @company_id.setter
    def company_id(self, company_id):
        """Sets the company_id of this Owner.

        The Intrinio ID for the company for which the Security is issued  # noqa: E501

        :param company_id: The company_id of this Owner.  # noqa: E501
        :type: str
        """

        self._company_id = company_id

    @property
    def owner_cik(self):
        """Gets the owner_cik of this Owner.  # noqa: E501

        The Central Index Key issued by the SEC, which is the unique identifier all owner filings  # noqa: E501

        :return: The owner_cik of this Owner.  # noqa: E501
        :rtype: str
        """
        return self._owner_cik
        
    @property
    def owner_cik_dict(self):
        """Gets the owner_cik of this Owner.  # noqa: E501

        The Central Index Key issued by the SEC, which is the unique identifier all owner filings as a dictionary. Useful for Panda Dataframes.  # noqa: E501

        :return: The owner_cik of this Owner.  # noqa: E501
        :rtype: str
        """

        result = None

        value = self.owner_cik
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
            result = { 'owner_cik': value }

        
        return result
        

    @owner_cik.setter
    def owner_cik(self, owner_cik):
        """Sets the owner_cik of this Owner.

        The Central Index Key issued by the SEC, which is the unique identifier all owner filings  # noqa: E501

        :param owner_cik: The owner_cik of this Owner.  # noqa: E501
        :type: str
        """

        self._owner_cik = owner_cik

    @property
    def name(self):
        """Gets the name of this Owner.  # noqa: E501

        The name of the owner  # noqa: E501

        :return: The name of this Owner.  # noqa: E501
        :rtype: str
        """
        return self._name
        
    @property
    def name_dict(self):
        """Gets the name of this Owner.  # noqa: E501

        The name of the owner as a dictionary. Useful for Panda Dataframes.  # noqa: E501

        :return: The name of this Owner.  # noqa: E501
        :rtype: str
        """

        result = None

        value = self.name
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
            result = { 'name': value }

        
        return result
        

    @name.setter
    def name(self, name):
        """Sets the name of this Owner.

        The name of the owner  # noqa: E501

        :param name: The name of this Owner.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def state(self):
        """Gets the state of this Owner.  # noqa: E501

        The state in which the owner is located  # noqa: E501

        :return: The state of this Owner.  # noqa: E501
        :rtype: str
        """
        return self._state
        
    @property
    def state_dict(self):
        """Gets the state of this Owner.  # noqa: E501

        The state in which the owner is located as a dictionary. Useful for Panda Dataframes.  # noqa: E501

        :return: The state of this Owner.  # noqa: E501
        :rtype: str
        """

        result = None

        value = self.state
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
            result = { 'state': value }

        
        return result
        

    @state.setter
    def state(self, state):
        """Sets the state of this Owner.

        The state in which the owner is located  # noqa: E501

        :param state: The state of this Owner.  # noqa: E501
        :type: str
        """

        self._state = state

    @property
    def state_inc(self):
        """Gets the state_inc of this Owner.  # noqa: E501

        The state in which the owner is incorporated  # noqa: E501

        :return: The state_inc of this Owner.  # noqa: E501
        :rtype: str
        """
        return self._state_inc
        
    @property
    def state_inc_dict(self):
        """Gets the state_inc of this Owner.  # noqa: E501

        The state in which the owner is incorporated as a dictionary. Useful for Panda Dataframes.  # noqa: E501

        :return: The state_inc of this Owner.  # noqa: E501
        :rtype: str
        """

        result = None

        value = self.state_inc
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
            result = { 'state_inc': value }

        
        return result
        

    @state_inc.setter
    def state_inc(self, state_inc):
        """Sets the state_inc of this Owner.

        The state in which the owner is incorporated  # noqa: E501

        :param state_inc: The state_inc of this Owner.  # noqa: E501
        :type: str
        """

        self._state_inc = state_inc

    @property
    def country_inc(self):
        """Gets the country_inc of this Owner.  # noqa: E501

        The country in which the owner is incorporated  # noqa: E501

        :return: The country_inc of this Owner.  # noqa: E501
        :rtype: str
        """
        return self._country_inc
        
    @property
    def country_inc_dict(self):
        """Gets the country_inc of this Owner.  # noqa: E501

        The country in which the owner is incorporated as a dictionary. Useful for Panda Dataframes.  # noqa: E501

        :return: The country_inc of this Owner.  # noqa: E501
        :rtype: str
        """

        result = None

        value = self.country_inc
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
            result = { 'country_inc': value }

        
        return result
        

    @country_inc.setter
    def country_inc(self, country_inc):
        """Sets the country_inc of this Owner.

        The country in which the owner is incorporated  # noqa: E501

        :param country_inc: The country_inc of this Owner.  # noqa: E501
        :type: str
        """

        self._country_inc = country_inc

    @property
    def business_address(self):
        """Gets the business_address of this Owner.  # noqa: E501

        The owner's business address  # noqa: E501

        :return: The business_address of this Owner.  # noqa: E501
        :rtype: str
        """
        return self._business_address
        
    @property
    def business_address_dict(self):
        """Gets the business_address of this Owner.  # noqa: E501

        The owner's business address as a dictionary. Useful for Panda Dataframes.  # noqa: E501

        :return: The business_address of this Owner.  # noqa: E501
        :rtype: str
        """

        result = None

        value = self.business_address
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
            result = { 'business_address': value }

        
        return result
        

    @business_address.setter
    def business_address(self, business_address):
        """Sets the business_address of this Owner.

        The owner's business address  # noqa: E501

        :param business_address: The business_address of this Owner.  # noqa: E501
        :type: str
        """

        self._business_address = business_address

    @property
    def business_phone_no(self):
        """Gets the business_phone_no of this Owner.  # noqa: E501

        The owner's business phone number  # noqa: E501

        :return: The business_phone_no of this Owner.  # noqa: E501
        :rtype: str
        """
        return self._business_phone_no
        
    @property
    def business_phone_no_dict(self):
        """Gets the business_phone_no of this Owner.  # noqa: E501

        The owner's business phone number as a dictionary. Useful for Panda Dataframes.  # noqa: E501

        :return: The business_phone_no of this Owner.  # noqa: E501
        :rtype: str
        """

        result = None

        value = self.business_phone_no
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
            result = { 'business_phone_no': value }

        
        return result
        

    @business_phone_no.setter
    def business_phone_no(self, business_phone_no):
        """Sets the business_phone_no of this Owner.

        The owner's business phone number  # noqa: E501

        :param business_phone_no: The business_phone_no of this Owner.  # noqa: E501
        :type: str
        """

        self._business_phone_no = business_phone_no

    @property
    def mailing_address(self):
        """Gets the mailing_address of this Owner.  # noqa: E501

        The owner's mailing address  # noqa: E501

        :return: The mailing_address of this Owner.  # noqa: E501
        :rtype: str
        """
        return self._mailing_address
        
    @property
    def mailing_address_dict(self):
        """Gets the mailing_address of this Owner.  # noqa: E501

        The owner's mailing address as a dictionary. Useful for Panda Dataframes.  # noqa: E501

        :return: The mailing_address of this Owner.  # noqa: E501
        :rtype: str
        """

        result = None

        value = self.mailing_address
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
            result = { 'mailing_address': value }

        
        return result
        

    @mailing_address.setter
    def mailing_address(self, mailing_address):
        """Sets the mailing_address of this Owner.

        The owner's mailing address  # noqa: E501

        :param mailing_address: The mailing_address of this Owner.  # noqa: E501
        :type: str
        """

        self._mailing_address = mailing_address

    @property
    def institutional(self):
        """Gets the institutional of this Owner.  # noqa: E501

        A boolean to include only insider owners who have filed forms 3, 4, or 5 with the SEC  # noqa: E501

        :return: The institutional of this Owner.  # noqa: E501
        :rtype: bool
        """
        return self._institutional
        
    @property
    def institutional_dict(self):
        """Gets the institutional of this Owner.  # noqa: E501

        A boolean to include only insider owners who have filed forms 3, 4, or 5 with the SEC as a dictionary. Useful for Panda Dataframes.  # noqa: E501

        :return: The institutional of this Owner.  # noqa: E501
        :rtype: bool
        """

        result = None

        value = self.institutional
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
            result = { 'institutional': value }

        
        return result
        

    @institutional.setter
    def institutional(self, institutional):
        """Sets the institutional of this Owner.

        A boolean to include only insider owners who have filed forms 3, 4, or 5 with the SEC  # noqa: E501

        :param institutional: The institutional of this Owner.  # noqa: E501
        :type: bool
        """

        self._institutional = institutional

    @property
    def updated_on(self):
        """Gets the updated_on of this Owner.  # noqa: E501

        The date and time when the data was last updated.  # noqa: E501

        :return: The updated_on of this Owner.  # noqa: E501
        :rtype: datetime
        """
        return self._updated_on
        
    @property
    def updated_on_dict(self):
        """Gets the updated_on of this Owner.  # noqa: E501

        The date and time when the data was last updated. as a dictionary. Useful for Panda Dataframes.  # noqa: E501

        :return: The updated_on of this Owner.  # noqa: E501
        :rtype: datetime
        """

        result = None

        value = self.updated_on
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
            result = { 'updated_on': value }

        
        return result
        

    @updated_on.setter
    def updated_on(self, updated_on):
        """Sets the updated_on of this Owner.

        The date and time when the data was last updated.  # noqa: E501

        :param updated_on: The updated_on of this Owner.  # noqa: E501
        :type: datetime
        """

        self._updated_on = updated_on

    @property
    def created_on(self):
        """Gets the created_on of this Owner.  # noqa: E501

        The date and time when the data was created  # noqa: E501

        :return: The created_on of this Owner.  # noqa: E501
        :rtype: datetime
        """
        return self._created_on
        
    @property
    def created_on_dict(self):
        """Gets the created_on of this Owner.  # noqa: E501

        The date and time when the data was created as a dictionary. Useful for Panda Dataframes.  # noqa: E501

        :return: The created_on of this Owner.  # noqa: E501
        :rtype: datetime
        """

        result = None

        value = self.created_on
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
            result = { 'created_on': value }

        
        return result
        

    @created_on.setter
    def created_on(self, created_on):
        """Sets the created_on of this Owner.

        The date and time when the data was created  # noqa: E501

        :param created_on: The created_on of this Owner.  # noqa: E501
        :type: datetime
        """

        self._created_on = created_on

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
        if not isinstance(other, Owner):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
