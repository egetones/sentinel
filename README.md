<div align="center">

# sentinel

![Python](https://img.shields.io/badge/Python-3.x-blue?style=flat&logo=python)
![License](https://img.shields.io/badge/License-MIT-green)
![Type](https://img.shields.io/badge/Type-Blue_Team-blue)

<p>
  <strong>A lightweight File Integrity Monitor (FIM) to detect unauthorized file changes.</strong>
</p>

[Report Bug](https://github.com/egetones/sentinel/issues) · [Request Feature](https://github.com/egetones/sentinel/issues)

</div>

---

## Description

**sentinel** is a cybersecurity defense tool written in Python. It functions as a File Integrity Monitor (FIM), a critical component in any Security Operations Center (SOC).

It calculates the cryptographic hash (SHA-256) of files in a target directory to create a "digital fingerprint." By continuously monitoring these files, Sentinel can detect and alert users to **modifications**, **deletions**, or **new file creations** in real-time. This is useful for detecting ransomware activity or unauthorized configuration changes.

### Key Features

  **SHA-256 Hashing:** Uses industry-standard hashing for precise integrity verification.
  **Real-Time Alerts:** Instantly notifies the user of any file system events.
  **Baseline Management:** Easily creates and updates the trusted state of a directory.
  **Color-Coded Output:** Distinguishes between critical alerts (Red) and info (Green).

---

## Usage

1. **Setup a test folder:**
   ```bash
   mkdir test_files
   echo "This is a safe file" > test_files/safe.txt
   ```

2. **Run the tool:**
   ```bash
   python3 sentinel.py
   ```

3. **Workflow:**
   * **Step 1:** Select Option `1` to create a **Baseline**. Enter `./test_files` as the target.
   * **Step 2:** Restart the tool and select Option `2` to **Monitor**.

4. **Simulate an Attack:**
   While Sentinel is running, open another terminal and modify the file:
   ```bash
   echo "HACKED" >> test_files/safe.txt
   ```
   *Sentinel will immediately trigger a generic RED ALERT.*

---

## ⚠️ Disclaimer

This tool is a Proof-of-Concept (PoC) for educational purposes. It is designed to teach the fundamentals of Host-based Intrusion Detection Systems (HIDS).

---

## License

Distributed under the MIT License. See `LICENSE` for more information.
