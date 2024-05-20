#!/usr/bin/env python3
import sys
import re
from http.connection_helper import HttpConnectionHelper


def parse_headers(response):
    """
    Parse HTTP response headers.
    :param response: Raw HTTP response.
    :return: Headers as a string.
    """
    header_end_idx = response.find(b"\r\n\r\n")
    headers = response[:header_end_idx].decode("latin1")
    return headers


def parse_body(response):
    """
    Parse HTTP response body.
    :param response: Raw HTTP response.
    :return: Body as a string.
    """
    header_end_idx = response.find(b"\r\n\r\n")
    body = response[header_end_idx + 4 :].decode("latin1")
    return body


def extract_links(html):
    """
    Extract links from HTML content.
    :param html: HTML content.
    :return: List of (link text, link URL) tuples.
    """
    link_pattern = re.compile(
        r'<a\s+(?:[^>]*?\s+)?href="([^"]*)">(.*?)</a>', re.IGNORECASE
    )
    links = re.findall(link_pattern, html)
    return links


def display_headers(headers):
    """
    Display the HTTP headers.
    :param headers: Headers as a string.
    """
    print("HTTP Response Headers:")
    for line in headers.split("\r\n"):
        if line:
            print(line)
    print()


def display_links(links):
    """
    Display the links found in HTML content.
    :param links: List of (link text, link URL) tuples.
    """
    print("Links found on the page:")
    for idx, (href, text) in enumerate(links, start=1):
        print(f"[{idx}] {text} -> {href}")


def main(url, port):
    """
    Main function to start the web browser.
    :param url: URL to open.
    :param port: Port to connect to.
    """
    if not url.startswith("http://"):
        url = "http://" + url

    host = url.split("://")[1].split("/")[0]
    path = "/" + "/".join(url.split("://")[1].split("/")[1:])
    if path == "/":
        path = "/example"

    port = int(port)

    con_helper = HttpConnectionHelper()
    con_helper.connect(host, port, False)

    request = f"GET {path} HTTP/1.1\r\nHost: {host}:{port}\r\n\r\n"
    con_helper.send_request(request)
    response = con_helper.receive_response()
    con_helper.close()

    # Debug print the raw response
    print("Raw Response:", response)

    response = response.encode("utf-8").decode("unicode_escape").encode("latin1")

    headers = parse_headers(response)
    body = parse_body(response)

    # Debug print the body content
    print("HTML Body:\n", body)

    display_headers(headers)
    links = extract_links(body)
    display_links(links)

    while True:
        choice = input("Press 0 to exit or enter the number of the link to visit: ")
        if choice == "0":
            break
        try:
            choice = int(choice)
            if 1 <= choice <= len(links):
                new_path = links[choice - 1][0]
                main(host + new_path, port)
            else:
                print("Invalid choice. Try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python webbrowser.py <URL> <PORT>")
    else:
        main(sys.argv[1], sys.argv[2])
