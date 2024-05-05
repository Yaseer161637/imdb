# IMDb Flask App

Welcome to the IMDb Flask App! This application allows users to explore movie information.

## Setup

### Prerequisites

Make sure you have the following installed on your system:

- Python 3.x
- MongoDB

### Installation

1. Clone the repository:
    ```bash
    cd imdb
    ```

2. Install dependencies:
    ```bash
    pip3 install -r requirements.txt
    ```

### Configuration

Before running the application, you need to configure the environment variables. update values in `bash_profile.imdb` file  if required.

```bash
source bash_profile.imdb
```

### Running the Application

Source virtual enviornment profile
```
ex: source venv/bin/active
```
To start the Flask development server, run the following command:


```bash
python3 app.py --debug
```


### Optional

to create database collections

```bash
python3 schema.py
```
