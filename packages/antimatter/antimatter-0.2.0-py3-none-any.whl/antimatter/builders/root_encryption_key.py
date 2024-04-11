
from typing import Union

from antimatter.client import (
    AWSServiceAccountKeyInfo, GCPServiceAccountKeyInfo, AntimatterDelegatedAWSKeyInfo, KeyInfosKeyInformation,
    KeyInfos
)

def aws_service_account_key_info(access_key_id: str, secret_access_key: str, key_arn: str = "") -> KeyInfos:
    """
    Create a KeyInfos object with AWS service account key information

    Example usage:
    ```
    key_info = aws_service_account_key_info(
        access_key_id="access_key_id", secret_access_key="secret_access_key", key_arn="key_arn"
    )
    ```

    :param access_key_id: The access key ID
    :param secret_access_key: The secret access key
    :param key_arn: The key ARN

    :return: A KeyInfos object with the specified key information
    """
    return KeyInfos(
        keyInformation=KeyInfosKeyInformation(
            actual_instance=AWSServiceAccountKeyInfo(
                access_key_id=access_key_id, secret_access_key=secret_access_key, key_arn=key_arn
            )
        )
    )

def antimatter_delegated_aws_key_info(key_arn: str) -> KeyInfos:
    """
    Create a KeyInfos object with Antimatter delegated AWS key information

    Example usage:
    ```
    key_info = antimatter_delegated_aws_key_info(key_arn="key_arn")
    ```

    :param key_arn: The key ARN

    :return: A KeyInfos object with the specified key information
    """
    return KeyInfos(
        keyInformation=KeyInfosKeyInformation(
            actual_instance=AntimatterDelegatedAWSKeyInfo(key_arn=key_arn)
        )
    )

def gcp_service_account_key_info(
        service_account_credentials: str, project_id: str, location: str, key_ring_id: str = "", key_id: str = ""
    ) -> KeyInfos:
    """
    Create a KeyInfos object with GCP service account key information

    Example usage:
    ```
    key_info = gcp_service_account_key_info(
        service_account_credentials="service_account_credentials", project_id="project_id", location="location",
        key_ring_id="key_ring_id", key_id="key_id"
    )
    ```

    :param service_account_credentials: The service account credentials
    :param project_id: The project ID
    :param location: The location
    :param key_ring_id: The key ring ID
    :param key_id: The key ID

    :return: A KeyInfos object with the specified key information
    """
    return KeyInfos(
        keyInformation=KeyInfosKeyInformation(
            actual_instance=GCPServiceAccountKeyInfo(
                service_account_credentials=service_account_credentials, project_id=project_id, location=location,
                key_ring_id=key_ring_id, key_id=key_id
            )
        )
    )
