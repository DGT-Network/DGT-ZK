# DGT-ZK Protocol: Encryption Package

The `encryption` package provides essential cryptographic tools for the DGT-ZK Protocol, supporting privacy-preserving transactions. The package includes modules for homomorphic encryption, Pedersen commitments, and an interface for zero-knowledge encryption. Together, these tools enable secure, verifiable transactions within a decentralized environment while maintaining compliance with privacy requirements.

## Package Structure

The package consists of the following modules:

- **homomorphic_encryption.py**: Implements homomorphic encryption using the Paillier scheme. This module allows for encrypted computations on transaction amounts, enabling privacy-preserving operations.
- **pedersen_commitment.py**: Provides functions to create and verify Pedersen commitments, which allow values to be committed without being revealed, supporting secure, verifiable commitments for transaction amounts.
- **zk_encryption_interface.py**: Combines homomorphic encryption and Pedersen commitments, allowing for secure transaction preparation and validation. This module also supports Bulletproofs for range validation without revealing the actual values.

## Setup Instructions

### Dependencies

To use the package, ensure that you have the following dependencies installed:

```bash
pip install ecdsa phe
```

The package uses:

- ecdsa: For elliptic curve operations with Pedersen commitments.
- phe: For homomorphic encryption using the Paillier scheme.

**Optional Dependencies**
fastecdsa: For alternative elliptic curve operations if installed. The package will use ecdsa by default if fastecdsa is not available.

## Modules
### 1 _init_.py

**Core Functions:** 
- Imports: encrypt_value and decrypt_value from homomorphic_encryption.py for handling encrypted transaction amounts.
create_commitment and verify_commitment from pedersen_commitment.py to manage the creation and verification of commitments.
prepare_encrypted_transaction and validate_transaction_with_bulletproof from zk_encryption_interface.py for higher-level cryptographic operations needed in DGT-ZK Protocol.
- __all__: Defines the public API for the encryption package, making the listed functions accessible when the package is imported.

### 2. homomorphic_encryption.py

**Core Functions:**

---------------------

1) encrypt_value:

Encrypts a transaction amount using the public key provided. This function uses homomorphic encryption, allowing the amount to be safely stored or transmitted while keeping it confidential.

**Parameters**:
- value: The integer transaction amount to encrypt.
- public_key: The public key for encryption, generated via Paillier.

**Returns**:
An encrypted number that represents the encrypted transaction amount.

----------------------

2) decrypt_value:

Decrypts an encrypted transaction amount using the private key provided.

**Parameters**:
- encrypted_value: The encrypted number (transaction amount).
- private_key: The private key corresponding to the public key used for encryption.

**Returns**:
The decrypted integer transaction amount.

----------------------

3) generate_paillier_keypair:

Generates a Paillier public-private key pair for encryption and decryption of transaction data.

**Returns**:
- public_key: The public key for encrypting transaction amounts.
- private_key: The private key for decrypting transaction amounts.

**Usage Example**

```python
from data.encryption.homomorphic_encryption import generate_paillier_keypair, encrypt_value, decrypt_value

# Generate a key pair
public_key, private_key = generate_paillier_keypair()

# Encrypt a transactions amount
transaction_amount = 500
encrypted_amount = encrypt_value(transaction_amount, public_key)
print("Encrypted Amount:", encrypted_amount)

# Decrypt the transactions amount
decrypted_amount = decrypt_value(encrypted_amount, private_key)
print("Decrypted Amount:", decrypted_amount)
```

**Key Considerations**
- **Paillier Homomorphic Encryption**: The Paillier encryption scheme allows mathematical operations on encrypted values, making it ideal for privacy-preserving computations in the DGT-ZK Protocol.
- **Compatibility**: Ensure that a compatible library like phe (Python Paillier library) is installed to handle homomorphic encryption.
- **Security**: Public and private keys must be securely managed and stored to prevent unauthorized access to encrypted data.

### 3. pedersen_commitment.py

**Core Functions**

1) generate_random:

Generates a random integer as a blinding factor, used to mask the actual value in the commitment.

**Returns**:
An integer representing the random blinding factor.

--------------------

2) create_commitment:

Generates a Pedersen commitment for a specific value using the blinding factor. If no blinding factor is provided, a random one is generated.

**Parameters**:
- value: The integer to commit to, such as a transaction amount.
- random_factor: An optional integer blinding factor. If not provided, it generates a new random factor.

**Returns**:
A tuple (commitment, random_factor), where commitment is an elliptic curve point representing the Pedersen commitment and random_factor is the blinding factor used.

--------------------

3) verify_commitment:

Checks the validity of a given Pedersen commitment by recalculating it with the provided value and blinding factor, ensuring they match.

**Parameters**:
- commitment: The elliptic curve point representing the commitment.
- value: The committed value.
- random_factor: The blinding factor used in the original commitment.

**Returns**:
True if the commitment is valid, False otherwise.

**Usage Example**
Here's an example of how to use the pedersen_commitment.py module to create and verify Pedersen commitments.

```python
from data.encryption.pedersen_commitment import create_commitment, verify_commitment

# Define a transactions amount to commit
transaction_amount = 500

# Create a Pedersen commitment for the transactions amount
commitment, random_factor = create_commitment(transaction_amount)

print("Commitment:", commitment)
print("Random Factor:", random_factor)

# Verify the commitment
is_valid = verify_commitment(commitment, transaction_amount, random_factor)
print("Commitment valid:", is_valid)
```

**Key Considerations**
- Security of Pedersen Commitments: Pedersen commitments are computationally hiding (conceal the committed value) and binding (the committed value cannot be changed once set), making them suitable for privacy-preserving protocols.
The blinding factor ensures that the commitment appears random, even if the same value is committed multiple times.
- Compatibility: This implementation uses the ecdsa library and is compatible with the secp256k1 curve, making it useful in environments that require standard elliptic curve cryptography.
This module is a core part of the DGT-ZK Protocol, supporting secure and private verification of transaction amounts without revealing the actual values.

### 4. zk_encryption_interface.py

**Core Functions**

1) prepare_encrypted_transaction:

Combines homomorphic encryption and Pedersen commitment for securely handling transaction amounts.

**Parameters**:
-sender: The sender’s public key or address.
-recipient: The recipient’s public key or address.
-amount: The integer transaction amount.
-public_key: The public key used for encryption.

**Returns**:
A dictionary containing the encrypted_amount (homomorphically encrypted value), commitment (Pedersen commitment), and random_factor (blinding factor used in the commitment).

----------------

2) validate_transaction_with_bulletproof:

Uses a Bulletproof to verify that the commitment amount is within a specified range without disclosing the actual value.

**Parameters**:
- commitment: The Pedersen commitment to be validated.
- range_min: Minimum allowable value for the range.
- range_max: Maximum allowable value for the range.

**Returns**:
True if the range proof is valid, False otherwise.

--------------

3) decrypt_transaction_amount:

Decrypts the encrypted transaction amount using the private key.

**Parameters**:
-encrypted_amount: The encrypted number representing the transaction amount.
-private_key: The private key for decryption.

**Returns**:
The integer amount decrypted from the encrypted_amount.

**Usage Example**

Here’s how to use the zk_encryption_interface.py module to prepare, validate, and decrypt a transaction.

```python
from data.encryption.zk_encryption_interface import (
    prepare_encrypted_transaction,
    validate_transaction_with_bulletproof,
    decrypt_transaction_amount,
)
from data.encryption.homomorphic_encryption import generate_paillier_keypair

# Generate public and private keys for encryption
public_key, private_key = generate_paillier_keypair()

# Prepare a transactions for the amount of 500
sender = "sender_public_key"
recipient = "recipient_public_key"
transaction_amount = 500

transaction_data = prepare_encrypted_transaction(sender, recipient, transaction_amount, public_key)

print("Encrypted Amount:", transaction_data["encrypted_amount"])
print("Commitment:", transaction_data["commitment"])
print("Random Factor:", transaction_data["random_factor"])

# Validate the commitment with Bulletproofs within a specified range
is_valid = validate_transaction_with_bulletproof(transaction_data["commitment"], range_min=0, range_max=1000)
print("Bulletproof validation result:", is_valid)

# Decrypt the transactions amount
decrypted_amount = decrypt_transaction_amount(transaction_data["encrypted_amount"], private_key)
print("Decrypted Amount:", decrypted_amount)
```

**Key Considerations**
- Privacy and Security: This interface module ensures the security of sensitive transaction data by combining homomorphic encryption and Pedersen commitments.
Bulletproofs further enhance privacy by allowing range checks on committed values without revealing the amount.
- Compatibility with DGT-ZK Protocol: The zk_encryption_interface module allows the DGT-ZK Protocol to perform private, verifiable transactions compatible with KYC/AML requirements.


### 5. signature.py
**Description**: Manages ECDSA digital signatures compatible with Ethereum address standards. This module allows for key generation, signing of transactions, verification of signatures, and generation of Ethereum-compatible addresses.

**Core Functions**:

-----------------

1) generate_keys:

Generates an ECDSA key pair using the SECP256k1 curve.

**Returns**:
- private_key: Hex-encoded private key as a string.
- public_key: Hex-encoded public key as a string.

- The private key is used for signing, while the public key is used to verify the signature.

-----------------

2) sign_transaction:

Signs a transaction using a given private key. The transaction data is hashed using the Keccak algorithm before signing.

**Parameters**:
- tx: The transaction data (as a dictionary) to be signed.
- private_key: Hex-encoded private key used for signing.

**Returns**:
- signature: Hex-encoded signature as a string, representing the signed transaction.

--------------

3) verify_signature:

Verifies a transaction’s signature against the provided public key.

**Parameters**:
- tx: The transaction data (as a dictionary) to be verified.
- public_key: Hex-encoded public key of the signer.
- signature: Hex-encoded signature to be verified.

**Returns**:
- True if the signature is valid; False otherwise.

- This function uses Keccak hashing and raises BadSignatureError if the signature is invalid, which is caught to return False.

-------------------

4) get_eth_address:

Converts a public key to an Ethereum-compatible address by applying Keccak hashing.

**Parameters**:
- public_key: Hex-encoded public key.

**Returns**:
Ethereum-compatible address as a hex string, prefixed with 0x.

The Ethereum address is the last 20 bytes (40 hex characters) of the Keccak hash of the public key.

**Usage Example**

```python
Here’s
an
example
demonstrating
the
use
of
signature.py:

from encryption.signature import generate_keys, sign_transaction, verify_signature, get_eth_address

# Generate a key pair
private_key, public_key = generate_keys()
print("Private Key:", private_key)
print("Public Key:", public_key)

# Create a sample transactions
transaction = {
    "sender": public_key,
    "recipient": "recipient_public_key_example",
    "amount": 100,
    "timestamp": "2024-01-01T10:00:00Z"
}

# Sign the transactions
signature = sign_transaction(transaction, private_key)
print("Signature:", signature)

# Verify the transactions signature
is_valid = verify_signature(transaction, public_key, signature)
print("Signature valid:", is_valid)

# Generate an Ethereum-compatible address
eth_address = get_eth_address(public_key)
print("Ethereum-compatible Address:", eth_address)
```

-----------------------------
5) create_secondary_address

This function creates a secondary protected address using a Pedersen-style commitment scheme, which combines two secret values (secret_s and secret_r) with elliptic curve generator points g and h.

**Parameters**:
- g: The primary generator point (G) on the elliptic curve (usually defined in the protocol).
- h: A secondary generator point (H) on the elliptic curve, independent of g.

**Returns**: A tuple containing:
- secondary_address: The created secondary address as a point on the elliptic curve.
- secret_s: The secret multiplier for the primary generator g.
- secret_r: The secret multiplier for the secondary generator h.

**Usage Example**
Here's an example of how to use the signature.py module to generate keys, create a secondary address, and sign a transaction.

```python
from encryption.signature import generate_keys, sign_transaction, verify_signature, get_eth_address,
    create_secondary_address
from ecdsa import SECP256k1

# Generate primary keys for the user
private_key, public_key = generate_keys()
print("Private Key:", private_key)
print("Public Key:", public_key)

# Generate an Ethereum-compatible address
eth_address = get_eth_address(public_key)
print("Ethereum-compatible Address:", eth_address)

# Create a secondary address using Pedersen-style commitments
g = SECP256k1.generator  # Primary generator for SECP256k1
h = SECP256k1.generator * 2  # Example secondary generator (independent of G)
secondary_address, secret_s, secret_r = create_secondary_address(g, h)

print("Secondary Address:", secondary_address)
print("Secret s:", secret_s)
print("Secret r:", secret_r)

# Create a transactions and sign it
transaction_data = {"sender": public_key, "recipient": eth_address, "amount": 100}
signature = sign_transaction(transaction_data, private_key)
print("Signature:", signature)

# Verify the transactions signature
is_verified = verify_signature(transaction_data, public_key, signature)
print("Signature Verified:", is_verified)
```

## Usage Examples
1. **Generate Encryption Keys**

To encrypt transaction amounts, you need to generate a public and private key pair for homomorphic encryption:

```python
from data.encryption.homomorphic_encryption import generate_paillier_keypair

public_key, private_key = generate_paillier_keypair()
```

2. **Create and Verify a Pedersen Commitment**

You can create a Pedersen commitment for a transaction amount to securely commit to a value without revealing it.

```python
from data.encryption.pedersen_commitment import create_commitment, verify_commitment

# Define a transactions amount
transaction_amount = 500

# Create a commitment
commitment, random_factor = create_commitment(transaction_amount)
print("Commitment:", commitment)
print("Random Factor:", random_factor)

# Verify the commitment
is_valid = verify_commitment(commitment, transaction_amount, random_factor)
print("Commitment valid:", is_valid)
```

3. **Prepare an Encrypted Transaction**

The zk_encryption_interface module allows you to prepare a transaction with both encryption and commitment, combining privacy and verifiability.

```python
from data.encryption.zk_encryption_interface import prepare_encrypted_transaction

sender = "sender_public_key"
recipient = "recipient_public_key"
transaction_amount = 500

transaction_data = prepare_encrypted_transaction(sender, recipient, transaction_amount, public_key)

print("Encrypted Amount:", transaction_data["encrypted_amount"])
print("Commitment:", transaction_data["commitment"])
print("Random Factor:", transaction_data["random_factor"])
```

4. Validate a Transaction with Bulletproofs
Use Bulletproofs to verify the range of a committed transaction amount without revealing the actual value.

```python
from data.encryption.zk_encryption_interface import validate_transaction_with_bulletproof

is_valid = validate_transaction_with_bulletproof(transaction_data["commitment"], range_min=0, range_max=1000)
print("Bulletproof validation result:", is_valid)
```

5. **Decrypt a Transaction Amount**

To retrieve the original transaction amount, decrypt it with the private key.

```python
from data.encryption.zk_encryption_interface import decrypt_transaction_amount

decrypted_amount = decrypt_transaction_amount(transaction_data["encrypted_amount"], private_key)
print("Decrypted Amount:", decrypted_amount)

```

**Key Considerations**

- Privacy: The package allows secure handling of sensitive data, ensuring that transaction amounts remain private during processing.
- Compliance: By combining homomorphic encryption, commitments, and Bulletproofs, the package supports compliance with privacy and regulatory standards, making it suitable for use in financial and regulated environments.
- Modularity: Each module is self-contained and can be used independently or together as required by the DGT-ZK Protocol.