import requests
import json

REST_API_KEY = "412149e33d726f187da21d36c76d55cf"

# 방금 보내주신 최신 인증 코드
AUTHORIZATION_CODE = "F5Pm3TuKn_f27Ssi-5dEWYnvKwfIzchIViiIrLROO4L9VU04R3oYDgAAAAQKFwAnAAABn83Us0eYFzyUYZmfhQ"

url = "https://kauth.kakao.com/oauth/token"
data = {
    "grant_type": "authorization_code",
    "client_id": REST_API_KEY,
    "redirect_uri": "http://localhost:3000",
    "code": AUTHORIZATION_CODE
}

response = requests.post(url, data=data)
tokens = response.json()

print("카카오 응답 결과:", tokens)

if "access_token" in tokens:
    with open("kakao_code.json", "w") as fp:
        json.dump(tokens, fp)
    print("\n🎉 kakao_code.json 파일이 성공적으로 생성되었습니다!")
else:
    print("\n❌ 토큰 발급 실패! 위 응답 메시지를 확인해 주세요.")