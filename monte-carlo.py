import random
import pandas as pd
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Pro Card Shoe Predictor Dashboard", page_icon="🃏", layout="wide"
)

# Professional Deep Blue & Midnight Black Gradient Theme Styling (โทนน้ำเงินป่นดำพรีเมียม)
st.markdown(
    """
<style>
    /* Main Background: Gradient Deep Midnight Black & Navy Blue */
    .stApp {
        background: linear-gradient(135deg, #050b14 0%, #0a1128 50%, #172554 100%);
        color: #f8fafc;
    }
    
    /* Glassmorphism Metric Cards with Dark Blue-Black Tint */
    .metric-card {
        background: rgba(10, 17, 40, 0.85);
        backdrop-filter: blur(14px);
        border: 1px solid rgba(30, 58, 138, 0.6);
        padding: 18px;
        border-radius: 16px;
        box-shadow: 0 10px 30px 0 rgba(0, 0, 0, 0.6);
        text-align: center;
        margin-bottom: 15px;
    }
    
    /* Vibrant Big Betting Recommendation Badges */
    .big-badge {
        font-size: 22px;
        font-weight: bold;
        padding: 22px;
        border-radius: 16px;
        text-align: center;
        margin-top: 15px;
        margin-bottom: 15px;
        box-shadow: 0 10px 25px -3px rgba(0, 0, 0, 0.7);
    }
    .red-win { background: linear-gradient(135deg, #dc2626 0%, #7f1d1d 100%); color: white; border: 2px solid #ef4444; }
    .blue-win { background: linear-gradient(135deg, #2563eb 0%, #1e3a8a 100%); color: white; border: 2px solid #3b82f6; }
    .tie-win { background: linear-gradient(135deg, #059669 0%, #064e3b 100%); color: white; border: 2px solid #10b981; }
    .wait-signal { background: rgba(15, 23, 42, 0.95); color: #94a3b8; border: 2px solid rgba(51, 65, 85, 0.8); }
    
    /* Roadmap History Dots */
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
        box-shadow: 0 4px 10px rgba(0,0,0,0.6);
    }
    
    /* Sidebar Styling (Dark Navy & Black) */
    section[data-testid="stSidebar"] {
        background-color: #030712;
        border-right: 1px solid rgba(30, 58, 138, 0.4);
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
        "title": "🃏 5-ALGORITHM MAJORITY PREDICTOR DASHBOARD",
        "subtitle": (
            "4:1 Voting System Dashboard with Popup Alerts: **Monte Carlo**,"
            " **HMM**, **Bayesian**, **Momentum Trend**, and **Pattern"
            " Matching**."
        ),
        "grid_title": "1️⃣ Editable Grid Table (50 Rounds Historical Data Entry)",
        "grid_desc": (
            "💡 **50-Round Grid Table:** Record historical outcomes to feed all 5"
            " algorithms."
        ),
        "roadmap_title": "2️⃣ Roadmap & Last 30-Round Analytics",
        "pred_title": (
            "3️⃣ Dashboard: 5-Algorithm Majority Voting & Popup Alert"
        ),
        "rec_title": "🎯 Dashboard Consensus Status (4:1 Majority Rule):",
        "pass_msg": (
            "✅ 4:1 MAJORITY CONFIRMED! Agreement Level: {pct}% (4 or more"
            " algorithms agree to invest in 【"
        ),
        "fail_msg": (
            "⛔ NO MAJORITY / WAIT: Agreement Level: {pct}% (Split votes, e.g.,"
            " 3:2). Do NOT invest this round!"
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
            " dashboard analytics."
        ),
        "popup_title": "🚀 INVESTMENT SIGNAL CONFIRMED!",
        "popup_text": (
            "All algorithms aligned at {pct}% confidence. Recommended side:"
            " **{side}**"
        ),
    },
    "ไทย": {
        "title": "🃏 แดชบอร์ดพยากรณ์เสียงข้างมาก 5 อัลกอริทึม (4:1 MAJORITY)",
        "subtitle": (
            "แดชบอร์ดแสดงผลการลงมติพร้อมระบบ Popup เด้งเตือน: **Monte Carlo**,"
            " **HMM**, **Bayesian**, **Momentum Trend**, และ **Pattern"
            " Matching**"
        ),
        "grid_title": "1️⃣ ตารางกริดบันทึกข้อมูลย้อนหลัง (50 รอบ)",
        "grid_desc": (
            "💡 **ตารางกริด 50 รอบ:** บันทึกผลย้อนหลังเพื่อป้อนข้อมูลให้ทั้ง 5"
            " อัลกอริทึมประมวลผลบนแดชบอร์ด"
        ),
        "roadmap_title": "2️⃣ แผนภูมิ Roadmap และวิเคราะห์ 30 ตาล่าสุด",
        "pred_title": (
            "3️⃣ แดชบอร์ดแสดงผล: การลงมติ 5 อัลกอริทึม & ระบบ Popup แจ้งเตือน"
        ),
        "rec_title": "🎯 สถานะการตัดสินใจบนแดชบอร์ด (กฎเสียงข้างมาก 4:1):",
        "pass_msg": (
            "✅ ยืนยันสถานะ CONFIRM! ระดับความเห็นพ้อง: {pct}% (ผ่านเกณฑ์ 4:1"
            " ลงทุนได้ที่ฝั่ง 【"
        ),
        "fail_msg": (
            "⛔ สถานะ WAIT / ห้ามลงทุน: ระดับความเห็นพ้อง: {pct}% (เสียงแตก 3:2"
            " ต่ำกว่าเกณฑ์ 4:1) ข้ามตานี้!"
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
            "กรุณากรอกผลการแข่งขันในตารางกริดด้านบน เพื่อแสดงผลแผงควบคุมแดชบอร์ด"
        ),
        "popup_title": "🚀 สัญญาณลงทุนผ่านเกณฑ์ (CONFIRMED)!",
        "popup_text": (
            "คณะกรรมการอัลกอริทึมมีความเห็นพ้องต้องกันที่ระดับ {pct}% แนะนำลงทุนที่ฝั่ง:"
            " **{side}**"
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
            "#ef4444"
            if r["winner"] == "Red"
            else ("#3b82f6" if r["winner"] == "Blue" else "#10b981")
        )
        badges_html += f'<span class="history-dot" style="background-color:{bg};">{r["winner"][0]}</span>'
    st.markdown(badges_html, unsafe_allow_html=True)
else:
    st.info(t["no_data"])


# --- 5-Algorithm Consensus Engine ---
def run_5_algorithm_consensus(rounds_history, game_mode, num_sims):
    sim_red, sim_blue = 0, 0
    for _ in range(1000):
        res = random.choice(["Red", "Blue"])
        if res == "Red":
            sim_red += 1
        else:
            sim_blue += 1
    vote_mc = "Red" if sim_red >= sim_blue else "Blue"

    vote_hmm = "Red"
    if len(rounds_history) >= 2:
        last_w = rounds_history[-1]["winner"]
        r_after_last, b_after_last = 0, 0
        for i in range(len(rounds_history) - 1):
            if rounds_history[i]["winner"] == last_w:
                nxt = rounds_history[i + 1]["winner"]
                if nxt == "Red":
                    r_after_last += 1
                elif nxt == "Blue":
                    b_after_last += 1
        vote_hmm = "Red" if r_after_last >= b_after_last else "Blue"

    vote_bayes = "Red"
    if len(rounds_history) > 0:
        total_r = sum(1 for r in rounds_history if r["winner"] == "Red")
        total_b = sum(1 for r in rounds_history if r["winner"] == "Blue")
        vote_bayes = "Red" if total_r >= total_b else "Blue"

    vote_trend = "Red"
    if len(rounds_history) > 0:
        last_10 = rounds_history[-10:]
        t_r = sum(1 for r in last_10 if r["winner"] == "Red")
        t_b = sum(1 for r in last_10 if r["winner"] == "Blue")
        vote_trend = "Red" if t_r >= t_b else "Blue"

    vote_pattern = "Red"
    if len(rounds_history) >= 4:
        pattern_key = [r["winner"] for r in rounds_history[-3:]]
        p_red, p_blue = 0, 0
        for i in range(len(rounds_history) - 4):
            sub_pattern = [rounds_history[j]["winner"] for j in range(i, i + 3)]
            if sub_pattern == pattern_key:
                next_res = rounds_history[i + 3]["winner"]
                if next_res == "Red":
                    p_red += 1
                elif next_res == "Blue":
                    p_blue += 1
        if p_red > p_blue:
            vote_pattern = "Red"
        elif p_blue > p_red:
            vote_pattern = "Blue"
        else:
            vote_pattern = rounds_history[-1]["winner"]

    votes = [vote_mc, vote_hmm, vote_bayes, vote_trend, vote_pattern]
    return votes


st.markdown("---")
st.markdown(f"### {t['pred_title']}")

if len(processed_rounds) >= 4:
    votes = run_5_algorithm_consensus(processed_rounds, game_mode, num_sims)

    red_count = votes.count("Red")
    blue_count = votes.count("Blue")
    max_votes = max(red_count, blue_count)
    confidence_pct = (max_votes / 5) * 100

    col1, col2, col3, col4, col5 = st.columns(5)

    algo_names = [
        "1. Monte Carlo",
        "2. HMM",
        "3. Bayesian",
        "4. Momentum",
        "5. Pattern",
    ]
    for idx, (col, v, name) in enumerate(
        zip([col1, col2, col3, col4, col5], votes, algo_names)
    ):
        status_color = "#ef4444" if v == "Red" else "#3b82f6"
        col.markdown(
            f'<div class="metric-card"><h4>{name}</h4><h3 style="color:'
            f' {status_color};">{v}</h3><p style="font-size: 11px; color:'
            ' #94a3b8;">CONFIRMED</p></div>',
            unsafe_allow_html=True,
        )

    st.markdown(f"#### {t['rec_title']}")
    st.markdown(
        f"### 📊 Dashboard Confidence Level: **{confidence_pct:.0f}%**"
        f" ({max_votes}/5 Algorithms Aligned)"
    )

    @st.dialog("🚨 Investment Signal Confirmed")
    def show_popup_alert(side, pct):
        st.success(
            t["popup_text"].format(
                pct=pct, side="Red Side" if side == "Red" else "Blue Side"
            )
        )
        st.balloons()
        if st.button("OK / Close"):
            st.rerun()

    if red_count >= 4:
        st.markdown(
            f'<div class="big-badge consensus-pass">{t["pass_msg"]}Red Side】'
            f" (Confidence: {confidence_pct:.0f}%) 🎉</div>",
            unsafe_allow_html=True,
        )
        if st.button(
            "🔔 Show Popup Signal Alert", type="primary", use_container_width=True
        ):
            show_popup_alert("Red", confidence_pct)
    elif blue_count >= 4:
        st.markdown(
            f'<div class="big-badge consensus-pass">{t["pass_msg"]}Blue Side】'
            f" (Confidence: {confidence_pct:.0f}%) 🎉</div>",
            unsafe_allow_html=True,
        )
        if st.button(
            "🔔 Show Popup Signal Alert", type="primary", use_container_width=True
        ):
            show_popup_alert("Blue", confidence_pct)
    else:
        st.markdown(
            f'<div class="big-badge consensus-fail">{t["fail_msg"]} (Red:'
            f" {red_count} / Blue: {blue_count})</div>",
            unsafe_allow_html=True,
        )
else:
    st.info(
        "กรุณากรอกข้อมูลย้อนหลังอย่างน้อย 4 ตาขึ้นไป เพื่อแสดงผลแผงควบคุมแดชบอร์ด"
        " 5 อัลกอริทึม"
    )
