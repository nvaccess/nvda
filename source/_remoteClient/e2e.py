# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025-2026 NV Access Limited and others.
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""End-to-end encryption for NVDA Remote.

Uses X25519 key exchange and XSalsa20-Poly1305 authenticated encryption
(NaCl crypto_box) to protect data-plane messages from the relay server.

Requires PyNaCl (libsodium Python binding).
"""

import base64
import hashlib
import json
import struct
from typing import Any

from logHandler import log
from nacl.public import Box, PrivateKey, PublicKey
from nacl.utils import random as nacl_random


class PeerKeyState:
	"""Tracks the E2E state for a single peer."""

	__slots__ = ("peer_id", "public_key", "nonce_prefix", "box", "send_counter")

	def __init__(self, peer_id: int, public_key: PublicKey, nonce_prefix: bytes):
		self.peer_id = peer_id
		self.public_key = public_key
		self.nonce_prefix = nonce_prefix
		self.box: Box | None = None
		self.send_counter: int = 0


class E2ESession:
	"""Manages E2E encryption for one channel session.

	Lifecycle:
	1. Created when channel_joined arrives with e2e_available=True and all peers e2e_supported
	2. Broadcasts public key via e2e_pubkey message
	3. Receives peer pubkeys, derives pairwise shared secrets
	4. Encrypts all outbound data-plane messages
	5. Decrypts all inbound e2e_data messages
	6. Destroyed on disconnect or when a non-E2E peer joins
	"""

	def __init__(self) -> None:
		self._private_key = PrivateKey.generate()
		self._public_key = self._private_key.public_key
		self._nonce_prefix = nacl_random(4)
		self._peers: dict[int, PeerKeyState] = {}
		log.debug("E2E: Generated ephemeral key pair")

	@property
	def public_key_b64(self) -> str:
		return base64.b64encode(bytes(self._public_key)).decode("ascii")

	@property
	def nonce_prefix_b64(self) -> str:
		return base64.b64encode(self._nonce_prefix).decode("ascii")

	def get_pubkey_message(self) -> dict[str, str]:
		"""Returns kwargs for transport.send(RemoteMessageType.E2E_PUBKEY, **kwargs)."""
		return {
			"pubkey": self.public_key_b64,
			"nonce_prefix": self.nonce_prefix_b64,
		}

	def add_peer(self, peer_id: int, pubkey_b64: str, nonce_prefix_b64: str) -> None:
		"""Process a received e2e_pubkey message from a peer."""
		peer_pubkey = PublicKey(base64.b64decode(pubkey_b64))
		nonce_prefix = base64.b64decode(nonce_prefix_b64)
		peer = PeerKeyState(peer_id, peer_pubkey, nonce_prefix)
		peer.box = Box(self._private_key, peer_pubkey)
		self._peers[peer_id] = peer
		log.info(f"E2E: Established pairwise key with peer {peer_id}")

	def remove_peer(self, peer_id: int) -> None:
		"""Remove a peer's key state (on disconnect)."""
		if peer_id in self._peers:
			log.info(f"E2E: Removed pairwise key for peer {peer_id}")
		self._peers.pop(peer_id, None)

	def has_peer(self, peer_id: int) -> bool:
		return peer_id in self._peers

	@property
	def peer_ids(self) -> list[int]:
		return list(self._peers.keys())

	def _make_nonce(self, peer: PeerKeyState) -> bytes:
		"""Build a 24-byte nonce for XChaCha20-Poly1305."""
		counter_bytes = struct.pack(">Q", peer.send_counter)
		peer.send_counter += 1
		return self._nonce_prefix + b"\x00" * 12 + counter_bytes

	def encrypt(self, type: str, from_id: int, **kwargs: Any) -> list[dict[str, Any]]:
		"""Encrypt a data-plane message for all peers.

		Returns a list of dicts, one per peer, each suitable as kwargs for:
			transport.send(RemoteMessageType.E2E_DATA, **msg)

		The sender's user_id is included inside the encrypted payload as '_from'
		for origin authenticity verification (defense-in-depth against a server
		that lies about the outer 'origin' field).
		"""
		plaintext = json.dumps({"type": type, "_from": from_id, **kwargs}).encode("utf-8")
		messages = []
		for peer in self._peers.values():
			if peer.box is None:
				log.error(f"E2E: Peer {peer.peer_id} has no derived box, skipping encryption")
				continue
			nonce = self._make_nonce(peer)
			ciphertext = peer.box.encrypt(plaintext, nonce).ciphertext
			messages.append(
				{
					"to": peer.peer_id,
					"ciphertext": base64.b64encode(ciphertext).decode("ascii"),
					"nonce": base64.b64encode(nonce).decode("ascii"),
				},
			)
		return messages

	def encrypt_preserialized(
		self,
		type: str,
		from_id: int,
		serialized_kwargs: bytes,
	) -> list[dict[str, Any]]:
		"""Encrypt a pre-serialized data-plane message for all peers.

		This variant accepts kwargs already serialized as JSON bytes,
		which is needed for speech commands that require the custom
		SpeechCommandJSONEncoder. The caller is responsible for serializing
		the kwargs (without the 'type' and '_from' fields).

		:param type: The message type string.
		:param from_id: The sender's user_id.
		:param serialized_kwargs: The message kwargs serialized as JSON bytes
			(should be a JSON object without 'type' and '_from').
		"""
		# Build the full plaintext by injecting type and _from into the JSON object
		# We parse and re-serialize to merge the fields properly
		obj = json.loads(serialized_kwargs)
		obj["type"] = type
		obj["_from"] = from_id
		plaintext = json.dumps(obj).encode("utf-8")
		messages = []
		for peer in self._peers.values():
			if peer.box is None:
				log.error(f"E2E: Peer {peer.peer_id} has no derived box, skipping encryption")
				continue
			nonce = self._make_nonce(peer)
			ciphertext = peer.box.encrypt(plaintext, nonce).ciphertext
			messages.append(
				{
					"to": peer.peer_id,
					"ciphertext": base64.b64encode(ciphertext).decode("ascii"),
					"nonce": base64.b64encode(nonce).decode("ascii"),
				},
			)
		return messages

	def decrypt(
		self,
		origin_id: int,
		ciphertext_b64: str,
		nonce_b64: str,
	) -> tuple[str, dict[str, Any]] | None:
		"""Decrypt an e2e_data message. Returns (message_type, kwargs) or None.

		Verifies that the '_from' field inside the decrypted payload matches
		the outer 'origin' set by the server. A mismatch indicates tampering.
		"""
		peer = self._peers.get(origin_id)
		if peer is None or peer.box is None:
			log.warning(f"E2E: No key for peer {origin_id}, cannot decrypt")
			return None
		try:
			ciphertext = base64.b64decode(ciphertext_b64)
			nonce = base64.b64decode(nonce_b64)
			plaintext = peer.box.decrypt(ciphertext, nonce)
			obj = json.loads(plaintext.decode("utf-8"))
			msg_type = obj.pop("type")
			# Verify sender authenticity: _from inside payload must match origin
			inner_from = obj.pop("_from", None)
			if inner_from is not None and inner_from != origin_id:
				log.warning(
					f"E2E: Origin mismatch — outer origin={origin_id}, inner _from={inner_from}. "
					"Possible tampering, rejecting message.",
				)
				return None
			log.debug(f"E2E: Decrypted message type '{msg_type}' from peer {origin_id}")
			return (msg_type, obj)
		except Exception:
			log.warning(
				f"E2E: Decryption failed for message from peer {origin_id}",
				exc_info=True,
			)
			return None

	def get_fingerprint(self, peer_id: int) -> str | None:
		"""Compute a verification fingerprint for MITM detection.

		Both sides compute the same fingerprint (keys are sorted).
		Returns hex string like "a3f2 91d0 e8c4 7b5a" or None.
		"""
		peer = self._peers.get(peer_id)
		if peer is None:
			return None
		keys = sorted([bytes(self._public_key), bytes(peer.public_key)])
		digest = hashlib.blake2b(keys[0] + keys[1], digest_size=8).hexdigest()
		fingerprint = " ".join(digest[i : i + 4] for i in range(0, len(digest), 4))
		log.debug(f"E2E: Computed fingerprint for peer {peer_id}: {fingerprint}")
		return fingerprint
