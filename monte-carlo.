import random
import pandas as pd
import streamlit as st

# ตั้งค่าหน้าเว็บ Streamlit
st.set_page_config(
    page_title="Card Shoe Monte Carlo Simulator", page_icon="🃏", layout="wide"
)

# สไตล์ CSS เพิ่มเติมสำหรับ UI
st.markdown(
    """
<style>
    .big-badge {
        font-size: 24px;
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
        width: 38px;
        height: 38px;
        line-height: 38px;
        border-radius: 50%;
        text-align: center;
        font-weight: bold;
        color: white;
        margin: 4px;
        font-size: 14px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
</style>
""",
    unsafe_allow_html=True,
)

st.title("🃏 ระบบจำลอง Monte Carlo วิเคราะห์ไพ่ในขอน (2-3 สำรับ)")
st.markdown(
    "ระบบคำนวณความน่าจะเป็นจาก **ไพ่ที่ถูกเปิดออกไปแล้ว** (Drawing Without Replacement) โดยจำลองสถานการณ์พร้อมกันทั้งกรณีไพ่ 2 สำรับ และ 3 สำรับ"
)

# --- จัดการ Session State สำหรับเก็บประวัติ ---
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
    """คำนวณแต้มไพ่ตามโหมดกติกา"""
    if (
        game_mode
        == "โหมดแต้มรวมหลักหน่วย (เช่น บาคาร่า / ป๊อกเด้ง: 10, J, Q, K = 0 แต้ม)"
    ):
        return 0 if card_rank >= 10 else card_rank
    else:
        return card_rank


# --- แถบตั้งค่าด้านข้าง (Sidebar) ---
st.sidebar.header("⚙️ ตั้งค่าพารามิเตอร์การจำลอง")

game_mode = st.sidebar.radio(
    "รูปแบบการคิดแต้มของกติกา:",
    [
        "โหมดแต้มรวมหลักหน่วย (เช่น บาคาร่า / ป๊อกเด้ง: 10, J, Q, K = 0 แต้ม)",
        "โหมดวัดแต้มหน้าไพ่สูงสุด (เช่น เสือมังกร: A=1 ถึง K=13)",
    ],
)

num_sims = st.sidebar.slider(
    "จำนวนรอบจำลอง Monte Carlo (ต่อสำรับ)",
    min_value=5000,
    max_value=50000,
    value=20000,
    step=5000,
)
confidence_threshold = st.sidebar.slider(
    "เกณฑ์ความได้เปรียบขั้นต่ำที่จะฟันธง (%)",
    min_value=45.0,
    max_value=60.0,
    value=48.5,
    step=0.5,
)

st.sidebar.markdown("---")
if st.sidebar.button(
    "🗑️ ล้างข้อมูลเริ่มขอนใหม่ (Reset Shoe)", use_container_width=True
):
    st.session_state.rounds = []
    st.session_state.used_cards = []
    st.rerun()

# --- ส่วนที่ 1: บันทึกประวัติการออกของไพ่และฝ่ายที่ชนะ ---
st.subheader("1️⃣ บันทึกหน้าไพ่ที่ออกและฝ่ายที่ชนะในตานั้น")

col_in1, col_in2, col_in3 = st.columns([2, 2, 1.5])

with col_in1:
    red_selected = st.multiselect(
        "🔴 เลือกเลขไพ่ที่ออกของ【ฝ่ายแดง】:",
        options=list(CARD_NAMES.keys()),
        format_func=lambda x: CARD_NAMES[x],
        key="red_input",
    )

with col_in2:
    blue_selected = st.multiselect(
        "🔵 เลือกเลขไพ่ที่ออกของ【ฝ่ายน้ำเงิน】:",
        options=list(CARD_NAMES.keys()),
        format_func=lambda x: CARD_NAMES[x],
        key="blue_input",
    )

with col_in3:
    winner_choice = st.selectbox(
        "🏆 ฝ่ายที่ชนะในตานี้:",
        options=[
            "คำนวณอัตโนมัติจากหน้าไพ่",
            "แดง (Red)",
            "น้ำเงิน (Blue)",
            "เสมอ (Tie)",
        ],
    )

btn_col1, btn_col2 = st.columns([1, 1])
with btn_col1:
    if st.button(
        "➕ บันทึกผลตานี้เข้าสู่ระบบ", type="primary", use_container_width=True
    ):
        if (
            not red_selected
            and not blue_selected
            and winner_choice == "คำนวณอัตโนมัติจากหน้าไพ่"
        ):
            st.warning(
                "⚠️ กรุณาเลือกหน้าไพ่ของฝ่ายแดง/น้ำเงิน หรือระบุฝ่ายที่ชนะก่อนบันทึกครับ"
            )
        else:
            if winner_choice == "คำนวณอัตโนมัติจากหน้าไพ่":
                if "หลักหน่วย" in game_mode:
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
                if "แดง" in winner_choice:
                    win_res = "Red"
                elif "น้ำเงิน" in winner_choice:
                    win_res = "Blue"
                else:
                    win_res = "Tie"

            st.session_state.rounds.append({
                "round": len(st.session_state.rounds) + 1,
                "red_cards": [CARD_NAMES[c] for c in red_selected],
                "blue_cards": [CARD_NAMES[c] for c in blue_selected],
                "raw_cards": red_selected + blue_selected,
                "winner": win_res,
            })
            st.session_state.used_cards.extend(red_selected + blue_selected)
            st.rerun()

with btn_col2:
    if st.button(
        "↩️ ลบตาที่บันทึกไว้ล่าสุด (Undo)", use_container_width=True
    ):
        if st.session_state.rounds:
            last_round = st.session_state.rounds.pop()
            for c in last_round["raw_cards"]:
                if c in st.session_state.used_cards:
                    st.session_state.used_cards.remove(c)
            st.rerun()

# --- แสดงกระดานประวัติ (Roadmap & Card Counter) ---
st.markdown("---")
st.subheader("2️⃣ ประวัติการออกไพ่และสถานะขอนไพ่ปัจจุบัน")

if st.session_state.rounds:
    badges_html = ""
    for r in st.session_state.rounds:
        if r["winner"] == "Red":
            bg = "#ff4b4b"
            txt = "แดง"
        elif r["winner"] == "Blue":
            bg = "#1f77b4"
            txt = "น้ำเงิน"
        else:
            bg = "#2ca02c"
            txt = "เสมอ"
        badges_html += f'<span class="history-dot" style="background-color:{bg};" title="ตาที่ {r[\'round\']}">{txt}</span>'

    st.markdown(badges_html, unsafe_allow_html=True)

    total_r = len(st.session_state.rounds)
    red_wins = sum(1 for r in st.session_state.rounds if r["winner"] == "Red")
    blue_wins = sum(1 for r in st.session_state.rounds if r["winner"] == "Blue")
    tie_wins = sum(1 for r in st.session_state.rounds if r["winner"] == "Tie")

    st.caption(
        f"รวมทั้งหมด: **{total_r}** ตา | 🔴 แดงชนะ: **{red_wins}** | 🔵 น้ำเงินชนะ: **{blue_wins}** | 🟢 เสมอ: **{tie_wins}** | ไพ่ถูกเปิดออกไปแล้ว: **{len(st.session_state.used_cards)}** ใบ"
    )

    with st.expander("📋 ดูตารางรายละเอียดเลขไพ่ที่ออกย้อนหลัง"):
        df_hist = pd.DataFrame([
            {
                "ตาที่": r["round"],
                "ไพ่ฝ่ายแดง": (
                    ", ".join(r["red_cards"]) if r["red_cards"] else "-"
                ),
                "ไพ่ฝ่ายน้ำเงิน": (
                    ", ".join(r["blue_cards"]) if r["blue_cards"] else "-"
                ),
                "ฝ่ายที่ชนะ": (
                    "🔴 แดง"
                    if r["winner"] == "Red"
                    else ("🔵 น้ำเงิน" if r["winner"] == "Blue" else "🟢 เสมอ")
                ),
            }
            for r in st.session_state.rounds
        ])
        st.dataframe(df_hist, use_container_width=True, hide_index=True)
else:
    st.info(
        "ยังไม่มีประวัติไพ่ในขอนนี้ คุณสามารถเริ่มบันทึกไพ่ที่ออก หรือดูผลจำลองเริ่มต้นได้เลย"
    )


# --- ฟังก์ชันจำลอง Monte Carlo (2-3 สำรับ) ---
def run_multi_deck_monte_carlo(
    used_cards, rounds_history, game_mode, num_simulations=20000
):
    possible_decks = [2, 3]
    valid_deck_results = {}

    for d_count in possible_decks:
        remaining_shoe = []
        is_possible = True

        for rank in range(1, 14):
            max_cards_of_rank = 4 * d_count
            used_of_rank = used_cards.count(rank)

            if used_of_rank > max_cards_of_rank:
                is_possible = False
                break

            remaining_count = max_cards_of_rank - used_of_rank
            remaining_shoe.extend([rank] * remaining_count)

        if not is_possible or len(remaining_shoe) < 6:
            continue

        sim_counts = {"Red": 0, "Blue": 0, "Tie": 0}
        cards_per_side = 2 if "หลักหน่วย" in game_mode else 1

        for _ in range(num_simulations):
            sampled = random.sample(remaining_shoe, cards_per_side * 2)
            r_hand = sampled[:cards_per_side]
            b_hand = sampled[cards_per_side:]

            if "หลักหน่วย" in game_mode:
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
    for d_probs in valid_deck_results.values():
        for k in avg_deck_probs:
            avg_deck_probs[k] += d_probs[k] / len(valid_deck_results)

    if len(rounds_history) >= 3:
        last_winner = rounds_history[-1]["winner"]
        trans_counts = {"Red": 0, "Blue": 0, "Tie": 0}
        trans_total = 0
        for i in range(len(rounds_history) - 1):
            if rounds_history[i]["winner"] == last_winner:
                nxt = rounds_history[i + 1]["winner"]
                trans_counts[nxt] += 1
                trans_total += 1

        if trans_total > 0:
            for k in avg_deck_probs:
                markov_prob = (trans_counts[k] / trans_total) * 100
                avg_deck_probs[k] = (avg_deck_probs[k] * 0.80) + (
                    markov_prob * 0.20
                )

    total_p = sum(avg_deck_probs.values())
    final_probs = {k: (v / total_p) * 100 for k, v in avg_deck_probs.items()}

    return final_probs, valid_deck_results


# --- ส่วนที่ 3: แสดงผลการจำลองและคำแนะนำฟันธงล่วงหน้า ---
st.markdown("---")
st.subheader("3️⃣ ผลการจำลอง Monte Carlo ล่วงหน้า (ตาถัดไป)")

final_probs, deck_breakdown = run_multi_deck_monte_carlo(
    st.session_state.used_cards, st.session_state.rounds, game_mode, num_sims
)

m_col1, m_col2, m_col3 = st.columns(3)
m_col1.metric("🔴 โอกาสออก【ฝ่ายแดง】", f"{final_probs['Red']:.2f}%")
m_col2.metric("🔵 โอกาสออก【ฝ่ายน้ำเงิน】", f"{final_probs['Blue']:.2f}%")
m_col3.metric("🟢 โอกาสออก【เสมอ】", f"{final_probs['Tie']:.2f}%")

best_side = "Red" if final_probs["Red"] >= final_probs["Blue"] else "Blue"
best_side_th = "ฝ่ายแดง (Red)" if best_side == "Red" else "ฝ่ายน้ำเงิน (Blue)"
best_prob = final_probs[best_side]
prob_diff = abs(final_probs["Red"] - final_probs["Blue"])

st.markdown("### 🎯 คำแนะนำการตัดสินใจในตาถัดไป:")

if final_probs["Tie"] >= 20.0:
    st.markdown(
        f'<div class="big-badge tie-win">✅ ควรลง: 【เสมอ (Tie)】 — ถูกต้องเเน่นอน! (โอกาสพุ่งสูงถึง {final_probs["Tie"]:.2f}%)</div>',
        unsafe_allow_html=True,
    )
elif best_prob >= confidence_threshold and prob_diff >= 1.5:
    badge_class = "red-win" if best_side == "Red" else "blue-win"
    st.markdown(
        f'<div class="big-badge {badge_class}">✅ ควรลง: 【{best_side_th}】 — ถูกต้องเเน่นอน! (โอกาสชนะ {best_prob:.2f}% | เหนือกว่าอีกฝั่ง {prob_diff:.2f}%)</div>',
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        f'<div class="big-badge wait-signal">⛔ ตานี้【ไม่ควรลง (ข้าม/Wait)】 — ความน่าจะเป็นสองฝั่งยังสูสีกันเกินไป (ต่างกันเพียง {prob_diff:.2f}%) รอจังหวะไพ่ชัดเจนกว่านี้</div>',
        unsafe_allow_html=True,
    )

if deck_breakdown:
    with st.expander(
        "🔍 ดูผลการจำลองแยกตามสมมติฐานจำนวนสำรับ (2 สำรับ vs 3 สำรับ)"
    ):
        cols_d = st.columns(len(deck_breakdown))
        for idx, (d_num, d_res) in enumerate(deck_breakdown.items()):
            with cols_d[idx]:
                st.markdown(
                    f"**กรณีไพ่ขอนนี้มี {d_num} สำรับ ({d_num*52 - len(st.session_state.used_cards)} ใบที่เหลือ):**"
                )
                st.write(f"- 🔴 แดง: `{d_res['Red']:.2f}%`")
                st.write(f"- 🔵 น้ำเงิน: `{d_res['Blue']:.2f}%`")
                st.write(f"- 🟢 เสมอ: `{d_res['Tie']:.2f}%`")
else:
    st.error(
        "⚠️ จำนวนไพ่ที่ระบุเกินขีดจำกัดของไพ่ 3 สำรับ กรุณาตรวจสอบประวัติไพ่หรือกดล้างขอนใหม่"
    )
