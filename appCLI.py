from appCore import appCreatorLinkedin, createRequest
from models.request_models import JobSearchRequest
from models.response_models import JobSearchResponse
import logging
import logging_config  # Import the logging configuration
import os
import json
import argparse
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    # use arg parser to parse the command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--json-file", help="Path to the json file",
                        default="input/sample_user.json")
    parser.add_argument(
        "--login-linkedin", help="use login command to login to linkedin", action="store_true")
    parser.add_argument(
        "--jobs-search", help="use jobs-search command to search for jobs", action="store_true")
    parser.add_argument(
        "--jobs-apply", help="use jobs-apply command to apply for jobs", action="store_true")
    args = parser.parse_args()
    # parse the json file
    Request = createRequest(args.json_file)
    app = appCreatorLinkedin(Request)
    if args.login_linkedin:
        app.tryCredentialsLinkedin()
    if args.jobs_search:
        app.searchJobs()
    if args.jobs_apply:
        app.applyJobs()
