# DGT-ZK
The DGT-ZK protocol manages shielded transactions for standard blockchain systems with an extension to off-chain oracles
=======
# DGT-ZK Protocol

## Overview

The **DGT-ZK Protocol** is a cryptographic protocol designed to facilitate secure, privacy-preserving transactions within a distributed ledger. It leverages zero-knowledge proofs, advanced encryption techniques, and compliance verification to support secure transactions that comply with regulatory standards without revealing sensitive data.

The protocol implements:
- **Zero-Knowledge (ZK) Proofs** with Bulletproofs for validating transaction amounts within defined ranges.
- **Private Set Intersection (PSI)** to enable off-chain compliance checks, ensuring that transactions meet KYC/AML standards.
- **Homomorphic Encryption** to securely transfer and manage transaction values.
- **Anchoring and Notarization** to add extra layers of security and integrity, with the ability to cancel transactions within defined windows.

This protocol is modular and extensible, allowing institutions to adopt components independently based on their compliance, security, and operational requirements.

## Problem Statement

In traditional distributed ledger environments, transactions are recorded on a public ledger. While secure, this transparency can conflict with data privacy and regulatory compliance requirements, especially in financial sectors where KYC/AML checks are critical. The DGT-ZK Protocol addresses these challenges by enabling:
- Private, encrypted transactions that do not reveal sensitive information publicly.
- Off-chain compliance verifications (KYC/AML) that maintain privacy while meeting regulatory standards.
- Flexible anchoring and cancellation mechanisms that support transaction reversibility within defined periods.

## Key Features

1. **Privacy-Preserving Transaction Verification**: Utilizes Bulletproofs to create range proofs, allowing verification that transaction amounts fall within specified limits without disclosing the exact amount.
2. **Compliance through Private Set Intersection (PSI)**: Supports compliance checks by ensuring transaction participants’ addresses do not overlap with blacklists or whitelists. PSI supports Paillier and Schnorr schemes, providing flexibility in cryptographic requirements.
3. **Homomorphic Encryption**: Enables encrypted transaction amounts, ensuring transaction values are secure even during processing.
4. **Anchoring and Notarization**: Implements a secure mechanism for anchoring transactions in a notary system with options for cancellation within a specified window, ensuring regulatory control and flexibility.

## Protocol Flow

1. **Transaction Creation**:
   - **Key Generation**: Sender and recipient generate key pairs, ensuring secure identity and signing.
   - **Secondary Address Creation**: The sender creates a temporary, secure address using Pedersen commitments.
   - **Encryption**: The transaction amount is encrypted with the recipient’s public key using homomorphic encryption.
   - **Signing**: The sender signs the transaction, including the encrypted amount and the commitment.

2. **Transaction Submission**:
   - **Submission to Validator**: The sender submits the signed transaction to the distributed ledger validator.
   - **Bulletproof Verification**: The validator verifies the transaction amount is within range using Bulletproofs.
   - **Notary Anchoring**: The transaction is anchored with a cancellation window, recorded in both the notary and distributed ledger systems.

3. **Compliance Checks**:
   - **Private Set Intersection**: Off-chain compliance checks are performed with PSI to verify the transaction participants' addresses against blacklists and whitelists.
   - **Regulatory Verification**: KYC/AML checks may include external agent verification or third-party regulatory access.

4. **Transaction Finalization**:
   - **Transaction Release**: After the compliance checks and expiration of the cancellation window, the notary releases the transaction.
   - **Recipient Verification**: The recipient verifies the transaction, decrypts the amount, and may transfer it to their main address or use it within the system.

5. **Optional Cancellation**:
   - Transactions may be canceled within the defined cancellation window, ensuring regulatory flexibility.

## Package Structure

This project is organized into modular packages, each handling specific aspects of the protocol:

### 1. **Encryption**
   - Handles all cryptographic operations, including homomorphic encryption, ECDSA-based signing, and Pedersen commitments.
   - Manages the generation, encryption, and verification of transaction amounts.

### 2. **Verification**
   - Includes submodules for Bulletproofs range proofs and Private Set Intersection (PSI) for KYC/AML compliance.
   - Manages compliance checks and validation routines to ensure transactions meet regulatory standards.

### 3. **Transaction**
   - Manages the transaction flow, anchoring, and cancellation logic.
   - Ensures transaction data is securely stored and verifiable within both the ledger and notary systems.

### 4. **Data**
   - Provides database handling for ledger and notary data, storing transactions and notarized records securely.
   - Supports data export functionality for analysis and compliance reporting.

### 5. **Utils**
   - Utility functions for data formatting, hashing, and timestamp generation, supporting consistent functionality across modules.

## Setup and Dependencies

### Prerequisites

- **Python 3.x**
- **Required Libraries**:
  - `lmdb`, `ecdsa`, `eth_keys`, `eth_utils`
  - Additional cryptographic libraries for specific functionalities such as Bulletproofs (FFI) and homomorphic encryption.

### Installation

Clone the repository and install the necessary packages:
```bash
git clone https://github.com/yourrepo/dgt_zk_protocol.git
cd dgt_zk_protocol
pip install -r requirements.txt
```

### Usage

#### Running the Protocol

The main entry point for the protocol is the `TransactionFlow` module within `transaction/transaction_flow.py`, which manages the lifecycle of a transaction. An example of initializing and running a transaction can be found in the package documentation or by running:

```python
from transaction.transaction_flow import TransactionFlow
from encryption.signature import generate_keys

# Generate sender's key pair
sender_private_key, sender_public_key = generate_keys()
recipient_public_key = "recipient_public_key_example"  # Replace with actual recipient's key

# Initialize transaction flow
tx_flow = TransactionFlow()

# Create and process a transaction
transaction = tx_flow.create_and_encrypt_transaction(
    tx_family="financial_tx",
    sender=sender_public_key,
    recipient=recipient_public_key,
    amount=100,
    private_key=sender_private_key
)
print("Created Transaction:", transaction)

# Validate and finalize the transaction
is_valid = tx_flow.validate_and_anchor_transaction(transaction, sender_public_key)
print("Transaction valid and anchored:", is_valid)
```

### License

The DGT-ZK Protocol is licensed under the AGPL-3.0 License. See LICENSE for more details.

## Contribution

Contributions to this project are welcome. Please see CONTRIBUTING.md for details on the code of conduct, development guidelines, and submission process.

## Future Enhancements

* **Consensus Integration**: Support for additional consensus protocols to enhance transaction finality.
* **Privacy and Compliance**: Extended compliance verification features, including dynamic PSI integration with regulatory bodies.
* **User Interface**: Tools for regulatory and user-friendly interfaces to interact with the DGT-ZK Protocol.

For more information, visit the official repository or contact the maintainers.

