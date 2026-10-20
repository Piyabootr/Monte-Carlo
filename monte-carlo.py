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
    "🃏 Card Shoe Monte Carlo Predictor & Last 30-Round Historical Analytics"
)
st.markdown(
    "Predicting the next round outcome based on **Remaining Cards in the Shoe** and **Last 30-Round Historical Trend Analysis**."
)

# Initialize Session State
if "rounds" not in st.session_state:
    st.session_state.rounds = []

if "used_cards" not in st.session_state:
    st.session_state.used_cards = []

CARD_NAMES = {
    1: "A (1)",
    2: "2",
    3: "3",
    4: "4",
    5: "5",
    6: "6",
    7: "7",
    8: "8",
    9: "9",
    10: "10",
    11: "J",
    12: "Q",
    13: "K",
}


def get_card_point(card_rank, game_mode):
    if "Baccarat" in game_mode:
        return 0 if card_rank >= 10 else card_rank
    else:
        return card_rank


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

# Strict Confidence Threshold set to 90% as requested
confidence_threshold = 90.0
st.sidebar.info(
    f"🔒 Strict Decision Threshold: **{confidence_threshold}%**\n\n(Will advise to bet **ONLY** if confidence reaches 90%+)"
)

st.sidebar.markdown("---")
if st.sidebar.button(
    "🗑️ Reset Shoe & Clear History", use_container_width=True
):
    st.session_state.rounds = []
    st.session_state.used_cards = []
    st.rerun()

# --- Section 1: Record Round History & Cards ---
st.subheader("1️⃣ Record Round History & Drawn Cards")

col_in1, col_in2, col_in3 = st.columns([2, 2, 1.5])

with col_in1:
    red_selected = st.multiselect(
        "🔴 Cards Drawn by【Red Side】:",
        options=list(CARD_NAMES.keys()),
        format_func=lambda x: CARD_NAMES[x],
        key="red_input",
    )

with col_in2:
    blue_selected = st.multiselect(
        "🔵 Cards Drawn by【Blue Side】:",
        options=list(CARD_NAMES.keys()),
        format_func=lambda x: CARD_NAMES[x],
        key="blue_input",
    )

with col_in3:
    winner_choice = st.selectbox(
        "🏆 Actual Winner:",
        options=[
            "Auto-calculate from cards",
            "Red Win",
            "Blue Win",
            "Tie (Draw)",
        ],
    )

btn_col1, btn_col2 = st.columns([1, 1])
with btn_col1:
    if st.button("➕ Record Round", type="primary", use_container_width=True):
        if (
            not red_selected
            and not blue_selected
            and winner_choice == "Auto-calculate from cards"
        ):
            st.warning(
                "⚠️ Please select cards or specify the winner before recording."
            )
        else:
            if winner_choice == "Auto-calculate from cards":
                if "Baccarat" in game_mode:
                    r_score = (
                        sum(get_card_point(c, game_mode) for c in red_selected)
                        % 10
                    )
                    b_score = (
                        sum(get_card_point(c, game_mode) for c in blue_selected)
                        % 10
                    )
                else:
                    r_score = sum(
                        get_card_point(c, game_mode) for c in red_selected
                    )
                    b_score = sum(
                        get_card_point(c, game_mode) for c in blue_selected
                    )

                if r_score > b_score:
                    win_res = "Red"
                elif b_score > r_score:
                    win_res = "Blue"
                else:
                    win_res = "Tie"
            else:
                if "Red" in winner_choice:
                    win_res = "Red"
                elif "Blue" in winner_choice:
                    win_res = "Blue"
                else:
                    win_res = "Tie"

            st.session_state.rounds.append({
                "round": len(st.session_state.rounds) + 1,
                "red_raw": red_selected,
                "blue_raw": blue_selected,
                "red_cards": [CARD_NAMES[c] for c in red_selected],
                "blue_cards": [CARD_NAMES[c] for c in blue_selected],
                "raw_cards": red_selected + blue_selected,
                "winner": win_res,
            })
            st.session_state.used_cards.extend(red_selected + blue_selected)
            st.rerun()

with btn_col2:
    if st.button("↩️ Undo Last Round", use_container_width=True):
        if st.session_state.rounds:
            last_round = st.session_state.rounds.pop()
            for c in last_round["raw_cards"]:
                if c in st.session_state.used_cards:
                    st.session_state.used_cards.remove(c)
            st.rerun()

# --- Section 2: Display History Table & Pivot Analytics ---
st.markdown("---")
st.subheader(
    "2️⃣ Shoe History Table & Last 30-Round Historical Pivot Analytics"
)

if st.session_state.rounds:
    badges_html = ""
    for r in st.session_state.rounds:
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

    tab_hist1, tab_hist2 = st.tabs([
        "📋 Detailed Round History",
        "📊 Last 30-Round Pivot Analytics",
    ])

    with tab_hist1:
        df_hist = pd.DataFrame([
            {
                "Round": r["round"],
                "Red Cards": (
                    ", ".join(r["red_cards"]) if r["red_cards"] else "-"
                ),
                "Blue Cards": (
                    ", ".join(r["blue_cards"]) if r["blue_cards"] else "-"
                ),
                "Winner": (
                    "🔴 Red"
                    if r["winner"] == "Red"
                    else ("🔵 Blue" if r["winner"] == "Blue" else "🟢 Tie")
                ),
            }
            for r in st.session_state.rounds
        ])
        st.dataframe(df_hist, use_container_width=True, hide_index=True)

    with tab_hist2:
        st.markdown(
            "**Last 30-Round Trend & Card Frequency Pivot:** Analyzes the subset of the last 30 rounds (or all rounds if less than 30)."
        )
        # ดึงเฉพาะ 30ตาล่าสุดมาทำ Pivot วิเคราะห์
        last_30_rounds = st.session_state.rounds[-30:]
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
            "Last 30 Rounds - Ties",
            f"{t_count_30} ({t_count_30/total_30*100:.1f}%)",
        )

        pivot_data = []
        for rank in range(1, 14):
            used_count = st.session_state.used_cards.count(rank)
            pivot_data.append({
                "Card Rank": CARD_NAMES[rank],
                "Used (2 Decks Max: 8)": f"{used_count} / 8",
                "Used (3 Decks Max: 12)": f"{used_count} / 12",
                "Total Used in Shoe": used_count,
            })
        df_pivot = pd.DataFrame(pivot_data)
        st.dataframe(df_pivot, use_container_width=True, hide_index=True)

    total_r = len(st.session_state.rounds)
    red_wins = sum(1 for r in st.session_state.rounds if r["winner"] == "Red")
    blue_wins = sum(1 for r in st.session_state.rounds if r["winner"] == "Blue")
    tie_wins = sum(1 for r in st.session_state.rounds if r["winner"] == "Tie")

    st.caption(
        f"Total Rounds Recorded: **{total_r}** | Red Wins: **{red_wins}** | Blue Wins: **{blue_wins}** | Ties: **{tie_wins}** | Cards Used: **{len(st.session_state.used_cards)}**"
    )
else:
    st.info(
        "No rounds recorded yet in this shoe. Please record round history."
    )


# --- Monte Carlo Simulation Combined with Last 30-Round History ---
def run_monte_carlo_with_history(
    used_cards, rounds_history, game_mode, num_simulations
):
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

    # ค่าเฉลี่ยจากส่วนที่เหลือในสำรับ (Shoe Composition)
    avg_deck_probs = {"Red": 0.0, "Blue": 0.0, "Tie": 0.0}
    for d_res in valid_deck_results.values():
        for k in avg_deck_probs:
            avg_deck_probs[k] += d_res[k] / len(valid_deck_results)

    # ผสมผสานน้ำหนักจากประวัติ 30 ตาล่าสุด (History Trend Weighting: 70% Shoe Probability + 30% Last 30 Rounds Trend)
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
st.subheader(
    "3️⃣ Monte Carlo & Last 30-Round Prediction & Strict Betting Decision"
)

final_probs, deck_breakdown = run_monte_carlo_with_history(
    st.session_state.used_cards, st.session_state.rounds, game_mode, num_sims
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

# ตรรกะคุมเข้ม: ถ้าความน่าจะเป็นสูงสุดไม่ถึง 90% ห้ามแนะนำให้ลงแทงเด็ดขาด
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
        f'<div class="big-badge wait-signal">⛔ Recommendation: 【DO NOT BET / WAIT】 — Confidence is {best_prob:.2f}% (Below the strict 90% requirement). Skip this round!</div>',
        unsafe_allow_html=True,
    )

if deck_breakdown:
    with st.expander("🔍 View Simulation Breakdown by Deck Hypotheses"):
        cols = st.columns(len(deck_breakdown))
        for idx, (d_num, d_res) in enumerate(deck_breakdown.items()):
            with cols[idx]:
                st.markdown(f"**Hypothesis: {d_num} Decks Left**")
                st.write(f"- Red: `{d_res['Red']:.2f}%`")
                st.write(f"- Blue: `{d_res['Blue']:.2f}%`")
                st.write(f"- Tie: `{d_res['Tie']:.2f}%`")
