import streamlit as st

# 페이지 기본 설정
st.set_page_config(page_title="천안오성고 퀴즈", page_icon="🏫", layout="centered")

# 세션 상태 초기화 (문제 단계, 점수 관리)
if "step" not in st.session_state:
    st.session_state.step = 1
    st.session_state.score = 0

# 퀴즈 데이터 (문제, 보기, 정답, 해설)
QUIZ_DATA = [
    {
        "num": 1,
        "type": "ox",
        "question": "Q1. 우리 학교의 개교기념일은 5월 1일이다?",
        "options": ["O", "X"],
        "answer": "O",
        "desc": "천안오성고의 개교기념일은 5월 1일입니다."
    },
    {
        "num": 2,
        "type": "choice",
        "question": "Q2. 우리 학교의 교훈으로 올바른 것은?",
        "options": ["성실, 창의, 봉사", "바른 생각, 바른 행동", "지혜롭고 건강하게", "자율, 정직, 근면"],
        "answer": "성실, 창의, 봉사",
        "desc": "교훈은 '성실, 창의, 봉사'입니다."
    },
    {
        "num": 3,
        "type": "ox",
        "question": "Q3. 부스 2의 주제는 '게시판 활성화 정책'이다?",
        "options": ["O", "X"],
        "answer": "O",
        "desc": "부스 2에 포스트잇으로 여러분의 아이디어를 남겨주세요!"
    }
]

# 제목
st.title("🏫 천안오성고 학교 정보 퀴즈")
st.markdown("---")

# 진행 단계별 화면 표시
current_step = st.session_state.step

if current_step <= len(QUIZ_DATA):
    quiz = QUIZ_DATA[current_step - 1]
    
    # 상단 진행도 표시
    st.caption(f"진행 상황: {current_step} / {len(QUIZ_DATA)}")
    st.subheader(quiz["question"])
    
    # 보기 버튼 생성 (O/X는 가로 배치, 객관식은 세로 배치)
    if quiz["type"] == "ox":
        col1, col2 = st.columns(2)
        for i, opt in enumerate(quiz["options"]):
            col = col1 if i == 0 else col2
            if col.button(opt, use_container_width=True, key=f"btn_{current_step}_{opt}"):
                if opt == quiz["answer"]:
                    st.session_state.score += 1
                st.session_state.step += 1
                st.rerun()
    else:
        for opt in quiz["options"]:
            if st.button(opt, use_container_width=True, key=f"btn_{current_step}_{opt}"):
                if opt == quiz["answer"]:
                    st.session_state.score += 1
                st.session_state.step += 1
                st.rerun()

else:
    # 퀴즈 종료 & 결과 화면
    score = st.session_state.score
    st.balloons() if score == 3 else None
    
    st.subheader("🎉 퀴즈 완료!")
    st.metric(label="내 점수", value=f"{score} / 3 점")
    
    if score == 3:
        st.success("✨ **만점입니다!** 스태프에게 화면을 보여주고 **ABC초콜릿 3개**를 받으세요! 🍫🍫🍫")
    else:
        st.info("👍 **참여 완료!** 스태프에게 화면을 보여주고 **ABC초콜릿 1개**를 받으세요! 🍫")
    
    st.markdown("---")
    # 다음 참여자를 위한 초기화 버튼
    if st.button("🔄 다음 학생 퀴즈 풀기", use_container_width=True, type="primary"):
        st.session_state.step = 1
        st.session_state.score = 0
        st.rerun()
