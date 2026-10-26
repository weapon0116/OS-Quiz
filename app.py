import streamlit as st
import random
import os

st.set_page_config(page_title="천안오성고 바로 알기 퀴즈", page_icon="🏫", layout="centered")

# ================= 전체 퀴즈 데이터베이스 (통합 풀) =================
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

# ================= 사이드바: 개발자 모드 =================
st.sidebar.title("🛠️ 관리자 패널")
dev_mode = st.sidebar.checkbox("개발자 모드 (문제 검수용)", value=False)

if dev_mode:
    st.sidebar.markdown("---")
    st.sidebar.subheader("🔍 특정 퀴즈 미리보기")
    
    quiz_titles = [f"[{q['category']}] {q['q'][:18]}..." for q in ALL_QUIZZES]
    selected_idx = st.sidebar.selectbox("검수할 문제를 선택하세요:", range(len(ALL_QUIZZES)), format_func=lambda x: quiz_titles[x])
    target_q = ALL_QUIZZES[selected_idx]
    
    st.sidebar.write(f"**ID:** `{target_q['id']}`")
    st.sidebar.write(f"**정답:** `{target_q['answer']}`")
    st.sidebar.caption(f"**해설:** {target_q['desc']}")
    
    if st.sidebar.button("👉 이 문제를 바로 메인에서 테스트", use_container_width=True):
        st.session_state.game_questions = [target_q]
        st.session_state.current_idx = 0
        st.session_state.score = 0
        st.session_state.show_feedback = False
        st.rerun()

    if st.sidebar.button("🔄 일반 3문제 모드로 되돌리기", use_container_width=True):
        init_game()
        st.rerun()

# ================= 메인 퀴즈 화면 =================
st.title("🏫 오성고 바로 알기 퀴즈")
st.markdown("---")

current_idx = st.session_state.current_idx
total_q = len(st.session_state.game_questions)

# 1. 문제 풀이 진행
if current_idx < total_q:
    q_data = st.session_state.game_questions[current_idx]
    
    st.caption(f"문제 {current_idx + 1} / {total_q}  ·  유형: {q_data['category']}")
    st.subheader(f"Q{current_idx + 1}. {q_data['q']}")

    # 1) 로고 비교 이미지
    if q_data.get("image_type") == "logo":
        col1, col2 = st.columns(2)
        with col1:
            if os.path.exists("images/logo_red.png"):
                st.image("images/logo_red.png", caption="1번 로고", width=180)
        with col2:
            if os.path.exists("images/logo_purple.png"):
                st.image("images/logo_purple.png", caption="2번 로고", width=180)

    # 2) 오별이 이미지
    elif q_data.get("image_type") == "obyeol":
        if os.path.exists("images/obyeol.png"):
            st.image("images/obyeol.png", caption="이 캐릭터의 이름은?", width=200)

    # 3) 배치도 퀴즈 이미지 (화면 꽉 차게 표시)
    elif "image_path" in q_data:
        img_path = q_data["image_path"]
        if os.path.exists(img_path):
            st.image(img_path, caption="[참고] 2026 천안오성고 공간조성 배치도", use_container_width=True)

    # 1-1. 정답 피드백 상태
    if st.session_state.show_feedback:
        res = st.session_state.last_result
        if res["is_correct"]:
            st.success(f"⭕ **정답입니다!**\n\n{res['desc']}")
        else:
            ans_display = res['answer'] if isinstance(res['answer'], str) else res['answer'][0]
            st.error(f"❌ **오답입니다!** (선택/입력한 답: {res['user_input']})\n\n👉 **정답: {ans_display}**\n\n💡 {res['desc']}")
            
        st.write("")
        if st.button("➡️ 다음으로 이동", use_container_width=True, type="primary"):
            st.session_state.show_feedback = False
            st.session_state.current_idx += 1
            st.rerun()

    # 1-2. 문제 풀이 입력 상태
    else:
        # 단답형
        if q_data["type"] == "short":
            with st.form(key=f"short_form_{current_idx}"):
                user_val = st.text_input("정답 입력 (숫자 또는 단어):", placeholder="여기에 정답을 입력하세요")
                submit = st.form_submit_button("정답 제출", use_container_width=True)
                
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

        # 객관식 형 (배치도 문제 포함)
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
    st.subheader("🎉 3문제를 모두 풀었습니다!")
    st.metric(label="최종 점수", value=f"{score} / {total_q} 점")

    if score == total_q:
        st.balloons()
        st.success("🏆 **만점입니다! 축하합니다!**\n\n스태프에게 이 화면을 보여주고 **ABC 초콜릿 3개**를 받으세요! 🍫🍫🍫")
    else:
        st.info("👏 **수고하셨습니다! (참여 완료)**\n\n스태프에게 이 화면을 보여주고 **ABC 초콜릿 1개**를 받으세요! 🍫")

    st.markdown("---")
    if st.button("🔄 다음 학생 퀴즈 시작하기", use_container_width=True, type="primary"):
        init_game()
        st.rerun()
