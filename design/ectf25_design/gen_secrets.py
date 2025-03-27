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


def gen_secrets(channels: list[int]) -> bytes:
    """Generate the contents secrets file

    This will be passed to the Encoder, ectf25_design.gen_subscription, and the build
    process of the decoder

    :param channels: List of channel numbers that will be valid in this deployment.
        Channel 0 is the emergency broadcast, which will always be valid and will
        NOT be included in this list

    :returns: Contents of the secrets file
    """
    key_hex = secrets.token_hex(16)

    channels_line = "char channels["+str(len(channels))+"] = {"+str(",".join(map(str, channels)))+"};"
    
    secret_numbers = list(bytearray.fromhex(key_hex))
    secret_key_line = "uint8_t secret_key_imported[16] = {"+str(",".join(map(str, secret_numbers)))+"};"
    
    h_file_contents = channels_line + "\n"+secret_key_line

    

    python_secrets = "// {" + f'\"channels": {channels}, "aes_key":"{str(key_hex).upper()}"' + "}"

    h_file_contents += "\n"+python_secrets
    print(h_file_contents) # // {"channels": [1, 3, 4, 8], "aes_key": "1C138BBE92FB6C1A8FE4DDE7F3A92AB2"}

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
        "secrets_file",
        type=Path,
        help="Path to the secrets file",
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

    secrets_h = gen_secrets(args.channels)

    # Open the file, erroring if the file exists unless the --force arg is provided
    with open(args.secrets_file, "wb" if args.force else "xb") as f:
        # Dump the secrets to the file
        f.write(secrets_h)

    # secrets_h = gen_secrets_header(args.channels, key_hex)

    # # Open the file, erroring if the file exists unless the --force arg is provided
    # with open(str(args.secrets_folder)+"/secrets.h", "wb" if args.force else "xb") as f:
    #     # Dump the secrets to the file
    #     f.write(secrets_h)


if __name__ == "__main__":
    main()
