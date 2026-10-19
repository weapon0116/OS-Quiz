import streamlit as st
import random

# 페이지 기본 설정
st.set_page_config(page_title="천안오성고 퀴즈 부스", page_icon="🏫", layout="centered")

# ================= 문제 데이터 =================
MULTIPLE_CHOICE_POOL = [
    {
        "q": "우리 학교의 교목은?",
        "options": ["소나무", "은행나무", "단풍나무", "느티나무"],
        "answer": "은행나무",
        "desc": "천안오성고의 교목은 '은행나무'입니다."
    },
    {
        "q": "우리 학교 음악실의 개수는?",
        "options": ["1개", "2개", "3개", "4개"],
        "answer": "2개",
        "desc": "음악실은 총 2개입니다."
    },
    {
        "q": "우리 학교에 도서관이 위치한 층수는?",
        "options": ["1층", "2층", "3층", "4층"],
        "answer": "2층",
        "desc": "도서관은 본관 2층에 위치해 있습니다."
    },
    {
        "q": "우리 학교 4층에 위치한 교실은 몇 학년 교실일까?",
        "options": ["1학년", "2학년", "3학년", "동아리실"],
        "answer": "3학년",
        "desc": "4층에는 3학년 교실이 있습니다."
    },
    {
        "q": "우리 학교 보건실이 위치한 층수는?",
        "options": ["1층", "2층", "3층", "지하 1층"],
        "answer": "1층",
        "desc": "보건실은 1층에 위치해 있습니다."
    }
]

OX_POOL = [
    {
        "q": "우리 학교가 위치한 동은 성성동이다.",
        "options": ["O", "X"],
        "answer": "O",
        "desc": "정답은 O입니다. (성성동 위치)"
    },
    {
        "q": "우리 학교의 과학실은 총 5개이다.",
        "options": ["O", "X"],
        "answer": "X",
        "desc": "정답은 X입니다! (과학실은 총 4개입니다)"
    },
    {
        "q": "우리 학교의 학습카페는 총 4개이다.",
        "options": ["O", "X"],
        "answer": "X",
        "desc": "정답은 X입니다! (학습카페는 총 3개입니다)"
    },
    {
        "q": "우리 학교의 소재지는 충청남도 천안시 서북구 과수원길 27이다.",
        "options": ["O", "X"],
        "answer": "O",
        "desc": "정답은 O입니다. 도로명 주소: 과수원길 27"
    }
]

# ================= 퀴즈 초기화 함수 =================
def init_quiz():
    st.session_state.current_idx = 0
    st.session_state.score = 0
    st.session_state.show_feedback = False
    st.session_state.last_result = None

    # 선택된 모드에 따라 3문제를 랜덤 추출 (총 풀 문제 수: 3문제)
    if st.session_state.quiz_mode == "객관식 퀴즈":
        st.session_state.questions = random.sample(MULTIPLE_CHOICE_POOL, 3)
    else:
        st.session_state.questions = random.sample(OX_POOL, 3)

# ================= 사이드바: 노트북별 모드 고정 =================
st.sidebar.title("⚙️ 부스 노트북 설정")
selected_mode = st.sidebar.radio(
    "이 노트북의 퀴즈 유형을 선택하세요:",
    ["O/X 퀴즈", "객관식 퀴즈"],
    index=0
)

# 모드가 바뀌었거나 처음 실행될 때 상태 초기화
if "quiz_mode" not in st.session_state or st.session_state.quiz_mode != selected_mode:
    st.session_state.quiz_mode = selected_mode
    init_quiz()

# ================= 메인 화면 =================
st.title("🏫 학교 정보 바로 알기 퀴즈")
st.caption(f"현재 부스: **{st.session_state.quiz_mode} 모드** (총 3문제)")
st.markdown("---")

current_idx = st.session_state.current_idx
total_q = len(st.session_state.questions)

# 1. 문제 풀이 진행 중
if current_idx < total_q:
    q_data = st.session_state.questions[current_idx]
    
    st.subheader(f"Q{current_idx + 1}. {q_data['q']}")

    # 피드백이 표시되는 상태(답을 선택한 직후)
    if st.session_state.show_feedback:
        res = st.session_state.last_result
        if res["is_correct"]:
            st.success(f"⭕ **정답입니다!**\n\n💡 {res['desc']}")
        else:
            st.error(f"❌ **오답입니다!** (선택한 답: {res['selected']})\n\n💡 정답: **{res['answer']}**\n\n👉 {res['desc']}")
            
        st.write("")
        if st.button("➡️ 다음 문제로 이동", use_container_width=True, type="primary"):
            st.session_state.show_feedback = False
            st.session_state.current_idx += 1
            st.rerun()

    # 문제를 푸는 상태
    else:
        st.write("정답을 선택해주세요:")
        if st.session_state.quiz_mode == "O/X 퀴즈":
            col1, col2 = st.columns(2)
            for idx, opt in enumerate(q_data["options"]):
                btn_col = col1 if idx == 0 else col2
                if btn_col.button(opt, use_container_width=True, key=f"ox_{current_idx}_{opt}"):
                    is_correct = (opt == q_data["answer"])
                    if is_correct:
                        st.session_state.score += 1
                    st.session_state.last_result = {
                        "is_correct": is_correct,
                        "selected": opt,
                        "answer": q_data["answer"],
                        "desc": q_data["desc"]
                    }
                    st.session_state.show_feedback = True
                    st.rerun()
        else:
            for opt in q_data["options"]:
                if st.button(opt, use_container_width=True, key=f"mc_{current_idx}_{opt}"):
                    is_correct = (opt == q_data["answer"])
                    if is_correct:
                        st.session_state.score += 1
                    st.session_state.last_result = {
                        "is_correct": is_correct,
                        "selected": opt,
                        "answer": q_data["answer"],
                        "desc": q_data["desc"]
                    }
                    st.session_state.show_feedback = True
                    st.rerun()

# 2. 3문제 풀이 완료 (결과 화면)
else:
    score = st.session_state.score
    st.subheader("🎉 퀴즈 종료!")
    st.metric(label="최종 점수", value=f"{score} / 3 점")

    if score == 3:
        st.balloons()
        st.success("🏆 **만점입니다!**\n\n스태프에게 이 화면을 보여주고 **ABC 초콜릿 3개**를 받으세요! 🍫🍫🍫")
    else:
        st.info("👏 **수고하셨습니다! (참여 완료)**\n\n스태프에게 이 화면을 보여주고 **ABC 초콜릿 1개**를 받으세요! 🍫")

    st.markdown("---")
    
    # 퀴즈 종류는 유지된 채 새 문제 3개로 초기화
    if st.button("🔄 다음 학생 시작하기", use_container_width=True, type="primary"):
        init_quiz()
        st.rerun()
