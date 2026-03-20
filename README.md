# 🤟 Text to Indian Sign Language (ISL) Translator

A Django-based AI project that converts **text and speech into Indian Sign Language (ISL)** using gesture videos. Designed as an assistive communication tool for the deaf and hard-of-hearing community.

---

## Features

* Text → ISL Translation
* Speech → ISL Conversion
* Sequential Gesture Video Playback
* Real-Time Chat Mode (Text → ISL)
* Unknown Word Handling (Finger Spelling A–Z)


---

## How It Works

```text
User Input → NLP Processing → Word Mapping → Video Sequence → ISL Output
```

---

## Tech Stack

* **Backend:** Django (Python)
* **Frontend:** HTML, CSS, JavaScript
* **NLP:** Basic preprocessing (tokenization, stopword removal)
* **Dataset:** ISL gesture video dataset

---

## Project Structure

```text
text-to-isl/
│── translator/
│── text2isl_proj/
│── static/sign_assets/words/
│── templates/
│── manage.py
│── requirements.txt
```

---

## Setup Instructions

```bash
git clone https://github.com/anandu-narayanan/text-to-isl.git
cd text-to-isl
pip install -r requirements.txt
python manage.py runserver
```

---

## Use Cases

* Assistive communication tool
* ISL learning platform
* Real-time translation system

---

## Future Improvements

* AI-based ISL grammar conversion
* 3D avatar sign generation
* Live multi-user chat system

---

