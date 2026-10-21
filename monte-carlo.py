import math
import random
import pandas as pd
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Advanced 12-Algorithm Pro Predictor Dashboard",
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
        padding: 16px;
        border-radius: 16px;
        box-shadow: 0 10px 30px 0 rgba(0, 0, 0, 0.6);
        text-align: center;
        margin-bottom: 12px;
    }
    .metric-card-synergy {
        background: rgba(15, 23, 42, 0.9);
        backdrop-filter: blur(14px);
        border: 1px solid rgba(16, 185, 129, 0.55);
        padding: 14px;
        border-radius: 14px;
        box-shadow: 0 8px 24px 0 rgba(0, 0, 0, 0.55);
        text-align: center;
        margin-bottom: 12px;
    }
    .algo-profile-box {
        background: rgba(15, 23, 42, 0.7);
        border-left: 4px solid #38bdf8;
        padding: 12px;
        border-radius: 8px;
        margin-bottom: 10px;
        font-size: 13px;
    }
    .algo-synergy-box {
        background: rgba(6, 78, 59, 0.25);
        border-left: 4px solid #10b981;
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
        margin-bottom: 15px;
        font-size: 15px;
        font-weight: bold;
        text-align: center;
    }
    .sniper-box {
        background: rgba(16, 185, 129, 0.15);
        border: 1px solid #10b981;
        padding: 15px;
        border-radius: 12px;
        margin-bottom: 15px;
        font-size: 15px;
        text-align: center;
    }
    .volatility-box {
        background: rgba(220, 38, 38, 0.2);
        border: 1px solid #ef4444;
        padding: 15px;
        border-radius: 12px;
        margin-bottom: 15px;
        font-size: 15px;
        font-weight: bold;
        text-align: center;
        color: #fca5a5;
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
        "title": "🃏 ADVANCED 12-ALGORITHM SYNERGY PRO PREDICTOR (SNIPER EDITION)",
        "subtitle": "5 Core Engines + 7 Blind-Spot Complementary Algorithms with Self-Backtesting, Bankroll Management & What-If Matrix.",
        "bankroll_title": "💰 Bankroll & Risk Management",
        "init_fund": "Initial Capital",
        "target_profit": "Daily Profit Goal",
        "max_loss": "Max Stop-Loss Limit",
        "base_bet": "Base Unit Bet Size",
        "strict_mode_label": "🛡️ Decision Strictness Mode:",
        "mode_sniper": "Sniper Mode (Ultra-Careful: 12-Algo Synergy Filter)",
        "mode_standard": "Standard Majority Mode",
        "min_vote_label": "Minimum Algorithms Aligned (out of 12):",
        "grid_title": "1️⃣ Historical Data & P/L Entry (50 Rounds)",
        "grid_desc": "💡 Fill out round outcomes and actual Profit/Loss in **My P/L**. Click **Confirm Data** to analyze.",
        "confirm_btn": "✅ Confirm Grid Data & Analyze",
        "confirm_success": "✅ Data Confirmed! 12-Algorithm synergy & walk-forward backtest updated.",
        "roadmap_title": "2️⃣ Roadmap & Real-time Pattern Analyzer",
        "streak_msg": "🔥 DRAGON STREAK ALERT: {side} has repeated for {count} consecutive rounds! (Historical Max Ceiling: {max_c})",
        "pingpong_msg": "🏓 PING-PONG ALTERNATING DETECTED: Sides have switched back and forth for {count} rounds!",
        "lcut_msg": "📐 L-PATTERN / CUT-POINT DETECTED: Current streak ({count}) reached historical cut ceiling ({max_c}). High probability of switching side!",
        "normal_msg": "📊 Normal Rhythm: Current streak is {count} on {side} (Shoe Max Streak: {max_c}).",
        "volatility_warning": "⚠️ SNIPER GUARD BLOCKED: High Entropy / Cut-Point Trap / Specialist Disagreement! Forced to WAIT to protect win rate.",
        "backtest_summary": "🎯 **Real-Time 12-Algo Shoe Backtest (Walk-Forward Validation):** Triggered **{total_bets}** sniper signals in this shoe ➡️ **Won: {wins}** | **Lost: {losses}** (Actual Win Rate: **{wr:.1f}%**)",
        "backtest_waiting": "🔍 **Real-Time 12-Algo Shoe Backtest:** Calibrating shoe rhythm... Waiting for high-certainty sniper setups.",
        "analytics_title": "💰 Bankroll & Profit Analytics",
        "metric_capital": "Current Capital",
        "metric_pl": "Total Profit/Loss",
        "metric_target": "Daily Target",
        "metric_stoploss": "Max Stop-Loss",
        "of_target": "of Target",
        "target_hit": "🎉 TARGET REACHED: You've hit your daily goal! Stop and enjoy your profits. (Stop Gain)",
        "stop_loss_hit": "⚠️ STOP-LOSS REACHED: You've hit your max loss limit! Stop immediately to protect your bankroll. (Stop Loss)",
        "pred_title": "3️⃣ Intensive 12-Algorithm Synergy Voting, Shoe Accuracy & Stake Sizing",
        "orig_5_header": "🔵 Core 5 Algorithms (Original Foundation Engines)",
        "new_7_header": "🟢 New 7 Complementary Algorithms (Blind-Spot Correctors & Synergy Boosters)",
        "sim_title": "🔮 What-If Scenario Matrix (Next Round Money Management Simulation)",
        "sim_desc": "Simulating the subsequent round and financial impact if the outcome turns out to be:",
        "if_red": "If Next is RED (Win/Loss P/L)",
        "if_blue": "If Next is BLUE (Win/Loss P/L)",
        "if_tie": "If Next is TIE (Win/Loss P/L)",
        "confirmed_status": "CONFIRMED (SNIPER PASS)",
        "wait_status": "WAIT (Filtered/Unsafe)",
        "algo_intensity_header": "⚡ 12-Algorithm Synergy & Blind-Spot Coverage Profiles",
        "algo_1_name": "1. True Shoe Equilibrium MC",
        "algo_1_desc": "[Core] Simulates remaining shoe card density & equilibrium pull.",
        "algo_2_name": "2. Multi-Order HMM (1-3 Step)",
        "algo_2_desc": "[Core] Evaluates 1, 2, and 3-step Markov transition matrices.",
        "algo_3_name": "3. Bayesian Run-Length",
        "algo_3_desc": "[Core] Calculates streak survival vs. cut probability from shoe ceiling.",
        "algo_4_name": "4. Regime & Rhythm AI",
        "algo_4_desc": "[Core] Detects active table regime (Ping-Pong, 2-2 Pair, L-Cut, Dragon).",
        "algo_5_name": "5. Multi-Scale N-Gram",
        "algo_5_desc": "[Core] Scans exact 3, 4, and 5-Gram historical sequences.",
        "algo_6_name": "6. Derived Roads AI (3 Roads)",
        "algo_6_desc": "[Fixes Algo 3 & 4] Computes Big Eye, Small Road & Cockroach symmetry across columns.",
        "algo_7_name": "7. Fuzzy K-NN Matcher",
        "algo_7_desc": "[Fixes Algo 5] Finds closest 6-round patterns allowing 1 bit of noise/glitch.",
        "algo_8_name": "8. Z-Score Mean Reversion",
        "algo_8_desc": "[Fixes Algo 1] Detects statistical overextension (|Z|>1.65) to catch snap-back reversals.",
        "algo_9_name": "9. Streak-to-Streak Matrix",
        "algo_9_desc": "[Fixes Algo 2 & 3] Tracks column-length transitions (e.g., what follows a 1-cut or 2-cut).",
        "algo_10_name": "10. Tie-Shock Catalyst",
        "algo_10_desc": "[Fixes All Algos] Analyzes post-Tie state shifts and parity alternation momentum.",
        "algo_11_name": "11. MACD & RSI Oscillator",
        "algo_11_desc": "[Fixes Momentum Lag] Compares Fast (3) vs. Slow (10) EMA crossover & RSI turning points.",
        "algo_12_name": "12. Meta-Critic Anti-Trap",
        "algo_12_desc": "[Fixes False Positives] Detects pattern traps when standard algos miss and flips to fade.",
        "algo_1": "1. Shoe MC", "algo_2": "2. Multi-HMM", "algo_3": "3. Bayes Cut", "algo_4": "4. Regime AI", "algo_5": "5. N-Gram Pro",
        "algo_6": "6. Derived Roads", "algo_7": "7. Fuzzy K-NN", "algo_8": "8. Z-Reversion", "algo_9": "9. Col-Matrix", "algo_10": "10. Tie-Catalyst", "algo_11": "11. MACD/RSI", "algo_12": "12. Meta-Critic",
        "shoe_acc_label": "Shoe Accuracy",
        "chart_header": "📊 12-Algorithm Consensus Vote Distribution",
        "rec_title": "🎯 Actionable Strategy (12-Algorithm Synergy + Sniper Gatekeeper):",
        "conf_level": "📊 Weighted 12-Algo Sniper Confidence",
        "algo_aligned": "Algorithms Aligned",
        "pass_msg": "✅ SNIPER 12-ALGO SIGNAL CONFIRMED! Target Side: 【",
        "fail_msg": "⛔ WAIT / DO NOT INVEST: Signal did not pass 12-Algorithm Sniper Safety Filter. Preserve your bankroll!",
        "pred_stake": "💡 Predicted Stake Size for Next Round:",
        "wait_stake": "0 (WAIT - SKIP ROUND)",
        "reset": "🗑️ Reset Data & Clear History",
        "mode": "Game Scoring Mode:",
        "sims": "Monte Carlo Intensity",
        "no_data": "No data available. Please confirm your grid data.",
        "need_more_data": "Please enter and confirm at least 5 rounds to unlock 12-Algorithm Sniper predictions."
    },
    "ไทย": {
        "title": "🃏 แดชบอร์ดพยากรณ์ขั้นสูง 12 อัลกอริทึมเสริมจุดบอด (รุ่นสไนเปอร์ คิดรอบคอบ)",
        "subtitle": "ผสาน 5 อัลกอริทึมหลัก + 7 อัลกอริทึมใหม่อุดจุดบอดซึ่งกันและกัน พร้อมระบบตรวจข้อสอบจริงในขอน และจำลองการเดินเงิน",
        "bankroll_title": "💰 ตั้งค่าเงินทุนและเป้าหมาย",
        "init_fund": "เงินทุนเริ่มต้น",
        "target_profit": "เป้าหมายกำไรต่อวัน",
        "max_loss": "จุดตัดขาดทุนสูงสุด",
        "base_bet": "เงินเดิมพันขั้นต่ำ",
        "strict_mode_label": "🛡️ โหมดความรอบคอบในการคัดสัญญาณ:",
        "mode_sniper": "โหมดสไนเปอร์ 12 อัลกอริทึม (คิดรอบคอบสูงสุด อุดจุดบอดครบทุกมิติ)",
        "mode_standard": "โหมดเสียงข้างมากมาตรฐาน",
        "min_vote_label": "จำนวนอัลกอริทึมขั้นต่ำที่ต้องเห็นตรงกัน (จาก 12 ตัว):",
        "grid_title": "1️⃣ ตารางบันทึกผลและกำไร/ขาดทุน (50 รอบ)",
        "grid_desc": "💡 ติ๊กผลที่ออกและใส่กำไร/ขาดทุนจริง (ได้เสียเป็นบาท) ที่ช่อง `My P/L` จากนั้นกด Confirm",
        "confirm_btn": "✅ ยืนยันข้อมูลและเริ่มวิเคราะห์เชิงลึก (12 อัลกอริทึม)",
        "confirm_success": "✅ ยืนยันข้อมูลสำเร็จ! ประมวลผล 12 อัลกอริทึมและตรวจข้อสอบย้อนหลังเรียบร้อยแล้ว",
        "roadmap_title": "2️⃣ แผนภูมิ Roadmap และตัววิเคราะห์เค้าไพ่/จุดตัด",
        "streak_msg": "🔥 เค้าไพ่มังกร: ฝั่ง {side} ออกติดกัน {count} ตา! (สถิติสูงสุดขอนนี้เคยยาวสุด: {max_c} ตา)",
        "pingpong_msg": "🏓 เค้าไพ่ปิงปอง: ออกสลับฝั่งกันมาแล้ว {count} ตาติด!",
        "lcut_msg": "📐 แจ้งเตือนจุดเสี่ยงไพ่ตัด (ขา L): แถวปัจจุบัน ({count} ตา) ชนเพดานที่ขอนนี้ชอบตัด ({max_c} ตา) ระวังไพ่ตัดเปลี่ยนสี!",
        "normal_msg": "📊 จังหวะเค้าไพ่ปกติ: ล่าสุดออก {side} ติดกัน {count} ตา (ขอนนี้เคยไหลยาวสุด {max_c} ตา)",
        "volatility_warning": "⚠️ ระบบสไนเปอร์ 12 อัลกอริทึมสั่งเบรก (BLOCKED): พบสัญญาณขัดแย้งจากตัวอุดจุดบอด / เสี่ยงไพ่ตัด / ขอนแกว่งตัวสูง! บังคับเป็น WAIT เพื่อเซฟเงินทุน",
        "backtest_summary": "🎯 **ผลตรวจข้อสอบจริง 12 อัลกอริทึมในขอนนี้ (Walk-Forward Backtest):** สั่งลุยไป **{total_bets}** ครั้ง ➡️ **ชนะ: {wins} ครั้ง** | **แพ้: {losses} ครั้ง** (อัตราชนะจริง: **{wr:.1f}%**)",
        "backtest_waiting": "🔍 **ผลตรวจข้อสอบจริง 12 อัลกอริทึมในขอนนี้:** กำลังเก็บสถิติความแม่นยำรายตัว... จะเปิดสัญญาณเฉพาะจังหวะที่ชัวร์ที่สุดเท่านั้น",
        "analytics_title": "💰 สถานะการเงินและเป้าหมาย",
        "metric_capital": "เงินทุนปัจจุบัน",
        "metric_pl": "กำไร/ขาดทุนรวม",
        "metric_target": "เป้าหมายกำไร",
        "metric_stoploss": "จุดตัดขาดทุน",
        "of_target": "ของเป้าหมาย",
        "target_hit": "🎉 ถึงเป้าหมายแล้ว: คุณทำกำไรถึงเป้าหมายรายวัน แนะนำให้หยุดพักและถอนกำไรออก!",
        "stop_loss_hit": "⚠️ ตัดขาดทุน: ขาดทุนถึงจุดที่กำหนดไว้ แนะนำให้หยุดเล่นทันทีเพื่อป้องกันเงินทุนสูญหาย!",
        "pred_title": "3️⃣ ผลลงมติ 12 อัลกอริทึม (5 ตัวหลัก + 7 ตัวเสริมจุดบอด) & คำนวณเงินเดิมพัน",
        "orig_5_header": "🔵 กลุ่มที่ 1: อัลกอริทึมหลัก 5 ตัวเดิม (Core Foundation Engines)",
        "new_7_header": "🟢 กลุ่มที่ 2: อัลกอริทึมใหม่ 7 ตัว (ออกแบบมาอุดจุดบอดและเสริมความแม่นยำให้กันและกัน)",
        "sim_title": "🔮 เมทริกซ์จำลองสถานการณ์และการเดินเงินล่วงหน้า (What-If Scenario Simulation)",
        "sim_desc": "จำลองสถานการณ์การเดินเงิน ว่าหากตาถัดไปผลออกมาเป็น แดง, น้ำเงิน หรือ เสมอ สถานะการเงินและพยากรณ์ตาถัดไปจะเป็นอย่างไร:",
        "if_red": "สมมติว่าตาถัดไปออก 🔴 RED",
        "if_blue": "สมมติว่าตาถัดไปออก 🔵 BLUE",
        "if_tie": "สมมติว่าตาถัดไปออก 🟢 TIE",
        "confirmed_status": "ผ่านเกณฑ์สไนเปอร์ (ลุยได้)",
        "wait_status": "รอจังหวะ (ยังไม่ชัวร์)",
        "algo_intensity_header": "⚡ รายละเอียดการคิด การอุดจุดบอด และความแม่นยำจริงในขอนนี้ของทั้ง 12 อัลกอริทึม",
        "algo_1_name": "1. True Shoe Equilibrium MC",
        "algo_1_desc": "[ตัวหลัก] จำลองสมดุลขอนไพ่ที่เหลือจริงและแรงดึงกลับตามกฎจำนวนมาก",
        "algo_2_name": "2. Multi-Order HMM (1-3 Step)",
        "algo_2_desc": "[ตัวหลัก] วิเคราะห์เมทริกซ์การเปลี่ยนผ่านเค้าไพ่ระยะ 1, 2 และ 3 ก้าวย้อนหลัง",
        "algo_3_name": "3. Bayesian Run-Length",
        "algo_3_desc": "[ตัวหลัก] คำนวณโอกาสที่แถวจะไหลต่อเทียบกับโอกาสโดนตัดจากเพดานขอนจริง",
        "algo_4_name": "4. Regime & Rhythm AI",
        "algo_4_desc": "[ตัวหลัก] จำแนกโหมดขอนไพ่ (ปิงปองสลับ, ไพ่คู่ 2-2, ขาตัด L, หรือมังกร)",
        "algo_5_name": "5. Multi-Scale N-Gram",
        "algo_5_desc": "[ตัวหลัก] ค้นหารูปแบบซ้ำซ้อนตรงเป๊ะทั้งชุด 3 ตา, 4 ตา และ 5 ตา",
        "algo_6_name": "6. Derived Roads AI (3 เค้าไพ่รอง)",
        "algo_6_desc": "[อุดจุดบอดตัวที่ 3 & 4] คำนวณตารางไข่ปลา ซาลาเปา และแมลงสาบ เช็กความสมมาตรข้ามคอลัมน์",
        "algo_7_name": "7. Fuzzy K-NN Matcher",
        "algo_7_desc": "[อุดจุดบอดตัวที่ 5] ค้นหาแพทเทิร์น 6 ตาที่คล้ายที่สุดแม้จะมีไพ่หลุด/เพี้ยนปนอยู่ 1 เม็ด",
        "algo_8_name": "8. Z-Score Mean Reversion",
        "algo_8_desc": "[อุดจุดบอดตัวที่ 1] ดักจุดตึงตัวทางสถิติ (|Z|>1.65) เมื่อสีใดออกมากเกินไปโดยไม่ใช่มังกร",
        "algo_9_name": "9. Streak-to-Streak Matrix",
        "algo_9_desc": "[อุดจุดบอดตัวที่ 2 & 3] วิเคราะห์ความยาวคอลัมน์ชนคอลัมน์ (เช่น หลังไพ่ตัด 1 แล้วชอบออกอะไร)",
        "algo_10_name": "10. Tie-Shock Catalyst",
        "algo_10_desc": "[อุดจุดบอดทุกตัว] วิเคราะห์ผลกระทบหลังไพ่ออกเสมอ (Tie) ว่าชอบเปลี่ยนสีหรือย้ำสีเดิม",
        "algo_11_name": "11. MACD & RSI Oscillator",
        "algo_11_desc": "[อุดจุดบอดโมเมนตัมช้า] เทียบเส้นค่าเฉลี่ยไว (3) ตัดเส้นช้า (10) และดักจุดกลับตัว RSI",
        "algo_12_name": "12. Meta-Critic Anti-Trap",
        "algo_12_desc": "[อุดจุดบอดไพ่หลอก] ตรวจจับจังหวะที่ขอนไพ่กำลังสับขาหลอกตัวหลัก แล้วสั่งดักสวนกับดักทันที",
        "algo_1": "1. Shoe MC", "algo_2": "2. Multi-HMM", "algo_3": "3. Bayes ดักตัด", "algo_4": "4. Regime AI", "algo_5": "5. N-Gram Pro",
        "algo_6": "6. 3 เค้าไพ่รอง", "algo_7": "7. Fuzzy K-NN", "algo_8": "8. Z-ดักตึงตัว", "algo_9": "9. เมทริกซ์แถว", "algo_10": "10. วิเคราะห์ Tie", "algo_11": "11. MACD/RSI", "algo_12": "12. ดักไพ่หลอก",
        "shoe_acc_label": "ความแม่นในขอนนี้",
        "chart_header": "📊 กราฟเปรียบเทียบคะแนนโหวตของทั้ง 12 อัลกอริทึม",
        "rec_title": "🎯 กลยุทธ์การลงทุนตาถัดไป (ระบบสไนเปอร์ 12 อัลกอริทึม):",
        "conf_level": "📊 ระดับความมั่นใจถ่วงน้ำหนัก 12 อัลกอริทึม (Weighted Confidence)",
        "algo_aligned": "อัลกอริทึมเห็นตรงกัน",
        "pass_msg": "✅ สัญญาณสไนเปอร์ 12 อัลกอริทึมยืนยัน (ชัวร์)! แนะนำให้ลงทุนฝั่ง: 【",
        "fail_msg": "⛔ ห้ามลงทุน / รอจังหวะ (WAIT): สัญญาณยังไม่ผ่านเกณฑ์ความปลอดภัย 12 อัลกอริทึม ข้ามตานี้เพื่อรักษาสถิติชนะ!",
        "pred_stake": "💡 พยากรณ์ขนาดเงินเดิมพันตาถัดไป:",
        "wait_stake": "0 (รอจังหวะชัวร์)",
        "reset": "🗑️ ล้างข้อมูลและเริ่มขอนใหม่",
        "mode": "รูปแบบการคิดแต้ม:",
        "sims": "ความเข้มข้นของตัวจำลอง",
        "no_data": "ยังไม่มีข้อมูล กรุณายืนยันข้อมูลในตารางกริด",
        "need_more_data": "กรุณากรอกและยืนยันข้อมูลอย่างน้อย 5 ตาขึ้นไป เพื่อเปิดใช้งานระบบสไนเปอร์ 12 อัลกอริทึม"
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
strictness_mode = st.sidebar.radio(
    t["strict_mode_label"],
    [t["mode_sniper"], t["mode_standard"]],
    index=0
)
is_sniper_mode = (strictness_mode == t["mode_sniper"])

min_votes_required = st.sidebar.slider(
    t["min_vote_label"], min_value=7, max_value=12, value=9, step=1
)

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
        if row.get("Red Winner", False):
            winner = "Red"
        elif row.get("Blue Winner", False):
            winner = "Blue"
        elif row.get("Tie (Draw)", False):
            winner = "Tie"

        if winner:
            processed_rounds.append({
                "round": idx + 1,
                "winner": winner,
                "pl": pl,
                "notes": str(row.get("Notes", ""))
            })

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


# ==============================================================================
# 🧠 CORE MATHEMATICAL ENGINE: 12 SYNERGISTIC ALGORITHMS (5 CORE + 7 COMPLEMENTARY)
# ==============================================================================
def extract_streaks(rb_seq):
    """แยกความยาวแถว (Run-lengths / Columns) ของ Red และ Blue ในขอนไพ่"""
    if not rb_seq:
        return [], 0, None
    streaks = []
    curr_color = rb_seq[0]
    curr_len = 0
    for c in rb_seq:
        if c == curr_color:
            curr_len += 1
        else:
            streaks.append((curr_color, curr_len))
            curr_color = c
            curr_len = 1
    streaks.append((curr_color, curr_len))
    return streaks, curr_len, curr_color


def compute_12_algorithms_single_step(rounds_history, game_mode, num_sims):
    """
    คำนวณโหวตและค่าความมั่นใจ (0.50 - 0.99) ของอัลกอริทึมทั้ง 12 ตัว:
    - ตัวที่ 1 ถึง 5: อัลกอริทึมหลัก (Core Foundation)
    - ตัวที่ 6 ถึง 12: อัลกอริทึมเสริมจุดบอด (Complementary Blind-Spot Correctors)
    """
    rb_seq = [r["winner"] for r in rounds_history if r["winner"] in ["Red", "Blue"]]
    n_rb = len(rb_seq)
    if n_rb < 3:
        return ["Red"] * 12, [0.5] * 12, {"at_cut_trap": False, "entropy": 1.0, "max_ceiling": 1, "curr_streak": 1}

    streaks, curr_len, curr_color = extract_streaks(rb_seq)
    opp_color = "Blue" if curr_color == "Red" else "Red"
    completed_streaks = [length for _, length in streaks[:-1]]
    max_ceiling = max(completed_streaks) if completed_streaks else curr_len

    # ------------------------------------------------------------------
    # [ALGO 1] True Shoe Equilibrium & Card Density Monte Carlo
    # ------------------------------------------------------------------
    total_r = rb_seq.count("Red")
    total_b = rb_seq.count("Blue")
    shoe_capacity = 120.0
    rem_r = max(10.0, (shoe_capacity / 2.0) - total_r)
    rem_b = max(10.0, (shoe_capacity / 2.0) - total_b)

    short_window = rb_seq[-8:]
    sw_r = short_window.count("Red") / len(short_window)
    sw_b = short_window.count("Blue") / len(short_window)

    p_red_mc = 0.35 * (rem_r / (rem_r + rem_b)) + 0.65 * sw_r
    p_blue_mc = 0.35 * (rem_b / (rem_r + rem_b)) + 0.65 * sw_b
    norm_mc = p_red_mc + p_blue_mc
    p_red_mc /= norm_mc

    rng = random.Random(n_rb * 1009 + total_r * 37 + total_b * 73)
    sim_iters = min(5000, max(1000, num_sims // 10))
    sim_r = sum(1 for _ in range(sim_iters) if rng.random() < p_red_mc)
    mc_ratio = sim_r / sim_iters
    if abs(mc_ratio - 0.5) < 0.005:
        vote_1 = curr_color
        conf_1 = 0.52
    else:
        vote_1 = "Red" if mc_ratio > 0.5 else "Blue"
        conf_1 = min(0.95, 0.5 + abs(mc_ratio - 0.5) * 1.8)

    # ------------------------------------------------------------------
    # [ALGO 2] Multi-Order HMM (1-Step, 2-Step, and 3-Step Transitions)
    # ------------------------------------------------------------------
    r_hmm, b_hmm = 0.0, 0.0
    for order, weight in [(1, 1.0), (2, 2.2), (3, 3.8)]:
        if n_rb > order:
            target_state = tuple(rb_seq[-order:])
            match_r, match_b = 0.0, 0.0
            for i in range(n_rb - order):
                if tuple(rb_seq[i:i + order]) == target_state:
                    recency_boost = 1.0 + (i / n_rb)
                    if rb_seq[i + order] == "Red":
                        match_r += recency_boost
                    else:
                        match_b += recency_boost
            if (match_r + match_b) > 0:
                r_hmm += weight * (match_r / (match_r + match_b))
                b_hmm += weight * (match_b / (match_b + match_r))

    if (r_hmm + b_hmm) == 0 or abs(r_hmm - b_hmm) < 0.01:
        vote_2 = curr_color
        conf_2 = 0.51
    else:
        vote_2 = "Red" if r_hmm > b_hmm else "Blue"
        conf_2 = min(0.96, 0.5 + abs(r_hmm - b_hmm) / (r_hmm + b_hmm))

    # ------------------------------------------------------------------
    # [ALGO 3] Bayesian Run-Length Survival (ตัวดักไพ่ตัด / ขา L)
    # ------------------------------------------------------------------
    survived_count = 0.5
    cut_count = 0.5
    for _, (s_col, s_len) in enumerate(streaks[:-1]):
        col_w = 1.5 if s_col == curr_color else 1.0
        if s_len > curr_len:
            survived_count += col_w
        elif s_len == curr_len:
            cut_count += col_w

    prob_continue = survived_count / (survived_count + cut_count)
    if prob_continue >= 0.5:
        vote_3 = curr_color
        conf_3 = min(0.96, prob_continue)
    else:
        vote_3 = opp_color
        conf_3 = min(0.96, 1.0 - prob_continue)

    # ------------------------------------------------------------------
    # [ALGO 4] Table Regime & Rhythm Classifier
    # ------------------------------------------------------------------
    recent_lens = [length for _, length in streaks[-5:-1]]
    if curr_len >= 4:
        vote_4 = curr_color
        conf_4 = 0.88
    elif len(recent_lens) >= 2 and all(x == 1 for x in recent_lens[-2:]) and curr_len == 1:
        vote_4 = opp_color
        conf_4 = 0.86
    elif len(recent_lens) >= 2 and all(x == 2 for x in recent_lens[-2:]):
        if curr_len == 1:
            vote_4 = curr_color
            conf_4 = 0.85
        else:
            vote_4 = opp_color
            conf_4 = 0.85
    elif completed_streaks and curr_len == max_ceiling and completed_streaks.count(max_ceiling) >= 2:
        vote_4 = opp_color
        conf_4 = 0.84
    else:
        ema_r, ema_b, dec = 0.0, 0.0, 1.0
        for c in reversed(rb_seq[-10:]):
            if c == "Red":
                ema_r += dec
            else:
                ema_b += dec
            dec *= 0.78
        vote_4 = "Red" if ema_r >= ema_b else "Blue"
        conf_4 = 0.5 + abs(ema_r - ema_b) / (ema_r + ema_b + 0.001) * 0.4

    # ------------------------------------------------------------------
    # [ALGO 5] Multi-Scale N-Gram Pattern Engine (3, 4, 5-Gram)
    # ------------------------------------------------------------------
    pat_r, pat_b = 0.0, 0.0
    for k_gram, k_weight in [(3, 1.5), (4, 3.0), (5, 5.0)]:
        if n_rb > k_gram:
            key_seq = rb_seq[-k_gram:]
            for i in range(n_rb - k_gram):
                if rb_seq[i:i + k_gram] == key_seq:
                    nxt_c = rb_seq[i + k_gram]
                    rec_w = k_weight * (0.5 + (i / n_rb))
                    if nxt_c == "Red":
                        pat_r += rec_w
                    else:
                        pat_b += rec_w

    if (pat_r + pat_b) == 0:
        vote_5 = vote_2
        conf_5 = 0.55
    else:
        vote_5 = "Red" if pat_r >= pat_b else "Blue"
        conf_5 = min(0.97, 0.5 + abs(pat_r - pat_b) / (pat_r + pat_b))

    # ==================================================================
    # 🟢 NEW 7 COMPLEMENTARY ALGORITHMS (ALGO 6 TO ALGO 12)
    # ==================================================================

    # ------------------------------------------------------------------
    # [ALGO 6] Derived Roads AI (Big Eye Boy, Small Road, Cockroach Pig)
    # อุดจุดบอด Algo 3 & 4: เช็กความสมมาตรของความลึกคอลัมน์ย้อนหลัง 1, 2 และ 3 แถว
    # ------------------------------------------------------------------
    sym_continue_score = 0.0
    sym_cut_score = 0.0
    num_cols = len(streaks)
    for lookback, lb_w in [(1, 1.2), (2, 1.5), (3, 1.8)]:
        if num_cols > lookback:
            ref_len = streaks[-(lookback + 1)][1]
            # เช็กว่าขอนนี้ชอบความสมมาตร (เท่ากับแถวอ้างอิงแล้วตัด) หรือไม่
            sym_matches = 0
            asym_matches = 0
            for c_idx in range(lookback, num_cols - 1):
                if streaks[c_idx][1] == streaks[c_idx - lookback][1]:
                    sym_matches += 1
                else:
                    asym_matches += 1
            prefer_symmetry = (sym_matches >= asym_matches)

            if curr_len < ref_len:
                # ยังไม่ถึงความลึกของแถวอ้างอิง ถ้าขอนสมมาตรจะต้องไหลต่อให้เท่ากัน
                if prefer_symmetry:
                    sym_continue_score += lb_w
                else:
                    sym_cut_score += lb_w * 0.7
            elif curr_len == ref_len:
                # ชนความลึกของแถวอ้างอิงพอดี ถ้าขอนสมมาตรจะต้องตัดเปลี่ยนสี!
                if prefer_symmetry:
                    sym_cut_score += lb_w * 1.4
                else:
                    sym_continue_score += lb_w
            else:
                # ทะลุแถวอ้างอิงไปแล้ว (กลายเป็นมังกร)
                sym_continue_score += lb_w * 1.1

    if (sym_continue_score + sym_cut_score) == 0:
        vote_6 = vote_3
        conf_6 = 0.54
    elif sym_continue_score >= sym_cut_score:
        vote_6 = curr_color
        conf_6 = min(0.95, 0.5 + (sym_continue_score - sym_cut_score) / (sym_continue_score + sym_cut_score) * 0.45)
    else:
        vote_6 = opp_color
        conf_6 = min(0.95, 0.5 + (sym_cut_score - sym_continue_score) / (sym_continue_score + sym_cut_score) * 0.45)

    # ------------------------------------------------------------------
    # [ALGO 7] Fuzzy K-NN Sequence Matcher (Hamming Distance Tolerance)
    # อุดจุดบอด Algo 5 (N-Gram): ทำงานได้แม้รูปแบบย้อนหลังมีไพ่หลุด/เพี้ยน 1 เม็ด
    # ------------------------------------------------------------------
    knn_r, knn_b = 0.0, 0.0
    win_k = min(6, n_rb - 1)
    if win_k >= 3:
        target_vec = rb_seq[-win_k:]
        for i in range(n_rb - win_k):
            cand_vec = rb_seq[i:i + win_k]
            mismatches = sum(1 for a, b in zip(target_vec, cand_vec) if a != b)
            if mismatches <= 1:
                sim_w = (4.0 if mismatches == 0 else 1.2) * (0.6 + 0.4 * (i / n_rb))
                if rb_seq[i + win_k] == "Red":
                    knn_r += sim_w
                else:
                    knn_b += sim_w

    if (knn_r + knn_b) == 0:
        vote_7 = vote_2
        conf_7 = 0.53
    else:
        vote_7 = "Red" if knn_r >= knn_b else "Blue"
        conf_7 = min(0.95, 0.5 + abs(knn_r - knn_b) / (knn_r + knn_b) * 0.45)

    # ------------------------------------------------------------------
    # [ALGO 8] Z-Score Mean Reversion & Bollinger Pull
    # อุดจุดบอด Algo 1: ดักการดีดกลับเมื่อสีใดสีหนึ่งตึงเกินค่าสถิติใน 12 ตาล่าสุด
    # ------------------------------------------------------------------
    z_win = rb_seq[-12:]
    n_z = len(z_win)
    r_z = z_win.count("Red")
    mean_r = n_z * 0.5
    std_r = math.sqrt(n_z * 0.25) if n_z > 0 else 1.0
    z_score = (r_z - mean_r) / std_r

    if abs(z_score) >= 1.60 and curr_len <= 2:
        # ตึงตัวเกินขีดจำกัดสถิติ (และไม่ได้เป็นมังกรยาว) -> สั่งดักตบสวนเข้าหาค่าเฉลี่ย
        vote_8 = "Blue" if z_score > 0 else "Red"
        conf_8 = min(0.92, 0.55 + (abs(z_score) - 1.5) * 0.2)
    else:
        # อยู่ในกรอบสถิติปกติ -> ไหลตาม Drift ของขอน
        vote_8 = "Red" if z_score >= 0 else "Blue"
        conf_8 = min(0.86, 0.52 + abs(z_score) * 0.15)

    # ------------------------------------------------------------------
    # [ALGO 9] Streak-to-Streak Column Matrix
    # อุดจุดบอด Algo 2 & 3: ดูว่าหลังแถวก่อนหน้าจบที่ความยาว X แถวปัจจุบันชอบตัดหรือไหล
    # ------------------------------------------------------------------
    if len(streaks) >= 3:
        prev_col_len = streaks[-2][1]
        col_cont, col_cut = 0.5, 0.5
        for s_i in range(1, len(streaks) - 1):
            if streaks[s_i - 1][1] == prev_col_len:
                if streaks[s_i][1] > curr_len:
                    col_cont += 1.5
                elif streaks[s_i][1] == curr_len:
                    col_cut += 1.5
        p_col_cont = col_cont / (col_cont + col_cut)
        vote_9 = curr_color if p_col_cont >= 0.5 else opp_color
        conf_9 = min(0.94, max(p_col_cont, 1.0 - p_col_cont))
    else:
        vote_9 = vote_3
        conf_9 = 0.55

    # ------------------------------------------------------------------
    # [ALGO 10] Tie-Shock Catalyst & Parity Alternation Specialist
    # อุดจุดบอดทุกตัวที่ละเลยไพ่เสมอ (Tie): วิเคราะห์พฤติกรรมหลังออก Tie
    # ------------------------------------------------------------------
    all_winners = [r["winner"] for r in rounds_history]
    if all_winners and all_winners[-1] == "Tie":
        tie_same, tie_switch = 0.5, 0.5
        last_non_tie = curr_color
        for idx_w in range(1, len(all_winners) - 1):
            if all_winners[idx_w] == "Tie":
                before_cols = [x for x in all_winners[:idx_w] if x in ["Red", "Blue"]]
                after_cols = [x for x in all_winners[idx_w + 1:] if x in ["Red", "Blue"]]
                if before_cols and after_cols:
                    if before_cols[-1] == after_cols[0]:
                        tie_same += 1.8
                    else:
                        tie_switch += 1.8
        if tie_same >= tie_switch:
            vote_10 = last_non_tie
            conf_10 = min(0.94, tie_same / (tie_same + tie_switch))
        else:
            vote_10 = opp_color
            conf_10 = min(0.94, tie_switch / (tie_same + tie_switch))
    else:
        # หากตาก่อนหน้าไม่ใช่ Tie ให้คำนวณโมเมนตัมการสลับฟันปลา (Alternation vs Repeat Ratio)
        recent_pairs = rb_seq[-7:]
        same_steps = sum(1 for i in range(1, len(recent_pairs)) if recent_pairs[i] == recent_pairs[i - 1])
        diff_steps = (len(recent_pairs) - 1) - same_steps
        if same_steps >= diff_steps:
            vote_10 = curr_color
            conf_10 = min(0.90, 0.52 + (same_steps - diff_steps) / max(1, len(recent_pairs)) * 0.4)
        else:
            vote_10 = opp_color
            conf_10 = min(0.90, 0.52 + (diff_steps - same_steps) / max(1, len(recent_pairs)) * 0.4)

    # ------------------------------------------------------------------
    # [ALGO 11] MACD & RSI Momentum Oscillator
    # อุดจุดบอด EMA ช้า: จับจุดตัดเส้นค่าเฉลี่ยไว (3 ตา) กับเส้นช้า (10 ตา)
    # ------------------------------------------------------------------
    num_vals = [1.0 if c == "Red" else 0.0 for c in rb_seq]
    fast_ema = sum(num_vals[-3:]) / len(num_vals[-3:])
    slow_ema = sum(num_vals[-10:]) / len(num_vals[-10:])
    macd_diff = fast_ema - slow_ema

    if abs(macd_diff) >= 0.05:
        vote_11 = "Red" if macd_diff > 0 else "Blue"
        conf_11 = min(0.93, 0.55 + abs(macd_diff) * 0.75)
    else:
        vote_11 = "Red" if fast_ema >= 0.5 else "Blue"
        conf_11 = 0.54

    # ------------------------------------------------------------------
    # [ALGO 12] Meta-Critic Anti-Trap (ดักทางไพ่สับขาหลอก)
    # อุดจุดบอดเวลาขอนไพ่เปลี่ยนจังหวะกะทันหันเพื่อกินฝั่งตามเทรนด์
    # ------------------------------------------------------------------
    core_5_votes = [vote_1, vote_2, vote_3, vote_4, vote_5]
    new_6_votes = [vote_6, vote_7, vote_8, vote_9, vote_10, vote_11]
    core_maj = "Red" if core_5_votes.count("Red") >= 3 else "Blue"
    new_maj = "Red" if new_6_votes.count("Red") >= 3 else "Blue"

    # หากกลุ่มอุดจุดบอด ( বিশেষตัวดักตัด Algo 3, 6, 9) เห็นต่างจากกลุ่มเทรนด์ แปลว่ามีโอกาสเป็นกับดักไพ่ตัด
    cut_specialists = [vote_3, vote_6, vote_9]
    cut_maj = "Red" if cut_specialists.count("Red") >= 2 else "Blue"
    if cut_maj != core_maj and curr_len >= max(2, max_ceiling):
        vote_12 = cut_maj
        conf_12 = 0.89
    else:
        vote_12 = new_maj if new_maj == core_maj else cut_maj
        conf_12 = 0.82 if new_maj == core_maj else 0.65

    # ตรวจสอบกับดักไพ่ตัด (Cut-Point Trap) และ Shannon Entropy
    at_cut_trap = bool(completed_streaks and curr_len == max_ceiling and 0.43 <= prob_continue <= 0.57 and cut_maj != core_maj)

    recent_trans = [1 if rb_seq[i] == rb_seq[i - 1] else 0 for i in range(max(1, n_rb - 8), n_rb)]
    p_same = sum(recent_trans) / len(recent_trans) if recent_trans else 0.5
    if 0 < p_same < 1:
        entropy = -(p_same * math.log2(p_same) + (1 - p_same) * math.log2(1 - p_same))
    else:
        entropy = 0.0

    votes = [
        vote_1, vote_2, vote_3, vote_4, vote_5,
        vote_6, vote_7, vote_8, vote_9, vote_10, vote_11, vote_12
    ]
    confs = [
        conf_1, conf_2, conf_3, conf_4, conf_5,
        conf_6, conf_7, conf_8, conf_9, conf_10, conf_11, conf_12
    ]
    meta = {
        "at_cut_trap": at_cut_trap,
        "entropy": entropy,
        "max_ceiling": max_ceiling,
        "curr_streak": curr_len,
        "prob_continue": prob_continue
    }
    return votes, confs, meta


def run_walk_forward_sniper_analysis(rounds_history, game_mode, num_sims, sniper_mode=True, min_votes_req=9):
    """ระบบตรวจข้อสอบย้อนหลังในขอนจริงสำหรับทั้ง 12 อัลกอริทึม (Walk-Forward Validation)"""
    num_algos = 12
    algo_correct = [0] * num_algos
    algo_total = [0] * num_algos

    sniper_wins = 0
    sniper_losses = 0

    for t_idx in range(5, len(rounds_history)):
        actual_next = rounds_history[t_idx]["winner"]
        if actual_next == "Tie":
            continue

        sub_hist = rounds_history[:t_idx]
        v_step, c_step, m_step = compute_12_algorithms_single_step(sub_hist, game_mode, num_sims)

        w_red, w_blue = 0.0, 0.0
        best_algo_idx = 0
        best_algo_acc = -1.0

        for a_i in range(num_algos):
            hist_acc = (algo_correct[a_i] + 2.0) / (algo_total[a_i] + 4.0)
            if hist_acc > best_algo_acc:
                best_algo_acc = hist_acc
                best_algo_idx = a_i

            power = (hist_acc ** 2.2) * c_step[a_i]
            if v_step[a_i] == "Red":
                w_red += power
            else:
                w_blue += power

        r_cnt = v_step.count("Red")
        b_cnt = v_step.count("Blue")
        maj_side = "Red" if w_red >= w_blue else "Blue"
        maj_cnt = r_cnt if maj_side == "Red" else b_cnt
        w_ratio = max(w_red, w_blue) / (w_red + w_blue + 1e-9)

        leader_agrees = (v_step[best_algo_idx] == maj_side)
        # ตรวจสอบว่ากลุ่มดักจุดตัด (Algo 3, 6, 9) อย่างน้อย 2 ใน 3 เห็นพ้องกับมติหลัก
        cut_specialists_agree = ([v_step[2], v_step[5], v_step[8]].count(maj_side) >= 2)
        low_trap = not m_step["at_cut_trap"]

        if sniper_mode:
            signal_pass = (
                maj_cnt >= min_votes_req
                and w_ratio >= 0.75
                and leader_agrees
                and cut_specialists_agree
                and low_trap
            )
        else:
            signal_pass = (maj_cnt >= min_votes_req)

        if signal_pass:
            if maj_side == actual_next:
                sniper_wins += 1
            else:
                sniper_losses += 1

        for a_i in range(num_algos):
            algo_total[a_i] += 1
            if v_step[a_i] == actual_next:
                algo_correct[a_i] += 1

    curr_votes, curr_confs, curr_meta = compute_12_algorithms_single_step(rounds_history, game_mode, num_sims)

    algo_accuracies = []
    w_red_now, w_blue_now = 0.0, 0.0
    best_algo_idx_now = 0
    best_acc_now = -1.0

    for a_i in range(num_algos):
        if algo_total[a_i] > 0:
            acc_pct = (algo_correct[a_i] / algo_total[a_i]) * 100.0
            bayesian_acc = (algo_correct[a_i] + 2.0) / (algo_total[a_i] + 4.0)
        else:
            acc_pct = 75.0
            bayesian_acc = 0.75

        algo_accuracies.append(acc_pct)
        if bayesian_acc > best_acc_now:
            best_acc_now = bayesian_acc
            best_algo_idx_now = a_i

        power_now = (bayesian_acc ** 2.2) * curr_confs[a_i]
        if curr_votes[a_i] == "Red":
            w_red_now += power_now
        else:
            w_blue_now += power_now

    r_cnt_now = curr_votes.count("Red")
    b_cnt_now = curr_votes.count("Blue")
    maj_side_now = "Red" if w_red_now >= w_blue_now else "Blue"
    maj_cnt_now = r_cnt_now if maj_side_now == "Red" else b_cnt_now
    weighted_conf_pct = (max(w_red_now, w_blue_now) / (w_red_now + w_blue_now + 1e-9)) * 100.0

    leader_agrees_now = (curr_votes[best_algo_idx_now] == maj_side_now)
    cut_specialists_agree_now = ([curr_votes[2], curr_votes[5], curr_votes[8]].count(maj_side_now) >= 2)
    low_trap_now = not curr_meta["at_cut_trap"]

    if sniper_mode:
        is_safe_to_bet = (
            maj_cnt_now >= min_votes_req
            and weighted_conf_pct >= 75.0
            and leader_agrees_now
            and cut_specialists_agree_now
            and low_trap_now
        )
    else:
        is_safe_to_bet = (maj_cnt_now >= min_votes_req)

    return {
        "votes": curr_votes,
        "confs": curr_confs,
        "algo_accs": algo_accuracies,
        "algo_correct": algo_correct,
        "algo_total": algo_total,
        "maj_side": maj_side_now,
        "maj_cnt": maj_cnt_now,
        "red_cnt": r_cnt_now,
        "blue_cnt": b_cnt_now,
        "weighted_conf": weighted_conf_pct,
        "is_safe": is_safe_to_bet,
        "sniper_wins": sniper_wins,
        "sniper_losses": sniper_losses,
        "meta": curr_meta
    }


# --- แสดง Roadmap & ตัววิเคราะห์เค้าไพ่ / จุดตัดขา L ---
st.markdown("---")
st.markdown(f"### {t['roadmap_title']}")

if processed_rounds:
    badges_html = ""
    for r in processed_rounds:
        bg = "#ef4444" if r["winner"] == "Red" else ("#3b82f6" if r["winner"] == "Blue" else "#10b981")
        badges_html += f'<span class="history-dot" style="background-color:{bg};">{r["winner"][0]}</span>'
    st.markdown(badges_html, unsafe_allow_html=True)

    rb_only = [r["winner"] for r in processed_rounds if r["winner"] in ["Red", "Blue"]]
    if rb_only:
        streaks_info, c_streak, c_side = extract_streaks(rb_only)
        comp_lens = [l for _, l in streaks_info[:-1]]
        max_c = max(comp_lens) if comp_lens else c_streak

        pp_count = 1
        for i in range(len(rb_only) - 1, 0, -1):
            if rb_only[i] != rb_only[i - 1]:
                pp_count += 1
            else:
                break

        if c_streak >= 4:
            pattern_text = t["streak_msg"].format(side=c_side, count=c_streak, max_c=max_c)
        elif pp_count >= 4:
            pattern_text = t["pingpong_msg"].format(count=pp_count)
        elif comp_lens and c_streak == max_c and max_c >= 2:
            pattern_text = t["lcut_msg"].format(count=c_streak, max_c=max_c)
        else:
            pattern_text = t["normal_msg"].format(side=c_side, count=c_streak, max_c=max_c)

        st.markdown(f'<div class="pattern-box">{pattern_text}</div>', unsafe_allow_html=True)
else:
    st.info(t["no_data"])

# --- แสดงผลลงมติ 12 อัลกอริทึม + ผลตรวจข้อสอบย้อนหลังในขอนจริง ---
st.markdown("---")
st.markdown(f"### {t['pred_title']}")

if len(processed_rounds) >= 5:
    res = run_walk_forward_sniper_analysis(
        processed_rounds, game_mode, num_sims, is_sniper_mode, min_votes_required
    )
    votes = res["votes"]
    red_count = res["red_cnt"]
    blue_count = res["blue_cnt"]
    max_votes = res["maj_cnt"]
    confidence_pct = res["weighted_conf"]
    is_safe = res["is_safe"]

    # แสดงสถิติตรวจข้อสอบย้อนหลังในขอนนี้ (Walk-Forward Backtest Scoreboard)
    total_sniper_bets = res["sniper_wins"] + res["sniper_losses"]
    if total_sniper_bets > 0:
        actual_wr = (res["sniper_wins"] / total_sniper_bets) * 100.0
        st.markdown(
            f'<div class="sniper-box">{t["backtest_summary"].format(total_bets=total_sniper_bets, wins=res["sniper_wins"], losses=res["sniper_losses"], wr=actual_wr)}</div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(f'<div class="sniper-box">{t["backtest_waiting"]}</div>', unsafe_allow_html=True)

    # หากโหวตผ่านเกณฑ์ขั้นต่ำแต่โดนระบบสไนเปอร์สั่งเบรก ให้แจ้งเตือนชัดเจน
    if max_votes >= min_votes_required and not is_safe:
        st.markdown(f'<div class="volatility-box">{t["volatility_warning"]}</div>', unsafe_allow_html=True)

    # --- แถวที่ 1: แสดงอัลกอริทึมหลัก 5 ตัวเดิม ---
    st.markdown(f"#### {t['orig_5_header']}")
    c_d1, c_d2, c_d3, c_d4, c_d5 = st.columns(5)
    core_desc_cols = [c_d1, c_d2, c_d3, c_d4, c_d5]
    for i in range(5):
        acc_val = res["algo_accs"][i]
        c_cnt = res["algo_correct"][i]
        t_cnt = res["algo_total"][i]
        n_key = f"algo_{i+1}_name"
        d_key = f"algo_{i+1}_desc"
        with core_desc_cols[i]:
            st.markdown(
                f'<div class="algo-profile-box"><b>{t[n_key]}</b><br>{t[d_key]}<br>'
                f'<span style="color:#38bdf8; font-weight:bold;">{t["shoe_acc_label"]}: {acc_val:.1f}% ({c_cnt}/{t_cnt})</span></div>',
                unsafe_allow_html=True
            )

    col1, col2, col3, col4, col5 = st.columns(5)
    for idx, col in enumerate([col1, col2, col3, col4, col5]):
        v = votes[idx]
        name = t[f"algo_{idx+1}"]
        status_color = "#ef4444" if v == "Red" else "#3b82f6"
        algo_conf = res["confs"][idx] * 100.0
        col.markdown(
            f'<div class="metric-card"><h4>{name}</h4><h3 style="color: {status_color};">{v}</h3>'
            f'<p style="font-size: 12px; color: #94a3b8;">Conf: {algo_conf:.0f}% | Acc: {res["algo_accs"][idx]:.0f}%</p></div>',
            unsafe_allow_html=True,
        )

    # --- แถวที่ 2: แสดงอัลกอริทึมใหม่ 7 ตัวที่ช่วยอุดจุดบอดและเสริมกัน ---
    st.markdown(f"#### {t['new_7_header']}")
    s_cols_top = st.columns(4)
    for i in range(5, 9):
        acc_val = res["algo_accs"][i]
        c_cnt = res["algo_correct"][i]
        t_cnt = res["algo_total"][i]
        v = votes[i]
        name = t[f"algo_{i+1}"]
        status_color = "#ef4444" if v == "Red" else "#3b82f6"
        algo_conf = res["confs"][i] * 100.0
        with s_cols_top[i - 5]:
            st.markdown(
                f'<div class="algo-synergy-box"><b>{t[f"algo_{i+1}_name"]}</b><br>{t[f"algo_{i+1}_desc"]}<br>'
                f'<span style="color:#34d399; font-weight:bold;">{t["shoe_acc_label"]}: {acc_val:.1f}% ({c_cnt}/{t_cnt})</span></div>',
                unsafe_allow_html=True
            )
            st.markdown(
                f'<div class="metric-card-synergy"><h4>{name}</h4><h3 style="color: {status_color};">{v}</h3>'
                f'<p style="font-size: 12px; color: #a7f3d0;">Conf: {algo_conf:.0f}% | Acc: {acc_val:.0f}%</p></div>',
                unsafe_allow_html=True
            )

    s_cols_bot = st.columns(3)
    for i in range(9, 12):
        acc_val = res["algo_accs"][i]
        c_cnt = res["algo_correct"][i]
        t_cnt = res["algo_total"][i]
        v = votes[i]
        name = t[f"algo_{i+1}"]
        status_color = "#ef4444" if v == "Red" else "#3b82f6"
        algo_conf = res["confs"][i] * 100.0
        with s_cols_bot[i - 9]:
            st.markdown(
                f'<div class="algo-synergy-box"><b>{t[f"algo_{i+1}_name"]}</b><br>{t[f"algo_{i+1}_desc"]}<br>'
                f'<span style="color:#34d399; font-weight:bold;">{t["shoe_acc_label"]}: {acc_val:.1f}% ({c_cnt}/{t_cnt})</span></div>',
                unsafe_allow_html=True
            )
            st.markdown(
                f'<div class="metric-card-synergy"><h4>{name}</h4><h3 style="color: {status_color};">{v}</h3>'
                f'<p style="font-size: 12px; color: #a7f3d0;">Conf: {algo_conf:.0f}% | Acc: {acc_val:.0f}%</p></div>',
                unsafe_allow_html=True
            )

    # กราฟแท่งเปรียบเทียบคะแนนโหวต 12 อัลกอริทึม
    st.markdown(f"#### {t['chart_header']}")
    vote_summary_df = pd.DataFrame(
        {"Side": ["Red Side", "Blue Side"], "Votes (out of 12)": [red_count, blue_count]}
    )
    st.bar_chart(vote_summary_df.set_index("Side"), color="#3b82f6")

    # คำนวณ Stake Sizing พยากรณ์เงินตาต่อไปอย่างรอบคอบ
    if not is_safe:
        suggested_stake = 0.0
    elif max_votes >= 11 and confidence_pct >= 88.0:
        suggested_stake = base_bet * 2.0
    else:
        suggested_stake = base_bet * 1.0

    st.markdown(f"#### {t['rec_title']}")
    st.markdown(
        f"### {t['conf_level']}: **{confidence_pct:.1f}%** "
        f"({max_votes}/12 {t['algo_aligned']} | Red: {red_count}, Blue: {blue_count})"
    )

    stake_str = f"{suggested_stake:,.0f}" if suggested_stake > 0 else t["wait_stake"]

    if is_safe and res["maj_side"] == "Red":
        st.markdown(
            f'<div class="big-badge consensus-pass">{t["pass_msg"]}Red】<br><br>{t["pred_stake"]} <b>{stake_str}</b></div>',
            unsafe_allow_html=True,
        )
    elif is_safe and res["maj_side"] == "Blue":
        st.markdown(
            f'<div class="big-badge consensus-pass">{t["pass_msg"]}Blue】<br><br>{t["pred_stake"]} <b>{stake_str}</b></div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f'<div class="big-badge consensus-fail">{t["fail_msg"]}<br><br>{t["pred_stake"]} <b>{stake_str}</b></div>',
            unsafe_allow_html=True
        )

    # --- What-If Scenario Matrix (เมทริกซ์จำลองสถานการณ์และการเดินเงินล่วงหน้า) ---
    st.markdown("---")
    st.markdown(f"### {t['sim_title']}")
    st.markdown(t["sim_desc"])

    sim_col1, sim_col2, sim_col3 = st.columns(3)
    
    scenarios = {}
    for hyp in ["Red", "Blue", "Tie"]:
        temp_history = processed_rounds.copy()
        temp_history.append({"round": len(temp_history) + 1, "winner": hyp, "pl": 0.0, "notes": ""})
        
        sim_res = run_walk_forward_sniper_analysis(
            temp_history, game_mode, num_sims, is_sniper_mode, min_votes_required
        )
        s_favored = sim_res["maj_side"]
        s_conf = sim_res["weighted_conf"]
        s_passed = sim_res["is_safe"]
        
        if not is_safe:
            sim_pl_impact = 0.0
        elif hyp == "Tie":
            sim_pl_impact = 0.0
        elif hyp == res["maj_side"]:
            sim_pl_impact = suggested_stake
        else:
            sim_pl_impact = -suggested_stake

        scenarios[hyp] = {"favored": s_favored, "conf": s_conf, "passed": s_passed, "impact": sim_pl_impact}

    for hyp_key, col_obj, title_text in [("Red", sim_col1, t["if_red"]), ("Blue", sim_col2, t["if_blue"]), ("Tie", sim_col3, t["if_tie"])]:
        scen = scenarios[hyp_key]
        c_status = t["confirmed_status"] if scen["passed"] else t["wait_status"]
        fav_color = "#ef4444" if scen["favored"] == "Red" else "#3b82f6"
        pl_color = "#10b981" if scen["impact"] >= 0 else "#ef4444"
        
        with col_obj:
            st.markdown(
                f'<div class="sim-box"><b>{title_text}</b><br>'
                f'Next Favored: <span style="color:{fav_color}">{scen["favored"]}</span><br>'
                f'Weighted Conf: {scen["conf"]:.1f}%<br>'
                f'Status: <b>{c_status}</b><br>'
                f'Current Bet P/L: <span style="color:{pl_color}; font-weight:bold;">{scen["impact"]:+,.0f} ฿</span></div>',
                unsafe_allow_html=True
            )

else:
    st.info(t["need_more_data"])
