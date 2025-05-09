from flask import Flask, render_template, request
import requests
from urllib.parse import urljoin, urlparse

app = Flask(__name__)

def is_valid_url(url):
    """
    Checks if a URL is valid.
    Args:
        url (str): The URL to validate.
    Returns:
        bool: True if the URL is valid, False otherwise.
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def get_website_status(url):
    """
    Fetches the HTTP status code of a website.

    Args:
        url (str): The URL of the website to check.

    Returns:
        int: The HTTP status code, or None if an error occurs.
    """
    try:
        # Ensure the URL starts with http:// or https://
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url  # Try with https first, then http if that fails.

        response = requests.get(url, timeout=10)  # Add a timeout to prevent indefinite waiting
        return response.status_code
    except requests.exceptions.RequestException as e:
        print(f"Error fetching status for {url}: {e}") # Log the error
        return None  # Return None on error

@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Handles the main route for the web application.
    If it's a GET request, it renders the input form.
    If it's a POST request, it fetches the website status and displays it.
    """
    status_code = None
    url = None
    error_message = None

    if request.method == 'POST':
        url = request.form['url']
        if not url:
            error_message = "Please enter a URL."
        elif not is_valid_url(url):
            error_message = "Invalid URL. Please enter a valid URL (e.g., https://www.example.com)."
        else:
            status_code = get_website_status(url)
            if status_code is None:
                error_message = "Failed to retrieve status.  Check the URL and try again."

    return render_template('index.html', status_code=status_code, url=url, error_message=error_message)

if __name__ == "__main__":
    app.run(debug=True) #remove debug=True for production