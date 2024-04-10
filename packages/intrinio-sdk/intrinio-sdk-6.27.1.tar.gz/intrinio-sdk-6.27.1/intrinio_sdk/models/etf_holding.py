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


class ETFHolding(object):
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
        'as_of_date': 'date',
        'name': 'str',
        'ticker': 'str',
        'type': 'str',
        'composite_figi': 'str',
        'share_class_figi': 'str',
        'isin': 'str',
        'ric': 'str',
        'sedol': 'str',
        'face': 'float',
        'coupon': 'float',
        'market_value_held': 'float',
        'notional_value': 'float',
        'maturity': 'date',
        'quantity_held': 'float',
        'weighting': 'float',
        'quantity_units': 'float',
        'quantity_per_share': 'float',
        'contract_expiry_date': 'date'
    }

    attribute_map = {
        'as_of_date': 'as_of_date',
        'name': 'name',
        'ticker': 'ticker',
        'type': 'type',
        'composite_figi': 'composite_figi',
        'share_class_figi': 'share_class_figi',
        'isin': 'isin',
        'ric': 'ric',
        'sedol': 'sedol',
        'face': 'face',
        'coupon': 'coupon',
        'market_value_held': 'market_value_held',
        'notional_value': 'notional_value',
        'maturity': 'maturity',
        'quantity_held': 'quantity_held',
        'weighting': 'weighting',
        'quantity_units': 'quantity_units',
        'quantity_per_share': 'quantity_per_share',
        'contract_expiry_date': 'contract_expiry_date'
    }

    def __init__(self, as_of_date=None, name=None, ticker=None, type=None, composite_figi=None, share_class_figi=None, isin=None, ric=None, sedol=None, face=None, coupon=None, market_value_held=None, notional_value=None, maturity=None, quantity_held=None, weighting=None, quantity_units=None, quantity_per_share=None, contract_expiry_date=None):  # noqa: E501
        """ETFHolding - a model defined in Swagger"""  # noqa: E501

        self._as_of_date = None
        self._name = None
        self._ticker = None
        self._type = None
        self._composite_figi = None
        self._share_class_figi = None
        self._isin = None
        self._ric = None
        self._sedol = None
        self._face = None
        self._coupon = None
        self._market_value_held = None
        self._notional_value = None
        self._maturity = None
        self._quantity_held = None
        self._weighting = None
        self._quantity_units = None
        self._quantity_per_share = None
        self._contract_expiry_date = None
        self.discriminator = None

        if as_of_date is not None:
            self.as_of_date = as_of_date
        if name is not None:
            self.name = name
        if ticker is not None:
            self.ticker = ticker
        if type is not None:
            self.type = type
        if composite_figi is not None:
            self.composite_figi = composite_figi
        if share_class_figi is not None:
            self.share_class_figi = share_class_figi
        if isin is not None:
            self.isin = isin
        if ric is not None:
            self.ric = ric
        if sedol is not None:
            self.sedol = sedol
        if face is not None:
            self.face = face
        if coupon is not None:
            self.coupon = coupon
        if market_value_held is not None:
            self.market_value_held = market_value_held
        if notional_value is not None:
            self.notional_value = notional_value
        if maturity is not None:
            self.maturity = maturity
        if quantity_held is not None:
            self.quantity_held = quantity_held
        if weighting is not None:
            self.weighting = weighting
        if quantity_units is not None:
            self.quantity_units = quantity_units
        if quantity_per_share is not None:
            self.quantity_per_share = quantity_per_share
        if contract_expiry_date is not None:
            self.contract_expiry_date = contract_expiry_date

    @property
    def as_of_date(self):
        """Gets the as_of_date of this ETFHolding.  # noqa: E501

        The date on which the holding and their weights correspond  # noqa: E501

        :return: The as_of_date of this ETFHolding.  # noqa: E501
        :rtype: date
        """
        return self._as_of_date
        
    @property
    def as_of_date_dict(self):
        """Gets the as_of_date of this ETFHolding.  # noqa: E501

        The date on which the holding and their weights correspond as a dictionary. Useful for Panda Dataframes.  # noqa: E501

        :return: The as_of_date of this ETFHolding.  # noqa: E501
        :rtype: date
        """

        result = None

        value = self.as_of_date
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
            result = { 'as_of_date': value }

        
        return result
        

    @as_of_date.setter
    def as_of_date(self, as_of_date):
        """Sets the as_of_date of this ETFHolding.

        The date on which the holding and their weights correspond  # noqa: E501

        :param as_of_date: The as_of_date of this ETFHolding.  # noqa: E501
        :type: date
        """

        self._as_of_date = as_of_date

    @property
    def name(self):
        """Gets the name of this ETFHolding.  # noqa: E501

        The common name for the holding  # noqa: E501

        :return: The name of this ETFHolding.  # noqa: E501
        :rtype: str
        """
        return self._name
        
    @property
    def name_dict(self):
        """Gets the name of this ETFHolding.  # noqa: E501

        The common name for the holding as a dictionary. Useful for Panda Dataframes.  # noqa: E501

        :return: The name of this ETFHolding.  # noqa: E501
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
        """Sets the name of this ETFHolding.

        The common name for the holding  # noqa: E501

        :param name: The name of this ETFHolding.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def ticker(self):
        """Gets the ticker of this ETFHolding.  # noqa: E501

        The common exchange ticker for the holding  # noqa: E501

        :return: The ticker of this ETFHolding.  # noqa: E501
        :rtype: str
        """
        return self._ticker
        
    @property
    def ticker_dict(self):
        """Gets the ticker of this ETFHolding.  # noqa: E501

        The common exchange ticker for the holding as a dictionary. Useful for Panda Dataframes.  # noqa: E501

        :return: The ticker of this ETFHolding.  # noqa: E501
        :rtype: str
        """

        result = None

        value = self.ticker
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
            result = { 'ticker': value }

        
        return result
        

    @ticker.setter
    def ticker(self, ticker):
        """Sets the ticker of this ETFHolding.

        The common exchange ticker for the holding  # noqa: E501

        :param ticker: The ticker of this ETFHolding.  # noqa: E501
        :type: str
        """

        self._ticker = ticker

    @property
    def type(self):
        """Gets the type of this ETFHolding.  # noqa: E501

        The type of instrument for this holding.  Examples (Bond = 'BOND', Equity = 'EQUI', Options = 'OPTN')  # noqa: E501

        :return: The type of this ETFHolding.  # noqa: E501
        :rtype: str
        """
        return self._type
        
    @property
    def type_dict(self):
        """Gets the type of this ETFHolding.  # noqa: E501

        The type of instrument for this holding.  Examples (Bond = 'BOND', Equity = 'EQUI', Options = 'OPTN') as a dictionary. Useful for Panda Dataframes.  # noqa: E501

        :return: The type of this ETFHolding.  # noqa: E501
        :rtype: str
        """

        result = None

        value = self.type
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
            result = { 'type': value }

        
        return result
        

    @type.setter
    def type(self, type):
        """Sets the type of this ETFHolding.

        The type of instrument for this holding.  Examples (Bond = 'BOND', Equity = 'EQUI', Options = 'OPTN')  # noqa: E501

        :param type: The type of this ETFHolding.  # noqa: E501
        :type: str
        """

        self._type = type

    @property
    def composite_figi(self):
        """Gets the composite_figi of this ETFHolding.  # noqa: E501

        DEPRECATED  # noqa: E501

        :return: The composite_figi of this ETFHolding.  # noqa: E501
        :rtype: str
        """
        return self._composite_figi
        
    @property
    def composite_figi_dict(self):
        """Gets the composite_figi of this ETFHolding.  # noqa: E501

        DEPRECATED as a dictionary. Useful for Panda Dataframes.  # noqa: E501

        :return: The composite_figi of this ETFHolding.  # noqa: E501
        :rtype: str
        """

        result = None

        value = self.composite_figi
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
            result = { 'composite_figi': value }

        
        return result
        

    @composite_figi.setter
    def composite_figi(self, composite_figi):
        """Sets the composite_figi of this ETFHolding.

        DEPRECATED  # noqa: E501

        :param composite_figi: The composite_figi of this ETFHolding.  # noqa: E501
        :type: str
        """

        self._composite_figi = composite_figi

    @property
    def share_class_figi(self):
        """Gets the share_class_figi of this ETFHolding.  # noqa: E501

        The OpenFIGI symbol for the holding  # noqa: E501

        :return: The share_class_figi of this ETFHolding.  # noqa: E501
        :rtype: str
        """
        return self._share_class_figi
        
    @property
    def share_class_figi_dict(self):
        """Gets the share_class_figi of this ETFHolding.  # noqa: E501

        The OpenFIGI symbol for the holding as a dictionary. Useful for Panda Dataframes.  # noqa: E501

        :return: The share_class_figi of this ETFHolding.  # noqa: E501
        :rtype: str
        """

        result = None

        value = self.share_class_figi
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
            result = { 'share_class_figi': value }

        
        return result
        

    @share_class_figi.setter
    def share_class_figi(self, share_class_figi):
        """Sets the share_class_figi of this ETFHolding.

        The OpenFIGI symbol for the holding  # noqa: E501

        :param share_class_figi: The share_class_figi of this ETFHolding.  # noqa: E501
        :type: str
        """

        self._share_class_figi = share_class_figi

    @property
    def isin(self):
        """Gets the isin of this ETFHolding.  # noqa: E501

        International Securities Identification Number (ISIN) for the holding  # noqa: E501

        :return: The isin of this ETFHolding.  # noqa: E501
        :rtype: str
        """
        return self._isin
        
    @property
    def isin_dict(self):
        """Gets the isin of this ETFHolding.  # noqa: E501

        International Securities Identification Number (ISIN) for the holding as a dictionary. Useful for Panda Dataframes.  # noqa: E501

        :return: The isin of this ETFHolding.  # noqa: E501
        :rtype: str
        """

        result = None

        value = self.isin
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
            result = { 'isin': value }

        
        return result
        

    @isin.setter
    def isin(self, isin):
        """Sets the isin of this ETFHolding.

        International Securities Identification Number (ISIN) for the holding  # noqa: E501

        :param isin: The isin of this ETFHolding.  # noqa: E501
        :type: str
        """

        self._isin = isin

    @property
    def ric(self):
        """Gets the ric of this ETFHolding.  # noqa: E501

        Reuters Instrument Code (RIC) for the holding  # noqa: E501

        :return: The ric of this ETFHolding.  # noqa: E501
        :rtype: str
        """
        return self._ric
        
    @property
    def ric_dict(self):
        """Gets the ric of this ETFHolding.  # noqa: E501

        Reuters Instrument Code (RIC) for the holding as a dictionary. Useful for Panda Dataframes.  # noqa: E501

        :return: The ric of this ETFHolding.  # noqa: E501
        :rtype: str
        """

        result = None

        value = self.ric
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
            result = { 'ric': value }

        
        return result
        

    @ric.setter
    def ric(self, ric):
        """Sets the ric of this ETFHolding.

        Reuters Instrument Code (RIC) for the holding  # noqa: E501

        :param ric: The ric of this ETFHolding.  # noqa: E501
        :type: str
        """

        self._ric = ric

    @property
    def sedol(self):
        """Gets the sedol of this ETFHolding.  # noqa: E501

        Stock Exchange Daily Official List (SEDOL) for the holding  # noqa: E501

        :return: The sedol of this ETFHolding.  # noqa: E501
        :rtype: str
        """
        return self._sedol
        
    @property
    def sedol_dict(self):
        """Gets the sedol of this ETFHolding.  # noqa: E501

        Stock Exchange Daily Official List (SEDOL) for the holding as a dictionary. Useful for Panda Dataframes.  # noqa: E501

        :return: The sedol of this ETFHolding.  # noqa: E501
        :rtype: str
        """

        result = None

        value = self.sedol
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
            result = { 'sedol': value }

        
        return result
        

    @sedol.setter
    def sedol(self, sedol):
        """Sets the sedol of this ETFHolding.

        Stock Exchange Daily Official List (SEDOL) for the holding  # noqa: E501

        :param sedol: The sedol of this ETFHolding.  # noqa: E501
        :type: str
        """

        self._sedol = sedol

    @property
    def face(self):
        """Gets the face of this ETFHolding.  # noqa: E501

        Face value of the debt security, if available  # noqa: E501

        :return: The face of this ETFHolding.  # noqa: E501
        :rtype: float
        """
        return self._face
        
    @property
    def face_dict(self):
        """Gets the face of this ETFHolding.  # noqa: E501

        Face value of the debt security, if available as a dictionary. Useful for Panda Dataframes.  # noqa: E501

        :return: The face of this ETFHolding.  # noqa: E501
        :rtype: float
        """

        result = None

        value = self.face
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
            result = { 'face': value }

        
        return result
        

    @face.setter
    def face(self, face):
        """Sets the face of this ETFHolding.

        Face value of the debt security, if available  # noqa: E501

        :param face: The face of this ETFHolding.  # noqa: E501
        :type: float
        """

        self._face = face

    @property
    def coupon(self):
        """Gets the coupon of this ETFHolding.  # noqa: E501

        Coupon rate of the debt security, if available  # noqa: E501

        :return: The coupon of this ETFHolding.  # noqa: E501
        :rtype: float
        """
        return self._coupon
        
    @property
    def coupon_dict(self):
        """Gets the coupon of this ETFHolding.  # noqa: E501

        Coupon rate of the debt security, if available as a dictionary. Useful for Panda Dataframes.  # noqa: E501

        :return: The coupon of this ETFHolding.  # noqa: E501
        :rtype: float
        """

        result = None

        value = self.coupon
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
            result = { 'coupon': value }

        
        return result
        

    @coupon.setter
    def coupon(self, coupon):
        """Sets the coupon of this ETFHolding.

        Coupon rate of the debt security, if available  # noqa: E501

        :param coupon: The coupon of this ETFHolding.  # noqa: E501
        :type: float
        """

        self._coupon = coupon

    @property
    def market_value_held(self):
        """Gets the market_value_held of this ETFHolding.  # noqa: E501

        The market value of this holding in the ETF as of the `as_of_date`  # noqa: E501

        :return: The market_value_held of this ETFHolding.  # noqa: E501
        :rtype: float
        """
        return self._market_value_held
        
    @property
    def market_value_held_dict(self):
        """Gets the market_value_held of this ETFHolding.  # noqa: E501

        The market value of this holding in the ETF as of the `as_of_date` as a dictionary. Useful for Panda Dataframes.  # noqa: E501

        :return: The market_value_held of this ETFHolding.  # noqa: E501
        :rtype: float
        """

        result = None

        value = self.market_value_held
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
            result = { 'market_value_held': value }

        
        return result
        

    @market_value_held.setter
    def market_value_held(self, market_value_held):
        """Sets the market_value_held of this ETFHolding.

        The market value of this holding in the ETF as of the `as_of_date`  # noqa: E501

        :param market_value_held: The market_value_held of this ETFHolding.  # noqa: E501
        :type: float
        """

        self._market_value_held = market_value_held

    @property
    def notional_value(self):
        """Gets the notional_value of this ETFHolding.  # noqa: E501

        Notional value of derivatives contracts held in the Exchange Traded Fund (ETF) or Exchange Traded Note (ETN)  # noqa: E501

        :return: The notional_value of this ETFHolding.  # noqa: E501
        :rtype: float
        """
        return self._notional_value
        
    @property
    def notional_value_dict(self):
        """Gets the notional_value of this ETFHolding.  # noqa: E501

        Notional value of derivatives contracts held in the Exchange Traded Fund (ETF) or Exchange Traded Note (ETN) as a dictionary. Useful for Panda Dataframes.  # noqa: E501

        :return: The notional_value of this ETFHolding.  # noqa: E501
        :rtype: float
        """

        result = None

        value = self.notional_value
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
            result = { 'notional_value': value }

        
        return result
        

    @notional_value.setter
    def notional_value(self, notional_value):
        """Sets the notional_value of this ETFHolding.

        Notional value of derivatives contracts held in the Exchange Traded Fund (ETF) or Exchange Traded Note (ETN)  # noqa: E501

        :param notional_value: The notional_value of this ETFHolding.  # noqa: E501
        :type: float
        """

        self._notional_value = notional_value

    @property
    def maturity(self):
        """Gets the maturity of this ETFHolding.  # noqa: E501

        Maturity date for the debt security, if available  # noqa: E501

        :return: The maturity of this ETFHolding.  # noqa: E501
        :rtype: date
        """
        return self._maturity
        
    @property
    def maturity_dict(self):
        """Gets the maturity of this ETFHolding.  # noqa: E501

        Maturity date for the debt security, if available as a dictionary. Useful for Panda Dataframes.  # noqa: E501

        :return: The maturity of this ETFHolding.  # noqa: E501
        :rtype: date
        """

        result = None

        value = self.maturity
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
            result = { 'maturity': value }

        
        return result
        

    @maturity.setter
    def maturity(self, maturity):
        """Sets the maturity of this ETFHolding.

        Maturity date for the debt security, if available  # noqa: E501

        :param maturity: The maturity of this ETFHolding.  # noqa: E501
        :type: date
        """

        self._maturity = maturity

    @property
    def quantity_held(self):
        """Gets the quantity_held of this ETFHolding.  # noqa: E501

        Number of units of the security held if available  # noqa: E501

        :return: The quantity_held of this ETFHolding.  # noqa: E501
        :rtype: float
        """
        return self._quantity_held
        
    @property
    def quantity_held_dict(self):
        """Gets the quantity_held of this ETFHolding.  # noqa: E501

        Number of units of the security held if available as a dictionary. Useful for Panda Dataframes.  # noqa: E501

        :return: The quantity_held of this ETFHolding.  # noqa: E501
        :rtype: float
        """

        result = None

        value = self.quantity_held
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
            result = { 'quantity_held': value }

        
        return result
        

    @quantity_held.setter
    def quantity_held(self, quantity_held):
        """Sets the quantity_held of this ETFHolding.

        Number of units of the security held if available  # noqa: E501

        :param quantity_held: The quantity_held of this ETFHolding.  # noqa: E501
        :type: float
        """

        self._quantity_held = quantity_held

    @property
    def weighting(self):
        """Gets the weighting of this ETFHolding.  # noqa: E501

        Fraction of the funds market value held  # noqa: E501

        :return: The weighting of this ETFHolding.  # noqa: E501
        :rtype: float
        """
        return self._weighting
        
    @property
    def weighting_dict(self):
        """Gets the weighting of this ETFHolding.  # noqa: E501

        Fraction of the funds market value held as a dictionary. Useful for Panda Dataframes.  # noqa: E501

        :return: The weighting of this ETFHolding.  # noqa: E501
        :rtype: float
        """

        result = None

        value = self.weighting
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
            result = { 'weighting': value }

        
        return result
        

    @weighting.setter
    def weighting(self, weighting):
        """Sets the weighting of this ETFHolding.

        Fraction of the funds market value held  # noqa: E501

        :param weighting: The weighting of this ETFHolding.  # noqa: E501
        :type: float
        """

        self._weighting = weighting

    @property
    def quantity_units(self):
        """Gets the quantity_units of this ETFHolding.  # noqa: E501

        The unit of the `quanity_held` field. Examples ('oz', 'shares', 'contracts')  # noqa: E501

        :return: The quantity_units of this ETFHolding.  # noqa: E501
        :rtype: float
        """
        return self._quantity_units
        
    @property
    def quantity_units_dict(self):
        """Gets the quantity_units of this ETFHolding.  # noqa: E501

        The unit of the `quanity_held` field. Examples ('oz', 'shares', 'contracts') as a dictionary. Useful for Panda Dataframes.  # noqa: E501

        :return: The quantity_units of this ETFHolding.  # noqa: E501
        :rtype: float
        """

        result = None

        value = self.quantity_units
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
            result = { 'quantity_units': value }

        
        return result
        

    @quantity_units.setter
    def quantity_units(self, quantity_units):
        """Sets the quantity_units of this ETFHolding.

        The unit of the `quanity_held` field. Examples ('oz', 'shares', 'contracts')  # noqa: E501

        :param quantity_units: The quantity_units of this ETFHolding.  # noqa: E501
        :type: float
        """

        self._quantity_units = quantity_units

    @property
    def quantity_per_share(self):
        """Gets the quantity_per_share of this ETFHolding.  # noqa: E501

        Number of units of the security held per units of shares outstanding of the Exchange Traded Fund (ETF), if available  # noqa: E501

        :return: The quantity_per_share of this ETFHolding.  # noqa: E501
        :rtype: float
        """
        return self._quantity_per_share
        
    @property
    def quantity_per_share_dict(self):
        """Gets the quantity_per_share of this ETFHolding.  # noqa: E501

        Number of units of the security held per units of shares outstanding of the Exchange Traded Fund (ETF), if available as a dictionary. Useful for Panda Dataframes.  # noqa: E501

        :return: The quantity_per_share of this ETFHolding.  # noqa: E501
        :rtype: float
        """

        result = None

        value = self.quantity_per_share
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
            result = { 'quantity_per_share': value }

        
        return result
        

    @quantity_per_share.setter
    def quantity_per_share(self, quantity_per_share):
        """Sets the quantity_per_share of this ETFHolding.

        Number of units of the security held per units of shares outstanding of the Exchange Traded Fund (ETF), if available  # noqa: E501

        :param quantity_per_share: The quantity_per_share of this ETFHolding.  # noqa: E501
        :type: float
        """

        self._quantity_per_share = quantity_per_share

    @property
    def contract_expiry_date(self):
        """Gets the contract_expiry_date of this ETFHolding.  # noqa: E501

        Expiry date for the futures contract held in the Exchange Traded Fund (ETF) or Exchange Traded Note (ETN)  # noqa: E501

        :return: The contract_expiry_date of this ETFHolding.  # noqa: E501
        :rtype: date
        """
        return self._contract_expiry_date
        
    @property
    def contract_expiry_date_dict(self):
        """Gets the contract_expiry_date of this ETFHolding.  # noqa: E501

        Expiry date for the futures contract held in the Exchange Traded Fund (ETF) or Exchange Traded Note (ETN) as a dictionary. Useful for Panda Dataframes.  # noqa: E501

        :return: The contract_expiry_date of this ETFHolding.  # noqa: E501
        :rtype: date
        """

        result = None

        value = self.contract_expiry_date
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
            result = { 'contract_expiry_date': value }

        
        return result
        

    @contract_expiry_date.setter
    def contract_expiry_date(self, contract_expiry_date):
        """Sets the contract_expiry_date of this ETFHolding.

        Expiry date for the futures contract held in the Exchange Traded Fund (ETF) or Exchange Traded Note (ETN)  # noqa: E501

        :param contract_expiry_date: The contract_expiry_date of this ETFHolding.  # noqa: E501
        :type: date
        """

        self._contract_expiry_date = contract_expiry_date

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
        if not isinstance(other, ETFHolding):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
