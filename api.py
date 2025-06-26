from fastapi import FastAPI
from fastapi.responses import FileResponse
from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper
from bidi.algorithm import get_display
from datetime import datetime
import jdatetime #Required for Jalali date or the so called persian date

app = FastAPI()

def crocctTextFa(text):
    reshaped_text = arabic_reshaper.reshape(text)  
    bidi_text = get_display(reshaped_text) 
    return bidi_text  

@app.get("/generate-image")
def generate_image():
    # Get's date
    now_gregorian = datetime.now()
    gregorian_year = now_gregorian.year
    gregorian_month = now_gregorian.strftime("%b")  # Jan, Feb, ...
    gregorian_day = now_gregorian.day
    weekday_en = now_gregorian.strftime("%A")

    # Get's persian date (Jalali date)
    now_jalali = jdatetime.date.today()
    persian_year = str(now_jalali.year)
    persian_month = now_jalali.j_months_fa[now_jalali.month - 1]
    persian_day = str(now_jalali.day)
    weekday_fa = now_jalali.strftime("%A")

    match weekday_fa:
        case "Saturday":
            weekday_fa = "شنبه"

        case "Sunday":
            weekday_fa = "یکشنبه"

        case "Monday":
            weekday_fa = "دوشنبه"
    
        case "Tuesday":
            weekday_fa = "سه شنبه"

        case "Wednesday":
            weekday_fa = "چهارشنبه"

        case "Thursday":
            weekday_fa = "پنجشنبه"

        case "Friday":
            weekday_fa = "جمعه"
    # Set's the Image.png which can be replaced, for background 
    background = Image.open("image.jpg")
    draw = ImageDraw.Draw(background)

    # Setting Fonts
    font_title = ImageFont.truetype("B Titr Bold_0.ttf", 38)
    font_textFa = ImageFont.truetype("B Titr Bold_0.ttf", 38)
    font_textEn = ImageFont.truetype("Anton-Regular.ttf", 38)

    def crocctTextFa(text):
        reshaped_text = arabic_reshaper.reshape(text)  
        bidi_text = get_display(reshaped_text) 
        return bidi_text
    print(crocctTextFa(weekday_fa))
    # Writing on the background on the given coordination
    draw.text((375, 120), persian_year, font=font_title, fill=(223, 194, 102))
    draw.text((120, 155), crocctTextFa(persian_month), font=font_title, fill=(223, 194, 102))
    draw.text((225, 165), persian_day, font=font_title, fill=(0, 0, 0))
    draw.text((355, 165), crocctTextFa(weekday_fa), font=font_title, fill=(0, 0, 0))
    draw.text((205, 220), str(gregorian_day), font=font_textEn, fill=(0, 0, 0))
    draw.text((115, 215), gregorian_month, font=font_textEn, fill=(223, 194, 102))
    draw.text((275, 220), weekday_en, font=font_textEn, fill=(0, 0, 0))
    draw.text((375, 270), str(gregorian_year), font=font_textEn, fill=(223, 194, 102))

    output_path = "output.webp"
    background.save(output_path)

    return FileResponse(output_path, media_type="image/webp", filename="output.webp")
# This is for making sure that the bot gives an output. The output will pop up in the etc/n8n/bot a file named output.webp
generate_image()