# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Test deployment of Data Science Agent to Agent Engine."""

import os

import vertexai
from absl import app, flags
from dotenv import load_dotenv
from vertexai import agent_engines

# 首先確保環境變數已經設置正確
print(f"檢查環境變數設置:")
print(f"BQML_AGENT_MODEL: {os.getenv('BQML_AGENT_MODEL')}")
print(f"BIGQUERY_AGENT_MODEL: {os.getenv('BIGQUERY_AGENT_MODEL')}")
print(f"SQL_AGENT_MODEL: {os.getenv('SQL_AGENT_MODEL')}")
print(f"CODE_AGENT_MODEL: {os.getenv('CODE_AGENT_MODEL')}")
print(f"ROOT_AGENT_MODEL: {os.getenv('ROOT_AGENT_MODEL')}")

# 如果環境變數未設置，設置它們
if not os.getenv('BQML_AGENT_MODEL'):
    os.environ['BQML_AGENT_MODEL'] = 'gemini-2.0-flash-001'
if not os.getenv('BIGQUERY_AGENT_MODEL'):
    os.environ['BIGQUERY_AGENT_MODEL'] = 'gemini-2.0-flash-001'
if not os.getenv('SQL_AGENT_MODEL'):
    os.environ['SQL_AGENT_MODEL'] = 'gemini-2.0-flash-001'
if not os.getenv('CODE_AGENT_MODEL'):
    os.environ['CODE_AGENT_MODEL'] = 'gemini-2.0-flash-001'
if not os.getenv('ROOT_AGENT_MODEL'):
    os.environ['ROOT_AGENT_MODEL'] = 'gemini-2.0-flash-001'

FLAGS = flags.FLAGS

flags.DEFINE_string("project_id", None, "GCP project ID.")
flags.DEFINE_string("location", None, "GCP location.")
flags.DEFINE_string("bucket", None, "GCP bucket.")
flags.DEFINE_string(
    "resource_id",
    None,
    "ReasoningEngine resource ID (returned after deploying the agent)",
)
flags.DEFINE_string("user_id", None, "User ID (can be any string).")
flags.mark_flag_as_required("resource_id")
flags.mark_flag_as_required("user_id")


def main(argv: list[str]) -> None:  # pylint: disable=unused-argument

    load_dotenv()

    project_id = (
        FLAGS.project_id if FLAGS.project_id else os.getenv("GOOGLE_CLOUD_PROJECT")
    )
    location = FLAGS.location if FLAGS.location else os.getenv("GOOGLE_CLOUD_LOCATION")

    default_bucket_name = f"{project_id}-adk-staging" if project_id else None
    bucket_name = (
        FLAGS.bucket
        if FLAGS.bucket
        else os.getenv("GOOGLE_CLOUD_STORAGE_BUCKET", default_bucket_name)
    )

    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    location = os.getenv("GOOGLE_CLOUD_LOCATION")

    if not project_id:
        print("Missing required environment variable: GOOGLE_CLOUD_PROJECT")
        return
    elif not location:
        print("Missing required environment variable: GOOGLE_CLOUD_LOCATION")
        return
    elif not bucket_name:
        print("Missing required environment variable: GOOGLE_CLOUD_STORAGE_BUCKET")
        return

    vertexai.init(
        project=project_id,
        location=location,
        staging_bucket=f"gs://{bucket_name}",
    )

    agent = agent_engines.get(FLAGS.resource_id)
    print(f"Found agent with resource ID: {FLAGS.resource_id}")
    session = agent.create_session(user_id=FLAGS.user_id)
    print(f"Created session for user ID: {FLAGS.user_id}")
    print("Type 'quit' to exit.")
    while True:
        user_input = input("Input: ")
        if user_input == "quit":
            break

        for event in agent.stream_query(
            user_id=FLAGS.user_id, session_id=session["id"], message=user_input
        ):
            if "content" in event:
                if "parts" in event["content"]:
                    parts = event["content"]["parts"]
                    for part in parts:
                        if "text" in part:
                            text_part = part["text"]
                            print(f"Response: {text_part}")

    agent.delete_session(user_id=FLAGS.user_id, session_id=session["id"])
    print(f"Deleted session for user ID: {FLAGS.user_id}")


if __name__ == "__main__":
    app.run(main)
