import os
import json
import boto3
import time
from datetime import datetime
from pytz import timezone


def update_aws_configuration(access_key_id: str, secret_access_key: str, session_token: str, profile: str) -> str:
    command = \
        f"aws configure set aws_access_key_id {access_key_id} --profile {profile} & "\
        f"aws configure set aws_secret_access_key {secret_access_key} --profile {profile} & "\
        f"aws configure set aws_session_token {session_token} --profile {profile} & "

    os.system(command)


def format_date(date: datetime) -> datetime:
    return date.astimezone(timezone("Europe/London"))


def auth_identities(mfa_arn):
    mfa_token_code = input("Enter MFA code: ")

    session = boto3.session.Session(profile_name="nhsd")
    client = session.client("sts")

    response = client.get_session_token(
        SerialNumber=mfa_arn,
        TokenCode=mfa_token_code
    )

    credentials = response["Credentials"]
    access_key_id = credentials["AccessKeyId"]
    secret_access_key = credentials["SecretAccessKey"]
    session_token = credentials["SessionToken"]
    expiration = credentials["Expiration"]

    update_aws_configuration(access_key_id, secret_access_key, session_token, "nhsd-identities")

    print(f"identity authed, will expire at {format_date(expiration)}")


def auth_roles(roles: list):
    session = boto3.session.Session(profile_name="nhsd-identities")
    client = session.client("sts")

    for role in roles:
        if role["isEnabled"] is True:
            response = client.assume_role(
                RoleSessionName=role["name"],
                RoleArn=role["arn"],
                DurationSeconds=3600 # 1 hour
            )

            credentials = response["Credentials"]
            access_key_id = credentials["AccessKeyId"]
            secret_access_key = credentials["SecretAccessKey"]
            session_token = credentials["SessionToken"]
            expiration = credentials["Expiration"]

            update_aws_configuration(access_key_id, secret_access_key, session_token, role["profile"])

            print(f"{role['name']} expire at {format_date(expiration)}")


if __name__ == '__main__':
    data = json.load(open('config.json', 'r'))

    auth_identities(data["mfa_arn"])

    while True:
        auth_roles(data["roles"])
        time.sleep(60*59)
