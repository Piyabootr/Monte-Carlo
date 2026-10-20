import random
import pandas as pd
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Card Shoe Monte Carlo Simulator", page_icon="🃏", layout="wide"
)

# Custom CSS Styling
st.markdown(
    """
<style>
    .big-badge {
        font-size: 22px;
        font-weight: bold;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 15px;
    }
    .red-win { background-color: #ff4b4b; color: white; }
    .blue-win { background-color: #1f77b4; color: white; }
    .tie-win { background-color: #2ca02c; color: white; }
    .wait-signal { background-color: #6c757d; color: white; }
    .history-dot {
        display: inline-block;
        width: 35px;
        height: 35px;
        line-height: 35px;
        border-radius: 50%;
        text-align: center;
        font-weight: bold;
        color: white;
        margin: 3px;
        font-size: 13px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
</style>
""",
    unsafe_allow_html=True,
)

st.title(
    "🃏 Card Shoe Monte Carlo Predictor & Editable Grid History Analytics"
)
st.markdown(
    "Predicting outcomes using **Editable Grid Data Entry**, **Last 30-Round Analytics**, and **Remaining Cards Simulation**."
)

# Initialize Session State for Grid Table History
if "grid_history" not in st.session_state:
    initial_data = []
    for i in range(1, 11):
        initial_data.append({
            "Round": i,
            "Red Winner": False,
            "Blue Winner": False,
            "Tie (Draw)": False,
            "Notes / Card Ranks": "",
        })
    st.session_state.grid_history = pd.DataFrame(initial_data)

# --- Sidebar Settings ---
st.sidebar.header("⚙️ Simulation Parameters")

game_mode = st.sidebar.radio(
    "Game Scoring Mode:",
    [
        "Baccarat / Dragon Tiger Style (10, J, Q, K = 0 for Baccarat)",
        "Single Card High Value (A=1 to K=13)",
    ],
)

num_sims = st.sidebar.slider(
    "Monte Carlo Iterations (per deck)",
    min_value=10000,
    max_value=50000,
    value=20000,
    step=5000,
)

# Strict Confidence Threshold set to 90%
confidence_threshold = 90.0
st.sidebar.info(
    f"🔒 Strict Decision Threshold: **{confidence_threshold}%**\n\n(Will advise to bet **ONLY** if confidence reaches 90%+)"
)

st.sidebar.markdown("---")
if st.sidebar.button(
    "🗑️ Reset Grid Data & Clear History", use_container_width=True
):
    reset_data = []
    for i in range(1, 11):
        reset_data.append({
            "Round": i,
            "Red Winner": False,
            "Blue Winner": False,
            "Tie (Draw)": False,
            "Notes / Card Ranks": "",
        })
    st.session_state.grid_history = pd.DataFrame(reset_data)
    st.rerun()

# --- Section 1: Editable Grid Table for Historical Data Analysis ---
st.subheader("1️⃣ Editable Grid Table (Historical Data Entry & Analysis)")
st.markdown(
    "💡 **คุณสามารถคลิกช่องในตารางด้านล่างเพื่อพิมพ์ หรือติ๊กเลือกผลย้อนหลังได้โดยตรงเหมือน Excel** เพื่อให้ระบบนำไปวิเคราะห์ผลลัพธ์ 30 ตาและรัน Monte Carlo ต่อไป"
)

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
st.subheader("2️⃣ Roadmap & Last 30-Round Trend Analytics")

if processed_rounds:
    badges_html = ""
    for r in processed_rounds:
        if r["winner"] == "Red":
            bg = "#ff4b4b"
            txt = "R"
        elif r["winner"] == "Blue":
            bg = "#1f77b4"
            txt = "B"
        else:
            bg = "#2ca02c"
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
    col_p1.metric(
        "Last 30 Rounds - Red Wins",
        f"{r_count_30} ({r_count_30/total_30*100:.1f}%)",
    )
    col_p2.metric(
        "Last 30 Rounds - Blue Wins",
        f"{b_count_30} ({b_count_30/total_30*100:.1f}%)",
    )
    col_p3.metric(
        "Last 30 Rounds - Ties", f"{t_count_30} ({t_count_30/total_30*100:.1f}%)"
    )

    total_r = len(processed_rounds)
    red_wins = sum(1 for r in processed_rounds if r["winner"] == "Red")
    blue_wins = sum(1 for r in processed_rounds if r["winner"] == "Blue")
    tie_wins = sum(1 for r in processed_rounds if r["winner"] == "Tie")

    st.caption(
        f"Total Valid Rounds: **{total_r}** | Red Wins: **{red_wins}** | Blue Wins: **{blue_wins}** | Ties: **{tie_wins}**"
    )
else:
    st.info(
        "กรุณากรอกข้อมูลผลแพ้ชนะในตารางกริดด้านบน (ติ๊กถูกช่อง Red, Blue หรือ Tie) เพื่อเริ่มการวิเคราะห์"
    )


# --- Monte Carlo Simulation Combined with Last 30-Round History ---
def run_monte_carlo_grid(used_cards, rounds_history, game_mode, num_simulations):
    possible_decks = [2, 3]
    valid_deck_results = {}

    for d_count in possible_decks:
        remaining_shoe = []
        is_possible = True

        for rank in range(1, 14):
            max_cards = 4 * d_count
            used_count = used_cards.count(rank)
            if used_count > max_cards:
                is_possible = False
                break
            remaining_shoe.extend([rank] * (max_cards - used_count))

        if not is_possible or len(remaining_shoe) < 6:
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

    if not valid_deck_results:
        return {"Red": 45.0, "Blue": 45.0, "Tie": 10.0}, {}

    avg_deck_probs = {"Red": 0.0, "Blue": 0.0, "Tie": 0.0}
    for d_res in valid_deck_results.values():
        for k in avg_deck_probs:
            avg_deck_probs[k] += d_res[k] / len(valid_deck_results)

    if len(rounds_history) > 0:
        last_30 = rounds_history[-30:]
        h_red = sum(1 for r in last_30 if r["winner"] == "Red")
        h_blue = sum(1 for r in last_30 if r["winner"] == "Blue")
        h_tie = sum(1 for r in last_30 if r["winner"] == "Tie")
        h_total = len(last_30)

        hist_probs = {
            "Red": (h_red / h_total) * 100,
            "Blue": (h_blue / h_total) * 100,
            "Tie": (h_tie / h_total) * 100,
        }

        for k in avg_deck_probs:
            avg_deck_probs[k] = (avg_deck_probs[k] * 0.70) + (
                hist_probs[k] * 0.30
            )

    total_p = sum(avg_deck_probs.values())
    final_probs = {k: (v / total_p) * 100 for k, v in avg_deck_probs.items()}
    return final_probs, valid_deck_results


# --- Section 3: Prediction & Strict 90% Confidence Decision ---
st.markdown("---")
st.subheader("3️⃣ Monte Carlo Next Round Prediction & Strict Betting Decision")

final_probs, deck_breakdown = run_monte_carlo_grid(
    [], processed_rounds, game_mode, num_sims
)

m1, m2, m3 = st.columns(3)
m1.metric("🔴 Red Win Probability", f"{final_probs['Red']:.2f}%")
m2.metric("🔵 Blue Win Probability", f"{final_probs['Blue']:.2f}%")
m3.metric("🟢 Tie Probability", f"{final_probs['Tie']:.2f}%")

best_side = max(final_probs, key=final_probs.get)
best_side_name = (
    "Red Side"
    if best_side == "Red"
    else ("Blue Side" if best_side == "Blue" else "Tie")
)
best_prob = final_probs[best_side]

st.markdown("### 🎯 Betting Recommendation (Strict 90% Rule):")

if best_prob >= confidence_threshold:
    if best_side == "Tie":
        badge_cls = "tie-win"
    elif best_side == "Red":
        badge_cls = "red-win"
    else:
        badge_cls = "blue-win"

    st.markdown(
        f'<div class="big-badge {badge_cls}">✅ Recommendation: Bet on 【{best_side_name}】 — Absolutely Confirmed! (Confidence: {best_prob:.2f}% >= 90%)</div>',
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        f'<div class="big-badge wait-signal">⛔ Recommendation: 【DO NOT BET / WAIT】 — Confidence is {best_prob:.2f}% (Below strict 90% requirement). Skip this round!</div>',
        unsafe_allow_html=True,
    )
