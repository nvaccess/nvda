# NVDA Remote Protocol Specification

This document specifies the NVDA Remote relay protocol (versions 1 through 3),
covering connection lifecycle, message formats, relay behaviour, and end-to-end
encryption. It is written for security auditors and contributors who need to
understand the protocol without reading the implementation.

## 1. Protocol Overview

NVDA Remote enables two or more NVDA screen reader instances to communicate
through a relay server. One instance acts as the **leader** (controller) sending
keyboard and braille input, while the other acts as the **follower** (controlled)
sending speech, tones, and display output back.

* **Wire format**: UTF-8 JSON, one message per line (`\n`-delimited)
* **Transport**: TCP wrapped in TLS (self-signed certificates)
* **Default port**: 6837
* **Architecture**: Star topology — all clients connect to a relay server that
  forwards messages. Direct peer-to-peer connections are also supported (via the
  built-in NVDA server) but use the same message format.

## 2. Version History

| Version | Additions |
|---------|-----------|
| v1 | Base protocol: connect, join channel, relay messages |
| v2 | Server injects `origin` (client ID) into relayed messages; adds `client`/`clients` fields to join/leave notifications; backwards-compatible stripping for v1 peers |
| v3 | End-to-end encryption support: `e2e_pubkey` and `e2e_data` message types; `e2e_available` and `e2e_supported` fields; `user_id` in `channel_joined`. Wire-level extensibility for custom message types (see §5.5). |

## 3. Connection Handshake

1. Client opens a TCP connection to the server and completes a TLS handshake.
2. Client sends `protocol_version` to declare its capabilities.
3. Client sends `join` with a channel key and connection type to enter a channel.
4. Server responds with `channel_joined` containing the channel state, the
   client's own `user_id`, and info about any existing members.
5. Server may also send a `motd` (message of the day).
6. The connection is now in the data-plane phase: any further messages the client
   sends are relayed to other channel members, and vice versa.

Alternatively, a client may send `generate_key` instead of `join` (step 3) to
request a new channel key from the server, then reconnect with that key.

### 3.1 `protocol_version` (client -> server)

```json
{"type": "protocol_version", "version": 3}
```

Must be the first message sent. The server records the version and uses it to
determine which fields to include in relayed messages and whether the client
supports E2E encryption.

### 3.2 `generate_key` (client -> server -> client)

```json
{"type": "generate_key"}
```

Server responds with:

```json
{"type": "generate_key", "key": "123456789"}
```

The key is a randomly generated 9-digit numeric string. The client disconnects
and reconnects using this key in a `join` message.

### 3.3 `join` (client -> server)

```json
{"type": "join", "channel": "123456789", "connection_type": "master"}
```

* `channel`: The channel key (string). Acts as a shared secret for room joining.
* `connection_type`: `"master"` (leader/controller) or `"slave"` (follower/controlled).
  This is metadata only; the server treats both identically for relay purposes.

### 3.4 `channel_joined` (server -> client)

Sent after a successful `join`:

```json
{
  "type": "channel_joined",
  "channel": "123456789",
  "user_id": 5,
  "user_ids": [1, 2],
  "clients": [
    {"id": 1, "connection_type": "master", "e2e_supported": true},
    {"id": 2, "connection_type": "slave", "e2e_supported": false}
  ],
  "e2e_available": true
}
```

| Field | Version | Description |
|-------|---------|-------------|
| `channel` | v1+ | The joined channel key |
| `user_ids` | v1+ | IDs of existing channel members |
| `user_id` | v3+ | The client's own assigned ID |
| `clients` | v2+ | Full info for each existing member |
| `e2e_available` | v3+ | Whether the server allows E2E encryption |

### 3.5 `motd` (server -> client)

```json
{"type": "motd", "motd": "Welcome to NVDA Remote", "force_display": true}
```

Sent after `channel_joined`. `force_display` indicates the message should always
be shown, even if the user has seen it before.

### 3.6 `client_joined` / `client_left` (server -> client)

```json
{
  "type": "client_joined",
  "user_id": 5,
  "client": {"id": 5, "connection_type": "slave", "e2e_supported": true}
}
```

```json
{
  "type": "client_left",
  "user_id": 5,
  "client": {"id": 5, "connection_type": "slave", "e2e_supported": true}
}
```

The `client` field (v2+) includes `e2e_supported` (v3+).

### 3.7 `ping` (server -> client)

```json
{"type": "ping"}
```

Sent periodically (every 120 seconds on the Rust relay server) to keep the
connection alive through NAT/firewalls. No response is required.

### 3.8 `error` (server -> client)

```json
{"type": "error", "error": "invalid_parameters"}
```

## 4. Data-Plane Message Reference

These messages are relayed opaquely by the server to all other channel members.
The server adds an `origin` field (v2+) containing the sender's `user_id`.

### Input Messages (leader -> follower)

| Type | Fields | Description |
|------|--------|-------------|
| `key` | `vk_code`, `extended`, `pressed`, `scan_code` | Keyboard input |
| `braille_input` | Gesture-specific fields, optional `scriptPath` | Braille display input |
| `send_SAS` | *(none)* | Secure Attention Sequence (Ctrl+Alt+Del) |
| `set_braille_info` | `name`, `numCells` | Leader's braille display info |
| `set_display_size` | `sizes` | Leader's braille display dimensions |

### Output Messages (follower -> leader)

| Type | Fields | Description |
|------|--------|-------------|
| `speak` | `sequence`, `priority` | Speech output (sequence contains speech command objects) |
| `cancel` | *(none)* | Cancel speech |
| `pause_speech` | `switch` | Pause/resume speech |
| `tone` | `frequency`, `duration`, etc. | Beep tone |
| `wave` | Wave file parameters | Play audio file |
| `display` | `cells` | Braille display cell data |
| `index` | Index parameters | Speech index reached |

### Bidirectional Messages

| Type | Fields | Description |
|------|--------|-------------|
| `set_clipboard_text` | `text` | Clipboard content transfer |

### System Messages

| Type | Fields | Description |
|------|--------|-------------|
| `version_mismatch` | *(none)* | Protocol version incompatibility |
| `nvda_not_connected` | *(none)* | Remote NVDA instance not available |

## 5. Relay Behaviour

### 5.1 Opaque Forwarding

The server does not parse data-plane messages. Any JSON message from an
authenticated client that the server does not recognize as a control message
is forwarded to all other members of the same channel.

### 5.2 Origin Injection (v2+)

For v2+ recipients, the server adds an `origin` field containing the sender's
`user_id`:

```json
{"type": "key", "vk_code": 65, "pressed": true, "origin": 1}
```

For v1 recipients, `origin`, `client`, and `clients` fields are stripped.

### 5.3 No Echo

The sender never receives their own relayed message.

### 5.4 Channel Isolation

Messages are only relayed within a channel. Different channels are fully isolated.

### 5.5 Extensibility

The protocol is extensible at the wire level. The relay server forwards any
message type it does not recognize as a control message (see §5.1), so custom
message types can be introduced without any server-side changes, provided all
participating clients understand them.

The current NVDA client only accepts message types defined in the
`RemoteMessageType` enum. Unknown types received from the server are ignored.
To add a new message type, the enum and corresponding handlers must be updated
in the client. Third-party relay implementations are free to support additional
types as long as they respect the rules in this specification.

When E2E encryption is active, the client uses a **control-plane blacklist**
rather than a data-plane whitelist to decide what to encrypt. Only a fixed set
of control-plane message types (`protocol_version`, `join`, `channel_joined`,
`client_joined`, `client_left`, `generate_key`, `motd`, `version_mismatch`,
`ping`, `error`, `nvda_not_connected`, `e2e_pubkey`, `e2e_data`) are sent in
plaintext — the server must be able to parse these. All other message types
are encrypted when E2E is active. New message types added to
`RemoteMessageType` are encrypted by default as long as they are not added to
the control-plane blacklist.

## 6. End-to-End Encryption (Protocol v3)

### 6.1 Design Goals

* Protect data-plane content (keystrokes, speech, clipboard) from the relay server
* Per-session forward secrecy via ephemeral keys
* Pairwise authenticated encryption preventing sender spoofing
* Fingerprint-based MITM detection

### 6.2 Scope

E2E applies **only to relay connections**. Direct connections already use
point-to-point TLS with no intermediary, so E2E would add complexity for zero
security benefit. The direct-connection server sets `e2e_available: false`.

### 6.3 Cryptographic Primitives

| Purpose | Algorithm | Library |
|---------|-----------|---------|
| Key exchange | X25519 (Curve25519 DH) | PyNaCl |
| Authenticated encryption | XSalsa20-Poly1305 (NaCl crypto_box) | PyNaCl |
| Fingerprint | BLAKE2b (64-bit digest) | hashlib |

### 6.4 All-or-Nothing Rule

If **any** peer in the channel does not support E2E (`e2e_supported: false`),
the entire channel operates in plaintext. Mixed mode is not supported because
the server would see plaintext from/to the non-E2E peer, defeating the purpose.

### 6.5 Key Exchange

1. Each client generates an ephemeral X25519 keypair and a random 4-byte nonce
   prefix on session start.

2. After receiving `channel_joined` with `e2e_available: true` and all peers
   having `e2e_supported: true`, the client broadcasts its public key:

```json
{
  "type": "e2e_pubkey",
  "pubkey": "<base64 32-byte X25519 public key>",
  "nonce_prefix": "<base64 4-byte random prefix>"
}
```

1. The server relays this with `origin` added. Each receiving client derives a
   pairwise shared secret using X25519 DH:

```
shared_secret = X25519(own_private_key, peer_public_key)
```

1. PyNaCl's `Box` class handles the DH derivation and encryption in one step.

### 6.6 Message Encryption

For each data-plane message, the sender encrypts separately for each peer:

**Nonce construction** (24 bytes for XSalsa20):

[4-byte sender prefix][12 bytes zero padding][8-byte big-endian counter]
```

The counter increments per message per peer, ensuring nonce uniqueness.

**Encrypted message format**:
```json
{
  "type": "e2e_data",
  "to": 3,
  "ciphertext": "<base64 XSalsa20-Poly1305 ciphertext>",
  "nonce": "<base64 24-byte nonce>"
}
```

The `to` field is the intended recipient's `user_id`. The server adds `origin`
when relaying.

**Encrypted payload** (plaintext before encryption):

{
  "type": "key",
  "_from": 1,
  "vk_code": 65,
  "pressed": true
}
```

The `_from` field contains the sender's `user_id` for origin authenticity
verification (defense-in-depth). The receiver verifies that `_from` matches
the outer `origin` field set by the server. A mismatch indicates tampering
and the message is rejected.

### 6.7 Message Decryption

1. Receiver gets `e2e_data` with `origin` (from server) and `to` (from sender)
2. Checks `to == own_user_id` (ignore messages for other peers)
3. Looks up pairwise key using `origin` as peer ID
4. Decrypts with XChaCha20-Poly1305 (AEAD rejects tampered ciphertexts)
5. Parses plaintext JSON
6. Verifies `_from == origin` (defense-in-depth)
7. Dispatches inner message to normal handlers

### 6.8 Fingerprint Verification

To detect MITM attacks (malicious server substituting public keys):

```
sorted_keys = sort([own_public_key, peer_public_key])
fingerprint = BLAKE2b(sorted_keys[0] || sorted_keys[1], digest_size=8)
```

Both sides compute the same fingerprint (keys are sorted before hashing).
Users verify out-of-band (phone call, separate chat). A mismatch indicates
key substitution.

The fingerprint is displayed as a hex string: `"a3f2 91d0 e8c4 7b5a"`.

### 6.9 E2E Session Lifecycle

1. **Init**: `channel_joined` received with `e2e_available=true`, all peers
   `e2e_supported=true` -> create `E2ESession`, broadcast `e2e_pubkey`
2. **Key exchange**: Receive peer `e2e_pubkey` messages, derive pairwise keys
3. **Active**: All data-plane sends go through `session.send()` which
   transparently encrypts for each peer
4. **Peer join**: New E2E peer -> send pubkey to them. New non-E2E peer ->
   tear down E2E, fall back to plaintext.
5. **Peer leave**: Remove peer's key state
6. **Disconnect**: E2E session destroyed, ephemeral keys discarded

### 6.10 Threat Model

**Protected**:

* Data-plane content (keystrokes, speech, braille, clipboard) encrypted end-to-end
* Forward secrecy: ephemeral keys per session

* Sender authenticity: pairwise AEAD + `_from` verification

**Not protected**:

* Metadata: server sees who's in which channel, timing, message sizes

* Control plane: `protocol_version`, `join`, `generate_key` are plaintext
* MITM: a malicious server can swap public keys during exchange (detectable
  only by fingerprint verification)

### 6.11 Design Compromises vs Signal Protocol

| Feature | Signal | NVDA Remote | Rationale |
|---------|--------|-------------|-----------|
| Key exchange | X3DH | Single X25519 DH | No offline messages; both peers online |
| Ratcheting | Double Ratchet | Per-session keys | Per-message forward secrecy unnecessary; session-level is sufficient |
| Identity keys | Persistent | Ephemeral only | No long-term identity needed; users verify per session |
| Group keys | Sender keys | Pairwise | 2-4 clients; O(n^2) is fine |
| Offline messages | Yes | No | Real-time screen reader relay |

## 7. Direct Connection Mode

When one NVDA instance connects directly to another via the built-in server
(`server.py`), no relay intermediary exists. The TLS tunnel runs point-to-point.

The direct-connection server:


* Sets `e2e_available: false` in `channel_joined`
* Does not include `e2e_supported` in client info (defaults to `false`)
* Uses the same message format and types as the relay protocol

E2E is never initiated on direct connections.

## 8. Wire Format Examples


**Client A connects and joins:**

```
-> {"type":"protocol_version","version":3}
-> {"type":"join","channel":"123456789","connection_type":"master"}
<- {"type":"channel_joined","channel":"123456789","user_id":1,"user_ids":[],"clients":[],"e2e_available":true}

<- {"type":"motd","motd":"Welcome","force_display":false}
```

**Client B connects and joins:**

```
-> {"type":"protocol_version","version":3}

-> {"type":"join","channel":"123456789","connection_type":"slave"}
<- {"type":"channel_joined","channel":"123456789","user_id":2,"user_ids":[1],"clients":[{"id":1,"connection_type":"master","e2e_supported":true}],"e2e_available":true}
```

**Client A receives notification:**

```
```

**Key exchange:**

```

A -> {"type":"e2e_pubkey","pubkey":"<b64>","nonce_prefix":"<b64>"}
     (server relays to B with origin=1)
B -> {"type":"e2e_pubkey","pubkey":"<b64>","nonce_prefix":"<b64>"}
     (server relays to A with origin=2)
```

**Encrypted key press (A -> B):**

A -> {"type":"e2e_data","to":2,"ciphertext":"<b64>","nonce":"<b64>"}
     (server relays to B with origin=1)

```

Decrypted payload inside ciphertext:

```json
{"type":"key","_from":1,"vk_code":65,"extended":false,"pressed":true,"scan_code":30}

```

**Encrypted speech (B -> A):**

```
B -> {"type":"e2e_data","to":1,"ciphertext":"<b64>","nonce":"<b64>"}
     (server relays to A with origin=2)
```

Decrypted payload:

```json
{"type":"speak","_from":2,"sequence":["hello world"],"priority":null}
```
