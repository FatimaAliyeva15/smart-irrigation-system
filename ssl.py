import urequests

url = "https://192.168.0.140:5000"
headers = {"Authorization": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2N2ZkZmZmYmYwOTZiMzY1N2VlNzZlNzAiLCJ1c2VybmFtZSI6ImZhdGltYTEyMyIsInJvbGUiOiJhZG1pbiIsImlhdCI6MTc0NzgxMTA1MiwiZXhwIjoxNzQ3ODE0NjUyfQ.cOSdhWDOmhkgSIkJxTSP6b-X16Z8U7E9D8Y_v1NgwwQ"}

response = urequests.get(url, headers=headers)
print(response.text)
response.close()
