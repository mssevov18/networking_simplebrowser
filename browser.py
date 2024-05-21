#!/usr/bin/env python
import socket
import re
import sys


def get_http_response(host, port, path):
    """Send an HTTP GET request and return the response."""
    request = f"GET {path} HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"

    # Create a socket and connect to the server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(request.encode())

        response = b""
        while True:
            data = s.recv(1024)
            if not data:
                break
            response += data

    return response.decode()


def parse_response(response):
    """Parse the HTTP response into headers and body."""
    header, _, body = response.partition("\r\n\r\n")
    headers = header.split("\r\n")
    return headers, body


def display_headers(headers):
    """Display the headers."""
    for header in headers:
        print(header)


def extract_links(body):
    """Extract and return links from the HTML body."""
    link_pattern = re.compile(
        r'<a\s+(?:[^>]*?\s+)?href="([^"]*)">(.*?)</a>', re.IGNORECASE
    )
    links = link_pattern.findall(body)
    return links


def display_links(links):
    """Display links in a numbered list."""
    for i, (href, text) in enumerate(links, 1):
        print(f"[{i}] {text} -> {href}")


def main(url):
    if not url.startswith("http://"):
        url = "http://" + url

    # Parse the URL
    match = re.match(r"http://([^/]+)(/?.*)", url)
    if not match:
        print("Invalid URL format")
        return

    host, path = match.groups()
    path = path if path else "/"

    while True:
        response = get_http_response(host, 80, path)
        headers, body = parse_response(response)

        display_headers(headers)
        links = extract_links(body)
        display_links(links)

        choice = input("Press 0 to exit or enter the link number to follow: ")
        if choice == "0":
            break

        try:
            choice = int(choice)
            if 1 <= choice <= len(links):
                path = links[choice - 1][0]
                if not path.startswith("/"):
                    path = "/" + path
            else:
                print("Invalid choice")
        except ValueError:
            print("Invalid input")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python browser.py <URL>")
    else:
        main(sys.argv[1])
