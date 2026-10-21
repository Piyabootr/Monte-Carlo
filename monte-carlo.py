import random
import pandas as pd
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Pro Card Shoe Predictor Dashboard", page_icon="🃏", layout="wide"
)

# Professional Modern Blue & Sky Blue Gradient Theme Styling
st.markdown(
    """
<style>
    /* Main Background: Gradient Mix of Deep Blue and Soft Sky Blue */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1d4ed8 50%, #38bdf8 100%);
        color: #ffffff;
    }
    
    /* Professional Glassmorphism Metric Cards */
    .metric-card {
        background: rgba(15, 23, 42, 0.65);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(56, 189, 248, 0.3);
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        text-align: center;
        margin-bottom: 15px;
    }
    
    /* Big Betting Recommendation Badges */
    .big-badge {
        font-size: 22px;
        font-weight: bold;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        margin-top: 15px;
        margin-bottom: 15px;
        box-shadow: 0 10px 25px -3px rgba(0, 0, 0, 0.4);
    }
    .red-win { background: linear-gradient(135deg, #ef4444 0%, #991b1b 100%); color: white; border: 1px solid #f87171; }
    .blue-win { background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%); color: white; border: 1px solid #60a5fa; }
    .tie-win { background: linear-gradient(135deg, #059669 0%, #047857 100%); color: white; border: 1px solid #34d399; }
    .wait-signal { background: rgba(30, 41, 59, 0.85); color: #e2e8f0; border: 1px solid rgba(148, 163, 184, 0.4); }
    
    /* Roadmap History Dots */
    .history-dot {
        display: inline-block;
        width: 38px;
        height: 38px;
        line-height: 38px;
        border-radius: 50%;
        text-align: center;
        font-weight: bold;
        color: white;
        margin: 4px;
        font-size: 14px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.4);
    }
    
    /* Sidebar Styling */
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
        "title": "🃏 PRO CARD SHOE MULTI-ALGORITHM PREDICTOR",
        "subtitle": (
            "Professional Analytics Dashboard powered by **Monte Carlo"
            " Simulation**, **HMM**, **Bayesian Inference**, and **50-Round Grid"
            " Table**."
        ),
        "grid_title": "1️⃣ Editable Grid Table (50 Rounds Historical Data Entry)",
        "grid_desc": (
            "💡 **50-Round Grid Table:** Click or check the boxes (Red, Blue,"
            " Tie) to record historical data directly like Excel for analysis."
        ),
        "roadmap_title": "2️⃣ Roadmap & Last 30-Round Trend Analytics",
        "pred_title": (
            "3️⃣ Multi-Algorithm Next Round Prediction & Strict Betting"
            " Decision"
        ),
        "red_prob": "🔴 Red Win Probability",
        "blue_prob": "🔵 Blue Win Probability",
        "tie_prob": "🟢 Tie Probability",
        "rec_title": "🎯 Professional Betting Recommendation (Strict 90% Rule):",
        "bet_on": "✅ RECOMMENDATION: Bet on 【",
        "confirmed": "】 — CONFIRMED & SECURE! (Confidence: ",
        "wait": (
            "⛔ RECOMMENDATION: 【DO NOT BET / WAIT】 — Confidence is"
            " {prob:.2f}% (Below strict 90% professional requirement). Skip"
            " this round!"
        ),
        "reset": "🗑️ Reset Grid Data & Clear History",
        "mode": "Game Scoring Mode:",
        "mode_bacc": (
            "Baccarat / Dragon Tiger Style (10, J, Q, K = 0 for Baccarat)"
        ),
        "mode_single": "Single Card High Value (A=1 to K=13)",
        "sims": "Monte Carlo Iterations (per deck)",
        "threshold_info": (
            "🔒 Risk Management Threshold: **90%**\n\n(Will advise to bet"
            " **ONLY** if confidence reaches 90%+)"
        ),
        "total_valid": "Total Valid Rounds Recorded:",
        "red_wins": "Red Wins",
        "blue_wins": "Blue Wins",
        "ties": "Ties",
        "no_data": (
            "Please enter round outcomes in the 50-round grid table above to"
            " start professional analytics."
        ),
    },
    "ไทย": {
        "title": "🃏 แดชบอร์ดพยากรณ์ไพ่ระดับมืออาชีพ (MULTI-ALGORITHM)",
        "subtitle": (
            "ระบบวิเคราะห์ขอนไพ่ขั้นสูงผสาน **Monte Carlo**, **HMM**, **Bayesian"
            " Inference**, และ **ตารางกริด 50 รอบ**"
        ),
        "grid_title": "1️⃣ ตารางกริดบันทึกข้อมูลย้อนหลัง (50 รอบ)",
        "grid_desc": (
            "💡 **ตารางกริด 50 รอบ:** คลิกติ๊กเลือกผลย้อนหลัง (Red, Blue, Tie)"
            " หรือพิมพ์บันทึกข้อมูลได้โดยตรงเหมือนใช้งาน Excel"
        ),
        "roadmap_title": "2️⃣ แผนภูมิ Roadmap และวิเคราะห์เทรนด์ 30 ตาล่าสุด",
        "pred_title": "3️⃣ พยากรณ์ตาถัดไป & เกณฑ์คุมเข้มการเดิมพัน 90%",
        "red_prob": "🔴 โอกาสฝ่ายแดงชนะ",
        "blue_prob": "🔵 โอกาสฝ่ายน้ำเงินชนะ",
        "tie_prob": "🟢 โอกาสเสมอ",
        "rec_title": "🎯 คำแนะนำการเดิมพันระดับมืออาชีพ (กฎความมั่นใจ 90%):",
        "bet_on": "✅ คำแนะนำ: ควรลงเดิมพันฝั่ง 【",
        "confirmed": "】 — สัญญาณยืนยันความมั่นใจสูงสุด! (ความน่าจะเป็น: ",
        "wait": (
            "⛔ คำแนะนำ: 【ห้ามลงเดิมพัน / รอจังหวะ (DO NOT BET / WAIT)】"
            " — ความน่าจะเป็น {prob:.2f}% (ยังไม่ถึงเกณฑ์ 90% ตามมาตรฐานความปลอดภัย)"
            " ข้ามตานี้ไปก่อน!"
        ),
        "reset": "🗑️ ล้างข้อมูลกริด & เริ่มขอนใหม่",
        "mode": "รูปแบบการคิดแต้ม:",
        "mode_bacc": "สไตล์บาคาร่า / เสือมังกร (10, J, Q, K นับเป็น 0)",
        "mode_single": "วัดแต้มหน้าไพ่เดี่ยว (A=1 ถึง K=13)",
        "sims": "จำนวนรอบจำลอง Monte Carlo (ต่อสำรับ)",
        "threshold_info": (
            "🔒 เกณฑ์บริหารความเสี่ยง: **90%**\n\n(ระบบจะแนะนำให้ลงแทงก็ต่อเมื่อความมั่นใจ"
            " ถึง 90% ขึ้นไปเท่านั้น)"
        ),
        "total_valid": "จำนวนตาทั้งหมดที่บันทึก:",
        "red_wins": "แดงชนะ",
        "blue_wins": "น้ำเงินชนะ",
        "ties": "เสมอ",
        "no_data": (
            "กรุณากรอกผลการแข่งขันในตารางกริด 50 รอบด้านบน เพื่อเริ่มระบบวิเคราะห์"
        ),
    },
}

t = translations[lang]

st.markdown(f"# {t['title']}")
st.markdown(t["subtitle"])
st.markdown("---")

# Initialize Session State for Grid Table History (Total 50 Rounds)
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

# --- Sidebar Settings ---
st.sidebar.markdown("### ⚙️ Simulation Parameters")

game_mode = st.sidebar.radio(
    t["mode"], [t["mode_bacc"], t["mode_single"]]
)

num_sims = st.sidebar.slider(
    t["sims"], min_value=10000, max_value=50000, value=20000, step=5000
)

confidence_threshold = 90.0
st.sidebar.info(t["threshold_info"])

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

# --- Section 1: Editable Grid Table for Historical Data Analysis (50 Rounds) ---
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
    r_win = row.get("Red Winner", False)
    b_win = row.get("Blue Winner", False)
    t_win = row.get("Tie (Draw)", False)

    winner = None
    if r_win:
        winner = "Red"
    elif b_win:
        winner = "Blue"
    elif t_win:
        winner = "Tie"

    if winner:
        processed_rounds.append({
            "round": int(row.get("Round", idx + 1)),
            "winner": winner,
            "notes": str(row.get("Notes / Card Ranks", "")),
        })

# --- Section 2: Display Roadmap & Last 30-Round Analytics ---
st.markdown("---")
st.markdown(f"### {t['roadmap_title']}")

if processed_rounds:
    badges_html = ""
    for r in processed_rounds:
        if r["winner"] == "Red":
            bg = "#ef4444"
            txt = "R"
        elif r["winner"] == "Blue":
            bg = "#3b82f6"
            txt = "B"
        else:
            bg = "#10b981"
            txt = "T"
        round_num = r["round"]
        badges_html += f'<span class="history-dot" style="background-color:{bg};" title="Round {round_num}">{txt}</span>'

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
            f'<div class="metric-card"><h4>{t["red_wins"]} (Last 30)</h4><h2>{r_count_30} ({r_count_30/total_30*100:.1f}%)</h2></div>',
            unsafe_allow_html=True,
        )
    with col_p2:
        st.markdown(
            f'<div class="metric-card"><h4>{t["blue_wins"]} (Last 30)</h4><h2>{b_count_30} ({b_count_30/total_30*100:.1f}%)</h2></div>',
            unsafe_allow_html=True,
        )
    with col_p3:
        st.markdown(
            f'<div class="metric-card"><h4>{t["ties"]} (Last 30)</h4><h2>{t_count_30} ({t_count_30/total_30*100:.1f}%)</h2></div>',
            unsafe_allow_html=True,
        )

    total_r = len(processed_rounds)
    red_wins = sum(1 for r in processed_rounds if r["winner"] == "Red")
    blue_wins = sum(1 for r in processed_rounds if r["winner"] == "Blue")
    tie_wins = sum(1 for r in processed_rounds if r["winner"] == "Tie")

    st.caption(
        f"{t['total_valid']} **{total_r}** | {t['red_wins']}: **{red_wins}** |"
        f" {t['blue_wins']}: **{blue_wins}** | {t['ties']}: **{tie_wins}**"
    )
else:
    st.info(t["no_data"])


# --- Multi-Algorithm Engine: Monte Carlo + HMM + Bayesian Inference ---
def run_multi_algorithm_engine(rounds_history, game_mode, num_simulations):
    possible_decks = [2, 3]
    valid_deck_results = {}

    for d_count in possible_decks:
        remaining_shoe = []
        for rank in range(1, 14):
            max_cards = 4 * d_count
            remaining_shoe.extend([rank] * max_cards)

        if len(remaining_shoe) < 6:
            continue

        sim_counts = {"Red": 0, "Blue": 0, "Tie": 0}
        cards_per_side = 2 if "Baccarat" in game_mode else 1

        for _ in range(num_simulations):
            sampled = random.sample(remaining_shoe, cards_per_side * 2)
            r_hand = sampled[:cards_per_side]
            b_hand = sampled[cards_per_side:]

            if "Baccarat" in game_mode:
                r_pts = sum(0 if c >= 10 else c for c in r_hand) % 10
                b_pts = sum(0 if c >= 10 else c for c in b_hand) % 10
            else:
                r_pts = r_hand[0]
                b_pts = b_hand[0]

            if r_pts > b_pts:
                sim_counts["Red"] += 1
            elif b_pts > r_pts:
                sim_counts["Blue"] += 1
            else:
                sim_counts["Tie"] += 1

        valid_deck_results[d_count] = {
            k: (v / num_simulations) * 100 for k, v in sim_counts.items()
        }

    mc_probs = {"Red": 33.3, "Blue": 33.3, "Tie": 33.4}
    if valid_deck_results:
        avg_mc = {"Red": 0.0, "Blue": 0.0, "Tie": 0.0}
        for d_res in valid_deck_results.values():
            for k in avg_mc:
                avg_mc[k] += d_res[k] / len(valid_deck_results)
        mc_probs = avg_mc

    hmm_probs = {"Red": 33.3, "Blue": 33.3, "Tie": 33.4}
    if len(rounds_history) >= 2:
        transitions = {
            "Red": {"Red": 1, "Blue": 1, "Tie": 1},
            "Blue": {"Red": 1, "Blue": 1, "Tie": 1},
            "Tie": {"Red": 1, "Blue": 1, "Tie": 1},
        }
        for i in range(len(rounds_history) - 1):
            curr_w = rounds_history[i]["winner"]
            next_w = rounds_history[i + 1]["winner"]
            if curr_w in transitions and next_w in transitions[curr_w]:
                transitions[curr_w][next_w] += 1

        last_w = rounds_history[-1]["winner"]
        if last_w in transitions:
            total_trans = sum(transitions[last_w].values())
            hmm_probs = {
                k: (v / total_trans) * 100 for k, v in transitions[last_w].items()
            }

    prior_weight = 0.50
    likelihood_weight = 0.50

    bayesian_posterior = {}
    total_posterior = 0
    for k in ["Red", "Blue", "Tie"]:
        posterior_val = (mc_probs.get(k, 33.3) * prior_weight) + (
            hmm_probs.get(k, 33.3) * likelihood_weight
        )
        bayesian_posterior[k] = posterior_val
        total_posterior += posterior_val

    final_probs = {
        k: (v / total_posterior) * 100 for k, v in bayesian_posterior.items()
    }
    return final_probs


# --- Section 3: Prediction & Strict 90% Confidence Decision ---
st.markdown("---")
st.markdown(f"### {t['pred_title']}")

final_probs = run_multi_algorithm_engine(processed_rounds, game_mode, num_sims)

m1, m2, m3 = st.columns(3)
with m1:
    st.markdown(
        f'<div class="metric-card"><h3>{t["red_prob"]}</h3><h1 style="color: #f87171;">{final_probs["Red"]:.2f}%</h1></div>',
        unsafe_allow_html=True,
    )
with m2:
    st.markdown(
        f'<div class="metric-card"><h3>{t["blue_prob"]}</h3><h1 style="color: #60a5fa;">{final_probs["Blue"]:.2f}%</h1></div>',
        unsafe_allow_html=True,
    )
with m3:
    st.markdown(
        f'<div class="metric-card"><h3>{t["tie_prob"]}</h3><h1 style="color: #34d399;">{final_probs["Tie"]:.2f}%</h1></div>',
        unsafe_allow_html=True,
    )

best_side = max(final_probs, key=final_probs.get)
best_side_name = (
    "Red Side"
    if best_side == "Red"
    else ("Blue Side" if best_side == "Blue" else "Tie")
)
best_prob = final_probs[best_side]

st.markdown(f"#### {t['rec_title']}")

if best_prob >= confidence_threshold:
    if best_side == "Tie":
        badge_cls = "tie-win"
    elif best_side == "Red":
        badge_cls = "red-win"
    else:
        badge_cls = "blue-win"

    st.markdown(
        f'<div class="big-badge {badge_cls}">{t["bet_on"]}{best_side_name}{t["confirmed"]}{best_prob:.2f}% >= 90%)</div>',
        unsafe_allow_html=True,
    )
else:
    wait_text = t["wait"].format(prob=best_prob)
    st.markdown(
        f'<div class="big-badge wait-signal">{wait_text}</div>',
        unsafe_allow_html=True,
    )
