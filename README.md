# FTPshare

This project provides a high-performance, adaptive FTP server and client written in Python. It is designed to efficiently transfer large files (e.g., ISO images) across multiple clients while optimizing CPU and memory usage.

## Features

- **Adaptive Server**
  - Preloads files into RAM if sufficient memory is available for faster transfers.
  - Falls back to disk if RAM is insufficient.
  - Supports multiple simultaneous clients without overloading CPU.

- **Adaptive Client**
  - Automatically detects CPU cores and free RAM.
  - Adjusts the number of download threads and block size for optimal performance.
  - Multi-threaded downloads to maximize network throughput.

- **Cross-Platform**
  - Works on Windows, Linux, and macOS.

## Requirements

- Python 3.8+
- Packages listed in `requirements.txt`:
  ```text
  pyftpdlib>=1.5.7
  psutil>=5.9.5

## Setup Instructions

1. **Install dependencies**

```bash
pip install -r requirements.txt
```

2. **Prepare the server**

* Place the file you want to serve (e.g., `kali.iso`) inside the `ftp_root/` directory.
* Start the server:

```bash
python ftpserver.py
```

3. **Prepare the client**

* Update the `SERVER_IP` variable in `ftprecv.py` with your server's IP address.
* Run the client:

```bash
python ftprecv.py
```

## Configuration

* **FTP Port**: Default is `2121`. Can be changed in `ftpserver.py` and `ftprecv.py`.
* **ISO / File Name**: Change the `ISO_FILENAME` in server and `REMOTE_FILE` in client if serving a different file.
* **Adaptive settings**: Threads and block size are automatically adjusted based on system CPU cores and RAM.

## Usage Notes

* Recommended for LAN usage to achieve maximum speeds.
* Works efficiently even on low-end PCs with i3/i5 CPUs.
* Server can handle multiple clients simultaneously.
* Client supports multi-threaded downloads to saturate fast networks without straining CPU.

## License

This project is open-source and free to use.
