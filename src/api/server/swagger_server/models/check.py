# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server.models.token import Token  # noqa: F401,E501
from swagger_server import util


class Check(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, domain: str=None, nameservers: List[str]=None, token: str=None):  # noqa: E501
        """Check - a model defined in Swagger

        :param domain: The domain of this Check.  # noqa: E501
        :type domain: str
        :param nameservers: The nameservers of this Check.  # noqa: E501
        :type nameservers: List[str]
        :param token: The token of this Check.  # noqa: E501
        :type token: str
        """
        self.swagger_types = {
            'domain': str,
            'nameservers': List[str],
            'token': str
        }

        self.attribute_map = {
            'domain': 'domain',
            'nameservers': 'nameservers',
            'token': 'token'
        }
        self._domain = domain
        self._nameservers = nameservers
        self._token = token

    @classmethod
    def from_dict(cls, dikt) -> 'Check':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Check of this Check.  # noqa: E501
        :rtype: Check
        """
        return util.deserialize_model(dikt, cls)

    @property
    def domain(self) -> str:
        """Gets the domain of this Check.

        The domain to be delegated  # noqa: E501

        :return: The domain of this Check.
        :rtype: str
        """
        return self._domain

    @domain.setter
    def domain(self, domain: str):
        """Sets the domain of this Check.

        The domain to be delegated  # noqa: E501

        :param domain: The domain of this Check.
        :type domain: str
        """

        self._domain = domain

    @property
    def nameservers(self) -> List[str]:
        """Gets the nameservers of this Check.

        Name servers as strings  # noqa: E501

        :return: The nameservers of this Check.
        :rtype: List[str]
        """
        return self._nameservers

    @nameservers.setter
    def nameservers(self, nameservers: List[str]):
        """Sets the nameservers of this Check.

        Name servers as strings  # noqa: E501

        :param nameservers: The nameservers of this Check.
        :type nameservers: List[str]
        """

        self._nameservers = nameservers

    @property
    def token(self) -> str:
        """Gets the token of this Check.


        :return: The token of this Check.
        :rtype: str
        """
        return self._token

    @token.setter
    def token(self, token: str):
        """Sets the token of this Check.


        :param token: The token of this Check.
        :type token: str
        """

        self._token = token
