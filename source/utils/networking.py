# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2012-2025 NV Access Limited, Zahari Yurukov,
# Babbage B.V., Joseph Lee, Christopher Proß

import ctypes
import ctypes.wintypes
import ssl

import requests

from logHandler import log


_FETCH_TIMEOUT_S = 30
"""Timeout for fetching in seconds."""


# These structs are only complete enough to achieve what we need.
class _CERT_USAGE_MATCH(ctypes.Structure):
	_fields_ = (
		("dwType", ctypes.wintypes.DWORD),
		# CERT_ENHKEY_USAGE struct
		("cUsageIdentifier", ctypes.wintypes.DWORD),
		("rgpszUsageIdentifier", ctypes.c_void_p),  # LPSTR *
	)


class _CERT_CHAIN_PARA(ctypes.Structure):
	_fields_ = (
		("cbSize", ctypes.wintypes.DWORD),
		("RequestedUsage", _CERT_USAGE_MATCH),
		("RequestedIssuancePolicy", _CERT_USAGE_MATCH),
		("dwUrlRetrievalTimeout", ctypes.wintypes.DWORD),
		("fCheckRevocationFreshnessTime", ctypes.wintypes.BOOL),
		("dwRevocationFreshnessTime", ctypes.wintypes.DWORD),
		("pftCacheResync", ctypes.c_void_p),  # LPFILETIME
		("pStrongSignPara", ctypes.c_void_p),  # PCCERT_STRONG_SIGN_PARA
		("dwStrongSignFlags", ctypes.wintypes.DWORD),
	)


def _getCertificate(url: str) -> bytes:
	"""Gets the certificate from the server."""
	log.debug(f"Getting certificate from: {url}")
	with requests.get(
		url,
		timeout=_FETCH_TIMEOUT_S,
		# Use an unverified connection to avoid a certificate error.
		verify=False,
		stream=True,
	) as response:
		# Get the server certificate.
		return response.raw.connection.sock.getpeercert(True)


def _updateWindowsRootCertificates(cert: bytes) -> None:
	"""Adds the certificate to the Windows root certificates."""
	log.debug("Updating Windows root certificates")
	crypt = ctypes.windll.crypt32
	# Convert to a form usable by Windows.
	certCont = crypt.CertCreateCertificateContext(
		0x00000001,  # X509_ASN_ENCODING
		cert,
		len(cert),
	)
	# Ask Windows to build a certificate chain, thus triggering a root certificate update.
	chainCont = ctypes.c_void_p()
	crypt.CertGetCertificateChain(
		None,
		certCont,
		None,
		None,
		ctypes.byref(
			_CERT_CHAIN_PARA(
				cbSize=ctypes.sizeof(_CERT_CHAIN_PARA),
				RequestedUsage=_CERT_USAGE_MATCH(),
			),
		),
		0,
		None,
		ctypes.byref(chainCont),
	)
	crypt.CertFreeCertificateChain(chainCont)
	crypt.CertFreeCertificateContext(certCont)


def _is_cert_verification_error(exception: requests.exceptions.SSLError) -> bool:
	return (
		exception.__context__
		and exception.__context__.__cause__
		and exception.__context__.__cause__.__context__
		and isinstance(exception.__context__.__cause__.__context__, ssl.SSLCertVerificationError)
		and hasattr(exception.__context__.__cause__.__context__, "reason")
		and exception.__context__.__cause__.__context__.reason == "CERTIFICATE_VERIFY_FAILED"
	)


def _fetchUrlAndUpdateRootCertificates(url: str, certFetchUrl: str | None = None) -> requests.Response:
	"""Fetches the content of a URL and updates the Windows root certificates.

	:param url: The URL to fetch.
	:param certFetchUrl: An optional URL to use for fetching the certificate if the original URL fails due to a certificate error.
	:return: The content of the URL.
	"""
	try:
		log.debug(f"Fetching data from: {url}")
		result = requests.get(url, timeout=_FETCH_TIMEOUT_S)
		log.debug(f"Got response with status code: {result.status_code}")
	except requests.exceptions.SSLError as e:
		if _is_cert_verification_error(e):
			# #4803: Windows fetches trusted root certificates on demand.
			# Python doesn't trigger this fetch (PythonIssue:20916), so try it ourselves.
			cert = _getCertificate(certFetchUrl or url)
			_updateWindowsRootCertificates(cert)
			log.debug(f"Retrying fetching data from: {url}")
			result = requests.get(url, timeout=_FETCH_TIMEOUT_S)
		else:
			raise
	return result
