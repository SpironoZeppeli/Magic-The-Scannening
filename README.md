Magic the Gathering Card Scanner ReadMe

This tool has been made to facilitate the selling of cards automatically using card image recognition.
Although it was originally intended to work with a robot, automatically scanning and sorting cards, this functionality was
stripped due to the disruption of the coronavirus. Additional files have been included for review. The files required by the software 
are main.py, appORB.py, preprocessORB.py, ebay.py, camCapture.py and camCaptureUi.py 

'details.yaml' has been created to easily change user info. Please fill this information in accordingly

'ebay.yaml' contains information used for authorisation of the application to the user. To use the application, acquire the
corresponding keys and enter them into the field of this file.
Details on how to gather this data can be found at https://developer.ebay.com/api-docs/static/oauth-ui-tokens.html

To run the software, install the required python packages and run main.py. Alternatively, opening the project folder
within the PyCharm IDE will detect the resources required.