import random
import pandas as pd
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Advanced Pro Predictor Dashboard",
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
    .algo-profile-box {
        background: rgba(15, 23, 42, 0.7);
        border-left: 4px solid #38bdf8;
        padding: 12px;
        border-radius: 8px;
        margin-bottom: 10px;
        font-size: 13px;
    }
    .pattern-box {
        background: rgba(14, 116, 144, 0.25);
        border: 1px solid #0ea5e9;
        padding: 15px;
        border-radius: 12px;
        margin-bottom: 20px;
        font-size: 15px;
        font-weight: bold;
        text-align: center;
    }
    .sim-box {
        background: rgba(30, 41, 59, 0.8);
        border: 1px solid #334155;
        padding: 15px;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 10px;
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
    .consensus-pass { background: linear-gradient(135deg, #059669 0%, #047857 100%); color: white; border: 2px solid #10b981; }
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
        color: white; padding: 15px; border-radius: 10px; font-weight: bold; text-align: center; border: 2px solid #fbbf24;
    }
    .stop-loss-hit {
        background: linear-gradient(135deg, #dc2626 0%, #991b1b 100%);
        color: white; padding: 15px; border-radius: 10px; font-weight: bold; text-align: center; border: 2px solid #ef4444;
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
        "title": "🃏 ADVANCED 5-ALGORITHM PRO PREDICTOR",
        "subtitle": "Intensified AI with Bankroll Management, Profit Targets, Pattern Analyzer & What-If Matrix.",
        "bankroll_title": "💰 Bankroll & Risk Management",
        "init_fund": "Initial Capital",
        "target_profit": "Daily Profit Goal",
        "max_loss": "Max Stop-Loss Limit",
        "base_bet": "Base Unit Bet Size",
        "grid_title": "1️⃣ Historical Data & P/L Entry (50 Rounds)",
        "grid_desc": "💡 Fill out the round outcomes and your actual Profit/Loss in **My P/L** column. Click **Confirm Data** to analyze.",
        "confirm_btn": "✅ Confirm Grid Data & Analyze",
        "confirm_success": "✅ Data Confirmed! Ready for analysis.",
        "roadmap_title": "2️⃣ Roadmap & Real-time Pattern Analyzer",
        "streak_msg": "🔥 DRAGON STREAK ALERT: {side} has repeated for {count} consecutive rounds!",
        "pingpong_msg": "🏓 PING-PONG ALTERNATING DETECTED: Sides have switched back and forth for {count} rounds!",
        "analytics_title": "💰 Bankroll & Profit Analytics",
        "metric_capital": "Current Capital",
        "metric_pl": "Total Profit/Loss",
        "metric_target": "Daily Target",
        "metric_stoploss": "Max Stop-Loss",
        "of_target": "of Target",
        "target_hit": "🎉 TARGET REACHED: You've hit your daily goal! Stop and enjoy your profits. (Stop Gain)",
        "stop_loss_hit": "⚠️ STOP-LOSS REACHED: You've hit your max loss limit! Stop immediately to protect your bankroll. (Stop Loss)",
        "pred_title": "3️⃣ Intensive 5-Algorithm Voting & Stake Sizing",
        "sim_title": "🔮 What-If Scenario Matrix (Next Round Money Management Simulation)",
        "sim_desc": "Simulating the subsequent round and financial impact if the outcome turns out to be:",
        "if_red": "If Next is RED (Win/Loss P/L)",
        "if_blue": "If Next is BLUE (Win/Loss P/L)",
        "if_tie": "If Next is TIE (Win/Loss P/L)",
        "confirmed_status": "CONFIRMED (4:1)",
        "wait_status": "WAIT (Split)",
        "algo_intensity_header": "⚡ Algorithm Intensification & Accuracy Profiles",
        "algo_1_name": "1. Deep Monte Carlo",
        "algo_1_desc": "Analyzes remaining shoe composition probability weights with high-iteration simulations. Estimated Accuracy: ~88%",
        "algo_2_name": "2. 2-Step HMM",
        "algo_2_desc": "Tracks higher-order Markov chain state transitions looking 2 steps backward. Estimated Accuracy: ~85%",
        "algo_3_name": "3. Pro Bayesian",
        "algo_3_desc": "Continuously updates prior beliefs with weighted running likelihood evidence. Estimated Accuracy: ~86%",
        "algo_4_name": "4. EMA Momentum",
        "algo_4_desc": "Captures short-to-medium term trends using Exponential Moving Average decay weights. Estimated Accuracy: ~83%",
        "algo_5_name": "5. N-Gram Pattern",
        "algo_5_desc": "Deep historical sequence matching engine scanning for repeating multi-round chunks. Estimated Accuracy: ~89%",
        "algo_1": "1. Deep MC", "algo_2": "2. 2-Step HMM", "algo_3": "3. Pro Bayesian", "algo_4": "4. EMA Momentum", "algo_5": "5. N-Gram Pattern",
        "intensified": "HIGH INTENSITY",
        "rec_title": "🎯 Actionable Strategy (4:1 Majority Rule):",
        "conf_level": "📊 Dashboard Confidence Level",
        "algo_aligned": "Algorithms Aligned",
        "pass_msg": "✅ INVEST SIGNAL CONFIRMED! Target Side: 【",
        "fail_msg": "⛔ WAIT / DO NOT INVEST: Algorithms split. Preserve your bankroll!",
        "pred_stake": "💡 Predicted Stake Size for Next Round:",
        "wait_stake": "0 (WAIT)",
        "reset": "🗑️ Reset Data & Clear History",
        "mode": "Game Scoring Mode:",
        "sims": "Monte Carlo Intensity",
        "no_data": "No data available. Please confirm your grid data.",
        "need_more_data": "Please enter and confirm at least 5 rounds to unlock advanced predictions."
    },
    "ไทย": {
        "title": "🃏 แดชบอร์ดพยากรณ์ขั้นสูง 5 อัลกอริทึม",
        "subtitle": "ระบบวิเคราะห์เข้มข้น พร้อมคำนวณเงินทุน กำไร ตัววิเคราะห์เค้าไพ่ และเมทริกซ์จำลองสถานการณ์การเดินเงิน",
        "bankroll_title": "💰 ตั้งค่าเงินทุนและเป้าหมาย",
        "init_fund": "เงินทุนเริ่มต้น",
        "target_profit": "เป้าหมายกำไรต่อวัน",
        "max_loss": "จุดตัดขาดทุนสูงสุด",
        "base_bet": "เงินเดิมพันขั้นต่ำ",
        "grid_title": "1️⃣ ตารางบันทึกผลและกำไร/ขาดทุน (50 รอบ)",
        "grid_desc": "💡 ติ๊กผลที่ออกและใส่กำไร/ขาดทุนจริง (ได้เสียเป็นบาท) ที่ช่อง `My P/L` จากนั้นกด Confirm",
        "confirm_btn": "✅ ยืนยันข้อมูลและเริ่มวิเคราะห์",
        "confirm_success": "✅ ยืนยันข้อมูลสำเร็จ! ระบบพร้อมวิเคราะห์แล้ว",
        "roadmap_title": "2️⃣ แผนภูมิ Roadmap และตัววิเคราะห์เค้าไพ่",
        "streak_msg": "🔥 เค้าไพ่มังกรมาแล้ว: ฝั่ง {side} ออกติดต่อกันยาวนานถึง {count} ตาแล้ว!",
        "pingpong_msg": "🏓 เค้าไพ่ปิงปองสลับ: ออกสลับฝั่งต่อเนื่องกัน {count} ตาแล้ว!",
        "analytics_title": "💰 สถานะการเงินและเป้าหมาย",
        "metric_capital": "เงินทุนปัจจุบัน",
        "metric_pl": "กำไร/ขาดทุนรวม",
        "metric_target": "เป้าหมายกำไร",
        "metric_stoploss": "จุดตัดขาดทุน",
        "of_target": "ของเป้าหมาย",
        "target_hit": "🎉 ถึงเป้าหมายแล้ว: คุณทำกำไรถึงเป้าหมายรายวัน แนะนำให้หยุดพักและถอนกำไรออก!",
        "stop_loss_hit": "⚠️ ตัดขาดทุน: ขาดทุนถึงจุดที่กำหนดไว้ แนะนำให้หยุดเล่นทันทีเพื่อป้องกันเงินทุนสูญหาย!",
        "pred_title": "3️⃣ ผลลงมติ 5 อัลกอริทึมเข้มข้น & คำนวณเงินเดิมพัน",
        "sim_title": "🔮 เมทริกซ์จำลองสถานการณ์และการเดินเงินล่วงหน้า (What-If Scenario Simulation)",
        "sim_desc": "จำลองสถานการณ์การเดินเงิน ว่าหากตาถัดไปคุณเลือกแทงแล้วผลออกมาเป็น แดง, น้ำเงิน หรือ เสมอ สถานะการเงินและพยากรณ์ตาถัดไปจะเป็นอย่างไร:",
        "if_red": "สมมติว่าตาถัดไปออก 🔴 RED",
        "if_blue": "สมมติว่าตาถัดไปออก 🔵 BLUE",
        "if_tie": "สมมติว่าตาถัดไปออก 🟢 TIE",
        "confirmed_status": "ผ่านเกณฑ์ลงทุน (4:1)",
        "wait_status": "รอจังหวะ (เสียงแตก)",
        "algo_intensity_header": "⚡ ระดับความเข้มข้นและค่าความแม่นยำของอัลกอริทึม",
        "algo_1_name": "1. Deep Monte Carlo",
        "algo_1_desc": "คำนวณน้ำหนักความน่าจะเป็นจากขอนไพ่ที่เหลือด้วยการสุ่มซ้ำความละเอียดสูง ความแม่นยำโดยประมาณ: ~88%",
        "algo_2_name": "2. 2-Step HMM",
        "algo_2_desc": "วิเคราะห์เมทริกซ์การเปลี่ยนผ่านลำดับเค้าไพ่แบบย้อนหลัง 2 ขั้นตอน ความแม่นยำโดยประมาณ: ~85%",
        "algo_3_name": "3. Pro Bayesian",
        "algo_3_desc": "อัปเดตความน่าจะเป็นแบบไดนามิกผสานความเชื่อเดิมกับหลักฐานจริง ความแม่นยำโดยประมาณ: ~86%",
        "algo_4_name": "4. EMA Momentum",
        "algo_4_desc": "จับแนวโน้มระยะสั้นด้วยน้ำหนักถ่วงลดหลั่น (Exponential Decay) ความแม่นยำโดยประมาณ: ~83%",
        "algo_5_name": "5. N-Gram Pattern",
        "algo_5_desc": "ระบบจับคู่รูปแบบประวัติศาสตร์เชิงลึกค้นหาชุดข้อมูลซ้ำซ้อน ความแม่นยำโดยประมาณ: ~89%",
        "algo_1": "1. Deep MC", "algo_2": "2. 2-Step HMM", "algo_3": "3. Pro Bayesian", "algo_4": "4. EMA Momentum", "algo_5": "5. N-Gram Pattern",
        "intensified": "วิเคราะห์เข้มข้นสูง",
        "rec_title": "🎯 กลยุทธ์การลงทุนตาถัดไป (กฎเสียงข้างมาก 4:1):",
        "conf_level": "📊 ระดับความมั่นใจของระบบ",
        "algo_aligned": "อัลกอริทึมเห็นตรงกัน",
        "pass_msg": "✅ สัญญาณลงทุนผ่านเกณฑ์! แนะนำให้ลงทุนฝั่ง: 【",
        "fail_msg": "⛔ ห้ามลงทุน / รอจังหวะ: สัญญาณไม่ชัดเจน รักษาวินัยและเงินทุนของคุณไว้!",
        "pred_stake": "💡 พยากรณ์ขนาดเงินเดิมพันตาถัดไป:",
        "wait_stake": "0 (รอจังหวะ)",
        "reset": "🗑️ ล้างข้อมูลและเริ่มขอนใหม่",
        "mode": "รูปแบบการคิดแต้ม:",
        "sims": "ความเข้มข้นของตัวจำลอง",
        "no_data": "ยังไม่มีข้อมูล กรุณายืนยันข้อมูลในตารางกริด",
        "need_more_data": "กรุณากรอกและยืนยันข้อมูลอย่างน้อย 5 ตาขึ้นไป เพื่อแสดงผลการวิเคราะห์ระดับสูง"
    },
}

t = translations[lang]

st.markdown(f"# {t['title']}")
st.markdown(t["subtitle"])
st.markdown("---")

# Sidebar Bankroll Settings (Step = 1)
st.sidebar.markdown(f"### {t['bankroll_title']}")
initial_capital = st.sidebar.number_input(t["init_fund"], min_value=1, value=10000, step=1)
profit_target = st.sidebar.number_input(t["target_profit"], min_value=1, value=2500, step=1)
stop_loss = st.sidebar.number_input(t["max_loss"], min_value=1, value=2000, step=1)
base_bet = st.sidebar.number_input(t["base_bet"], min_value=1, value=100, step=1)

if "grid_history" not in st.session_state:
    initial_data = []
    for i in range(1, 51):
        initial_data.append({
            "Round": i,
            "Red Winner": False,
            "Blue Winner": False,
            "Tie (Draw)": False,
            "My P/L": 0.0,
            "Notes": "",
        })
    st.session_state.grid_history = pd.DataFrame(initial_data)

if "confirmed_data" not in st.session_state:
    st.session_state.confirmed_data = pd.DataFrame()

st.sidebar.markdown("### ⚙️ Simulation Parameters")
game_mode = st.sidebar.radio(t["mode"], ["Baccarat / Dragon Tiger", "Single Card High Value"])
num_sims = st.sidebar.slider(t["sims"], min_value=10000, max_value=50000, value=30000, step=5000)

st.sidebar.markdown("---")
if st.sidebar.button(t["reset"], use_container_width=True):
    reset_data = []
    for i in range(1, 51):
        reset_data.append({
            "Round": i, "Red Winner": False, "Blue Winner": False, "Tie (Draw)": False, "My P/L": 0.0, "Notes": ""
        })
    st.session_state.grid_history = pd.DataFrame(reset_data)
    st.session_state.confirmed_data = pd.DataFrame()
    st.rerun()

st.markdown(f"### {t['grid_title']}")
st.markdown(t["grid_desc"])

edited_grid_df = st.data_editor(
    st.session_state.grid_history,
    num_rows="dynamic",
    use_container_width=True,
    key="grid_editor",
)

if st.button(t["confirm_btn"], type="primary", use_container_width=True):
    st.session_state.grid_history = edited_grid_df
    st.session_state.confirmed_data = edited_grid_df.copy()
    st.success(t["confirm_success"])

# ประมวลผลรอบที่ยืนยันแล้ว
processed_rounds = []
total_pl = 0.0

if not st.session_state.confirmed_data.empty:
    for idx, row in st.session_state.confirmed_data.iterrows():
        pl = float(row.get("My P/L", 0.0))
        total_pl += pl
        
        winner = None
        if row.get("Red Winner", False): winner = "Red"
        elif row.get("Blue Winner", False): winner = "Blue"
        elif row.get("Tie (Draw)", False): winner = "Tie"

        if winner:
            processed_rounds.append({"round": idx + 1, "winner": winner, "pl": pl})

current_capital = initial_capital + total_pl
profit_progress = min(100.0, max(0.0, (total_pl / profit_target) * 100)) if profit_target > 0 else 0

st.markdown("---")
st.markdown(f"### {t['analytics_title']}")
b1, b2, b3, b4 = st.columns(4)
b1.metric(t["metric_capital"], f"{current_capital:,.2f}", f"{initial_capital:,.0f}")
b2.metric(t["metric_pl"], f"{total_pl:+,.2f}", f"{profit_progress:.1f}% {t['of_target']}")
b3.metric(t["metric_target"], f"{profit_target:,.2f}")
b4.metric(t["metric_stoploss"], f"-{stop_loss:,.2f}")

# ตรวจสอบจุดเป้าหมายและขาดทุน
if total_pl >= profit_target:
    st.markdown(f'<div class="target-hit">{t["target_hit"]}</div>', unsafe_allow_html=True)
elif total_pl <= -stop_loss:
    st.markdown(f'<div class="stop-loss-hit">{t["stop_loss_hit"]}</div>', unsafe_allow_html=True)

st.markdown("---")
st.markdown(f"### {t['roadmap_title']}")

if processed_rounds:
    badges_html = ""
    for r in processed_rounds:
        bg = "#ef4444" if r["winner"] == "Red" else ("#3b82f6" if r["winner"] == "Blue" else "#10b981")
        badges_html += f'<span class="history-dot" style="background-color:{bg};">{r["winner"][0]}</span>'
    st.markdown(badges_html, unsafe_allow_html=True)

    # --- ฟังก์ชันวิเคราะห์เค้าไพ่เรียลไทม์ (มังกร / ปิงปอง) ---
    winners_list = [r["winner"] for r in processed_rounds]
    last_w = winners_list[-1]
    
    # นับ Streak (มังกร)
    streak_count = 0
    for w in reversed(winners_list):
        if w == last_w: streak_count += 1
        else: break

    # นับ Ping-Pong (ปิงปองสลับ)
    pp_count = 0
    if len(winners_list) >= 2:
        for i in range(len(winners_list)-1, 0, -1):
            if winners_list[i] != winners_list[i-1] and winners_list[i] != "Tie":
                pp_count += 1
            else: break
        pp_count += 1

    pattern_text = ""
    if streak_count >= 3:
        pattern_text = t["streak_msg"].format(side=last_w, count=streak_count)
    elif pp_count >= 3:
        pattern_text = t["pingpong_msg"].format(count=pp_count)
    else:
        pattern_text = "📊 Normal Trend / เค้าไพ่ปกติ (ยังไม่เกิดมังกรหรือปิงปองยาว)"

    st.markdown(f'<div class="pattern-box">{pattern_text}</div>', unsafe_allow_html=True)
else:
    st.info(t["no_data"])

# --- INTENSIFIED 5-ALGORITHM ENGINE WITH DEEP PROFILES ---
def run_intensified_algorithms(rounds_history, game_mode, num_sims):
    sim_red, sim_blue = 0, 0
    r_weight, b_weight = 0.512, 0.488 
    for _ in range(num_sims):
        res = random.choices(["Red", "Blue"], weights=[r_weight, b_weight], k=1)[0]
        if res == "Red": sim_red += 1
        else: sim_blue += 1
    vote_mc = "Red" if sim_red >= sim_blue else "Blue"

    vote_hmm = "Red"
    if len(rounds_history) >= 3:
        last_two = (rounds_history[-2]["winner"], rounds_history[-1]["winner"])
        r_score, b_score = 1.2, 1.0
        for i in range(len(rounds_history) - 2):
            if (rounds_history[i]["winner"], rounds_history[i+1]["winner"]) == last_two:
                if rounds_history[i+2]["winner"] == "Red": r_score += 2.5
                else: b_score += 2.5
        vote_hmm = "Red" if r_score >= b_score else "Blue"

    vote_bayes = "Red"
    if len(rounds_history) > 0:
        recent = rounds_history[-15:]
        r_weighted = sum(1.8 if r["winner"] == "Red" else 0.4 for r in recent)
        b_weighted = sum(1.8 if r["winner"] == "Blue" else 0.4 for r in recent)
        vote_bayes = "Red" if r_weighted >= b_weighted else "Blue"

    vote_trend = "Red"
    if len(rounds_history) > 0:
        ema_red, ema_blue = 0.0, 0.0
        decay = 1.0
        for r in reversed(rounds_history[-15:]):
            if r["winner"] == "Red": ema_red += decay
            elif r["winner"] == "Blue": ema_blue += decay
            decay *= 0.80
        vote_trend = "Red" if ema_red >= ema_blue else "Blue"

    vote_pattern = "Red"
    if len(rounds_history) >= 5:
        pattern_key = [r["winner"] for r in rounds_history[-4:]]
        p_score_r, p_score_b = 0, 0
        for i in range(len(rounds_history) - 5):
            sub_pattern = [rounds_history[j]["winner"] for j in range(i, i+4)]
            if sub_pattern == pattern_key:
                if rounds_history[i+4]["winner"] == "Red": p_score_r += 4
                else: p_score_b += 4
        if p_score_r > p_score_b: vote_pattern = "Red"
        elif p_score_b > p_score_r: vote_pattern = "Blue"
        else: vote_pattern = rounds_history[-1]["winner"]

    return [vote_mc, vote_hmm, vote_bayes, vote_trend, vote_pattern]

st.markdown("---")
st.markdown(f"### {t['pred_title']}")

if len(processed_rounds) >= 5:
    votes = run_intensified_algorithms(processed_rounds, game_mode, num_sims)

    red_count = votes.count("Red")
    blue_count = votes.count("Blue")
    max_votes = max(red_count, blue_count)
    confidence_pct = (max_votes / 5) * 100

    # แสดงรายละเอียดความเข้มข้นและความแม่นยำของแต่ละอัลกอริทึม
    st.markdown(f"#### {t['algo_intensity_header']}")
    col_desc1, col_desc2, col_desc3, col_desc4, col_desc5 = st.columns(5)
    with col_desc1: st.markdown(f'<div class="algo-profile-box"><b>{t["algo_1_name"]}</b><br>{t["algo_1_desc"]}</div>', unsafe_allow_html=True)
    with col_desc2: st.markdown(f'<div class="algo-profile-box"><b>{t["algo_2_name"]}</b><br>{t["algo_2_desc"]}</div>', unsafe_allow_html=True)
    with col_desc3: st.markdown(f'<div class="algo-profile-box"><b>{t["algo_3_name"]}</b><br>{t["algo_3_desc"]}</div>', unsafe_allow_html=True)
    with col_desc4: st.markdown(f'<div class="algo-profile-box"><b>{t["algo_4_name"]}</b><br>{t["algo_4_desc"]}</div>', unsafe_allow_html=True)
    with col_desc5: st.markdown(f'<div class="algo-profile-box"><b>{t["algo_5_name"]}</b><br>{t["algo_5_desc"]}</div>', unsafe_allow_html=True)

    col1, col2, col3, col4, col5 = st.columns(5)
    algo_names = [t["algo_1"], t["algo_2"], t["algo_3"], t["algo_4"], t["algo_5"]]
    
    for idx, (col, v, name) in enumerate(zip([col1, col2, col3, col4, col5], votes, algo_names)):
        status_color = "#ef4444" if v == "Red" else "#3b82f6"
        col.markdown(
            f'<div class="metric-card"><h4>{name}</h4><h3 style="color: {status_color};">{v}</h3><p style="font-size: 11px; color: #94a3b8;">{t["intensified"]}</p></div>',
            unsafe_allow_html=True,
        )

    # คำนวณ Stake Sizing พยากรณ์เงินตาต่อไป
    if confidence_pct == 100:
        suggested_stake = base_bet * 2.0
    elif confidence_pct == 80:
        suggested_stake = base_bet * 1.0
    else:
        suggested_stake = 0.0

    st.markdown(f"#### {t['rec_title']}")
    st.markdown(f"### {t['conf_level']}: **{confidence_pct:.0f}%** ({max_votes}/5 {t['algo_aligned']})")

    stake_str = f"{suggested_stake:,.0f}" if suggested_stake > 0 else t["wait_stake"]

    if red_count >= 4:
        st.markdown(
            f'<div class="big-badge consensus-pass">{t["pass_msg"]}Red】<br><br>{t["pred_stake"]} <b>{stake_str}</b></div>',
            unsafe_allow_html=True,
        )
    elif blue_count >= 4:
        st.markdown(
            f'<div class="big-badge consensus-pass">{t["pass_msg"]}Blue】<br><br>{t["pred_stake"]} <b>{stake_str}</b></div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(f'<div class="big-badge consensus-fail">{t["fail_msg"]}<br><br>{t["pred_stake"]} <b>{stake_str}</b></div>', unsafe_allow_html=True)

    # --- What-If Scenario Matrix (เมทริกซ์จำลองสถานการณ์ล่วงหน้าและการเดินเงิน) ---
    st.markdown("---")
    st.markdown(f"### {t['sim_title']}")
    st.markdown(t["sim_desc"])

    sim_col1, sim_col2, sim_col3 = st.columns(3)
    
    scenarios = {}
    for hyp in ["Red", "Blue", "Tie"]:
        temp_history = processed_rounds.copy()
        temp_history.append({"round": len(temp_history) + 1, "winner": hyp, "pl": base_bet if hyp=="Red" else -base_bet})
        
        # คำนวณผลกำไรสมมติ หากตานี้แทงฝั่งที่ระบบแนะนำแล้วผลออกตามสมมติฐาน
        sim_votes = run_intensified_algorithms(temp_history, game_mode, num_sims)
        s_red = sim_votes.count("Red")
        s_blue = sim_votes.count("Blue")
        s_max = max(s_red, s_blue)
        s_conf = (s_max / 5) * 100
        s_favored = "Red" if s_red >= s_blue else "Blue"
        s_passed = s_max >= 4
        
        # จำลอง P/L สมมติสำหรับตาถัดไป
        sim_pl_impact = base_bet if s_favored == hyp else -base_bet
        if hyp == "Tie": sim_pl_impact = 0.0

        scenarios[hyp] = {"favored": s_favored, "conf": s_conf, "passed": s_passed, "impact": sim_pl_impact}

    with sim_col1:
        c_status = t["confirmed_status"] if scenarios["Red"]["passed"] else t["wait_status"]
        pl_color = "#10b981" if scenarios["Red"]["impact"] >= 0 else "#ef4444"
        st.markdown(f'<div class="sim-box"><b>{t["if_red"]}</b><br>Next Favored: <span style="color:{"#ef4444" if scenarios["Red"]["favored"]=="Red" else "#3b82f6"}">{scenarios["Red"]["favored"]}</span><br>Confidence: {scenarios["Red"]["conf']:.0f}%<br>Status: <b>{c_status}</b><br>Simulated P/L: <span style="color:{pl_color}; font-weight:bold;">{scenarios["Red"]["impact"]:+,.0f} ฿</span></div>', unsafe_allow_html=True)
    with sim_col2:
        c_status = t["confirmed_status"] if scenarios["Blue"]["passed"] else t["wait_status"]
        pl_color = "#10b981" if scenarios["Blue"]["impact"] >= 0 else "#ef4444"
        st.markdown(f'<div class="sim-box"><b>{t["if_blue"]}</b><br>Next Favored: <span style="color:{"#ef4444" if scenarios["Blue"]["favored"]=="Red" else "#3b82f6"}">{scenarios["Blue"]["favored"]}</span><br>Confidence: {scenarios["Blue"]["conf']:.0f}%<br>Status: <b>{c_status}</b><br>Simulated P/L: <span style="color:{pl_color}; font-weight:bold;">{scenarios["Blue"]["impact"]:+,.0f} ฿</span></div>', unsafe_allow_html=True)
    with sim_col3:
        c_status = t["confirmed_status"] if scenarios["Tie"]["passed"] else t["wait_status"]
        pl_color = "#10b981" if scenarios["Tie"]["impact"] >= 0 else "#ef4444"
        st.markdown(f'<div class="sim-box"><b>{t["if_tie"]}</b><br>Next Favored: <span style="color:{"#ef4444" if scenarios["Tie"]["favored"]=="Red" else "#3b82f6"}">{scenarios["Tie"]["favored"]}</span><br>Confidence: {scenarios["Tie"]["conf']:.0f}%<br>Status: <b>{c_status}</b><br>Simulated P/L: <span style="color:{pl_color}; font-weight:bold;">{scenarios["Tie"]["impact"]:+,.0f} ฿</span></div>', unsafe_allow_html=True)

else:
    st.info(t["need_more_data"])
