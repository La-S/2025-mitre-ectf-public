"""
Author: Ben Janis
Date: 2025

This source file is part of an example system for MITRE's 2025 Embedded System CTF
(eCTF). This code is being provided only for educational purposes for the 2025 MITRE
eCTF competition, and may not meet MITRE standards for quality. Use this code at your
own risk!

Copyright: Copyright (c) 2025 The MITRE Corporation
"""

import argparse
import json
from pathlib import Path
import secrets

from loguru import logger


def gen_secrets_json(channels: list[int], key_hex) -> bytes:
    """Generate the contents secrets file

    This will be passed to the Encoder, ectf25_design.gen_subscription, and the build
    process of the decoder

    :param channels: List of channel numbers that will be valid in this deployment.
        Channel 0 is the emergency broadcast, which will always be valid and will
        NOT be included in this list

    :returns: Contents of the secrets file
    """
    # TODO: Update this function to generate any system-wide secrets needed by
    #   your design

    # Create the secrets object
    # You can change this to generate any secret material
    # The secrets file will never be shared with attackers
    secrets = {
        "channels": channels,
        "aes_key":str(key_hex).upper()
    }

    # NOTE: if you choose to use JSON for your file type, you will not be able to
    # store binary data, and must either use a different file type or encode the
    # binary data to hex, base64, or another type of ASCII-only encoding
    return json.dumps(secrets).encode()


def gen_secrets_header(channels: list[int], key_hex) -> bytes:
    """Generate the contents secrets file

    This will be passed to the Encoder, ectf25_design.gen_subscription, and the build
    process of the decoder

    :param channels: List of channel numbers that will be valid in this deployment.
        Channel 0 is the emergency broadcast, which will always be valid and will
        NOT be included in this list

    :returns: Contents of the secrets file
    """

    channels_line = "extern char channels["+str(len(channels))+"] = {"+str(",".join(map(str, channels)))+"};"
    
    secret_numbers = list(bytearray.fromhex(key_hex))
    secret_key_line = "extern int secret_key_imported[16] = {"+str(",".join(map(str, secret_numbers)))+"};"
    
    h_file_contents = channels_line + "\n"+secret_key_line
    # """
    # extern char channels[3] = {1, 2, 3};
    # extern int secret_key_imported[16] = {129, 186, 203, 50, 132, 39, 232, 200, 178, 206, 57, 56, 130, 217, 171, 205};
    # """

    return h_file_contents.encode()

def parse_args():
    """Define and parse the command line arguments

    NOTE: Your design must not change this function
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--force",
        "-f",
        action="store_true",
        help="Force creation of secrets file, overwriting existing file",
    )
    parser.add_argument(
        "secrets_folder",
        type=Path,
        help="Path to the secrets folder",
    )
    parser.add_argument(
        "channels",
        nargs="+",
        type=int,
        help="Supported channels. Channel 0 (broadcast) is always valid and will not"
        " be provided in this list",
    )
    return parser.parse_args()


def main():
    """
    Main function of gen_secrets. We did change this function...
    """
    # Parse the command line arguments
    args = parse_args()

    key_hex = secrets.token_hex(16)

    secrets_json = gen_secrets_json(args.channels, key_hex)

    # Open the file, erroring if the file exists unless the --force arg is provided
    with open(str(args.secrets_folder)+"/secrets.json", "wb" if args.force else "xb") as f:
        # Dump the secrets to the file
        f.write(secrets_json)

    secrets_h = gen_secrets_header(args.channels, key_hex)

    # Open the file, erroring if the file exists unless the --force arg is provided
    with open(str(args.secrets_folder)+"/secrets.h", "wb" if args.force else "xb") as f:
        # Dump the secrets to the file
        f.write(secrets_h)


if __name__ == "__main__":
    main()
