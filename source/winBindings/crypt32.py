# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Functions exported by crypt32.dll, and supporting data structures and enumerations."""

from ctypes import (
	Structure,
	POINTER,
	windll,
	c_void_p,
	c_byte,
)
from ctypes.wintypes import (
	BOOL,
	DWORD,
	HANDLE,
	LPSTR,
)
from .kernel32 import FILETIME


PCCERT_CONTEXT = c_void_p
PCCERT_CHAIN_CONTEXT = c_void_p
HCERTSTORE = HANDLE
HCERTCHAINENGINE = HANDLE
LPFILETIME = POINTER(FILETIME)


class CERT_USAGE_MATCH(Structure):
	"""
	Provides criteria for identifying issuer certificates to be used to build a certificate chain.

	.. seealso::
		https://learn.microsoft.com/en-us/windows/win32/api/wincrypt/ns-wincrypt-cert_usage_match
	"""

	_fields_ = (
		("dwType", DWORD),
		# CERT_ENHKEY_USAGE struct
		("cUsageIdentifier", DWORD),
		("rgpszUsageIdentifier", POINTER(LPSTR)),
	)


class CERT_CHAIN_PARA(Structure):
	"""
	Establishes the searching and matching criteria to be used in building a certificate chain.

	.. seealso::
		https://learn.microsoft.com/en-us/windows/win32/api/wincrypt/ns-wincrypt-cert_chain_para
	"""

	_fields_ = (
		("cbSize", DWORD),
		("RequestedUsage", CERT_USAGE_MATCH),
		("RequestedIssuancePolicy", CERT_USAGE_MATCH),
		("dwUrlRetrievalTimeout", DWORD),
		("fCheckRevocationFreshnessTime", BOOL),
		("dwRevocationFreshnessTime", DWORD),
		("pftCacheResync", LPFILETIME),
		("pStrongSignPara", c_void_p),  # PCCERT_STRONG_SIGN_PARA
		("dwStrongSignFlags", DWORD),
	)


PCERT_CHAIN_PARA = POINTER(CERT_CHAIN_PARA)


dll = windll.crypt32


CertCreateCertificateContext = dll.CertCreateCertificateContext
"""
Creates a certificate context from an encoded certificate.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/wincrypt/nf-wincrypt-certcreatecertificatecontext
"""
CertCreateCertificateContext.argtypes = (
	DWORD,  # dwCertEncodingType
	POINTER(c_byte),  # pbCertEncoded
	DWORD,  # cbCertEncoded
)
CertCreateCertificateContext.restype = PCCERT_CONTEXT

CertFreeCertificateChain = dll.CertFreeCertificateChain
"""
Frees a certificate chain context.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/wincrypt/nf-wincrypt-certfreecertificatechain
"""
CertFreeCertificateChain.argtypes = (
	PCCERT_CHAIN_CONTEXT,  # pChainContext
)
CertFreeCertificateChain.restype = None

CertFreeCertificateContext = dll.CertFreeCertificateContext
"""
Frees a certificate context.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/wincrypt/nf-wincrypt-certfreecertificatecontext
"""
CertFreeCertificateContext.argtypes = (
	PCCERT_CONTEXT,  # pCertContext
)
CertFreeCertificateContext.restype = BOOL

CertGetCertificateChain = dll.CertGetCertificateChain
"""
Builds a certificate chain context starting from a specified certificate context.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/wincrypt/nf-wincrypt-certgetcertificatechain
"""
CertGetCertificateChain.argtypes = (
	HCERTCHAINENGINE,  # hChainEngine
	PCCERT_CONTEXT,  # pCertContext
	LPFILETIME,  # pTime
	HCERTSTORE,  # hAdditionalStore
	PCERT_CHAIN_PARA,  # pChainPara
	DWORD,  # dwFlags
	c_void_p,  # pvReserved
	POINTER(PCCERT_CHAIN_CONTEXT),  # ppChainContext
)
CertGetCertificateChain.restype = BOOL
