import pyttsx3
# TTS 엔진 초기화
engine = pyttsx3.init()

# 말하는 속도
engine.setProperty('rate', 180)
rate = engine.getProperty('rate')

# 소리 크기
engine.setProperty('volume', 0.5) # 0~1 
volume = engine.getProperty('volume')

# 목소리
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id) # 남성
#engine.setProperty('voice', voices[1].id) # 여성

# 말하기
engine.say("안녕하세요.") 
engine.runAndWait() # 말 다할때까지 대기
engine.stop() # 끝