# RISC-V Summit 2020 Video Metadata

**The files are only provided for archival and educational purposes!**

This repository contains metadata about the uploaded videos for the RISC-V
Summit 2020, containing the time, title, description or topic, as well as the
link to the Swapcard event and the direct Vimeo videos.
The metadata is stored in form of JSON-files in the respective directories of
each day.

The tool used for creating the directories was the Selenium framework for
remote-controlling the browser to semi-automate the process of web-scraping.
The source can be found in the `scrape.py` file.

Using the direct links to Vimeo, you can also download the videos directly
using youtube-dl.
A script to automate this process as well is shipped as `download.sh`.
