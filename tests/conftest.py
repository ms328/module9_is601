# tests/e2e/conftest.py

import subprocess
import sys
import socket
import os
import time
import pytest
from playwright.sync_api import sync_playwright
import requests

@pytest.fixture(scope='session')
def fastapi_server():
    """
    Fixture to start the FastAPI server before E2E tests and stop it after tests complete.
    """
    # Choose a free port dynamically to avoid conflicts with other processes
    sock = socket.socket()
    sock.bind(('127.0.0.1', 0))
    host, port = sock.getsockname()
    sock.close()

    # Start FastAPI app using the same Python executable running the tests via uvicorn
    fastapi_process = subprocess.Popen([
        sys.executable, '-m', 'uvicorn', 'main:app', '--host', '127.0.0.1', '--port', str(port)
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Define the URL to check if the server is up
    server_url = f'http://127.0.0.1:{port}/'

    # Expose server URL to tests via environment variable
    os.environ['TEST_SERVER_URL'] = server_url
    
    # Wait for the server to start by polling the root endpoint
    timeout = 30  # seconds
    start_time = time.time()
    server_up = False
    
    print("Starting FastAPI server...")
    
    while time.time() - start_time < timeout:
        try:
            response = requests.get(server_url)
            if response.status_code == 200:
                server_up = True
                print("FastAPI server is up and running.")
                break
        except requests.exceptions.ConnectionError:
            pass
        time.sleep(1)
    
    if not server_up:
        fastapi_process.terminate()
        raise RuntimeError("FastAPI server failed to start within timeout period.")
    
    yield
    
    # Terminate FastAPI server
    print("Shutting down FastAPI server...")
    fastapi_process.terminate()
    fastapi_process.wait()
    print("FastAPI server has been terminated.")

@pytest.fixture(scope="session")
def playwright_instance_fixture():
    """
    Fixture to manage Playwright's lifecycle.
    """
    with sync_playwright() as p:
        yield p

@pytest.fixture(scope="session")
def browser(playwright_instance_fixture):
    """
    Fixture to launch a browser instance.
    """
    browser = playwright_instance_fixture.chromium.launch(headless=True)
    yield browser
    browser.close()

@pytest.fixture(scope="function")
def page(browser):
    """
    Fixture to create a new page for each test.
    """
    page = browser.new_page()
    yield page
    page.close()
