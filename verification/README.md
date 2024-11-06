# DGT-ZK Protocol: Verification Package

This package provides comprehensive verification and compliance mechanisms for the DGT-ZK Protocol, ensuring that transactions meet regulatory and security standards. It includes tools for cryptographic verification, compliance checks, and secure handling of sensitive information using Private Set Intersection (PSI) with support for both Paillier and Schnorr schemes.

---

## Package Modules

### 1. `verification_constants.py`

**Description**: Defines constants essential for setting up PSI schemes, managing compliance levels, and configuring the paths to database files for blacklists and whitelists.

#### Key Constants
- **PSI_PAILLIER** and **PSI_SCHNORR**: Configures the type of PSI scheme used (Paillier or Schnorr) for compliance.
- **DEFAULT_HASH_ALGORITHM**: Hashing algorithm used across modules to maintain uniformity.
- **COMPLIANCE_LEVEL_BASIC** and **COMPLIANCE_LEVEL_ADVANCED**: Compliance levels for transaction validation, providing flexibility in security checks.
- **BLACKLIST_DB_PATH** and **WHITELIST_DB_PATH**: Standardized paths for accessing blacklists and whitelists.
- **ENABLE_KYC_CHECK** and **ENABLE_AML_CHECK**: Flags to toggle KYC and AML checks as needed.
- **REGULATORY_REPORT_PATH**: Path for storing reports related to compliance checks.

This module centralizes configuration, enabling consistent, configurable verification settings across the entire package.

---

### 2. `encryption_utils.py`

**Description**: Provides cryptographic utilities for hashing and key exchanges, particularly for Schnorr signatures used in the PSI scheme.

#### Key Functions
- **hash_data(data, algorithm)**: Hashes data using a specified algorithm, supporting uniform hashing across protocol modules.
- **generate_schnorr_keypair()**: Generates a Schnorr keypair for use in secure PSI operations.
- **schnorr_sign(message, private_key_hex)**: Signs a message with the Schnorr signature, ensuring data authenticity.
- **schnorr_verify(message, r, s, public_key_hex)**: Verifies Schnorr signatures, validating sender authenticity within the protocol.

These functions ensure the security and consistency of cryptographic operations, particularly in the compliance and verification components of the protocol.

---

### 3. `psi_protocol.py`

**Description**: Implements Private Set Intersection (PSI) to allow secure compliance checks on encrypted data using both Paillier and Schnorr schemes.

#### Key Functions
- **__init__(self, scheme_type)**: Initializes the PSI scheme (Paillier or Schnorr) based on the specified type.
- **encrypt_set(self, data_set)**: Encrypts a data set with the specified PSI scheme.
- **compute_intersection(self, encrypted_set, reference_set)**: Computes the intersection between two encrypted sets to check for common elements.
- **verify_item(self, item, reference_set)**: Verifies the presence of an encrypted item in a reference set (specific to the Schnorr scheme).

#### Usage Examples
```python
# Initialize Paillier-based PSI
psi_paillier = PSIScheme(scheme_type="paillier")
encrypted_data_set = psi_paillier.encrypt_set([123, 456, 789])
intersection = psi_paillier.compute_intersection(encrypted_data_set, reference_set)
```

This module is crucial for regulatory compliance, allowing encrypted address sets to be compared with encrypted blacklists or whitelists.

* * *

### 4. `compliance_verification.py`

**Description**: Performs compliance checks, such as KYC/AML, using PSI to verify addresses against blacklist and whitelist databases.

#### Key Functions

* ****init**(self, scheme_type, compliance_level)**: Sets up the compliance verification system.
* **load_blacklist(self)**: Loads blacklist entries.
* **load_whitelist(self)**: Loads whitelist entries.
* **check_compliance(self, address_set)**: Uses PSI to check if addresses are compliant by comparing them against the blacklist and whitelist.
* **verify_transaction(self, tx)**: Validates a transaction's compliance status based on KYC/AML requirements.

#### Usage Examples

```python
# Initialize compliance verification with Schnorr PSI
compliance = ComplianceVerification(scheme_type="schnorr", compliance_level=COMPLIANCE_LEVEL_ADVANCED)
compliance_result = compliance.verify_transaction(transaction)
print("Compliance Status:", compliance_result)
```

* * *

### 5. `transaction_verification.py`

**Description**: The main module that combines compliance checks, transaction validation, and verification functions to ensure secure and compliant transactions within the protocol.

#### Key Functions

* **compliance_check(tx, level)**: Conducts KYC/AML checks on a transaction based on the specified compliance level.
* **verify_amount_range(tx)**: Validates that the transaction amount is within an acceptable range using Bulletproofs.
* **verify_signature(tx, public_key)**: Confirms that the transaction's digital signature is valid.
* **is_blacklisted(address)** and **is_whitelisted(address)**: Functions to check addresses against blacklist/whitelist databases.

This module unifies transaction compliance and verification, ensuring secure, regulatory-compliant interactions within the DGT-ZK Protocol.

* * *

### Bulletproofs Subpackage

The `bulletproofs` subpackage provides secure range proofs for verifying transaction amounts without revealing sensitive data. These proofs are essential for validating the integrity of transactions in compliance with the protocol’s security standards.

* * *

## Example Usage

Below is a consolidated example of how to perform a complete compliance and verification workflow with the DGT-ZK Protocol's `verification` package.

```python
from verification.transaction_verification import compliance_check, verify_amount_range, verify_signature
from verification.encryption_utils import generate_schnorr_keypair, schnorr_sign, schnorr_verify

# Generate keys for signing
private_key, public_key = generate_schnorr_keypair()

# Sample transaction
transaction = {
    "sender": public_key,
    "recipient": "recipient_public_key",
    "timestamp": "2024-01-01T10:00:00Z",
    "amount": 500
}

# Sign the transaction
signature = schnorr_sign(transaction, private_key)

# Compliance check
compliant = compliance_check(transaction, level=COMPLIANCE_LEVEL_BASIC)
print("Compliance:", "Passed" if compliant else "Failed")

# Amount range verification
in_range = verify_amount_range(transaction)
print("Amount Range Verification:", "Valid" if in_range else "Invalid")

# Signature verification
signature_valid = verify_signature(transaction, public_key)
print("Signature Verification:", "Valid" if signature_valid else "Invalid")
```