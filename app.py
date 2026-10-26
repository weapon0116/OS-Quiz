import streamlit as st
import random
import os

st.set_page_config(page_title="천안오성고 바로 알기 퀴즈", page_icon="🏫", layout="centered")

# ================= 토스(Toss) 스타일 글로벌 커스텀 CSS =================
st.markdown("""
<style>
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');

    /* 전체 배경 및 폰트 */
    html, body, [class*="css"] {
        font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif !important;
        background-color: #F9FAFB !important;
        color: #191F28 !important;
    }

    /* 불필요한 기본 푸터/메뉴만 숨기고 사이드바 토글 버튼은 살림 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* 좌우 너비 대폭 확장 (노트북 화면 최적화: 860px) */
    .block-container {
        padding-top: 2.5rem !important;
        padding-bottom: 4rem !important;
        max-width: 860px !important;
    }

    /* 토스 스타일 화이트 카드 */
    .toss-card {
        background: #FFFFFF;
        border-radius: 28px;
        padding: 36px 36px;
        box-shadow: 0 4px 24px rgba(0, 0, 0, 0.04);
        margin-bottom: 24px;
        border: 1px solid #F2F4F6;
    }

    /* 토스 뱃지 */
    .toss-badge {
        display: inline-block;
        background: #E8F3FF;
        color: #1B64DA;
        font-size: 14px;
        font-weight: 700;
        padding: 6px 14px;
        border-radius: 100px;
        margin-bottom: 16px;
    }

    /* 문제 제목 스타일 (시원하게 크기 확대) */
    .toss-title {
        font-size: 26px;
        font-weight: 800;
        color: #191F28;
        line-height: 1.5;
        margin-bottom: 12px;
        word-break: keep-all;
    }

    /* 진행도 바 (Step Bar) */
    .progress-bar-bg {
        width: 100%;
        height: 8px;
        background-color: #E5E8EB;
        border-radius: 100px;
        margin-bottom: 28px;
        overflow: hidden;
    }
    .progress-bar-fill {
        height: 100%;
        background-color: #3182F6;
        border-radius: 100px;
        transition: width 0.3s ease;
    }

    /* 버튼 공통 토스 스타일 (크기 확대 & 클릭감 향상) */
    .stButton > button {
        border-radius: 18px !important;
        font-size: 18px !important;
        font-weight: 700 !important;
        padding: 16px 24px !important;
        background-color: #FFFFFF !important;
        color: #333D4B !important;
        border: 1.5px solid #E5E8EB !important;
        box-shadow: 0 2px 10px rgba(0,0,0,0.02) !important;
        transition: all 0.15s ease-in-out !important;
    }
    .stButton > button:hover {
        border-color: #3182F6 !important;
        color: #3182F6 !important;
        background-color: #F8FAFF !important;
        transform: translateY(-2px);
    }
    .stButton > button:active {
        transform: scale(0.99);
    }

    /* 강조 버튼 (Primary) */
    .stButton > button[kind="primary"] {
        background-color: #3182F6 !important;
        color: #FFFFFF !important;
        border: none !important;
        box-shadow: 0 4px 14px rgba(49, 130, 246, 0.28) !important;
    }
    .stButton > button[kind="primary"]:hover {
        background-color: #1B64DA !important;
        color: #FFFFFF !important;
    }

    /* 텍스트 입력창 */
    .stTextInput input {
        border-radius: 16px !important;
        border: 1.5px solid #E5E8EB !important;
        padding: 16px 20px !important;
        font-size: 18px !important;
        background-color: #F9FAFB !important;
    }
    .stTextInput input:focus {
        border-color: #3182F6 !important;
        background-color: #FFFFFF !important;
    }
</style>
""", unsafe_allow_html=True)

# ================= 전체 퀴즈 데이터베이스 (기존 내용 100% 유지) =================
ALL_QUIZZES = [
    # [O/X 퀴즈]
    {
        "id": "OX-1",
        "category": "O/X",
        "q": "우리 학교에는 풋살장이 있다.",
        "type": "ox",
        "options": ["O", "X"],
        "answer": "O",
        "desc": "정답은 O입니다! 학교 뒤편 옆에 풋살장이 위치해 있습니다."
    },
    {
        "id": "OX-2",
        "category": "O/X",
        "q": "우리 학교 2026학년도 겨울방학식은 1월 9일이다.",
        "type": "ox",
        "options": ["O", "X"],
        "answer": "X",
        "desc": "정답은 X입니다! 겨울방학식은 1월 8일입니다."
    },
    {
        "id": "OX-3",
        "category": "O/X",
        "q": "우리 학교 전교생의 수는 2026년 기준 1300명 이상이다.",
        "type": "ox",
        "options": ["O", "X"],
        "answer": "X",
        "desc": "정답은 X입니다! 2026년 기준 전교생 수는 1,267명입니다."
    },
    {
        "id": "OX-4",
        "category": "O/X",
        "q": "우리 학교의 교훈은 ‘큰 꿈, 밝은 마음, 높은 지성’이다.",
        "type": "ox",
        "options": ["O", "X"],
        "answer": "O",
        "desc": "정답은 O입니다! 교훈은 '큰 꿈, 밝은 마음, 높은 지성'입니다."
    },
    {
        "id": "OX-5",
        "category": "O/X",
        "q": "우리 학교의 교화는 영산홍이다.",
        "type": "ox",
        "options": ["O", "X"],
        "answer": "O",
        "desc": "정답은 O입니다! 천안오성고의 교화는 영산홍입니다."
    },
    {
        "id": "OX-6",
        "category": "O/X",
        "q": "우리 학교의 비전은 ‘배움과 성장으로 큰 꿈 열어가는 행복한 학교‘이다.",
        "type": "ox",
        "options": ["O", "X"],
        "answer": "O",
        "desc": "정답은 O입니다!"
    },
    {
        "id": "OX-7",
        "category": "O/X",
        "q": "우리 학교가 위치한 동은 성성동이다.",
        "type": "ox",
        "options": ["O", "X"],
        "answer": "O",
        "desc": "정답은 O입니다! 성성동에 위치하고 있습니다."
    },
    {
        "id": "OX-8",
        "category": "O/X",
        "q": "우리 학교의 과학실은 총 5개이다.",
        "type": "ox",
        "options": ["O", "X"],
        "answer": "X",
        "desc": "정답은 X입니다! 5층에 위치한 화학실, 생명과학실, 지구과학실, 물리실 총 4개입니다."
    },
    {
        "id": "OX-9",
        "category": "O/X",
        "q": "우리 학교의 학습카페는 총 4개이다.",
        "type": "ox",
        "options": ["O", "X"],
        "answer": "X",
        "desc": "정답은 X입니다! 배치도 기준 2층(D204), 4층(D405), 5층(D503) 총 3개입니다."
    },
    {
        "id": "OX-10",
        "category": "O/X",
        "q": "우리 학교의 소재지는 충청남도 천안시 서북구 과수원길 27이다.",
        "type": "ox",
        "options": ["O", "X"],
        "answer": "O",
        "desc": "정답은 O입니다! 주소: 충청남도 천안시 서북구 과수원길 27"
    },
    {
        "id": "OX-11",
        "category": "O/X",
        "q": "2026년 기준 우리 학교 선생님은 100분이 넘는다.",
        "type": "ox",
        "options": ["O", "X"],
        "answer": "X",
        "desc": "정답은 X입니다! 총 92분입니다."
    },

    # [객관식 / 사진 퀴즈]
    {
        "id": "CHOICE-1",
        "category": "객관식",
        "q": "우리 학교는 AI 중점학교일까요, 과학 중점학교일까요?",
        "type": "choice",
        "options": ["AI 중점", "과학 중점"],
        "answer": "AI 중점",
        "desc": "천안오성고등학교는 'AI 중점' 학교입니다."
    },
    {
        "id": "CHOICE-2",
        "category": "객관식",
        "q": "우리 학교 매점의 운영 시간은 언제일까요?",
        "type": "choice",
        "options": [
            "하루 종일 운영",
            "2교시 쉬는시간부터 4교시 쉬는시간까지",
            "3교시 쉬는시간부터 4교시 쉬는시간까지",
            "방과 후에만 운영"
        ],
        "answer": "2교시 쉬는시간부터 4교시 쉬는시간까지",
        "desc": "매점은 2교시 쉬는시간부터 4교시 쉬는시간까지만 운영됩니다!"
    },
    {
        "id": "CHOICE-3",
        "category": "객관식(사진)",
        "q": "다음 중 천안오성고의 '진짜 로고'는 어느 것일까요?",
        "type": "choice",
        "image_type": "logo",
        "options": ["1번", "2번"],
        "answer": "1번",
        "desc": "진짜 로고는 은행잎 줄기 아래에 '빨간색 점'이 있습니다!"
    },
    {
        "id": "CHOICE-4",
        "category": "객관식(사진)",
        "q": "우리 학교 마스코트인 이 친구의 이름은 무엇일까요?",
        "type": "choice",
        "image_type": "obyeol",
        "options": ["오성이", "오별이", "오돌이"],
        "answer": "오별이",
        "desc": "우리 학교 대표 캐릭터의 이름은 '오별이'입니다!"
    },

    # --- 배치도 문제 4종 (이미지 연동) ---
    {
        "id": "CHOICE-5",
        "category": "객관식(배치도)",
        "q": "[배치도 퀴즈] 우리학교 로고로 표시되어 있는 3층 D305호에 위치하는 이곳은 어디일까요?",
        "type": "choice",
        "image_path": "images/floor_map_store.png",
        "options": ["매점", "교무센터1", "성적관리실"],
        "answer": "매점",
        "desc": "3층 D305호는 '매점'입니다."
    },
    {
        "id": "CHOICE-6",
        "category": "객관식(배치도)",
        "q": "[배치도 퀴즈] 우리학교 로고로 표시되어 있는 각 층 복도마다 학생들이 모여 쉴 수 있게 마련된 열린 공간의 명칭은?",
        "type": "choice",
        "image_path": "images/floor_map_homebase.png",
        "options": ["홈베이스", "홈그라운드", "센트럴홈"],
        "answer": "홈베이스",
        "desc": "배치도 곳곳에 위치한 학생 쉼터는 '홈베이스'입니다."
    },
    {
        "id": "CHOICE-7",
        "category": "객관식(배치도)",
        "q": "[배치도 퀴즈] 우리학교 로고로 표시되어 있는 3층 D310호에 위치한 교실의 올바른 명칭은?",
        "type": "choice",
        "image_path": "images/floor_map_ai.png",
        "options": ["AI 실습실", "AI 융합실", "AI 학습실"],
        "answer": "AI 실습실",
        "desc": "3층 동편 끝 D310호는 'AI 실습실'입니다."
    },
    {
        "id": "CHOICE-8",
        "category": "객관식(배치도)",
        "q": "[배치도 퀴즈] 우리학교 로고로 표시되어 있는 2층 D209호에 위치한 교실의 올바른 명칭은?",
        "type": "choice",
        "image_path": "images/floor_map_bigdata.png",
        "options": ["빅데이터 분석실", "빅데이터 활용실", "빅데이터 실습실"],
        "answer": "빅데이터 분석실",
        "desc": "2층 동편 끝 D209호는 '빅데이터 분석실'입니다."
    },

    # [단답형 퀴즈]
    {
        "id": "SHORT-1",
        "category": "단답형",
        "q": "우리 학교의 학급 수는 총 몇 개일까요? (숫자만 입력)",
        "type": "short",
        "answer": ["37", "37개"],
        "desc": "1학년 13학급, 2학년 12학급, 3학년 12학급으로 총 37개입니다."
    },
    {
        "id": "SHORT-2",
        "category": "단답형",
        "q": "우리 학교의 PBL실은 총 몇 개일까요? (숫자만 입력)",
        "type": "short",
        "answer": ["8", "8개"],
        "desc": "배치도 기준 5층 PBL8, 4층 PBL6·7, 3층 PBL5, 2층 PBL4 등 총 8개입니다."
    },
    {
        "id": "SHORT-3",
        "category": "단답형",
        "q": "우리 학교 교장 선생님의 성함은 무엇일까요?",
        "type": "short",
        "answer": ["윤상진", "윤상진선생님", "윤상진교장선생님"],
        "desc": "교장 선생님 성함은 '윤상진' 선생님이십니다."
    },
    {
        "id": "SHORT-4",
        "category": "단답형",
        "q": "우리 학교의 교목은 무엇일까요?",
        "type": "short",
        "answer": ["은행나무"],
        "desc": "천안오성고의 교목은 '은행나무'입니다."
    },
    {
        "id": "SHORT-5",
        "category": "단답형",
        "q": "우리 학교 음악실의 개수는 총 몇 개일까요? (숫자만 입력)",
        "type": "short",
        "answer": ["2", "2개"],
        "desc": "4층 음악실2(D410), 5층 음악실1(D508)로 총 2개입니다."
    },
    {
        "id": "SHORT-6",
        "category": "단답형",
        "q": "우리 학교 도서관(정보자료실)이 위치한 층수는 몇 층일까요? (숫자만 입력)",
        "type": "short",
        "answer": ["2", "2층"],
        "desc": "정보자료실(도서관)은 2층 중앙 D207호에 있습니다."
    },
    {
        "id": "SHORT-7",
        "category": "단답형",
        "q": "우리 학교 4층에 위치한 일반 교실들은 몇 학년 교실일까요? (숫자만 입력)",
        "type": "short",
        "answer": ["3", "3학년"],
        "desc": "2층은 1학년, 3층은 2학년, 4층은 3학년 교실입니다."
    },
    {
        "id": "SHORT-8",
        "category": "단답형",
        "q": "우리 학교 보건실이 위치한 층수는 몇 층일까요? (숫자만 입력)",
        "type": "short",
        "answer": ["1", "1층"],
        "desc": "보건실은 본관 1층에 위치해 있습니다."
    }
]

# ================= 퀴즈 초기화 =================
def init_game():
    st.session_state.current_idx = 0
    st.session_state.score = 0
    st.session_state.show_feedback = False
    st.session_state.last_result = None
    st.session_state.game_questions = random.sample(ALL_QUIZZES, 3)

if "game_questions" not in st.session_state:
    init_game()

# ================= 사이드바: 관리자/개발자 모드 복구 =================
with st.sidebar:
    st.title("🛠️ 관리자 패널")
    dev_mode = st.checkbox("개발자 모드 (문제 검수용)", value=False)

    if dev_mode:
        st.markdown("---")
        st.subheader("🔍 특정 퀴즈 미리보기")
        quiz_titles = [f"[{q['category']}] {q['q'][:18]}..." for q in ALL_QUIZZES]
        selected_idx = st.selectbox("검수할 문제를 선택하세요:", range(len(ALL_QUIZZES)), format_func=lambda x: quiz_titles[x])
        target_q = ALL_QUIZZES[selected_idx]
        
        st.write(f"**ID:** `{target_q['id']}`")
        st.write(f"**정답:** `{target_q['answer']}`")
        st.caption(f"**해설:** {target_q['desc']}")
        
        if st.button("👉 메인에서 테스트", use_container_width=True):
            st.session_state.game_questions = [target_q]
            st.session_state.current_idx = 0
            st.session_state.score = 0
            st.session_state.show_feedback = False
            st.rerun()

        if st.button("🔄 일반 3문제 모드로 복귀", use_container_width=True):
            init_game()
            st.rerun()

# ================= 메인 헤더 =================
st.markdown("""
    <div style="margin-bottom: 24px;">
        <span style="font-size: 14px; font-weight: 700; color: #8B95A1;">천안오성고 캠페인</span>
        <h1 style="font-size: 30px; font-weight: 800; color: #191F28; margin: 4px 0 0 0;">학교 정보 바로 알기</h1>
    </div>
""", unsafe_allow_html=True)

current_idx = st.session_state.current_idx
total_q = len(st.session_state.game_questions)

# 1. 문제 풀이 진행 화면
if current_idx < total_q:
    q_data = st.session_state.game_questions[current_idx]
    progress_percent = int(((current_idx + (1 if st.session_state.show_feedback else 0.5)) / total_q) * 100)

    # 토스형 상단 프로그레스 바
    st.markdown(f"""
        <div class="progress-bar-bg">
            <div class="progress-bar-fill" style="width: {progress_percent}%;"></div>
        </div>
    """, unsafe_allow_html=True)

    # 토스 메인 카드 래퍼 시작
    st.markdown(f"""
        <div class="toss-card">
            <span class="toss-badge">{q_data['category']} · 문제 {current_idx + 1}</span>
            <div class="toss-title">{q_data['q']}</div>
    """, unsafe_allow_html=True)

    # 1) 로고 비교 사진
    if q_data.get("image_type") == "logo":
        col1, col2 = st.columns(2)
        with col1:
            if os.path.exists("images/logo_red.png"):
                st.image("images/logo_red.png", caption="1번 로고", use_container_width=True)
        with col2:
            if os.path.exists("images/logo_purple.png"):
                st.image("images/logo_purple.png", caption="2번 로고", use_container_width=True)

    # 2) 오별이 캐릭터 사진
    elif q_data.get("image_type") == "obyeol":
        if os.path.exists("images/obyeol.png"):
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.image("images/obyeol.png", caption="이 친구의 이름은?", use_container_width=True)

    # 3) 배치도 퀴즈 사진
    elif "image_path" in q_data:
        img_path = q_data["image_path"]
        if os.path.exists(img_path):
            st.image(img_path, caption="[참고] 2026 천안오성고 배치도", use_container_width=True)

    # 1-1. 정답 피드백 상태
    if st.session_state.show_feedback:
        res = st.session_state.last_result
        if res["is_correct"]:
            st.markdown(f"""
                <div style="background-color: #E8F9EE; border-radius: 20px; padding: 24px; margin: 20px 0;">
                    <div style="font-size: 20px; font-weight: 800; color: #059669; margin-bottom: 8px;">🎉 정답이에요!</div>
                    <div style="font-size: 16px; color: #374151; line-height: 1.6;">{res['desc']}</div>
                </div>
            """, unsafe_allow_html=True)
        else:
            ans_display = res['answer'] if isinstance(res['answer'], str) else res['answer'][0]
            st.markdown(f"""
                <div style="background-color: #FEECEE; border-radius: 20px; padding: 24px; margin: 20px 0;">
                    <div style="font-size: 20px; font-weight: 800; color: #E11D48; margin-bottom: 8px;">아쉬워요, 정답이 아니에요</div>
                    <div style="font-size: 16px; color: #374151; margin-bottom: 8px;">선택한 답: <strong>{res['user_input']}</strong></div>
                    <div style="font-size: 16px; font-weight: 700; color: #111827;">👉 올바른 정답: {ans_display}</div>
                    <div style="font-size: 15px; color: #4B5563; margin-top: 8px; line-height: 1.6;">{res['desc']}</div>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True) # 카드 닫기
        
        if st.button("다음으로", use_container_width=True, type="primary"):
            st.session_state.show_feedback = False
            st.session_state.current_idx += 1
            st.rerun()

    # 1-2. 답안 선택/입력 상태
    else:
        st.markdown("</div>", unsafe_allow_html=True) # 카드 닫기

        # 단답형
        if q_data["type"] == "short":
            with st.form(key=f"short_form_{current_idx}"):
                user_val = st.text_input("정답 입력", placeholder="정답을 입력해주세요", label_visibility="collapsed")
                submit = st.form_submit_button("확인", use_container_width=True, type="primary")
                
                if submit:
                    clean_input = user_val.replace(" ", "").strip()
                    if clean_input == "":
                        st.warning("정답을 입력해주세요!")
                    else:
                        is_correct = any(clean_input == str(a).replace(" ", "").strip() for a in (q_data["answer"] if isinstance(q_data["answer"], list) else [q_data["answer"]]))
                        if is_correct:
                            st.session_state.score += 1
                        st.session_state.last_result = {
                            "is_correct": is_correct,
                            "user_input": user_val,
                            "answer": q_data["answer"],
                            "desc": q_data["desc"]
                        }
                        st.session_state.show_feedback = True
                        st.rerun()

        # O/X 형
        elif q_data["type"] == "ox":
            col1, col2 = st.columns(2)
            for idx, opt in enumerate(q_data["options"]):
                btn_col = col1 if idx == 0 else col2
                if btn_col.button(opt, use_container_width=True, key=f"ox_{current_idx}_{opt}"):
                    is_correct = (opt == q_data["answer"])
                    if is_correct:
                        st.session_state.score += 1
                    st.session_state.last_result = {
                        "is_correct": is_correct,
                        "user_input": opt,
                        "answer": q_data["answer"],
                        "desc": q_data["desc"]
                    }
                    st.session_state.show_feedback = True
                    st.rerun()

        # 객관식 형
        else:
            for opt in q_data["options"]:
                if st.button(opt, use_container_width=True, key=f"choice_{current_idx}_{opt}"):
                    is_correct = (opt == q_data["answer"])
                    if is_correct:
                        st.session_state.score += 1
                    st.session_state.last_result = {
                        "is_correct": is_correct,
                        "user_input": opt,
                        "answer": q_data["answer"],
                        "desc": q_data["desc"]
                    }
                    st.session_state.show_feedback = True
                    st.rerun()

# 2. 결과 화면
else:
    score = st.session_state.score

    if score == total_q:
        st.balloons()
        st.markdown(f"""
            <div class="toss-card" style="text-align: center; padding: 48px 32px;">
                <div style="font-size: 56px; margin-bottom: 16px;">🏆</div>
                <span class="toss-badge" style="background:#E8F3FF; color:#1B64DA;">만점 달성</span>
                <h2 style="font-size: 28px; font-weight: 800; color: #191F28; margin: 12px 0 8px 0;">3문제를 다 맞혔어요!</h2>
                <p style="font-size: 16px; color: #6B7684; margin-bottom: 28px;">오성고에 대해 정말 완벽하게 알고 계시네요.</p>
                <div style="background: #F8FAFF; border: 1.5px solid #E8F3FF; border-radius: 20px; padding: 22px; margin-bottom: 14px;">
                    <span style="font-size: 15px; color: #4B5563;">받으실 간식 혜택</span>
                    <div style="font-size: 24px; font-weight: 800; color: #1B64DA; margin-top: 4px;">🍫 ABC 초콜릿 3개</div>
                </div>
                <p style="font-size: 14px; color: #8B95A1;">부스 스태프에게 이 화면을 보여주세요!</p>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <div class="toss-card" style="text-align: center; padding: 48px 32px;">
                <div style="font-size: 56px; margin-bottom: 16px;">👏</div>
                <span class="toss-badge" style="background:#F2F4F6; color:#4E5968;">참여 완료</span>
                <h2 style="font-size: 28px; font-weight: 800; color: #191F28; margin: 12px 0 8px 0;">퀴즈를 완료했어요!</h2>
                <p style="font-size: 16px; color: #6B7684; margin-bottom: 28px;">총 3문제 중 <strong>{score}문제</strong>를 맞혔어요.</p>
                <div style="background: #F9FAFB; border: 1.5px solid #F2F4F6; border-radius: 20px; padding: 22px; margin-bottom: 14px;">
                    <span style="font-size: 15px; color: #4B5563;">받으실 간식 혜택</span>
                    <div style="font-size: 24px; font-weight: 800; color: #333D4B; margin-top: 4px;">🍫 ABC 초콜릿 1개</div>
                </div>
                <p style="font-size: 14px; color: #8B95A1;">부스 스태프에게 이 화면을 보여주세요!</p>
            </div>
        """, unsafe_allow_html=True)

    if st.button("처음으로 (다음 학생)", use_container_width=True, type="primary"):
        init_game()
        st.rerun()
