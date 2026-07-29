# CloudExify Cybersecurity Internship — Month 1 Final Submission

**Name:** Humayun Khawar
**Registration No:** CX-INT-2026-CYB-0052

## Project 1 — Network Penetration Testing

Scanning was performed against an isolated Metasploitable virtual machine from a Kali Linux VM, on a private VirtualBox host-only network.

nmap scans (basic, top-ports, `-sV`, `-A`, `-sU`, and a full `/24` subnet sweep) identified 17 open TCP ports and several open UDP ports. Wireshark was used to capture and filter live traffic during scanning, including SYN packets, source-IP-filtered traffic, and traffic on port 80.

The most significant finding was `vsftpd 2.3.4` on port 21, a version with a publicly known backdoor. This was confirmed and exploited using Metasploit (`exploit/unix/ftp/vsftpd_234_backdoor`), resulting in a remote root shell on the target.

Full details, screenshots, and remediation recommendations are in `penetration_test_report.pdf`. Raw scan output and packet captures are in `nmap_and_wireshark_labs/`.

## Project 2 — Cryptography & Password Security

### secure_auth.py

Implements a `SecureAuth` class that registers users and stores their passwords hashed with bcrypt in `users.json`. Passwords are never stored in plaintext.

Demonstrated behavior:
- Registering a new user succeeds
- Registering an existing username returns `"User exists!"`
- Logging in with the correct password returns `True`
- Logging in with an incorrect password returns `False`
- Hashing the same password twice with bcrypt produces two different hashes, because `bcrypt.gensalt()` generates a new random salt each time
- Hashing the same password twice with plain SHA-256 produces the identical hash both times, showing why SHA-256 alone is unsuitable for password storage and vulnerable to rainbow table attacks

### encryption_examples.py

Demonstrates symmetric encryption using Fernet:
- Generates a key and encrypts a sample piece of sensitive data
- Decrypts the data successfully using the correct key
- Attempts decryption with a different, incorrect key, which raises `InvalidToken`, confirming the encrypted data cannot be read without the correct key

## Key Takeaways

- Passwords must be hashed with a salted, slow algorithm such as bcrypt, never stored in plaintext or with fast general-purpose hashes like SHA-256
- A unique salt per password prevents rainbow table attacks and ensures identical passwords do not produce identical hashes
- Sensitive data in transit or at rest should use authenticated symmetric encryption such as Fernet, with keys kept separate from the encrypted data
- Outdated, unpatched services such as `vsftpd 2.3.4` can provide attackers with direct root access, reinforcing the need for regular patching and service hardening
