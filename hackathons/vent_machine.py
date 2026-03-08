"""
📣 THE VENT MACHINE — Anonymous Peer Support Network
Hackabyte Spring 2026 | DigiPen, Redmond WA

Run with: streamlit run vent_machine.py

Requirements:
    pip install streamlit plotly pandas mysql-connector-python

Make sure MySQL is running and you have initialized the DB:
    mysql -u root -p < database.sql
"""

import streamlit as st
import mysql.connector
import pandas as pd
import plotly.express as px
from datetime import datetime
import uuid
import random

# ── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="The Venting Machine 📣",
    page_icon="📣",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── MySQL Connection ───────────────────────────────────────────────────────────
DB_CONFIG = {
    "host":     "localhost",
    "port":     3306,
    "user":     "nopassuser",        
    "password": "",    
    "database": "ventmachine",
}

def get_conn():
    return mysql.connector.connect(**DB_CONFIG)

def query(sql: str, params=None) -> pd.DataFrame:
    conn = get_conn()
    df = pd.read_sql(sql, conn, params=params)
    conn.close()
    return df

def execute(sql: str, params=None):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(sql, params or ())
    conn.commit()
    cur.close()
    conn.close()

def safe(text: str) -> str:
    """Sanitize user text for safe injection into HTML strings."""
    return (str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#39;"))

# ── Anonymous Session Token ────────────────────────────────────────────────────
if "session_token" not in st.session_state:
    st.session_state["session_token"] = str(uuid.uuid4())
SESSION = st.session_state["session_token"]

# ── Styling ────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg, #000510 0%, #000d1a 50%, #001428 100%); }
    h1, h2, h3 { color: #22d3ee !important; font-family: 'Courier New', monospace; }
    .post-card {
        background: rgba(34,211,238,0.07);
        border: 1px solid rgba(34,211,238,0.25);
        border-radius: 16px;
        padding: 20px 24px;
        margin: 14px 0;
    }
    .post-card-flagged {
        background: rgba(239,68,68,0.08);
        border: 1px solid rgba(239,68,68,0.35);
        border-radius: 16px;
        padding: 20px 24px;
        margin: 14px 0;
    }
    .reply-card {
        background: rgba(255,255,255,0.04);
        border-left: 3px solid rgba(34,211,238,0.4);
        border-radius: 0 10px 10px 0;
        padding: 12px 18px;
        margin: 8px 0 8px 24px;
    }
    .tip-badge {
        background: rgba(16,185,129,0.2);
        border: 1px solid #10b981;
        border-radius: 20px;
        padding: 2px 10px;
        font-size: 0.75rem;
        color: #10b981;
        display: inline-block;
        margin-left: 8px;
    }
    .mood-pill {
        border-radius: 20px;
        padding: 3px 12px;
        font-size: 0.8rem;
        font-weight: bold;
        display: inline-block;
        margin: 4px 2px;
    }
    .cat-pill {
        background: rgba(34,211,238,0.15);
        border: 1px solid rgba(34,211,238,0.3);
        border-radius: 20px;
        padding: 3px 10px;
        font-size: 0.78rem;
        color: #22d3ee;
        display: inline-block;
    }
    .safe-banner {
        background: rgba(16,185,129,0.1);
        border: 1px solid rgba(16,185,129,0.3);
        border-radius: 12px;
        padding: 14px 18px;
        margin: 10px 0;
        font-size: 0.9rem;
        color: rgba(255,255,255,0.8);
    }
    .stat-box {
        background: rgba(255,255,255,0.05);
        border-radius: 12px;
        padding: 14px;
        text-align: center;
    }
    .big-num { font-size: 2.2rem; font-weight: bold; color: #22d3ee; }
    .anon-note {
        background: rgba(34,211,238,0.08);
        border-left: 4px solid #22d3ee;
        border-radius: 0 10px 10px 0;
        padding: 12px 16px;
        font-size: 0.88rem;
        color: rgba(255,255,255,0.65);
        margin-bottom: 18px;
    }
    .post-text {
        margin: 12px 0 6px 0;
        font-size: 1.05rem;
        color: rgba(255,255,255,0.9);
        line-height: 1.6;
        white-space: pre-wrap;
        word-wrap: break-word;
    }
    .reply-text {
        margin: 6px 0;
        color: rgba(255,255,255,0.85);
        white-space: pre-wrap;
        word-wrap: break-word;
    }
    .meta-text {
        color: rgba(255,255,255,0.35);
        font-size: 0.8rem;
    }
</style>
""", unsafe_allow_html=True)

# ── Mood Colors ────────────────────────────────────────────────────────────────
MOOD_COLOR = {
    "overwhelmed": "#ef4444",
    "anxious":     "#f97316",
    "sad":         "#8b5cf6",
    "confused":    "#3b82f6",
    "angry":       "#dc2626",
    "lonely":      "#6366f1",
    "frustrated":  "#f59e0b",
    "okay":        "#10b981",
    "hopeful":     "#06b6d4",
}

MOOD_EMOJI = {
    "overwhelmed": "😵",
    "anxious":     "😰",
    "sad":         "😢",
    "confused":    "😕",
    "angry":       "😡",
    "lonely":      "😔",
    "frustrated":  "😤",
    "okay":        "😐",
    "hopeful":     "🌱",
}

MOODS = list(MOOD_COLOR.keys())

CRISIS_KEYWORDS = [
    "kill myself", "want to die", "end my life", "suicide", "self harm",
    "hurt myself", "can't go on", "no reason to live", "cutting",
]

def check_crisis(text: str) -> tuple[bool, str]:
    text_lower = text.lower()
    for kw in CRISIS_KEYWORDS:
        if kw in text_lower:
            return True, f"Contains phrase: '{kw}'"
    return False, ""

SUPPORT_REMINDERS = [
    "💙 You are not alone in what you are feeling.",
    "🌱 It is okay to not be okay. That is what this space is for.",
    "🤝 Every post here is someone brave enough to say what they are really feeling.",
    "✨ Your feelings are valid. Full stop.",
    "🔒 Everything here is anonymous. No names, no judgment.",
]

def _hex_to_rgb(hex_color: str) -> str:
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"{r},{g},{b}"

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 📣 The Venting Machine")
    st.markdown("*`// no names. no judgment. just humans.`*")
    st.divider()

    page = st.radio("Navigate", [
        "🏠 The Feed",
        "📝 Post a Vent",
        "🔖 Browse by Category",
        "📊 Community Stats",
    ])

    st.divider()

    try:
        total_posts   = query("SELECT COUNT(*) AS c FROM posts").iloc[0]["c"]
        total_replies = query("SELECT COUNT(*) AS c FROM replies").iloc[0]["c"]
        st.markdown(f"<div style='background:rgba(255,255,255,0.05); border-radius:12px; padding:14px; text-align:center;'><div style='font-size:2.2rem; font-weight:bold; color:#22d3ee;'>{total_posts}</div><div>Vents Posted</div></div>", unsafe_allow_html=True)
        st.markdown(" ")
        st.markdown(f"<div style='background:rgba(255,255,255,0.05); border-radius:12px; padding:14px; text-align:center;'><div style='font-size:2.2rem; font-weight:bold; color:#22d3ee;'>{total_replies}</div><div>Replies Sent</div></div>", unsafe_allow_html=True)
    except Exception as e:
        st.error(f"DB connection failed. Check DB_CONFIG.\n\n{e}")

    st.divider()
    st.markdown(f"<div style='background:rgba(34,211,238,0.08); border-left:4px solid #22d3ee; border-radius:0 10px 10px 0; padding:12px 16px; font-size:0.88rem; color:rgba(255,255,255,0.65);'>🔒 You are anonymous.<br>Session ID: <code>{SESSION[:8]}…</code></div>", unsafe_allow_html=True)

# ── Helper: render one post ────────────────────────────────────────────────────
def render_post(post: pd.Series, show_replies: bool = False):
    mood       = post.get("mood", "okay")
    category   = post.get("category", "Other") or "Other"
    flagged    = int(post.get("flagged", 0))
    post_id    = int(post["id"])
    color      = MOOD_COLOR.get(mood, "#888")
    emoji      = MOOD_EMOJI.get(mood, "💬")
    ts         = str(post.get("timestamp", ""))[:16]
    content    = str(post["content"])

    # Mood + category pills (simple enough for HTML)
    flag_html = "⚠️ Support resources below &nbsp;" if flagged else ""
    st.markdown(f"""
        {flag_html}
        <span style="background:rgba({_hex_to_rgb(color)},0.2); border:1px solid {color}; color:{color}; border-radius:20px; padding:3px 12px; font-size:0.8rem; font-weight:bold; display:inline-block; margin:4px 2px;">{emoji} {mood}</span>
        <span style="background:rgba(34,211,238,0.15); border:1px solid rgba(34,211,238,0.3); border-radius:20px; padding:3px 10px; font-size:0.78rem; color:#22d3ee; display:inline-block;">{safe(category)}</span>
    """, unsafe_allow_html=True)

    # Post content and metadata — native Streamlit, no HTML
    st.write(content)
    st.caption(f"💬 {post.get('reply_count', 0)} replies · {ts}")
    st.divider()

    if flagged:
        st.warning("💙 **If you are struggling**, you do not have to go through it alone.  \n**Crisis Text Line:** Text HOME to 741741  \n**988 Suicide & Crisis Lifeline:** Call or text 988  \n**Trevor Project (LGBTQ+):** 1-866-488-7386")

    if show_replies:
        replies = query(
            "SELECT * FROM replies_full WHERE post_id = %s ORDER BY helpful_count DESC, timestamp ASC",
            params=(post_id,)
        )
        if not replies.empty:
            for _, r in replies.iterrows():
                reply_id   = int(r["id"])
                helpful    = int(r.get("helpful_count", 0))
                is_tip     = r["is_tip"]

                with st.container():
                    if is_tip:
                        st.markdown("""<span style="background:rgba(16,185,129,0.2); border:1px solid #10b981; border-radius:20px; padding:2px 10px; font-size:0.75rem; color:#10b981; display:inline-block;">✅ Coping Tip</span>""", unsafe_allow_html=True)
                    st.write(f"> {r['content']}")
                    st.caption(f"💚 {helpful} found this helpful")

                already_voted = not query(
                    "SELECT id FROM helpful_votes WHERE reply_id=%s AND session_token=%s",
                    params=(reply_id, SESSION)
                ).empty
                if not already_voted:
                    if st.button("💚 Helpful", key=f"vote_{reply_id}_{post_id}"):
                        execute(
                            "INSERT IGNORE INTO helpful_votes (reply_id, session_token) VALUES (%s, %s)",
                            (reply_id, SESSION)
                        )
                        st.rerun()
                else:
                    st.caption("✅ You marked this helpful")

        with st.form(key=f"reply_form_{post_id}"):
            reply_text = st.text_area("Write a reply", placeholder="Share support, advice, or just let them know they are not alone...", height=80)
            is_tip     = st.checkbox("This is a coping tip / strategy")
            submit     = st.form_submit_button("💬 Send Reply")

        if submit and reply_text.strip():
            execute(
                "INSERT INTO replies (post_id, content, is_tip) VALUES (%s, %s, %s)",
                (post_id, reply_text.strip(), int(is_tip))
            )
            execute(
                "UPDATE posts SET reply_count = reply_count + 1 WHERE id = %s",
                (post_id,)
            )
            st.success("💬 Reply sent!")
            st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: THE FEED
# ══════════════════════════════════════════════════════════════════════════════
if page == "🏠 The Feed":
    st.title("📣 The Venting Machine")
    st.markdown(f"<div style='background:rgba(34,211,238,0.08); border-left:4px solid #22d3ee; border-radius:0 10px 10px 0; padding:12px 16px; font-size:0.88rem; color:rgba(255,255,255,0.65); margin-bottom:18px;'>🔒 <code>// fully anonymous</code> &nbsp;·&nbsp; {random.choice(SUPPORT_REMINDERS)}</div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        filter_mood = st.selectbox("Filter by mood", ["All moods"] + MOODS)
    with col2:
        sort_by = st.selectbox("Sort by", ["Newest first", "Most replies", "Needs support (no replies)"])
    with col3:
        show_flagged = st.checkbox("Show flagged only", value=False)

    where_clauses = []
    params        = []

    if filter_mood != "All moods":
        where_clauses.append("mood = %s")
        params.append(filter_mood)
    if show_flagged:
        where_clauses.append("flagged = 1")

    where_sql = ("WHERE " + " AND ".join(where_clauses)) if where_clauses else ""
    order_sql = {
        "Newest first":               "ORDER BY timestamp DESC",
        "Most replies":               "ORDER BY reply_count DESC, timestamp DESC",
        "Needs support (no replies)": "ORDER BY reply_count ASC, timestamp DESC",
    }.get(sort_by, "ORDER BY timestamp DESC")

    posts = query(f"SELECT * FROM posts_full {where_sql} {order_sql} LIMIT 30",
                  params=tuple(params) if params else None)

    if posts.empty:
        st.info("No posts yet. Be the first to vent! 📣")
    else:
        for _, post in posts.iterrows():
            with st.expander(f"💬 click to read & reply — {safe(str(post['content'])[:60])}..."):
                render_post(post, show_replies=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: POST A VENT
# ══════════════════════════════════════════════════════════════════════════════
elif page == "📝 Post a Vent":
    st.title("📝 Post a Vent")
    st.markdown("""
    <div style="background:rgba(34,211,238,0.08); border-left:4px solid #22d3ee; border-radius:0 10px 10px 0; padding:12px 16px; font-size:0.88rem; color:rgba(255,255,255,0.65); margin-bottom:18px;">
        🔒 <b>100% anonymous.</b> No account. No username. No trace.<br>
        <code>// this is a safe space. say what you are actually feeling.</code>
    </div>
    """, unsafe_allow_html=True)

    with st.form("vent_form"):
        content = st.text_area(
            "What is on your mind?",
            height=160,
            placeholder="Say it. Do not filter yourself. This is your space.\n\nTell us what is going on — school stress, friendship drama, family stuff, or just feeling off..."
        )

        col1, col2 = st.columns(2)
        with col1:
            mood = st.selectbox("How are you feeling right now?", MOODS,
                                format_func=lambda m: f"{MOOD_EMOJI.get(m, '')} {m.capitalize()}")
        with col2:
            categories = query("SELECT id, name FROM categories")
            cat_map    = dict(zip(categories["name"], categories["id"]))
            category   = st.selectbox("Category", list(cat_map.keys()))

        submitted = st.form_submit_button("📣 Post Anonymously", use_container_width=True)

    if submitted:
        if not content.strip():
            st.warning("Write something first!")
        else:
            flagged, flag_reason = check_crisis(content)
            cat_id = cat_map[category]
            execute(
                "INSERT INTO posts (content, category_id, mood, flagged, flag_reason) VALUES (%s, %s, %s, %s, %s)",
                (content.strip(), cat_id, mood, int(flagged), flag_reason or None)
            )
            st.success("📣 Posted! Your vent is out there — and someone will respond.")
            st.balloons()

            if flagged:
                st.markdown("""
                <div style="background:rgba(16,185,129,0.1); border:1px solid rgba(16,185,129,0.3); border-radius:12px; padding:14px 18px; margin:10px 0; font-size:0.9rem; color:rgba(255,255,255,0.8);">
                    💙 <b>We noticed your post might be describing something serious.</b><br>
                    You do not have to go through this alone. Here are people who want to help:<br><br>
                    <b>Crisis Text Line:</b> Text HOME to 741741<br>
                    <b>988 Suicide &amp; Crisis Lifeline:</b> Call or text <b>988</b><br>
                    <b>Trevor Project (LGBTQ+):</b> 1-866-488-7386<br>
                    <b>Teen Line:</b> 1-800-852-8336
                </div>
                """, unsafe_allow_html=True)
            else:
                st.info(f"💬 {random.choice(SUPPORT_REMINDERS)}")

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: BROWSE BY CATEGORY
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🔖 Browse by Category":
    st.title("🔖 Browse by Category")

    categories = query("SELECT id, name FROM categories")

    CAT_EMOJI_MAP = {
        "Academic":      "📚",
        "Social":        "👥",
        "Family":        "🏠",
        "Mental Health": "💙",
        "Other":         "💬",
    }

    for _, cat in categories.iterrows():
        cat_name  = cat["name"]
        cat_emoji = CAT_EMOJI_MAP.get(cat_name, "💬")
        count_df  = query("SELECT COUNT(*) AS c FROM posts_full WHERE category = %s", params=(cat_name,))
        count     = int(count_df.iloc[0]["c"])

        with st.expander(f"{cat_emoji} {cat_name} — {count} posts"):
            posts = query(
                "SELECT * FROM posts_full WHERE category = %s ORDER BY timestamp DESC LIMIT 10",
                params=(str(cat_name),)
            )
            if posts.empty:
                st.info("No posts in this category yet.")
            else:
                for _, post in posts.iterrows():
                    with st.expander(f"💬 {int(post.get('reply_count', 0))} replies — {safe(str(post['content'])[:60])}..."):
                        render_post(post, show_replies=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: COMMUNITY STATS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "📊 Community Stats":
    st.title("📊 Community Stats")
    st.markdown("*You are not alone — here is proof.*")

    try:
        total_posts   = query("SELECT COUNT(*) AS c FROM posts").iloc[0]["c"]
        total_replies = query("SELECT COUNT(*) AS c FROM replies").iloc[0]["c"]
        total_tips    = query("SELECT COUNT(*) AS c FROM replies WHERE is_tip=1").iloc[0]["c"]
        total_votes   = query("SELECT COUNT(*) AS c FROM helpful_votes").iloc[0]["c"]

        c1, c2, c3, c4 = st.columns(4)
        for col, num, label in zip(
            [c1, c2, c3, c4],
            [total_posts, total_replies, total_tips, total_votes],
            ["Vents Posted", "Replies Sent", "Coping Tips", "Helpful Votes"]
        ):
            col.markdown(f"<div style='background:rgba(255,255,255,0.05); border-radius:12px; padding:14px; text-align:center;'><div style='font-size:2.2rem; font-weight:bold; color:#22d3ee;'>{num}</div><div>{label}</div></div>", unsafe_allow_html=True)

        st.markdown(" ")
        col_left, col_right = st.columns(2)

        with col_left:
            mood_df = query("SELECT mood, COUNT(*) AS count FROM posts GROUP BY mood ORDER BY count DESC")
            if not mood_df.empty:
                fig = px.pie(mood_df, values="count", names="mood",
                             title="How the Community Is Feeling",
                             color="mood", color_discrete_map=MOOD_COLOR)
                fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="white")
                st.plotly_chart(fig, use_container_width=True)

        with col_right:
            cat_df = query("""
                SELECT c.name AS category, COUNT(p.id) AS count
                FROM categories c
                LEFT JOIN posts p ON p.category_id = c.id
                GROUP BY c.name ORDER BY count DESC
            """)
            if not cat_df.empty:
                fig2 = px.bar(cat_df, x="category", y="count",
                              title="Posts by Category",
                              color="count", color_continuous_scale="Blues")
                fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                                   font_color="white", showlegend=False, coloraxis_showscale=False)
                st.plotly_chart(fig2, use_container_width=True)

        timeline_df = query("""
            SELECT DATE(timestamp) AS post_date, COUNT(*) AS count
            FROM posts GROUP BY DATE(timestamp) ORDER BY post_date
        """)
        if not timeline_df.empty:
            fig3 = px.area(timeline_df, x="post_date", y="count",
                           title="📅 Vents Over Time",
                           color_discrete_sequence=["#22d3ee"])
            fig3.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="white")
            st.plotly_chart(fig3, use_container_width=True)

        st.markdown("""
        <div style="background:rgba(34,211,238,0.08); border-left:4px solid #22d3ee; border-radius:0 10px 10px 0; padding:12px 16px; font-size:0.88rem; color:rgba(255,255,255,0.65); margin-top:20px; text-align:center;">
            <code>// every number above is a real teen who showed up and said something honest. 💙</code>
        </div>
        """, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Could not load stats. Check your MySQL connection.\n\n{e}")