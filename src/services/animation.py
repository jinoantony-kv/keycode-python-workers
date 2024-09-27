import requests
import os
import time

token = None
token_expiration = 0

def get_bearer_token():
        client_id = os.getenv("IMMERSITY_AI_CLIENT_ID")
        client_secret = os.getenv("IMMERSITY_AI_CLIENT_SECRET")

        try:
            
            url = "https://auth.immersity.ai/auth/realms/immersity/protocol/openid-connect/token"

            payload = {
                "grant_type": "client_credentials",
                "client_id": client_id,
                "client_secret": client_secret
                }
            headers = {
                "accept": "application/json",
                "content-type": "application/x-www-form-urlencoded"
                }

            response = requests.post(url, data=payload, headers=headers)
            token_data = response.json()
            token = token_data.get("access_token")
            # Set the token expiration time
            token_expiration = time.time() + token_data.get("expires_in") 
            print(token)
            return token

        except requests.exceptions.RequestException as e:
            print(f"Error fetching token: {str(e)}")
            return None

def get_token():
        if token is None or time.time() >= token_expiration - 60:  # Refresh if less than 60 seconds left
            return get_bearer_token()
        return token

def animate_image(data):
    ANIMATION_API_URL = "https://api.immersity.ai/api/v1/animation"
    DISPARITY_MAP_API_URL = "https://api.immersity.ai/api/v1/disparity"
    image_url_list = data.get("image-urls", [])
    animation_urls = []
    try:
        for image_url in image_url_list:
            print("in loop")
            headers = {
                "accept": "application/json",
                "content-type": "application/json",
                "authorization": f"Bearer {get_bearer_token()}"
            }

            # Prepare the disparity payload
            disparity_payload = {"inputImageUrl": image_url,
                                "inputType": "image2d",
                                "outputBitDepth": "uint16",
                                "dilation": 0.0063,}

            # Send the request for disparity map
            disparity_response = requests.post(DISPARITY_MAP_API_URL, json=disparity_payload, headers=headers)
            disparity_response.raise_for_status()
            disparity_result = disparity_response.json()        

            # Prepare the animation payload
            animation_payload = {
                "inputImageUrl": image_url,
                "inputDisparityUrl": disparity_result.get("resultPresignedUrl"),
                "resultPresignedUrl": "https://100units-multi-media-assets.s3.amazonaws.com/videos/uploads/immercity_1.mp4?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAV3LJZRBIB5JTGU7B%2F20240927%2Fap-south-1%2Fs3%2Faws4_request&X-Amz-Date=20240927T152519Z&X-Amz-Expires=36000&X-Amz-SignedHeaders=host&X-Amz-Signature=333ec905c1a5a2994d8df5001425a235079b3dc0e99b4a346a5186cafac323b6",
                "animationLength": 10
            }

            # Send the request for animation
            animation_response = requests.post(ANIMATION_API_URL, json=animation_payload, headers=headers)
            animation_response.raise_for_status()
            animation_result = animation_response.json()

            # Collect the animation URL
            animation_urls.append(animation_result.get("resultPresignedUrl"))

    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

    return animation_urls

if __name__ == "__main__":
    animate_image({
        "image-urls": ["https://leia-storage-service-production.s3.us-east-1.amazonaws.com/timed/D001/534e39bb-8e77-45b3-b881-ad8640785bfa/e5e3d5a3-a35d-4c2f-9f9e-5324f5f402ec/625a4b19-2e6a-4c46-bf6d-7d96b7e083fa?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=AKIASC7ECGJVHARKLZ6E%2F20240927%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20240927T042407Z&X-Amz-Expires=86400&X-Amz-Signature=6fcd50c4a1d46be2bb5b90da76f4bc6af319aa93907374154934fcfac850dd03&X-Amz-SignedHeaders=host&x-id=PutObject"]
    })
