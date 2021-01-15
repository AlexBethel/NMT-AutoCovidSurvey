(This is a draft document; the program doesn't work at all as of yet.)

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

This script requires Python (version 2 or 3), as well as the
`pip` package manager. With those installed, run `pip install -r
requirements.txt` in the repository to install all other dependencies.

Copy or rename the default `config.def.toml` to `config.toml`, and fill
out all the listed fields with correct information.

## Usage

Just run `./nmt-autocovidsurvey.py` to automatically fill out the
screening survey with the configured response.
