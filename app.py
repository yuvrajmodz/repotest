from flask import Flask, request, jsonify
from playwright.sync_api import sync_playwright
import os

app = Flask(__name__)

@app.route('/api', methods=['GET'])
def get_number_details():
    number = request.args.get('number')

    if not number:
        return jsonify({"error": "No number provided"}), 400
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Launch the browser in headless mode
        page = browser.new_page()

        # Go to the target site
        page.goto("https://getno.site/number")
        
        # Fill the number in the input field
        page.fill('input[name="mobileNumber"]', number)
        
        # Click the proceed button
        page.click('button[onclick="submitForm()"]')

        # Wait for the redirect and the result page to load
        page.wait_for_url("https://getno.site/result.html")
        
        # Get the full page source (similar to 'View Source' in a browser)
        full_page_source = page.content()

        # Close the browser
        browser.close()

    # Return the full page source as part of the API response
    return jsonify({"html_source": full_page_source})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=True)