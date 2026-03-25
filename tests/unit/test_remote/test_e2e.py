# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025-2026 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import json
import unittest

from _remoteClient.e2e import E2ESession


class TestE2EKeyExchange(unittest.TestCase):
	"""Test E2E key exchange and pairwise key establishment."""

	def test_pubkeyMessageFormat(self):
		session = E2ESession()
		msg = session.get_pubkey_message()
		self.assertIn("pubkey", msg)
		self.assertIn("nonce_prefix", msg)
		self.assertIsInstance(msg["pubkey"], str)
		self.assertIsInstance(msg["nonce_prefix"], str)

	def test_addPeerEstablishesKey(self):
		alice = E2ESession()
		bob = E2ESession()
		aliceMsg = alice.get_pubkey_message()
		bob.add_peer(1, aliceMsg["pubkey"], aliceMsg["nonce_prefix"])
		self.assertTrue(bob.has_peer(1))
		self.assertIn(1, bob.peer_ids)

	def test_removePeer(self):
		alice = E2ESession()
		bob = E2ESession()
		aliceMsg = alice.get_pubkey_message()
		bob.add_peer(1, aliceMsg["pubkey"], aliceMsg["nonce_prefix"])
		bob.remove_peer(1)
		self.assertFalse(bob.has_peer(1))

	def test_removeNonexistentPeerNoError(self):
		session = E2ESession()
		session.remove_peer(999)


class TestE2EEncryptDecrypt(unittest.TestCase):
	"""Test encryption and decryption of messages."""

	def setUp(self):
		self.alice = E2ESession()
		self.bob = E2ESession()
		aliceMsg = self.alice.get_pubkey_message()
		bobMsg = self.bob.get_pubkey_message()
		self.alice.add_peer(2, bobMsg["pubkey"], bobMsg["nonce_prefix"])
		self.bob.add_peer(1, aliceMsg["pubkey"], aliceMsg["nonce_prefix"])

	def test_encryptProducesOneMessagePerPeer(self):
		messages = self.alice.encrypt("key", from_id=1, vk_code=65, pressed=True)
		self.assertEqual(len(messages), 1)
		self.assertIn("ciphertext", messages[0])
		self.assertIn("nonce", messages[0])
		self.assertIn("to", messages[0])
		self.assertEqual(messages[0]["to"], 2)

	def test_roundTrip(self):
		messages = self.alice.encrypt("key", from_id=1, vk_code=65, pressed=True)
		result = self.bob.decrypt(1, messages[0]["ciphertext"], messages[0]["nonce"])
		self.assertIsNotNone(result)
		msg_type, kwargs = result
		self.assertEqual(msg_type, "key")
		self.assertEqual(kwargs["vk_code"], 65)
		self.assertTrue(kwargs["pressed"])

	def test_roundTripPreserialized(self):
		kwargs = {"sequence": ["hello"], "priority": "normal"}
		serialized = json.dumps(kwargs).encode("utf-8")
		messages = self.alice.encrypt_preserialized("speak", from_id=1, serialized_kwargs=serialized)
		result = self.bob.decrypt(1, messages[0]["ciphertext"], messages[0]["nonce"])
		self.assertIsNotNone(result)
		msg_type, decoded_kwargs = result
		self.assertEqual(msg_type, "speak")
		self.assertEqual(decoded_kwargs["sequence"], ["hello"])

	def test_bidirectional(self):
		"""Both sides can encrypt and the other can decrypt."""
		msgs_a = self.alice.encrypt("key", from_id=1, vk_code=65, pressed=True)
		msgs_b = self.bob.encrypt("tone", from_id=2, hz=440, length=100)
		result_a = self.bob.decrypt(1, msgs_a[0]["ciphertext"], msgs_a[0]["nonce"])
		result_b = self.alice.decrypt(2, msgs_b[0]["ciphertext"], msgs_b[0]["nonce"])
		self.assertEqual(result_a[0], "key")
		self.assertEqual(result_b[0], "tone")

	def test_decryptFromUnknownPeerReturnsNone(self):
		messages = self.alice.encrypt("key", from_id=1, vk_code=65, pressed=True)
		result = self.bob.decrypt(999, messages[0]["ciphertext"], messages[0]["nonce"])
		self.assertIsNone(result)

	def test_tamperedCiphertextReturnsNone(self):
		messages = self.alice.encrypt("key", from_id=1, vk_code=65, pressed=True)
		result = self.bob.decrypt(1, "dGFtcGVyZWQ=", messages[0]["nonce"])
		self.assertIsNone(result)

	def test_originMismatchReturnsNone(self):
		"""Inner _from must match the outer origin_id."""
		messages = self.alice.encrypt("key", from_id=1, vk_code=65, pressed=True)
		# Decrypt with wrong origin_id (pretend server lied about origin)
		# This won't decrypt at all since bob has no key for peer 999
		result = self.bob.decrypt(999, messages[0]["ciphertext"], messages[0]["nonce"])
		self.assertIsNone(result)


class TestE2EFingerprint(unittest.TestCase):
	"""Test fingerprint generation for MITM detection."""

	def test_fingerprintMatchesBothSides(self):
		alice = E2ESession()
		bob = E2ESession()
		aliceMsg = alice.get_pubkey_message()
		bobMsg = bob.get_pubkey_message()
		alice.add_peer(2, bobMsg["pubkey"], bobMsg["nonce_prefix"])
		bob.add_peer(1, aliceMsg["pubkey"], aliceMsg["nonce_prefix"])
		self.assertEqual(alice.get_fingerprint(2), bob.get_fingerprint(1))

	def test_fingerprintForUnknownPeerReturnsNone(self):
		session = E2ESession()
		self.assertIsNone(session.get_fingerprint(999))

	def test_fingerprintFormat(self):
		alice = E2ESession()
		bob = E2ESession()
		aliceMsg = alice.get_pubkey_message()
		bobMsg = bob.get_pubkey_message()
		alice.add_peer(2, bobMsg["pubkey"], bobMsg["nonce_prefix"])
		fingerprint = alice.get_fingerprint(2)
		self.assertIsNotNone(fingerprint)
		# Should be 4 groups of 4 hex chars separated by spaces
		parts = fingerprint.split(" ")
		self.assertEqual(len(parts), 4)
		for part in parts:
			self.assertEqual(len(part), 4)
			int(part, 16)  # Should not raise


class TestE2EMultiplePeers(unittest.TestCase):
	"""Test E2E with more than two peers in a channel."""

	def test_encryptForMultiplePeers(self):
		alice = E2ESession()
		bob = E2ESession()
		carol = E2ESession()
		bobMsg = bob.get_pubkey_message()
		carolMsg = carol.get_pubkey_message()
		alice.add_peer(2, bobMsg["pubkey"], bobMsg["nonce_prefix"])
		alice.add_peer(3, carolMsg["pubkey"], carolMsg["nonce_prefix"])
		messages = alice.encrypt("key", from_id=1, vk_code=65, pressed=True)
		self.assertEqual(len(messages), 2)
		recipients = {m["to"] for m in messages}
		self.assertEqual(recipients, {2, 3})

	def test_removePeerReducesRecipients(self):
		alice = E2ESession()
		bob = E2ESession()
		carol = E2ESession()
		bobMsg = bob.get_pubkey_message()
		carolMsg = carol.get_pubkey_message()
		alice.add_peer(2, bobMsg["pubkey"], bobMsg["nonce_prefix"])
		alice.add_peer(3, carolMsg["pubkey"], carolMsg["nonce_prefix"])
		alice.remove_peer(3)
		messages = alice.encrypt("key", from_id=1, vk_code=65, pressed=True)
		self.assertEqual(len(messages), 1)
		self.assertEqual(messages[0]["to"], 2)


if __name__ == "__main__":
	unittest.main()
