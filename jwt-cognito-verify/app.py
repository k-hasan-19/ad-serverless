import os
import json
import time
import urllib.request
from jose import jwk, jwt
from jose.utils import base64url_decode

region = os.getenv("AWS_REGION")
userpool_id = os.getenv("USER_POOL_ID")
app_client_id = os.getenv("APP_CLIENT_ID")
keys_url = "https://cognito-idp.{}.amazonaws.com/{}/.well-known/jwks.json".format(
    region, userpool_id
)
# instead of re-downloading the public keys every time
# we download them only on cold start
# https://aws.amazon.com/blogs/compute/container-reuse-in-lambda/
with urllib.request.urlopen(keys_url) as f:
    response = f.read()
keys = json.loads(response.decode("utf-8"))["keys"]


def lambda_handler(event, context):
    token = event["token"]
    # get the kid from the headers prior to verification
    headers = jwt.get_unverified_headers(token)
    kid = headers["kid"]
    # search for the kid in the downloaded public keys
    key_index = -1
    for i in range(len(keys)):
        if kid == keys[i]["kid"]:
            key_index = i
            break
    if key_index == -1:
        print("Public key not found in jwks.json")
        return False
    # construct the public key
    public_key = jwk.construct(keys[key_index])
    # get the last two sections of the token,
    # message and signature (encoded in base64)
    message, encoded_signature = str(token).rsplit(".", 1)
    # decode the signature
    decoded_signature = base64url_decode(encoded_signature.encode("utf-8"))
    # verify the signature
    if not public_key.verify(message.encode("utf8"), decoded_signature):
        print("Signature verification failed")
        return False
    print("Signature successfully verified")
    # since we passed the verification, we can now safely
    # use the unverified claims
    claims = jwt.get_unverified_claims(token)
    # additionally we can verify the token expiration
    if time.time() > claims["exp"]:
        print("Token is expired")
        return False
    # and the Audience  (use claims['client_id'] if verifying an access token)
    if claims["aud"] != app_client_id:
        print("Token was not issued for this audience")
        return False
    # now we can use the claims
    print(claims)
    return claims


# the following is useful to make this script executable in both
# AWS Lambda and any other local environments
if __name__ == "__main__":
    # for testing locally you can enter the JWT ID Token here
    event = {"Token": ""}
    lambda_handler(event, None)
