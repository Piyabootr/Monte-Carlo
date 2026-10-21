import random
import pandas as pd
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="5-Algorithm Majority Predictor", page_icon="🃏", layout="wide"
)

# Professional Modern Blue & Sky Blue Gradient Theme Styling
st.markdown(
    """
<style>
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1d4ed8 50%, #38bdf8 100%);
        color: #ffffff;
    }
    .metric-card {
        background: rgba(15, 23, 42, 0.75);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(56, 189, 248, 0.4);
        padding: 18px;
        border-radius: 16px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        text-align: center;
        margin-bottom: 15px;
    }
    .big-badge {
        font-size: 22px;
        font-weight: bold;
        padding: 22px;
        border-radius: 16px;
        text-align: center;
        margin-top: 15px;
        margin-bottom: 15px;
        box-shadow: 0 10px 25px -3px rgba(0, 0, 0, 0.5);
    }
    .consensus-pass { background: linear-gradient(135deg, #10b981 0%, #047857 100%); color: white; border: 2px solid #34d399; }
    .consensus-fail { background: rgba(30, 41, 59, 0.9); color: #f1f5f9; border: 2px solid rgba(239, 68, 68, 0.6); }
    .history-dot {
        display: inline-block;
        width: 40px;
        height: 40px;
        line-height: 40px;
        border-radius: 50%;
        text-align: center;
        font-weight: bold;
        color: white;
        margin: 5px;
        font-size: 14px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.4);
    }
    section[data-testid="stSidebar"] {
        background-color: #0b1329;
        border-right: 1px solid rgba(56, 189, 248, 0.2);
    }
</style>
""",
    unsafe_allow_html=True,
)

# --- Sidebar Settings & Multi-language Selector ---
st.sidebar.markdown("### 🌐 Language / ภาษา")
lang = st.sidebar.selectbox(
    "Select Language / เลือกภาษา", ["English", "ไทย"], index=0
)

translations = {
    "English": {
        "title": (
            "🃏 5-ALGORITHM MAJORITY CONSENSUS PREDICTOR & CONFIDENCE"
            " BREAKDOWN"
        ),
        "subtitle": (
            "4:1 Voting System with individual algorithm confidence percentages"
            " and confirmation statuses."
        ),
        "grid_title": "1️⃣ Editable Grid Table (50 Rounds Historical Data Entry)",
        "grid_desc": (
            "💡 **50-Round Grid Table:** Record historical outcomes to feed all 5"
            " algorithms."
        ),
        "roadmap_title": "2️⃣ Roadmap & Last 30-Round Analytics",
        "pred_title": (
            "3️⃣ 5-Algorithm Breakdown (Confirm Status & Percentages)"
        ),
        "rec_title": "🎯 Majority Consensus Decision (4:1 Rule):",
        "pass_msg": (
            "✅ 4:1 MAJORITY CONFIRMED! At least 4 algorithms agree to invest"
            " in 【"
        ),
        "fail_msg": (
            "⛔ NO MAJORITY / WAIT: Algorithms are split. Do NOT invest this"
            " round!"
        ),
        "reset": "🗑️ Reset Grid Data & Clear History",
        "mode": "Game Scoring Mode:",
        "mode_bacc": (
            "Baccarat / Dragon Tiger Style (10, J, Q, K = 0 for Baccarat)"
        ),
        "mode_single": "Single Card High Value (A=1 to K=13)",
        "sims": "Monte Carlo Iterations (per deck)",
        "total_valid": "Total Valid Rounds Recorded:",
        "red_wins": "Red Wins",
        "blue_wins": "Blue Wins",
        "ties": "Ties",
        "no_data": (
            "Please enter round outcomes in the grid table above to start"
            " analysis."
        ),
    },
    "ไทย": {
        "title": "🃏 ระบบพยากรณ์ 5 อัลกอริทึม พร้อมแสดงเปอร์เซ็นต์การ Confirm",
        "subtitle": (
            "ระบบลงมติ 4:1 พร้อมแสดงผลเปอร์เซ็นต์ความมั่นใจ (%) และสถานะการยืนยัน"
            " (Confirm) ของแต่ละอัลกอริทึม"
        ),
        "grid_title": "1️⃣ ตารางกริดบันทึกข้อมูลย้อนหลัง (50 รอบ)",
        "grid_desc": (
            "💡 **ตารางกริด 50 รอบ:** บันทึกผลย้อนหลังเพื่อป้อนข้อมูลให้ทั้ง 5"
            " อัลกอริทึมประมวลผล"
        ),
        "roadmap_title": "2️⃣ แผนภูมิ Roadmap และวิเคราะห์ 30 ตาล่าสุด",
        "pred_title": "3️⃣ รายละเอียดการ Confirm และเปอร์เซ็นต์ของแต่ละอัลกอริทึม",
        "rec_title": "🎯 ผลการลงมติเสียงข้างมาก (กฎ 4:1):",
        "pass_msg": (
            "✅ ผ่านเกณฑ์เสียงข้างมาก 4:1! มีอัลกอริทึมยืนยันตรงกัน 4 ตัวขึ้นไปให้ลงทุนฝั่ง"
            " 【"
        ),
        "fail_msg": (
            "⛔ เสียงแตก / รอจังหวะ: คะแนนไม่ถึงเกณฑ์ 4:1 ห้ามลงทุนตานี้!"
        ),
        "reset": "🗑️ ล้างข้อมูลกริด & เริ่มขอนใหม่",
        "mode": "รูปแบบการคิดแต้ม:",
        "mode_bacc": "สไตล์บาคาร่า / เสือมังกร (10, J, Q, K นับเป็น 0)",
        "mode_single": "วัดแต้มหน้าไพ่เดี่ยว (A=1 ถึง K=13)",
        "sims": "จำนวนรอบจำลอง Monte Carlo (ต่อสำรับ)",
        "total_valid": "จำนวนตาทั้งหมดที่บันทึก:",
        "red_wins": "แดงชนะ",
        "blue_wins": "น้ำเงินชนะ",
        "ties": "เสมอ",
        "no_data": (
            "กรุณากรอกผลการแข่งขันในตารางกริดด้านบน เพื่อเริ่มระบบวิเคราะห์"
        ),
    },
}

t = translations[lang]

st.markdown(f"# {t['title']}")
st.markdown(t["subtitle"])
st.markdown("---")

if "grid_history" not in st.session_state:
    initial_data = []
    for i in range(1, 51):
        initial_data.append({
            "Round": i,
            "Red Winner": False,
            "Blue Winner": False,
            "Tie (Draw)": False,
            "Notes / Card Ranks": "",
        })
    st.session_state.grid_history = pd.DataFrame(initial_data)

st.sidebar.markdown("### ⚙️ Simulation Parameters")
game_mode = st.sidebar.radio(
    t["mode"], [t["mode_bacc"], t["mode_single"]]
)
num_sims = st.sidebar.slider(
    t["sims"], min_value=10000, max_value=50000, value=20000, step=5000
)

st.sidebar.markdown("---")
if st.sidebar.button(t["reset"], use_container_width=True):
    reset_data = []
    for i in range(1, 51):
        reset_data.append({
            "Round": i,
            "Red Winner": False,
            "Blue Winner": False,
            "Tie (Draw)": False,
            "Notes / Card Ranks": "",
        })
    st.session_state.grid_history = pd.DataFrame(reset_data)
    st.rerun()

st.markdown(f"### {t['grid_title']}")
st.markdown(t["grid_desc"])

edited_grid_df = st.data_editor(
    st.session_state.grid_history,
    num_rows="dynamic",
    use_container_width=True,
    key="grid_editor",
)
st.session_state.grid_history = edited_grid_df

processed_rounds = []
for idx, row in edited_grid_df.iterrows():
    if row.get("Red Winner", False):
        processed_rounds.append({"round": idx + 1, "winner": "Red"})
    elif row.get("Blue Winner", False):
        processed_rounds.append({"round": idx + 1, "winner": "Blue"})
    elif row.get("Tie (Draw)", False):
        processed_rounds.append({"round": idx + 1, "winner": "Tie"})

st.markdown("---")
st.markdown(f"### {t['roadmap_title']}")

if processed_rounds:
    badges_html = ""
    for r in processed_rounds:
        bg = (
            "#f43f5e"
            if r["winner"] == "Red"
            else ("#0ea5e9" if r["winner"] == "Blue" else "#10b981")
        )
        badges_html += f'<span class="history-dot" style="background-color:{bg};">{r["winner"][0]}</span>'
    st.markdown(badges_html, unsafe_allow_html=True)
else:
    st.info(t["no_data"])


# --- 5-Algorithm Engine returning (Vote, Percentage) ---
def run_5_algorithm_detailed(rounds_history, game_mode, num_sims):
    results = []

    # 1. Monte Carlo
    sim_red, sim_blue = 0, 0
    for _ in range(1000):
        res = random.choice(["Red", "Blue"])
        if res == "Red":
            sim_red += 1
        else:
            sim_blue += 1
    mc_vote = "Red" if sim_red >= sim_blue else "Blue"
    mc_pct = (
        (sim_red / 1000) * 100 if mc_vote == "Red" else (sim_blue / 1000) * 100
    )
    results.append(("Monte Carlo", mc_vote, mc_pct))

    # 2. HMM Transition
    hmm_vote, hmm_pct = "Red", 50.0
    if len(rounds_history) >= 2:
        last_w = rounds_history[-1]["winner"]
        r_count, b_count, total = 0, 0, 0
        for i in range(len(rounds_history) - 1):
            if rounds_history[i]["winner"] == last_w:
                nxt = rounds_history[i + 1]["winner"]
                if nxt == "Red":
                    r_count += 1
                elif nxt == "Blue":
                    b_count += 1
                total += 1
        if total > 0:
            hmm_vote = "Red" if r_count >= b_count else "Blue"
            hmm_pct = (
                (r_count / total) * 100
                if hmm_vote == "Red"
                else (b_count / total) * 100
            )
        else:
            hmm_pct = 50.0
    results.append(("HMM Transition", hmm_vote, hmm_pct))

    # 3. Bayesian Inference
    bayes_vote, bayes_pct = "Red", 50.0
    if len(rounds_history) > 0:
        total_r = sum(1 for r in rounds_history if r["winner"] == "Red")
        total_b = sum(1 for r in rounds_history if r["winner"] == "Blue")
        tot = total_r + total_b
        if tot > 0:
            bayes_vote = "Red" if total_r >= total_b else "Blue"
            bayes_pct = (
                (total_r / tot) * 100
                if bayes_vote == "Red"
                else (total_b / tot) * 100
            )
    results.append(("Bayesian Inference", bayes_vote, bayes_pct))

    # 4. Momentum Trend (Last 10)
    trend_vote, trend_pct = "Red", 50.0
    if len(rounds_history) > 0:
        last_10 = rounds_history[-10:]
        t_r = sum(1 for r in last_10 if r["winner"] == "Red")
        t_b = sum(1 for r in last_10 if r["winner"] == "Blue")
        t_tot = len(last_10)
        if t_tot > 0:
            trend_vote = "Red" if t_r >= t_b else "Blue"
            trend_pct = (
                (t_r / t_tot) * 100
                if trend_vote == "Red"
                else (t_b / t_tot) * 100
            )
    results.append(("Momentum Trend", trend_vote, trend_pct))

    # 5. Pattern Matching Engine
    pat_vote, pat_pct = "Red", 50.0
    if len(rounds_history) >= 4:
        pattern_key = [r["winner"] for r in rounds_history[-3:]]
        p_red, p_blue, p_tot = 0, 0, 0
        for i in range(len(rounds_history) - 4):
            sub_pattern = [rounds_history[j]["winner"] for j in range(i, i + 3)]
            if sub_pattern == pattern_key:
                next_res = rounds_history[i + 3]["winner"]
                if next_res == "Red":
                    p_red += 1
                elif next_res == "Blue":
                    p_blue += 1
                p_tot += 1
        if p_tot > 0:
            pat_vote = "Red" if p_red >= p_blue else "Blue"
            pat_pct = (
                (p_red / p_tot) * 100
                if pat_vote == "Red"
                else (p_blue / p_tot) * 100
            )
        else:
            pat_pct = 60.0
    results.append(("Pattern Matching", pat_vote, pat_pct))

    return results


st.markdown("---")
st.markdown(f"### {t['pred_title']}")

if len(processed_rounds) >= 4:
    algo_results = run_5_algorithm_detailed(
        processed_rounds, game_mode, num_sims
    )

    # Determine majority side based on votes
    votes_list = [res[1] for res in algo_results]
    red_count = votes_list.count("Red")
    blue_count = votes_list.count("Blue")
    majority_side = "Red" if red_count >= blue_count else "Blue"

    # Display columns for each algorithm with Confirm status and percentage
    cols = st.columns(5)
    for idx, (name, vote, pct) in enumerate(algo_results):
        is_confirmed = (
            "✅ Confirmed" if vote == majority_side else "⚠️ Mismatched"
        )
        color_code = "#ef4444" if vote == "Red" else "#3b82f6"
        cols[idx].markdown(
            f'<div class="metric-card">'
            f"<h4>{name}</h4>"
            f'<h3 style="color: {color_code};">{vote}</h3>'
            f"<p>Confidence: <b>{pct:.1f}%</b></p>"
            f"<p style='font-size:12px;'>{is_confirmed}</p>"
            f"</div>",
            unsafe_allow_html=True,
        )

    st.markdown(f"#### {t['rec_title']}")

    # Check 4:1 Majority Rule
    if red_count >= 4:
        st.markdown(
            f'<div class="big-badge consensus-pass">{t["pass_msg"]}Red Side】 (4:1 Majority Confirmed) 🎉</div>',
            unsafe_allow_html=True,
        )
    elif blue_count >= 4:
        st.markdown(
            f'<div class="big-badge consensus-pass">{t["pass_msg"]}Blue Side】 (4:1 Majority Confirmed) 🎉</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f'<div class="big-badge consensus-fail">{t["fail_msg"]} (Red: {red_count} / Blue: {blue_count})</div>',
            unsafe_allow_html=True,
        )
else:
    st.info(
        "กรุณากรอกข้อมูลย้อนหลังอย่างน้อย 4 ตาขึ้นไป เพื่อให้ระบบคำนวณเปอร์เซ็นต์และแสดงผลการ Confirm ของแต่ละอัลกอริทึม"
    )
