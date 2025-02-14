from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from PIL import Image
import base64
import os


def generate_profile(
    name, student_major, team, photo_path, introduction, output_image_path
):
    # 이미지를 base64로 변환
    photo_tag = "<p>[Photo not available]</p>"
    if photo_path:
        base64_photo = image_to_base64(photo_path)
        photo_tag = f'<img src="data:image/jpeg;base64,{base64_photo}" alt="Profile Photo" class="profileImg" />'
    # HTML content with embedded CSS for the layout
    div_content = f"""
    <link href="https://fonts.googleapis.com/css2?family=Do+Hyeon&family=IBM+Plex+Sans+KR:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        body {{
            margin: 0;
            font-family: 'Jua', "Arial", sans-serif;  /* 한글 폰트 지정 */
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            background-color: white;
        }}
        .card {{
            font-family: Arial, sans-serif;
            width: 1920px;
            height: 1080px;
            display: flex;
            box-sizing: border-box;
            color: black;
        }}
        .photo-container {{
            flex: 1.5;
            display: flex;
            width: 40%;
            justify-content: center;
            align-items: center;
            height: 100%;
        }}
        .profileImg {{
            width: 100%;
            height: 100%;
            object-fit: cover;
        }}
        .content {{
            flex: 2;
            padding: 20px;
            display: flex;
            color: black;
            flex-direction: column;
            padding-top: 150px;
            padding-left: 100px;
            justify-content: top;
        }}
        .content h1 {{
            margin-bottom: 20px;
            font-size: 80px;
        }}
        .name {{
            font-size: 180px;
            margin: 0;
            font-family: "IBM Plex Sans KR", serif;
            font-weight: 700;
            font-style: normal;
            padding-left: 30px;
        }}
        .major {{
            font-size: 90px;
            margin: 0;
            font-family: "IBM Plex Sans KR", serif;
            font-weight: 600;
            padding-left: 30px;
        }}
        .intr {{
            font-size: 60px;
            margin: 0;
            font-family: "IBM Plex Sans KR", serif;
            font-weight: 400;
            padding-top: 30px;
            padding-left: 30px;
            word-wrap: break-word;
        }}
    </style>
    <div class="card">
        <div class="photo-container">
            {photo_tag}
        </div>
        <div class="content">
            <p class="name"><strong>{name}</strong></p>
            <p class="major"><strong>{team}팀/{student_major}</strong></p>
            <p class="intr">{introduction}</p>
        </div>
    </div>
    """

    # Selenium 설정
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # 헤드리스 모드
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=chrome_options
    )

    # HTML 파일 생성 및 로드
    with open("temp.html", "w", encoding="utf-8") as f:
        f.write(div_content)

    driver.get("file://" + os.path.abspath("temp.html"))
    driver.set_window_size(1920, 1080)  # 원하는 크기로 설정

    # 스크린샷 찍기
    driver.save_screenshot(output_image_path)

    driver.quit()
    os.remove("temp.html")  # 임시 HTML 파일 삭제

    print(f"Profile card saved as image: {output_image_path}")


def image_to_base64(image_path):
    """
    Converts an image file to base64 string.
    """
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")


# 과제--------------------------------------------------------------------------------
# 과제-1:팀 이름 입력(농구/야구/축구/E-Sports 중 적어주세요)
team = "축구"

# 과제-2:본인을 나타내는 사진을 !반드시! 동일 폴더 안에 넣고 아래에 옳은 파일명을 입력해주세요
photo_path = "image.jpg"

# 과제-3 한 줄 이내의 짧은 소개글을 써주세요
introduction = "모든 스포츠를 다 보는 축구팀 새내기 박성민입니다!"
# 이후 실행하고
# 터미널에 입력할 User inputs(이름, 전공)
name = input("Enter your name: ")
student_major = input("Enter your major: ")

# Generate and save profile as an image
generate_profile(
    name,
    student_major,
    team,
    photo_path,
    introduction,
    output_image_path=name + "_profile.png",
)


