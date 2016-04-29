# marionette_webconsole

PreReq: Start a marionette enabled Firefox instance with a js console open (to allow marionette to scrape the console logs), on OSX an example might be:

'''
/Applications/Firefox.app/Contents/MacOS/firefox-bin -marionette -profile default -jsconsole
'''

Create a virtual env, install the required packages and run the sample test which captures and asserts against the console log message '''Received a push notification'''

'''
virtualenv venv
./venv/bin/pip install -r requirements.txt
./venv/bin/py.test src/marionnette_webconsole_example.py
'''
