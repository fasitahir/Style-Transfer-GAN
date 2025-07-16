# 🎨 Image Stylization API Client

This project demonstrates how to send an image to a local image stylization API using a `curl` command and save the processed image locally.

## 🔧 Overview

The `curl` command sends a `POST` request to a locally hosted API, uploads an image file using multipart form-data, specifies the computation device (e.g., CPU), and stores the stylized output image.

---

## 📤 Curl Command

```bash
curl -X POST http://192.168.10.223:8000/stylize/ \
     -F "file=@D:/img.jpg" \
     -F "device=cpu" \
     --output "D:/output.jpeg"
```

---

## 🧩 Parameters Explained

| Parameter | Description |
|----------|-------------|
| `-X POST` | Sends a POST request to the specified URL. |
| `-F "file=@D:/img.jpg"` | Uploads the image located at `D:/img.jpg`. The `@` tells `curl` to send the file contents. |
| `-F "device=cpu"` | Tells the API to use the CPU for processing. Other options (like `cuda`) may be supported depending on the server. |
| `--output "D:/output.jpeg"` | Saves the response (processed image) to the specified location. |

---

## ✅ Requirements

- A local server running at `http://192.168.10.223:8000/stylize/`
- The file `D:/img.jpg` must exist and be accessible
- Write permissions on the output directory

---

## 🛠 Troubleshooting

- ❌ **Command does nothing?** Check server availability or firewall rules.
- ❌ **SSL Error?** If using HTTPS and encountering self-signed cert issues, add `-k`:
  ```bash
  curl -k -X POST https://192.168.10.223:8000/stylize/ ...
  ```
- ❌ **Path issues?** Avoid unnecessary escaping. Windows `curl` works fine with:
  ```bash
  -F "file=@D:/img.jpg"
  ```

---

## 💡 Example Use Case

Automated image stylization using a locally served AI model (e.g., using FastAPI or Flask) for real-time creative applications or preprocessing tasks.

---

## 📂 Output

The stylized image will be saved to:
```
D:/output.jpeg
```

Make sure this path is valid and writable.

---

## 📬 Contact

For questions or support, feel free to reach out to the developer or open an issue on the associated repository.

---
