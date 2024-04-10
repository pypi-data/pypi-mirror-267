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


class OptionPriceRealtime(object):
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
        'last': 'float',
        'last_size': 'int',
        'last_timestamp': 'datetime',
        'volume': 'int',
        'ask': 'float',
        'ask_size': 'int',
        'ask_timestamp': 'datetime',
        'bid': 'float',
        'bid_size': 'int',
        'bid_timestamp': 'datetime',
        'open_interest': 'int',
        'exercise_style': 'str'
    }

    attribute_map = {
        'last': 'last',
        'last_size': 'last_size',
        'last_timestamp': 'last_timestamp',
        'volume': 'volume',
        'ask': 'ask',
        'ask_size': 'ask_size',
        'ask_timestamp': 'ask_timestamp',
        'bid': 'bid',
        'bid_size': 'bid_size',
        'bid_timestamp': 'bid_timestamp',
        'open_interest': 'open_interest',
        'exercise_style': 'exercise_style'
    }

    def __init__(self, last=None, last_size=None, last_timestamp=None, volume=None, ask=None, ask_size=None, ask_timestamp=None, bid=None, bid_size=None, bid_timestamp=None, open_interest=None, exercise_style=None):  # noqa: E501
        """OptionPriceRealtime - a model defined in Swagger"""  # noqa: E501

        self._last = None
        self._last_size = None
        self._last_timestamp = None
        self._volume = None
        self._ask = None
        self._ask_size = None
        self._ask_timestamp = None
        self._bid = None
        self._bid_size = None
        self._bid_timestamp = None
        self._open_interest = None
        self._exercise_style = None
        self.discriminator = None

        if last is not None:
            self.last = last
        if last_size is not None:
            self.last_size = last_size
        if last_timestamp is not None:
            self.last_timestamp = last_timestamp
        if volume is not None:
            self.volume = volume
        if ask is not None:
            self.ask = ask
        if ask_size is not None:
            self.ask_size = ask_size
        if ask_timestamp is not None:
            self.ask_timestamp = ask_timestamp
        if bid is not None:
            self.bid = bid
        if bid_size is not None:
            self.bid_size = bid_size
        if bid_timestamp is not None:
            self.bid_timestamp = bid_timestamp
        if open_interest is not None:
            self.open_interest = open_interest
        if exercise_style is not None:
            self.exercise_style = exercise_style

    @property
    def last(self):
        """Gets the last of this OptionPriceRealtime.  # noqa: E501

        The price of the last trade  # noqa: E501

        :return: The last of this OptionPriceRealtime.  # noqa: E501
        :rtype: float
        """
        return self._last
        
    @property
    def last_dict(self):
        """Gets the last of this OptionPriceRealtime.  # noqa: E501

        The price of the last trade as a dictionary. Useful for Panda Dataframes.  # noqa: E501

        :return: The last of this OptionPriceRealtime.  # noqa: E501
        :rtype: float
        """

        result = None

        value = self.last
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
            result = { 'last': value }

        
        return result
        

    @last.setter
    def last(self, last):
        """Sets the last of this OptionPriceRealtime.

        The price of the last trade  # noqa: E501

        :param last: The last of this OptionPriceRealtime.  # noqa: E501
        :type: float
        """

        self._last = last

    @property
    def last_size(self):
        """Gets the last_size of this OptionPriceRealtime.  # noqa: E501

        The size of the last trade  # noqa: E501

        :return: The last_size of this OptionPriceRealtime.  # noqa: E501
        :rtype: int
        """
        return self._last_size
        
    @property
    def last_size_dict(self):
        """Gets the last_size of this OptionPriceRealtime.  # noqa: E501

        The size of the last trade as a dictionary. Useful for Panda Dataframes.  # noqa: E501

        :return: The last_size of this OptionPriceRealtime.  # noqa: E501
        :rtype: int
        """

        result = None

        value = self.last_size
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
            result = { 'last_size': value }

        
        return result
        

    @last_size.setter
    def last_size(self, last_size):
        """Sets the last_size of this OptionPriceRealtime.

        The size of the last trade  # noqa: E501

        :param last_size: The last_size of this OptionPriceRealtime.  # noqa: E501
        :type: int
        """

        self._last_size = last_size

    @property
    def last_timestamp(self):
        """Gets the last_timestamp of this OptionPriceRealtime.  # noqa: E501

        The time of the last trade  # noqa: E501

        :return: The last_timestamp of this OptionPriceRealtime.  # noqa: E501
        :rtype: datetime
        """
        return self._last_timestamp
        
    @property
    def last_timestamp_dict(self):
        """Gets the last_timestamp of this OptionPriceRealtime.  # noqa: E501

        The time of the last trade as a dictionary. Useful for Panda Dataframes.  # noqa: E501

        :return: The last_timestamp of this OptionPriceRealtime.  # noqa: E501
        :rtype: datetime
        """

        result = None

        value = self.last_timestamp
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
            result = { 'last_timestamp': value }

        
        return result
        

    @last_timestamp.setter
    def last_timestamp(self, last_timestamp):
        """Sets the last_timestamp of this OptionPriceRealtime.

        The time of the last trade  # noqa: E501

        :param last_timestamp: The last_timestamp of this OptionPriceRealtime.  # noqa: E501
        :type: datetime
        """

        self._last_timestamp = last_timestamp

    @property
    def volume(self):
        """Gets the volume of this OptionPriceRealtime.  # noqa: E501

        The cumulative volume of this options contract that traded that day.  # noqa: E501

        :return: The volume of this OptionPriceRealtime.  # noqa: E501
        :rtype: int
        """
        return self._volume
        
    @property
    def volume_dict(self):
        """Gets the volume of this OptionPriceRealtime.  # noqa: E501

        The cumulative volume of this options contract that traded that day. as a dictionary. Useful for Panda Dataframes.  # noqa: E501

        :return: The volume of this OptionPriceRealtime.  # noqa: E501
        :rtype: int
        """

        result = None

        value = self.volume
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
            result = { 'volume': value }

        
        return result
        

    @volume.setter
    def volume(self, volume):
        """Sets the volume of this OptionPriceRealtime.

        The cumulative volume of this options contract that traded that day.  # noqa: E501

        :param volume: The volume of this OptionPriceRealtime.  # noqa: E501
        :type: int
        """

        self._volume = volume

    @property
    def ask(self):
        """Gets the ask of this OptionPriceRealtime.  # noqa: E501

        The price of the top ask order  # noqa: E501

        :return: The ask of this OptionPriceRealtime.  # noqa: E501
        :rtype: float
        """
        return self._ask
        
    @property
    def ask_dict(self):
        """Gets the ask of this OptionPriceRealtime.  # noqa: E501

        The price of the top ask order as a dictionary. Useful for Panda Dataframes.  # noqa: E501

        :return: The ask of this OptionPriceRealtime.  # noqa: E501
        :rtype: float
        """

        result = None

        value = self.ask
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
            result = { 'ask': value }

        
        return result
        

    @ask.setter
    def ask(self, ask):
        """Sets the ask of this OptionPriceRealtime.

        The price of the top ask order  # noqa: E501

        :param ask: The ask of this OptionPriceRealtime.  # noqa: E501
        :type: float
        """

        self._ask = ask

    @property
    def ask_size(self):
        """Gets the ask_size of this OptionPriceRealtime.  # noqa: E501

        The size of the top ask order  # noqa: E501

        :return: The ask_size of this OptionPriceRealtime.  # noqa: E501
        :rtype: int
        """
        return self._ask_size
        
    @property
    def ask_size_dict(self):
        """Gets the ask_size of this OptionPriceRealtime.  # noqa: E501

        The size of the top ask order as a dictionary. Useful for Panda Dataframes.  # noqa: E501

        :return: The ask_size of this OptionPriceRealtime.  # noqa: E501
        :rtype: int
        """

        result = None

        value = self.ask_size
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
            result = { 'ask_size': value }

        
        return result
        

    @ask_size.setter
    def ask_size(self, ask_size):
        """Sets the ask_size of this OptionPriceRealtime.

        The size of the top ask order  # noqa: E501

        :param ask_size: The ask_size of this OptionPriceRealtime.  # noqa: E501
        :type: int
        """

        self._ask_size = ask_size

    @property
    def ask_timestamp(self):
        """Gets the ask_timestamp of this OptionPriceRealtime.  # noqa: E501

        The timestamp of the top ask order  # noqa: E501

        :return: The ask_timestamp of this OptionPriceRealtime.  # noqa: E501
        :rtype: datetime
        """
        return self._ask_timestamp
        
    @property
    def ask_timestamp_dict(self):
        """Gets the ask_timestamp of this OptionPriceRealtime.  # noqa: E501

        The timestamp of the top ask order as a dictionary. Useful for Panda Dataframes.  # noqa: E501

        :return: The ask_timestamp of this OptionPriceRealtime.  # noqa: E501
        :rtype: datetime
        """

        result = None

        value = self.ask_timestamp
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
            result = { 'ask_timestamp': value }

        
        return result
        

    @ask_timestamp.setter
    def ask_timestamp(self, ask_timestamp):
        """Sets the ask_timestamp of this OptionPriceRealtime.

        The timestamp of the top ask order  # noqa: E501

        :param ask_timestamp: The ask_timestamp of this OptionPriceRealtime.  # noqa: E501
        :type: datetime
        """

        self._ask_timestamp = ask_timestamp

    @property
    def bid(self):
        """Gets the bid of this OptionPriceRealtime.  # noqa: E501

        The price of the top bid order  # noqa: E501

        :return: The bid of this OptionPriceRealtime.  # noqa: E501
        :rtype: float
        """
        return self._bid
        
    @property
    def bid_dict(self):
        """Gets the bid of this OptionPriceRealtime.  # noqa: E501

        The price of the top bid order as a dictionary. Useful for Panda Dataframes.  # noqa: E501

        :return: The bid of this OptionPriceRealtime.  # noqa: E501
        :rtype: float
        """

        result = None

        value = self.bid
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
            result = { 'bid': value }

        
        return result
        

    @bid.setter
    def bid(self, bid):
        """Sets the bid of this OptionPriceRealtime.

        The price of the top bid order  # noqa: E501

        :param bid: The bid of this OptionPriceRealtime.  # noqa: E501
        :type: float
        """

        self._bid = bid

    @property
    def bid_size(self):
        """Gets the bid_size of this OptionPriceRealtime.  # noqa: E501

        The size of the top bid order  # noqa: E501

        :return: The bid_size of this OptionPriceRealtime.  # noqa: E501
        :rtype: int
        """
        return self._bid_size
        
    @property
    def bid_size_dict(self):
        """Gets the bid_size of this OptionPriceRealtime.  # noqa: E501

        The size of the top bid order as a dictionary. Useful for Panda Dataframes.  # noqa: E501

        :return: The bid_size of this OptionPriceRealtime.  # noqa: E501
        :rtype: int
        """

        result = None

        value = self.bid_size
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
            result = { 'bid_size': value }

        
        return result
        

    @bid_size.setter
    def bid_size(self, bid_size):
        """Sets the bid_size of this OptionPriceRealtime.

        The size of the top bid order  # noqa: E501

        :param bid_size: The bid_size of this OptionPriceRealtime.  # noqa: E501
        :type: int
        """

        self._bid_size = bid_size

    @property
    def bid_timestamp(self):
        """Gets the bid_timestamp of this OptionPriceRealtime.  # noqa: E501

        The time of the top bid order  # noqa: E501

        :return: The bid_timestamp of this OptionPriceRealtime.  # noqa: E501
        :rtype: datetime
        """
        return self._bid_timestamp
        
    @property
    def bid_timestamp_dict(self):
        """Gets the bid_timestamp of this OptionPriceRealtime.  # noqa: E501

        The time of the top bid order as a dictionary. Useful for Panda Dataframes.  # noqa: E501

        :return: The bid_timestamp of this OptionPriceRealtime.  # noqa: E501
        :rtype: datetime
        """

        result = None

        value = self.bid_timestamp
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
            result = { 'bid_timestamp': value }

        
        return result
        

    @bid_timestamp.setter
    def bid_timestamp(self, bid_timestamp):
        """Sets the bid_timestamp of this OptionPriceRealtime.

        The time of the top bid order  # noqa: E501

        :param bid_timestamp: The bid_timestamp of this OptionPriceRealtime.  # noqa: E501
        :type: datetime
        """

        self._bid_timestamp = bid_timestamp

    @property
    def open_interest(self):
        """Gets the open_interest of this OptionPriceRealtime.  # noqa: E501

        The total number of this options contract that are still open.  # noqa: E501

        :return: The open_interest of this OptionPriceRealtime.  # noqa: E501
        :rtype: int
        """
        return self._open_interest
        
    @property
    def open_interest_dict(self):
        """Gets the open_interest of this OptionPriceRealtime.  # noqa: E501

        The total number of this options contract that are still open. as a dictionary. Useful for Panda Dataframes.  # noqa: E501

        :return: The open_interest of this OptionPriceRealtime.  # noqa: E501
        :rtype: int
        """

        result = None

        value = self.open_interest
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
            result = { 'open_interest': value }

        
        return result
        

    @open_interest.setter
    def open_interest(self, open_interest):
        """Sets the open_interest of this OptionPriceRealtime.

        The total number of this options contract that are still open.  # noqa: E501

        :param open_interest: The open_interest of this OptionPriceRealtime.  # noqa: E501
        :type: int
        """

        self._open_interest = open_interest

    @property
    def exercise_style(self):
        """Gets the exercise_style of this OptionPriceRealtime.  # noqa: E501

        The exercise style of the option.  (\"A\" = \"American\", \"E\" = \"European\")  # noqa: E501

        :return: The exercise_style of this OptionPriceRealtime.  # noqa: E501
        :rtype: str
        """
        return self._exercise_style
        
    @property
    def exercise_style_dict(self):
        """Gets the exercise_style of this OptionPriceRealtime.  # noqa: E501

        The exercise style of the option.  (\"A\" = \"American\", \"E\" = \"European\") as a dictionary. Useful for Panda Dataframes.  # noqa: E501

        :return: The exercise_style of this OptionPriceRealtime.  # noqa: E501
        :rtype: str
        """

        result = None

        value = self.exercise_style
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
            result = { 'exercise_style': value }

        
        return result
        

    @exercise_style.setter
    def exercise_style(self, exercise_style):
        """Sets the exercise_style of this OptionPriceRealtime.

        The exercise style of the option.  (\"A\" = \"American\", \"E\" = \"European\")  # noqa: E501

        :param exercise_style: The exercise_style of this OptionPriceRealtime.  # noqa: E501
        :type: str
        """
        allowed_values = ["A", "E"]  # noqa: E501
        if exercise_style not in allowed_values:
            raise ValueError(
                "Invalid value for `exercise_style` ({0}), must be one of {1}"  # noqa: E501
                .format(exercise_style, allowed_values)
            )

        self._exercise_style = exercise_style

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
        if not isinstance(other, OptionPriceRealtime):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
