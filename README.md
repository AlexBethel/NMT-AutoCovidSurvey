# NMT-AutoCovidSurvey

This is a small Python script for automatically filling out the NMT
Student Daily COVID-19 Symptom Screening Form, which is required to be
filled out every day by everyone at the school.

This program uses headless web browser automation to simply play back
pre-recorded responses from a configuration file. **You are responsible
for ensuring these configured responses are accurate, up to date, and
submitted neither more nor less than once per day.** If you have COVID
symptoms, do not use this script; instead fill the form out manually.

## Installation & configuration

This script requires Python (version 2 or 3), as well as the `pip`
package manager, and an installation of the Chromium (or Chrome) web
browser. With those installed, run `pip install -r requirements.txt` in
the repository to install all other dependencies.

Copy or rename the default `config.def.toml` to `config.toml`, and fill
out all the listed fields with correct information.

### Generating a Google cookie

Getting the correct cookie value can be a little tricky, but here are
the basic steps you should follow:
1. Navigate to https://docs.google.com/, and sign in to the login
   page.
2. Press F12 to open the developer tools. (This will work on most
   major browsers including Firefox, Chrome, Edge, Internet Explorer
   and Brave, but the precise steps may vary for others.)
3. Navigate to the JavaScript Console tab and type in
   "document.cookie" (without the quotes).
4. Copy and paste the resulting string to the config file.

You may occasionally need to repeat this process as a result of
authentication tokens expiring (about once a month in general).

## Usage

Just run `./nmt-autocovidsurvey.py` (or `python ./nmt-autocovidsurvey.py`
if you prefer or are running Windows) to automatically fill out the
screening survey with the configured response.
