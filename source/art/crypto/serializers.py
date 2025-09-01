# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""
Encrypted Pyro5 serializer for ART RPC communication.

Provides transparent encryption wrapper around existing Pyro5 serializers
using XSalsa20-Poly1305 authenticated encryption via PyNaCl.
"""

import os
from typing import Any, Dict, Tuple

import nacl.secret
import Pyro5.serializers
from logHandler import log


class EncryptedSerializer(Pyro5.serializers.SerializerBase):
	"""Encrypted wrapper for Pyro5 serializers using XSalsa20-Poly1305."""
	
	serializer_id = 99  # Unused ID in Pyro5
	
	def __init__(self, inner_serializer_name: str = "msgpack", key_bytes: bytes = None):
		"""Initialize encrypted serializer.
		
		@param inner_serializer_name: Name of inner serializer to wrap
		@param key_bytes: 32-byte encryption key
		"""
		# Strict key validation
		if key_bytes is None:
			raise ValueError("key_bytes is required")
		if not isinstance(key_bytes, bytes):
			raise TypeError(f"key_bytes must be bytes, got {type(key_bytes)}")
		if len(key_bytes) != 32:
			raise ValueError(f"key_bytes must be exactly 32 bytes, got {len(key_bytes)}")
		
		# Strict serializer validation  
		if inner_serializer_name not in Pyro5.serializers.serializers:
			raise ValueError(f"unknown inner serializer: {inner_serializer_name}")
			
		self.inner = Pyro5.serializers.serializers[inner_serializer_name]
		self.box = nacl.secret.SecretBox(key_bytes)
		
		log.info(f"EncryptedSerializer initialized with inner={inner_serializer_name}")
	
	def dumps(self, data: Any) -> bytes:
		"""Serialize and encrypt data."""
		plaintext = self.inner.dumps(data)
		return self.box.encrypt(plaintext)  # Returns nonce + ciphertext
	
	def loads(self, data: bytes) -> Any:
		"""Decrypt and deserialize data.""" 
		plaintext = self.box.decrypt(data)  # Auto-extracts nonce, verifies MAC
		return self.inner.loads(plaintext)
	
	def dumpsCall(self, obj: Any, method: str, vargs: Tuple, kwargs: Dict[str, Any]) -> bytes:
		"""Serialize and encrypt method call."""
		plaintext = self.inner.dumpsCall(obj, method, vargs, kwargs)
		return self.box.encrypt(plaintext)
	
	def loadsCall(self, data: bytes) -> Tuple[Any, str, Tuple, Dict[str, Any]]:
		"""Decrypt and deserialize method call."""
		plaintext = self.box.decrypt(data)
		return self.inner.loadsCall(plaintext)
	
	def register_type_replacement(self, object_type: type, replacement_function):
		"""Delegate type replacement registration to inner serializer."""
		if hasattr(self.inner, 'register_type_replacement'):
			return self.inner.register_type_replacement(object_type, replacement_function)

	@classmethod
	def generate_key(cls) -> bytes:
		"""Generate cryptographically secure 32-byte key."""
		return os.urandom(32)