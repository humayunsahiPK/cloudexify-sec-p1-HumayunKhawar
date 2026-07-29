# CloudExify Cybersecurity Internship — Month 1 Final Submission

**Name:** Humayun Khawar
**Registration No:** CX-INT-2026-CYB-0052

## Project 1 — Network Penetration Testing

For this project I set up an isolated lab using a Kali Linux VM and a Metasploitable VM on a private VirtualBox host-only network, so nothing left the lab environment.

I started with basic ping and nmap scans to confirm the target was alive and to see what ports were open, then moved on to more detailed scans, including a service version scan (`-sV`), an aggressive scan (`-A`), a UDP scan, and a full scan across the `/24` subnet to make sure I wasn't missing any devices on the network. Altogether these scans turned up 17 open TCP ports and several open UDP ports on the Metasploitable machine. Alongside the scanning, I used Wireshark to capture and filter the live traffic, looking specifically at SYN packets, traffic filtered by source IP, and traffic on port 80, to get a feel for what the scans actually looked like at the packet level.

The most interesting finding by far was port 21 running `vsftpd 2.3.4`, a version that's well known for containing a backdoor. I confirmed this using `searchsploit` and then used the corresponding Metasploit module to exploit it, which gave me a remote root shell on the target with no valid credentials needed. That's about as severe as a vulnerability gets, since it hands over full control of the machine to anyone who knows how to find it.

The full writeup, including screenshots of every step and my remediation recommendations, is in `penetration_test_report.pdf`. The raw nmap output and Wireshark capture file are in the `nmap_and_wireshark_labs` folder.

## Project 2 — Cryptography & Password Security

### secure_auth.py

This file implements a small authentication system built around a `SecureAuth` class. It lets you register a new user, hashes their password with bcrypt before anything gets written to disk, and stores the result in a `users.json` file. Plaintext passwords are never saved anywhere.

Running the file walks through a few scenarios to prove the system behaves the way it should. Registering a new user succeeds normally, but trying to register the same username again correctly gets rejected. Logging in with the right password returns `True`, and logging in with the wrong one returns `False`. I also hashed the same password twice with bcrypt to show that the two resulting hashes come out completely different each time, since bcrypt generates a fresh random salt on every call. As a point of comparison, I did the same thing with plain SHA-256, which produced the exact same hash both times — a good illustration of why SHA-256 on its own is a poor choice for storing passwords and why the added salt in bcrypt matters so much.

### encryption_examples.py

This file demonstrates symmetric encryption using Fernet, from the `cryptography` library. It generates an encryption key, uses it to encrypt a sample piece of sensitive data, and then decrypts it again successfully using that same key. To show the other side of this, I also tried decrypting the same data with a completely different key, which correctly raises an `InvalidToken` exception rather than returning garbage or silently failing, confirming that the encrypted data really is protected without the right key.

## Key Takeaways

Working through both projects this month reinforced a few things that come up constantly in real-world security work. Passwords should always be hashed with something slow and salted like bcrypt rather than stored in plaintext or hashed with a fast algorithm like SHA-256, since a unique salt is really what stands between a stolen password database and a trivial rainbow table lookup. Sensitive data that needs to be reversible, rather than just verified, should be encrypted with something like Fernet, with the key kept separate from the data itself. And on the infrastructure side, the vsftpd exploit was a clear reminder of how much damage a single outdated, unpatched service can cause, which is really the whole argument for regular patching and keeping unnecessary services turned off in the first place.
