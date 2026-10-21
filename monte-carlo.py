import random
import pandas as pd
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Pro Predictor Dashboard",
    page_icon="🃏",
    layout="wide",
)

# Professional Deep Blue & Midnight Black Theme Styling
st.markdown(
    """
<style>
    .stApp {
        background: linear-gradient(135deg, #050b14 0%, #0a1128 50%, #172554 100%);
        color: #f8fafc;
    }
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
    .consensus-pass { background: linear-gradient(135deg, #059669 0%, #064e3b 100%); color: white; border: 2px solid #10b981; }
    .consensus-fail { background: rgba(15, 23, 42, 0.95); color: #94a3b8; border: 2px solid rgba(239, 68, 68, 0.6); }
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
    section[data-testid="stSidebar"] {
        background-color: #030712;
        border-right: 1px solid rgba(30, 58, 138, 0.4);
    }
    .target-hit {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        color: white; padding: 15px; border-radius: 10px; font-weight: bold; text-align: center; border: 2px solid #fbbf24; margin-top: 10px;
    }
    .stop-loss-hit {
        background: linear-gradient(135deg, #dc2626 0%, #991b1b 100%);
        color: white; padding: 15px; border-radius: 10px; font-weight: bold; text-align: center; border: 2px solid #ef4444; margin-top: 10px;
    }
</style>
""",
    unsafe_allow_html=True,
)

# 100% Pure English & 100% Pure Thai Dictionary
translations = {
    "English": {
        "lang_header": "🌐 Language",
        "lang_select": "Select Language",
        "title": "🃏 ADVANCED 5-ALGORITHM PRO PREDICTOR",
        "subtitle": "Intensified AI Dashboard with Bankroll Management, Profit Targets & Dynamic Stake Sizing.",
        "bankroll_title": "💰 Bankroll & Risk Management",
        "init_fund": "Initial Capital / Bankroll (฿)",
        "target_profit": "Daily Profit Goal (฿)",
        "max_loss": "Max Stop-Loss Limit (฿)",
        "base_bet": "Base Unit Bet Size (฿)",
        "sim_params": "⚙️ Simulation Parameters",
        "mode": "Game Scoring Mode:",
        "mode_bacc": "Baccarat / Dragon Tiger (10, J, Q, K = 0)",
        "mode_single": "Single Card High Value (A=1 to K=13)",
        "sims": "Monte Carlo Intensity (Iterations)",
        "reset": "🗑️ Reset Data & Clear History",
        "grid_title": "1️⃣ Historical Data & P/L Entry (50 Rounds)",
        "grid_desc": "💡 Check the round outcomes and enter your actual Profit/Loss. Click **Confirm Data & Analyze** below.",
        "col_round": "Round",
        "col_red": "Red Winner",
        "col_blue": "Blue Winner",
        "col_tie": "Tie (Draw)",
        "col_pl": "My P/L (฿)",
        "col_notes": "Notes / Card Ranks",
        "confirm_btn": "✅ Confirm Data & Analyze",
        "confirm_success": "✅ Data confirmed and analyzed successfully!",
        "bankroll_section": "💰 Bankroll & Profit Analytics",
        "curr_cap": "Current Capital",
        "init_prefix": "Initial",
        "total_pl_label": "Total Profit / Loss",
        "of_target": "of Target",
        "daily_target_label": "Daily Profit Goal",
        "max_sl_label": "Max Stop-Loss Limit",
        "target_reached": "🎉 TARGET REACHED: You have achieved your daily profit goal! Stop playing now to lock in your profits.",
        "sl_reached": "⚠️ STOP-LOSS REACHED: You have hit your maximum loss limit! Stop playing immediately to protect your capital.",
        "roadmap_title": "2️⃣ Roadmap & Last 30-Round Analytics",
        "no_data": "Please enter round outcomes in the table above and click Confirm Data & Analyze.",
        "last_30_red": "Red Wins (Last 30)",
        "last_30_blue": "Blue Wins (Last 30)",
        "last_30_tie": "Ties (Last 30)",
        "total_recorded": "Total Valid Rounds",
        "pred_title": "3️⃣ Intensive 5-Algorithm Voting & Stake Sizing",
        "algo_names": [
            "1. Deep Monte Carlo",
            "2. 2-Step HMM",
            "3. Pro Bayesian",
            "4. EMA Momentum",
            "5. N-Gram Pattern",
        ],
        "side_red": "Red",
        "side_blue": "Blue",
        "side_tie": "Tie",
        "dot_r": "R",
        "dot_b": "B",
        "dot_t": "T",
        "status_confirmed": "INTENSIFIED VOTE",
        "chart_title": "📊 Algorithm Consensus Analytics Chart",
        "chart_side": "Side",
        "chart_votes": "Votes",
        "rec_title": "🎯 Actionable Strategy (4:1 Majority Rule):",
        "conf_level": "📊 Dashboard Confidence Level",
        "aligned": "Algorithms Aligned",
        "pass_red": "✅ INVEST SIGNAL CONFIRMED! Target Side: 【Red Side】",
        "pass_blue": "✅ INVEST SIGNAL CONFIRMED! Target Side: 【Blue Side】",
        "stake_label": "💡 Forecasted Next Round Stake Size",
        "fail_msg": "⛔ WAIT / DO NOT INVEST: Algorithms are split. Preserve your bankroll!",
        "wait_stake": "0 ฿ (WAIT)",
        "popup_btn": "🔔 Show Investment Signal Popup",
        "popup_title": "🚨 Investment Signal Confirmed",
        "popup_body": "4:1 Majority Consensus Reached ({pct:.0f}% Confidence)!\n\nRecommended Side: **{side}**\n\nRecommended Stake: **{stake:,.0f} ฿**",
        "popup_close": "OK / Close",
        "min_rounds_msg": "Please record and confirm at least 5 rounds in the table above to activate the 5-Algorithm Predictor.",
    },
    "ไทย": {
        "lang_header": "🌐 ภาษา",
        "lang_select": "เลือกภาษา",
        "title": "🃏 แดชบอร์ดพยากรณ์ขั้นสูง 5 อัลกอริทึม",
        "subtitle": "ระบบวิเคราะห์ความเข้มข้นสูง พร้อมบริหารเงินทุน เป้าหมายกำไรรายวัน และพยากรณ์เงินเดิมพันอัตโนมัติ",
        "bankroll_title": "💰 ตั้งค่าเงินทุนและการบริหารความเสี่ยง",
        "init_fund": "เงินทุนเริ่มต้น (฿)",
        "target_profit": "เป้าหมายกำไรต่อวัน (฿)",
        "max_loss": "จุดตัดขาดทุนสูงสุด (฿)",
        "base_bet": "เงินเดิมพันฐานต่อหน่วย (฿)",
        "sim_params": "⚙️ ตั้งค่าพารามิเตอร์การจำลอง",
        "mode": "รูปแบบการคิดแต้ม:",
        "mode_bacc": "สไตล์บาคาร่า / เสือมังกร (10, J, Q, K นับเป็น 0)",
        "mode_single": "วัดแต้มหน้าไพ่เดี่ยวสูงสุด (A=1 ถึง K=13)",
        "sims": "ความเข้มข้นในการจำลอง (จำนวนรอบ)",
        "reset": "🗑️ ล้างข้อมูลตารางและเริ่มขอนใหม่",
        "grid_title": "1️⃣ ตารางบันทึกผลย้อนหลังและกำไร/ขาดทุน (50 รอบ)",
        "grid_desc": "💡 ติ๊กเลือกผลที่ออกและกรอกกำไร/ขาดทุนจริงในช่อง `กำไร/ขาดทุน (฿)` จากนั้นกดปุ่ม **ยืนยันข้อมูลและวิเคราะห์** ด้านล่าง",
        "col_round": "รอบที่",
        "col_red": "ฝ่ายแดงชนะ",
        "col_blue": "ฝ่ายน้ำเงินชนะ",
        "col_tie": "เสมอ",
        "col_pl": "กำไร/ขาดทุน (฿)",
        "col_notes": "หมายเหตุ / เลขไพ่",
        "confirm_btn": "✅ ยืนยันข้อมูลและเริ่มวิเคราะห์",
        "confirm_success": "✅ ยืนยันข้อมูลและอัปเดตผลการวิเคราะห์เรียบร้อยแล้ว!",
        "bankroll_section": "💰 ข้อมูลวิเคราะห์เงินทุนและเป้าหมายกำไร",
        "curr_cap": "เงินทุนปัจจุบัน",
        "init_prefix": "ทุนเริ่มต้น",
        "total_pl_label": "กำไร / ขาดทุนสุทธิ",
        "of_target": "ของเป้าหมาย",
        "daily_target_label": "เป้าหมายกำไรรายวัน",
        "max_sl_label": "จุดตัดขาดทุนสูงสุด",
        "target_reached": "🎉 ถึงเป้าหมายกำไรรายวันแล้ว: คุณทำกำไรได้ตามเป้าหมายที่ตั้งไว้ แนะนำให้หยุดพักและถอนกำไรทันที!",
        "sl_reached": "⚠️ แตะจุดตัดขาดทุนสูงสุด: ขาดทุนถึงเกณฑ์ที่กำหนดไว้ แนะนำให้หยุดเล่นทันทีเพื่อรักษาเงินทุนที่เหลือ!",
        "roadmap_title": "2️⃣ แผนภูมิเค้าไพ่และสถิติ 30 ตาล่าสุด",
        "no_data": "กรุณาติ๊กเลือกผลการแข่งขันในตารางด้านบน แล้วกดปุ่ม ยืนยันข้อมูลและเริ่มวิเคราะห์",
        "last_30_red": "แดงชนะ (30 ตาล่าสุด)",
        "last_30_blue": "น้ำเงินชนะ (30 ตาล่าสุด)",
        "last_30_tie": "เสมอ (30 ตาล่าสุด)",
        "total_recorded": "จำนวนรอบที่บันทึกทั้งหมด",
        "pred_title": "3️⃣ ผลการลงมติ 5 อัลกอริทึมเข้มข้น & พยากรณ์เงินเดิมพันตาถัดไป",
        "algo_names": [
            "1. มอนติคาร์โลเชิงลึก",
            "2. มาร์คอฟ 2 ขั้น (HMM)",
            "3. เบส์เซียนขั้นสูง",
            "4. โมเมนตัม EMA",
            "5. จับคู่รูปแบบเชิงลึก",
        ],
        "side_red": "ฝ่ายแดง",
        "side_blue": "ฝ่ายน้ำเงิน",
        "side_tie": "เสมอ",
        "dot_r": "ด",
        "dot_b": "น",
        "dot_t": "ส",
        "status_confirmed": "ยืนยันผลวิเคราะห์",
        "chart_title": "📊 กราฟเปรียบเทียบคะแนนเสียงของ 5 อัลกอริทึม",
        "chart_side": "ฝั่งที่โหวต",
        "chart_votes": "จำนวนเสียงโหวต",
        "rec_title": "🎯 กลยุทธ์การลงทุนตาถัดไป (กฎเสียงข้างมาก 4:1):",
        "conf_level": "📊 ระดับความเชื่อมั่นบนแดชบอร์ด",
        "aligned": "อัลกอริทึมเห็นตรงกัน",
        "pass_red": "✅ ยืนยันสัญญาณลงทุน! แนะนำให้ลงฝั่ง: 【ฝ่ายแดง】",
        "pass_blue": "✅ ยืนยันสัญญาณลงทุน! แนะนำให้ลงฝั่ง: 【ฝ่ายน้ำเงิน】",
        "stake_label": "💡 พยากรณ์ขนาดเงินเดิมพันตาถัดไป",
        "fail_msg": "⛔ ห้ามลงทุน / รอจังหวะ: อัลกอริทึมเสียงแตก รักษาวินัยและเงินทุนของคุณไว้!",
        "wait_stake": "0 ฿ (งดลงเดิมพัน)",
        "popup_btn": "🔔 แสดงป๊อปอัปแจ้งเตือนสัญญาณลงทุน",
        "popup_title": "🚨 ยืนยันสัญญาณการลงทุน",
        "popup_body": "ผ่านมติเสียงข้างมาก 4:1 (ความเชื่อมั่น {pct:.0f}%)!\n\nแนะนำให้ลงทุนฝั่ง: **{side}**\n\nขนาดเงินเดิมพันที่แนะนำ: **{stake:,.0f} ฿**",
        "popup_close": "ตกลง / ปิดหน้าต่าง",
        "min_rounds_msg": "กรุณากรอกข้อมูลในตารางและกดปุ่ม ยืนยันข้อมูล อย่างน้อย 5 ตาขึ้นไป เพื่อเริ่มการวิเคราะห์ด้วย 5 อัลกอริทึม",
    },
}

# --- Sidebar Language Selection ---
current_lang = st.session_state.get("lang_selector", "English")
st.sidebar.markdown(f"### {translations[current_lang]['lang_header']}")
lang = st.sidebar.selectbox(
    translations[current_lang]["lang_select"],
    ["English", "ไทย"],
    key="lang_selector",
)

t = translations[lang]

st.markdown(f"# {t['title']}")
st.markdown(t["subtitle"])
st.markdown("---")

# --- Sidebar Bankroll Settings (Step = 1 Baht as requested) ---
st.sidebar.markdown(f"### {t['bankroll_title']}")
initial_capital = st.sidebar.number_input(
    t["init_fund"], min_value=1, value=10000, step=1
)
profit_target = st.sidebar.number_input(
    t["target_profit"], min_value=1, value=2500, step=1
)
stop_loss = st.sidebar.number_input(
    t["max_loss"], min_value=1, value=2000, step=1
)
base_bet = st.sidebar.number_input(
    t["base_bet"], min_value=1, value=100, step=1
)

if "grid_history" not in st.session_state:
    initial_data = []
    for i in range(1, 51):
        initial_data.append({
            "Round": i,
            "Red Winner": False,
            "Blue Winner": False,
            "Tie (Draw)": False,
            "My P/L (฿)": 0.0,
            "Notes": "",
        })
    st.session_state.grid_history = pd.DataFrame(initial_data)

if "confirmed_data" not in st.session_state:
    st.session_state.confirmed_data = pd.DataFrame()

st.sidebar.markdown(f"### {t['sim_params']}")
game_mode = st.sidebar.radio(t["mode"], [t["mode_bacc"], t["mode_single"]])
num_sims = st.sidebar.slider(
    t["sims"], min_value=10000, max_value=50000, value=30000, step=5000
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
            "My P/L (฿)": 0.0,
            "Notes": "",
        })
    st.session_state.grid_history = pd.DataFrame(reset_data)
    st.session_state.confirmed_data = pd.DataFrame()
    st.rerun()

# --- Section 1: Editable Grid Table ---
st.markdown(f"### {t['grid_title']}")
st.markdown(t["grid_desc"])

edited_grid_df = st.data_editor(
    st.session_state.grid_history,
    num_rows="dynamic",
    use_container_width=True,
    key="grid_editor",
    column_config={
        "Round": st.column_config.NumberColumn(t["col_round"], step=1),
        "Red Winner": st.column_config.CheckboxColumn(t["col_red"]),
        "Blue Winner": st.column_config.CheckboxColumn(t["col_blue"]),
        "Tie (Draw)": st.column_config.CheckboxColumn(t["col_tie"]),
        "My P/L (฿)": st.column_config.NumberColumn(t["col_pl"], step=1.0),
        "Notes": st.column_config.TextColumn(t["col_notes"]),
    },
)

if st.button(t["confirm_btn"], type="primary", use_container_width=True):
    st.session_state.grid_history = edited_grid_df
    st.session_state.confirmed_data = edited_grid_df.copy()
    st.success(t["confirm_success"])

# Process Confirmed Rounds
processed_rounds = []
total_pl = 0.0

if not st.session_state.confirmed_data.empty:
    for idx, row in st.session_state.confirmed_data.iterrows():
        pl = float(row.get("My P/L (฿)", 0.0))
        total_pl += pl

        winner = None
        if row.get("Red Winner", False):
            winner = "Red"
        elif row.get("Blue Winner", False):
            winner = "Blue"
        elif row.get("Tie (Draw)", False):
            winner = "Tie"

        if winner:
            processed_rounds.append({"round": idx + 1, "winner": winner})

current_capital = initial_capital + total_pl
profit_progress = (
    min(100.0, max(0.0, (total_pl / profit_target) * 100))
    if profit_target > 0
    else 0.0
)

# --- Bankroll & Profit Analytics Section ---
st.markdown("---")
st.markdown(f"### {t['bankroll_section']}")
b1, b2, b3, b4 = st.columns(4)
b1.metric(
    t["curr_cap"],
    f"{current_capital:,.2f} ฿",
    f"{t['init_prefix']}: {initial_capital:,.0f} ฿",
)
b2.metric(
    t["total_pl_label"],
    f"{total_pl:+,.2f} ฿",
    f"{profit_progress:.1f}% {t['of_target']}",
)
b3.metric(t["daily_target_label"], f"{profit_target:,.2f} ฿")
b4.metric(t["max_sl_label"], f"-{stop_loss:,.2f} ฿")

if total_pl >= profit_target:
    st.markdown(
        f'<div class="target-hit">{t["target_reached"]}</div>',
        unsafe_allow_html=True,
    )
elif total_pl <= -stop_loss:
    st.markdown(
        f'<div class="stop-loss-hit">{t["sl_reached"]}</div>',
        unsafe_allow_html=True,
    )

# --- Section 2: Roadmap & Last 30-Round Analytics ---
st.markdown("---")
st.markdown(f"### {t['roadmap_title']}")

if processed_rounds:
    badges_html = ""
    for r in processed_rounds:
        if r["winner"] == "Red":
            bg = "#ef4444"
            dot_txt = t["dot_r"]
        elif r["winner"] == "Blue":
            bg = "#3b82f6"
            dot_txt = t["dot_b"]
        else:
            bg = "#10b981"
            dot_txt = t["dot_t"]
        round_num = r["round"]
        badges_html += f'<span class="history-dot" style="background-color:{bg};" title="{t[\'col_round\']} {round_num}">{dot_txt}</span>'
    st.markdown(badges_html, unsafe_allow_html=True)

    last_30_rounds = processed_rounds[-30:]
    recent_winners = [r["winner"] for r in last_30_rounds]
    r_count_30 = recent_winners.count("Red")
    b_count_30 = recent_winners.count("Blue")
    t_count_30 = recent_winners.count("Tie")
    total_30 = len(recent_winners)

    col_p1, col_p2, col_p3 = st.columns(3)
    with col_p1:
        st.markdown(
            f'<div class="metric-card"><h4>{t["last_30_red"]}</h4><h2>{r_count_30} ({r_count_30/total_30*100:.1f}%)</h2></div>',
            unsafe_allow_html=True,
        )
    with col_p2:
        st.markdown(
            f'<div class="metric-card"><h4>{t["last_30_blue"]}</h4><h2>{b_count_30} ({b_count_30/total_30*100:.1f}%)</h2></div>',
            unsafe_allow_html=True,
        )
    with col_p3:
        st.markdown(
            f'<div class="metric-card"><h4>{t["last_30_tie"]}</h4><h2>{t_count_30} ({t_count_30/total_30*100:.1f}%)</h2></div>',
            unsafe_allow_html=True,
        )

    st.caption(f"{t['total_recorded']}: **{len(processed_rounds)}**")
else:
    st.info(t["no_data"])


# --- INTENSIFIED 5-ALGORITHM ENGINE ---
def run_intensified_algorithms(rounds_history, num_sims):
    # 1. Deep Monte Carlo (Shoe Weighting)
    r_hist = sum(1 for r in rounds_history if r["winner"] == "Red")
    b_hist = sum(1 for r in rounds_history if r["winner"] == "Blue")
    total_decisive = max(1, r_hist + b_hist)
    r_weight = (r_hist + 10) / (total_decisive + 20)
    b_weight = (b_hist + 10) / (total_decisive + 20)

    sim_red, sim_blue = 0, 0
    for _ in range(num_sims):
        res = random.choices(["Red", "Blue"], weights=[r_weight, b_weight], k=1)[0]
        if res == "Red":
            sim_red += 1
        else:
            sim_blue += 1
    vote_mc = "Red" if sim_red >= sim_blue else "Blue"

    # 2. 2-Step HMM (Higher Order Markov Transition)
    vote_hmm = "Red"
    if len(rounds_history) >= 3:
        last_two = (rounds_history[-2]["winner"], rounds_history[-1]["winner"])
        r_score, b_score = 1.0, 1.0
        for i in range(len(rounds_history) - 2):
            if (rounds_history[i]["winner"], rounds_history[i + 1]["winner"]) == last_two:
                if rounds_history[i + 2]["winner"] == "Red":
                    r_score += 2.0
                elif rounds_history[i + 2]["winner"] == "Blue":
                    b_score += 2.0
        vote_hmm = "Red" if r_score >= b_score else "Blue"

    # 3. Dynamic Bayesian Inference
    vote_bayes = "Red"
    if len(rounds_history) > 0:
        recent = rounds_history[-15:]
        r_weighted = sum(1.5 if r["winner"] == "Red" else 0.5 for r in recent)
        b_weighted = sum(1.5 if r["winner"] == "Blue" else 0.5 for r in recent)
        vote_bayes = "Red" if r_weighted >= b_weighted else "Blue"

    # 4. EMA Momentum Trend (Decaying Weights)
    vote_trend = "Red"
    if len(rounds_history) > 0:
        ema_red, ema_blue = 0.0, 0.0
        decay = 1.0
        for r in reversed(rounds_history[-15:]):
            if r["winner"] == "Red":
                ema_red += decay
            elif r["winner"] == "Blue":
                ema_blue += decay
            decay *= 0.85
        vote_trend = "Red" if ema_red >= ema_blue else "Blue"

    # 5. N-Gram Pattern Matching (Deep Pattern)
    vote_pattern = "Red"
    if len(rounds_history) >= 5:
        pattern_key = [r["winner"] for r in rounds_history[-4:]]
        p_score_r, p_score_b = 0, 0
        for i in range(len(rounds_history) - 5):
            sub_pattern = [rounds_history[j]["winner"] for j in range(i, i + 4)]
            if sub_pattern == pattern_key:
                if rounds_history[i + 4]["winner"] == "Red":
                    p_score_r += 3
                elif rounds_history[i + 4]["winner"] == "Blue":
                    p_score_b += 3
        if p_score_r > p_score_b:
            vote_pattern = "Red"
        elif p_score_b > p_score_r:
            vote_pattern = "Blue"
        else:
            vote_pattern = (
                "Blue" if rounds_history[-1]["winner"] == "Blue" else "Red"
            )

    return [vote_mc, vote_hmm, vote_bayes, vote_trend, vote_pattern]


# --- Section 3: Prediction, Chart & Stake Sizing ---
st.markdown("---")
st.markdown(f"### {t['pred_title']}")

if len(processed_rounds) >= 5:
    votes = run_intensified_algorithms(processed_rounds, num_sims)

    red_count = votes.count("Red")
    blue_count = votes.count("Blue")
    max_votes = max(red_count, blue_count)
    confidence_pct = (max_votes / 5) * 100

    col1, col2, col3, col4, col5 = st.columns(5)
    algo_names = t["algo_names"]

    for col, v, name in zip([col1, col2, col3, col4, col5], votes, algo_names):
        status_color = "#ef4444" if v == "Red" else "#3b82f6"
        display_side = t["side_red"] if v == "Red" else t["side_blue"]
        col.markdown(
            f'<div class="metric-card"><h4>{name}</h4><h3 style="color: {status_color};">{display_side}</h3><p style="font-size: 11px; color: #94a3b8;">{t["status_confirmed"]}</p></div>',
            unsafe_allow_html=True,
        )

    # Consensus Chart
    st.markdown(f"#### {t['chart_title']}")
    vote_summary_df = pd.DataFrame({
        t["chart_side"]: [t["side_red"], t["side_blue"]],
        t["chart_votes"]: [red_count, blue_count],
    })
    st.bar_chart(vote_summary_df.set_index(t["chart_side"]), color="#3b82f6")

    # Dynamic Stake Sizing
    if confidence_pct == 100:
        suggested_stake = base_bet * 2.0
    elif confidence_pct >= 80:
        suggested_stake = base_bet * 1.0
    else:
        suggested_stake = 0.0

    st.markdown(f"#### {t['rec_title']}")
    st.markdown(
        f"### {t['conf_level']}: **{confidence_pct:.0f}%** ({max_votes}/5 {t['aligned']})"
    )

    @st.dialog(t["popup_title"])
    def show_signal_popup(side_text, stake_amt, pct):
        st.success(
            t["popup_body"].format(pct=pct, side=side_text, stake=stake_amt)
        )
        st.balloons()
        if st.button(t["popup_close"]):
            st.rerun()

    if red_count >= 4:
        st.markdown(
            f'<div class="big-badge consensus-pass">{t["pass_red"]}<br><br>{t["stake_label"]}: <b>{suggested_stake:,.0f} ฿</b></div>',
            unsafe_allow_html=True,
        )
        if st.button(t["popup_btn"], type="primary", use_container_width=True):
            show_signal_popup(t["side_red"], suggested_stake, confidence_pct)
    elif blue_count >= 4:
        st.markdown(
            f'<div class="big-badge consensus-pass">{t["pass_blue"]}<br><br>{t["stake_label"]}: <b>{suggested_stake:,.0f} ฿</b></div>',
            unsafe_allow_html=True,
        )
        if st.button(t["popup_btn"], type="primary", use_container_width=True):
            show_signal_popup(t["side_blue"], suggested_stake, confidence_pct)
    else:
        st.markdown(
            f'<div class="big-badge consensus-fail">{t["fail_msg"]} ({t["side_red"]}: {red_count} / {t["side_blue"]}: {blue_count})<br><br>{t["stake_label"]}: <b>{t["wait_stake"]}</b></div>',
            unsafe_allow_html=True,
        )
else:
    st.info(t["min_rounds_msg"])
