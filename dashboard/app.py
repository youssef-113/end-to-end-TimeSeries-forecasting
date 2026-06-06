import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from pathlib import Path


st.set_page_config(
    page_title="Campaign Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
/* ── Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ── Root palette ── */
:root {
    --bg-base   : #080d14;
    --bg-card   : #0f1923;
    --bg-card2  : #141f2e;
    --border    : rgba(6,182,212,.18);
    --cyan      : #06b6d4;
    --cyan-soft : rgba(6,182,212,.12);
    --green     : #10b981;
    --amber     : #f59e0b;
    --rose      : #f43f5e;
    --purple    : #8b5cf6;
    --text-1    : #e2e8f0;
    --text-2    : #94a3b8;
    --text-3    : #475569;
    --radius    : 14px;
}

/* ── Base app background ── */
.stApp { background: var(--bg-base); font-family: 'DM Sans', sans-serif; }
.block-container { padding: 1.5rem 2.5rem 4rem; max-width: 1600px; }

/* ── Hide default Streamlit chrome (keep header for sidebar toggle) ── */
#MainMenu, footer { visibility: hidden; }
header { visibility: visible; }
/* Hide the main menu button in header but keep sidebar toggle */
#MainMenu button { visibility: hidden; }

/* ── Hero banner ── */
.hero {
    background: linear-gradient(135deg, #0a1628 0%, #0f2847 50%, #0a1628 100%);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 2.4rem 3rem;
    margin-bottom: 1.8rem;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute; inset: 0;
    background: radial-gradient(ellipse 60% 80% at 80% 50%, rgba(6,182,212,.07) 0%, transparent 70%);
}
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 2.1rem; font-weight: 800;
    color: #fff; letter-spacing: -.5px;
    margin: 0 0 .35rem;
}
.hero-title span { color: var(--cyan); }
.hero-sub {
    color: var(--text-2); font-size: 1rem;
    font-weight: 300; margin: 0;
}
.hero-badge {
    display: inline-block;
    background: var(--cyan-soft);
    border: 1px solid var(--border);
    color: var(--cyan);
    font-size: .72rem; font-weight: 600;
    letter-spacing: .08em; text-transform: uppercase;
    padding: .25rem .7rem; border-radius: 999px;
    margin-bottom: .85rem;
}

/* ── KPI cards ── */
.kpi-wrap {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.2rem 1.4rem 1rem;
    position: relative; overflow: hidden;
    transition: border-color .2s;
}
.kpi-wrap:hover { border-color: var(--cyan); }
.kpi-wrap::after {
    content: '';
    position: absolute; left: 0; top: 0; bottom: 0;
    width: 3px; border-radius: 3px 0 0 3px;
}
.kpi-cyan::after   { background: var(--cyan); }
.kpi-green::after  { background: var(--green); }
.kpi-amber::after  { background: var(--amber); }
.kpi-purple::after { background: var(--purple); }
.kpi-rose::after   { background: var(--rose); }
.kpi-teal::after   { background: #14b8a6; }

.kpi-icon { font-size: 1.5rem; margin-bottom: .4rem; opacity: .9; }
.kpi-val {
    font-family: 'Syne', sans-serif;
    font-size: 1.8rem; font-weight: 700;
    color: #fff; line-height: 1;
    margin-top: .5rem;
}
.kpi-label {
    font-size: .95rem; font-weight: 600;
    color: var(--text-1); margin-bottom: .5rem;
    text-transform: uppercase; letter-spacing: .06em;
    cursor: help;
    position: relative;
}
.kpi-wrap {
    position: relative;
}
.kpi-tooltip {
    position: absolute;
    bottom: calc(100% + 12px);
    left: 50%;
    transform: translateX(-50%);
    background: #0f1923;
    border: 1px solid var(--border);
    color: var(--text-1);
    font-size: .85rem;
    font-weight: 400;
    padding: .75rem 1rem;
    border-radius: 10px;
    white-space: normal;
    width: 280px;
    max-width: 280px;
    z-index: 9999;
    box-shadow: 0 8px 24px rgba(0,0,0,.5);
    text-transform: none;
    letter-spacing: normal;
    line-height: 1.4;
    opacity: 0;
    visibility: hidden;
    transition: opacity 0.2s ease, visibility 0.2s ease;
    pointer-events: none;
}
.kpi-wrap:hover .kpi-tooltip {
    opacity: 1;
    visibility: visible;
}
.kpi-tooltip::before {
    content: '';
    position: absolute;
    bottom: -8px;
    left: 50%;
    transform: translateX(-50%);
    border-left: 8px solid transparent;
    border-right: 8px solid transparent;
    border-top: 8px solid #0f1923;
}
.kpi-tooltip::after {
    content: '';
    position: absolute;
    bottom: -10px;
    left: 50%;
    transform: translateX(-50%);
    border-left: 10px solid transparent;
    border-right: 10px solid transparent;
    border-top: 10px solid var(--border);
}

/* ── Section headers ── */
.sec-hdr {
    font-family: 'Syne', sans-serif;
    font-size: 1.05rem; font-weight: 700;
    color: var(--text-1);
    border-left: 3px solid var(--cyan);
    padding-left: .65rem;
    margin: 0 0 .9rem;
}

/* ── Chart card wrapper ── */
.chart-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.2rem 1.2rem .4rem;
    margin-bottom: .1rem;
}

/* ── Insight cards ── */
.insight {
    border-radius: var(--radius);
    padding: 1.2rem 1.4rem;
    border: 1px solid;
}
.insight-blue  { background:#0c2035; border-color:#1e4d7b; }
.insight-amber { background:#1a1200; border-color:#713f12; }
.insight-green { background:#042014; border-color:#14532d; }
.insight-title { font-weight:700; font-size:.9rem; color:#fff; margin:0 0 .4rem; }
.insight-body  { font-size:.82rem; color:var(--text-2); margin:0; line-height:1.5; }

/* ── Divider ── */
.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--border), transparent);
    margin: 1.6rem 0;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: #0a1221 !important;
    border-right: 1px solid var(--border);
}
section[data-testid="stSidebar"] .stSelectbox label,
section[data-testid="stSidebar"] .stDateInput label,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span { color: var(--text-2) !important; }
.sidebar-brand {
    font-family: 'Syne', sans-serif;
    font-size: 1.15rem; font-weight: 800;
    color: var(--cyan); margin-bottom: .2rem;
}
.sidebar-sub { font-size:.78rem; color:var(--text-3); margin-bottom:1.4rem; }
.filter-badge {
    background: var(--cyan-soft);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: .6rem 1rem;
    color: var(--cyan);
    font-size:.82rem; font-weight:600;
    text-align:center;
    margin-top:1rem;
}

/* ── Tab bar ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 4px;
    background: var(--bg-card);
    border-radius: 10px;
    padding: 5px;
    border: 1px solid var(--border);
}
.stTabs [data-baseweb="tab"] {
    border-radius: 7px !important;
    color: var(--text-2) !important;
    font-weight: 500 !important;
    padding: .45rem 1.2rem !important;
    transition: all .2s;
}
.stTabs [aria-selected="true"] {
    background: var(--cyan-soft) !important;
    color: var(--cyan) !important;
    border-bottom: none !important;
}

/* ── Dataframe ── */
.stDataFrame { border-radius: 10px; overflow: hidden; }

/* ── Footer ── */
.footer {
    text-align:center; color:var(--text-3);
    font-size:.78rem; padding: 2rem 0 .5rem;
}
.footer a { color:var(--cyan); text-decoration:none; }
</style>
""", unsafe_allow_html=True)


LAYOUT_BASE = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="DM Sans, sans-serif", color="#94a3b8", size=11),
    margin=dict(l=0, r=10, t=30, b=0),
    xaxis=dict(gridcolor="rgba(255,255,255,.05)", zerolinecolor="rgba(255,255,255,.08)"),
    yaxis=dict(gridcolor="rgba(255,255,255,.05)", zerolinecolor="rgba(255,255,255,.08)"),
    legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#94a3b8")),
    hoverlabel=dict(bgcolor="#0f1923", bordercolor="#06b6d4",
                    font=dict(color="#e2e8f0", family="DM Sans, sans-serif")),
)

def apply_theme(fig, height=340, title=""):
    layout = dict(LAYOUT_BASE)
    layout["height"] = height
    if title:
        layout["title"] = dict(text=title, font=dict(
            color="#e2e8f0", size=13, family="Syne, sans-serif"))
    fig.update_layout(**layout)
    return fig

# Status colour palette — matches Closing_status values in the cleaned data
STATUS_COLORS = {
    "Approved"              : "#10b981",
    "Cancelled"             : "#f43f5e",
    "Not interested"        : "#fb7185",
    "Not Eligible"          : "#f59e0b",
    "Follow up"             : "#38bdf8",
    "Pending Bank Approval" : "#8b5cf6",
    "Postdated"             : "#fb923c",
    "Retransfer to Client"  : "#2dd4bf",
    "Not closed"            : "#64748b",
}

@st.cache_data(show_spinner=False)
def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)

    # Parse date columns (already ISO-formatted in the cleaned file)
    DATE_COLS = [
        "Assign Date", "Finish Date", "Validation Date",
        "Date of Sale", "Creation Date", "Date of Payment",
        "sale Week", "sale Day",
    ]
    for col in DATE_COLS:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    # Minor text normalisation
    for col in ["Product", "Gender"]:
        if col in df.columns:
            df[col] = df[col].str.strip().str.title()

    return df

BASE_DIR = Path(__file__).resolve().parent
ROOT_DIR = BASE_DIR.parent   # go up from dashboard → repo root

DATA_PATH = ROOT_DIR / "data" / "data_cleaned.csv"
try:
    df = load_data(DATA_PATH)
except FileNotFoundError:
    st.error(f"Could not find `{DATA_PATH}`.  Place it in the same folder as app.py.")
    st.stop()


with st.sidebar:
    st.markdown('<div class="sidebar-brand">📊 CampaignIQ</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-sub">Marketing Analytics Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    products = ["All"] + sorted(df["Product"].dropna().unique().tolist())
    closers  = ["All"] + sorted(df["Closer Name"].dropna().unique().tolist())
    statuses = ["All"] + sorted(df["Closing_status"].dropna().unique().tolist())

    sel_product = st.selectbox("🏷️  Product",       products)
    sel_closer  = st.selectbox("👤  Closer",         closers)
    sel_status  = st.selectbox("📋  Closing Status", statuses)

    date_min = df["Creation Date"].dropna().min().date()
    date_max = df["Creation Date"].dropna().max().date()
    sel_dates = st.date_input(
        "📅  Date Range",
        value=(date_min, date_max),
        min_value=date_min, max_value=date_max,
    )

    # ── Apply filters
    fdf = df.copy()
    if sel_product != "All":
        fdf = fdf[fdf["Product"] == sel_product]
    if sel_closer != "All":
        fdf = fdf[fdf["Closer Name"] == sel_closer]
    if sel_status != "All":
        fdf = fdf[fdf["Closing_status"] == sel_status]
    if len(sel_dates) == 2:
        d0, d1 = pd.Timestamp(sel_dates[0]), pd.Timestamp(sel_dates[1])
        fdf = fdf[(fdf["Creation Date"] >= d0) & (fdf["Creation Date"] <= d1)]

    st.markdown(
        f'<div class="filter-badge">🔍 {len(fdf):,} records matched</div>',
        unsafe_allow_html=True,
    )

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.caption("Built by Eng. Youssef Bassiony")


st.markdown("""
<div class="hero">
  <div class="hero-badge">Marketing Intelligence</div>
  <h1 class="hero-title">Campaign <span>Analytics</span> Dashboard</h1>
  <p class="hero-sub">End-to-End Analysis · Operations · Quality Assurance · Sales Tracking</p>
</div>
""", unsafe_allow_html=True)


tab1, tab2, tab3 = st.tabs([
    "Overview & KPIs",
    "Deep-Dive Analysis",
    "Time-Series Forecast",
])


with tab1:

    # KPIs calculated from FULL dataset (df) - not filtered (fdf)
    # This ensures overall campaign performance is always visible
    total_leads    = len(df)
    total_approved = int(df["Is Approved"].sum())
    approval_rate  = total_approved / max(total_leads, 1) * 100
    est_revenue    = df[df["Is Approved"] == 1]["Monthly Price"].sum()
    avg_qs         = df["Quality Score %"].mean()
    # Payment Completion Rate: % of approved sales that received payment
    paid_sales     = df[df["Is Approved"] == 1]["Date of Payment"].notna().sum()
    payment_rate   = (paid_sales / max(total_approved, 1)) * 100
    # Lead-to-Payment Rate: % of all leads that resulted in payment (complete funnel)
    lead_to_payment_rate = (df["Payment Received"].sum() / max(total_leads, 1)) * 100
    qa_coverage    = df["Has Qa"].mean() * 100

    avg_qs_str = f"{avg_qs:.1f}" if pd.notna(avg_qs) else "N/A"

    k1, k2, k3, k4, k5, k6, k7, k8 = st.columns(8)
    kpi_defs = [
        (k1, "", f"{total_leads:,}",      "Total Leads",        "kpi-cyan",
         "Total number of leads in the entire campaign dataset"),
        (k2, "", f"{total_approved:,}",   "Approved Sales",      "kpi-green",
         "Total number of approved sales (Is Approved = 1) in the entire campaign"),
        (k3, "", f"{approval_rate:.1f}%", "Approval Rate",       "kpi-amber",
         f"Overall conversion rate: (Approved Sales / Total Leads) × 100 = {approval_rate:.1f}%"),
        (k4, "", f"${est_revenue:,.0f}",  "Est. Revenue / Mo",   "kpi-purple",
         "Total monthly recurring revenue from all approved sales in the campaign"),
        (k5, "", avg_qs_str,              "Avg QA Score",        "kpi-teal",
         "Average quality score across all QA-reviewed records in the campaign"),
        (k6, "", f"{payment_rate:.1f}%", "Payment Rate",        "kpi-rose",
         f"Payment completion rate: (Paid Sales / Approved Sales) × 100 = {payment_rate:.1f}% - shows cash collection efficiency"),
        (k7, "", f"{lead_to_payment_rate:.1f}%", "Lead-to-Payment", "kpi-purple",
         f"Complete funnel rate: (Payment Received / Total Leads) × 100 = {lead_to_payment_rate:.1f}% - measures end-to-end conversion from lead to cash"),
        (k8, "", f"{qa_coverage:.0f}%",   "QA Coverage",         "kpi-cyan",
         f"Percentage of records that received QA review: (Has Qa = 1 / Total Leads) × 100 = {qa_coverage:.0f}%"),
    ]
    for col, icon, val, label, cls, tooltip in kpi_defs:
        with col:
            st.markdown(f"""
            <div class="kpi-wrap {cls}">
              <div class="kpi-tooltip">{tooltip}</div>
              <div class="kpi-label">{label} ℹ</div>
              <div class="kpi-icon">{icon}</div>
              <div class="kpi-val">{val}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    col_a, col_b = st.columns(2, gap="medium")

    with col_a:
        st.markdown('<p class="sec-hdr">Lead Disposition</p>', unsafe_allow_html=True)
        status_counts = fdf["Closing_status"].value_counts().dropna()
        fig = px.bar(
            x=status_counts.values, y=status_counts.index,
            orientation="h", text=status_counts.values,
            color=status_counts.index,
            color_discrete_map=STATUS_COLORS,
        )
        fig.update_traces(textposition="outside",
                          textfont=dict(color="#e2e8f0", size=10),
                          marker_line_width=0)
        apply_theme(fig, height=360)
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        st.markdown('<p class="sec-hdr">Product Mix by Status</p>', unsafe_allow_html=True)
        prod_cross = (
            fdf.dropna(subset=["Product"])
            .groupby(["Product", "Closing_status"]).size()
            .reset_index(name="count")
        )
        fig2 = px.bar(
            prod_cross, x="Product", y="count",
            color="Closing_status", barmode="stack",
            color_discrete_map=STATUS_COLORS,
            labels={"count": "Count", "Product": "", "Closing_status": "Status"},
        )
        fig2.update_traces(marker_line_width=0)
        apply_theme(fig2, height=360)
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    col_c, col_d = st.columns(2, gap="medium")

    with col_c:
        st.markdown('<p class="sec-hdr">Top 10 Closers — Approved Sales</p>',
                    unsafe_allow_html=True)
        closer_agg = (
            fdf[fdf["Closer Name"].notna()]
            .groupby("Closer Name")
            .agg(approved=("Is Approved", "sum"), total=("Is Approved", "count"))
            .sort_values("approved", ascending=True).tail(10)
        )
        fig3 = px.bar(
            closer_agg.reset_index(),
            x="approved", y="Closer Name", orientation="h",
            text="approved",
            color="approved", color_continuous_scale=[[0,"#0c4a6e"],[1,"#06b6d4"]],
            labels={"approved": "Approved Sales", "Closer Name": ""},
        )
        fig3.update_traces(textposition="outside",
                           textfont=dict(color="#e2e8f0", size=10),
                           marker_line_width=0)
        fig3.update_layout(coloraxis_showscale=False)
        apply_theme(fig3, height=380)
        st.plotly_chart(fig3, use_container_width=True)

    with col_d:
        st.markdown('<p class="sec-hdr">Top 10 Openers — Conversion Rate</p>',
                    unsafe_allow_html=True)
        opener_agg = (
            fdf[fdf["Opener Name"].notna()]
            .groupby("Opener Name")
            .agg(approved=("Is Approved", "sum"), total=("Is Approved", "count"))
            .assign(rate=lambda x: x.approved / x.total * 100)
            .query("total >= 8")
            .sort_values("rate", ascending=True).tail(10)
        )
        fig4 = px.bar(
            opener_agg.reset_index(),
            x="rate", y="Opener Name", orientation="h",
            text=opener_agg["rate"].round(1).astype(str) + "%",
            color="rate", color_continuous_scale=[[0,"#064e3b"],[1,"#10b981"]],
            labels={"rate": "Conversion Rate (%)", "Opener Name": ""},
        )
        fig4.update_traces(textposition="outside",
                           textfont=dict(color="#e2e8f0", size=10),
                           marker_line_width=0)
        fig4.update_layout(coloraxis_showscale=False)
        apply_theme(fig4, height=380)
        st.plotly_chart(fig4, use_container_width=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    col_e, col_f, col_g = st.columns(3, gap="medium")

    with col_e:
        st.markdown('<p class="sec-hdr">Product Mix (Volume)</p>', unsafe_allow_html=True)
        prod_cnt = fdf["Product"].value_counts().dropna()
        fig_pm = go.Figure(go.Pie(
            labels=prod_cnt.index, values=prod_cnt.values,
            hole=.55,
            marker=dict(colors=["#06b6d4","#8b5cf6"],
                        line=dict(color="#080d14", width=3)),
            textfont=dict(color="#e2e8f0"),
        ))
        fig_pm.update_layout(
            showlegend=True,
            legend=dict(orientation="h", y=-.12, font=dict(color="#94a3b8")),
            annotations=[dict(text="Mix", x=.5, y=.5,
                              font=dict(size=14, color="#e2e8f0",
                                        family="Syne"), showarrow=False)],
        )
        apply_theme(fig_pm, height=280)
        st.plotly_chart(fig_pm, use_container_width=True)

    with col_f:
        st.markdown('<p class="sec-hdr">Revenue by Product</p>', unsafe_allow_html=True)
        rev_prod = (
            fdf[fdf["Is Approved"] == 1]
            .groupby("Product")["Monthly Price"].sum()
            .dropna().reset_index()
        )
        fig_rv = px.bar(
            rev_prod, x="Product", y="Monthly Price",
            text=rev_prod["Monthly Price"].apply(lambda v: f"${v:,.0f}"),
            color="Product",
            color_discrete_map={"Necklace": "#06b6d4", "Smart Watch": "#8b5cf6"},
            labels={"Monthly Price": "Revenue ($)", "Product": ""},
        )
        fig_rv.update_traces(textposition="outside",
                             textfont=dict(color="#e2e8f0", size=11),
                             marker_line_width=0)
        fig_rv.update_layout(showlegend=False)
        apply_theme(fig_rv, height=280)
        st.plotly_chart(fig_rv, use_container_width=True)

    with col_g:
        st.markdown('<p class="sec-hdr">Price Tier Split</p>', unsafe_allow_html=True)
        price_cnt = fdf["Monthly Price"].value_counts().sort_index().dropna()
        fig_pt = px.bar(
            x=[f"${p:.2f}" for p in price_cnt.index],
            y=price_cnt.values,
            text=price_cnt.values,
            color=price_cnt.values,
            color_continuous_scale=[[0,"#312e81"],[1,"#06b6d4"]],
            labels={"x": "Monthly Price", "y": "Count"},
        )
        fig_pt.update_traces(textposition="outside",
                             textfont=dict(color="#e2e8f0", size=11),
                             marker_line_width=0)
        fig_pt.update_layout(showlegend=False, coloraxis_showscale=False)
        apply_theme(fig_pt, height=280)
        st.plotly_chart(fig_pt, use_container_width=True)


with tab2:

    col_a, col_b = st.columns(2, gap="medium")

    with col_a:
        st.markdown('<p class="sec-hdr">Quality Score Distribution</p>',
                    unsafe_allow_html=True)
        qa_data = fdf["Quality Score %"].dropna()
        if len(qa_data) > 0:
            fig_qa = px.histogram(
                qa_data, nbins=15,
                color_discrete_sequence=["#2dd4bf"],
                labels={"value": "Quality Score (%)", "count": "Count"},
            )
            fig_qa.add_vline(
                x=qa_data.mean(), line_dash="dash", line_color="#f43f5e",
                annotation_text=f"Mean: {qa_data.mean():.1f}",
                annotation_font=dict(color="#f43f5e"),
            )
            fig_qa.add_vline(
                x=qa_data.median(), line_dash="dot", line_color="#f59e0b",
                annotation_text=f"Median: {qa_data.median():.1f}",
                annotation_font=dict(color="#f59e0b"),
            )
            fig_qa.update_traces(marker_line_width=0, opacity=.85)
            fig_qa.update_layout(showlegend=False)
            apply_theme(fig_qa, height=320)
            st.plotly_chart(fig_qa, use_container_width=True)
        else:
            st.info("No QA data available for current selection.")

    with col_b:
        st.markdown('<p class="sec-hdr">Approval Rate by Gender</p>',
                    unsafe_allow_html=True)
        gender_agg = (
            fdf.dropna(subset=["Gender"])
            .groupby("Gender")["Is Approved"]
            .agg(["mean", "count"]).reset_index()
            .rename(columns={"mean": "rate", "count": "leads"})
            .assign(rate_pct=lambda x: (x["rate"] * 100).round(1))
        )
        fig_g = px.bar(
            gender_agg, x="Gender", y="rate_pct",
            text=gender_agg["rate_pct"].astype(str) + "%",
            color="Gender",
            color_discrete_map={"Female": "#e879f9", "Male": "#38bdf8"},
            labels={"rate_pct": "Approval Rate (%)", "Gender": ""},
            range_y=[0, 100],
        )
        fig_g.update_traces(textposition="outside",
                            textfont=dict(color="#e2e8f0"),
                            marker_line_width=0, width=0.45)
        fig_g.update_layout(showlegend=False)
        apply_theme(fig_g, height=320)
        st.plotly_chart(fig_g, use_container_width=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    col_c, col_d = st.columns(2, gap="medium")

    with col_c:
        st.markdown('<p class="sec-hdr">Days from Creation to Payment</p>',
                    unsafe_allow_html=True)
        ttp = fdf["Days To Payment"].dropna()
        if len(ttp) > 0:
            ttp_clip = ttp[ttp <= ttp.quantile(0.99)]
            fig_ttp = px.histogram(
                ttp_clip, nbins=20,
                color_discrete_sequence=["#fb923c"],
                labels={"value": "Days", "count": "Count"},
            )
            fig_ttp.add_vline(
                x=ttp_clip.median(), line_dash="dash", line_color="#f43f5e",
                annotation_text=f"Median: {ttp_clip.median():.0f}d",
                annotation_font=dict(color="#f43f5e"),
            )
            fig_ttp.update_traces(marker_line_width=0, opacity=.85)
            fig_ttp.update_layout(showlegend=False)
            apply_theme(fig_ttp, height=320)
            st.plotly_chart(fig_ttp, use_container_width=True)
        else:
            st.info("No payment data available.")

    with col_d:
        st.markdown('<p class="sec-hdr">Top 12 States by Lead Volume</p>',
                    unsafe_allow_html=True)
        state_cnt = fdf["State"].value_counts().head(12).reset_index()
        state_cnt.columns = ["State", "Count"]
        fig_st = px.bar(
            state_cnt, x="State", y="Count", text="Count",
            color="Count",
            color_continuous_scale=[[0,"#1e1b4b"],[1,"#8b5cf6"]],
            labels={"Count": "Lead Count", "State": ""},
        )
        fig_st.update_traces(textposition="outside",
                             textfont=dict(color="#e2e8f0", size=10),
                             marker_line_width=0)
        fig_st.update_layout(coloraxis_showscale=False)
        apply_theme(fig_st, height=320)
        st.plotly_chart(fig_st, use_container_width=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    col_e, col_f = st.columns(2, gap="medium")

    with col_e:
        st.markdown('<p class="sec-hdr">Avg QA Score by Agent</p>',
                    unsafe_allow_html=True)
        qa_df = fdf[fdf["Quality Score %"].notna()]
        if len(qa_df) > 0:
            qa_agent = (
                qa_df.groupby("Quality Agent Name")["Quality Score %"]
                .agg(["mean", "count"]).query("count >= 3")
                .sort_values("mean", ascending=True)
            )
            fig_qa_ag = px.bar(
                qa_agent.reset_index(),
                x="mean", y="Quality Agent Name", orientation="h",
                text=qa_agent["mean"].round(1).values,
                color="mean",
                color_continuous_scale=[[0,"#064e3b"],[.5,"#10b981"],[1,"#6ee7b7"]],
                labels={"mean": "Avg Score", "Quality Agent Name": ""},
            )
            fig_qa_ag.update_traces(textposition="outside",
                                    textfont=dict(color="#e2e8f0", size=10),
                                    marker_line_width=0)
            fig_qa_ag.update_layout(coloraxis_showscale=False)
            apply_theme(fig_qa_ag, height=340)
            st.plotly_chart(fig_qa_ag, use_container_width=True)
        else:
            st.info("No QA agent data available.")

    with col_f:
        st.markdown('<p class="sec-hdr">Top States — Conversion Rate</p>',
                    unsafe_allow_html=True)
        state_conv = (
            fdf.groupby("State")
            .agg(total=("Is Approved", "count"), approved=("Is Approved", "sum"))
            .assign(rate=lambda x: x.approved / x.total * 100)
            .query("total >= 5")
            .sort_values("rate", ascending=False).head(12)
            .reset_index()
        )
        fig_stc = px.bar(
            state_conv, x="State", y="rate",
            text=state_conv["rate"].round(1).astype(str) + "%",
            color="rate",
            color_continuous_scale=[[0,"#1e3a5f"],[1,"#06b6d4"]],
            labels={"rate": "Conversion Rate (%)", "State": ""},
        )
        fig_stc.update_traces(textposition="outside",
                              textfont=dict(color="#e2e8f0", size=9),
                              marker_line_width=0)
        fig_stc.update_layout(coloraxis_showscale=False)
        apply_theme(fig_stc, height=340)
        st.plotly_chart(fig_stc, use_container_width=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    col_g, col_h = st.columns(2, gap="medium")

    with col_g:
        st.markdown('<p class="sec-hdr">QA Coverage</p>', unsafe_allow_html=True)
        qa_cov = fdf["Has Qa"].value_counts().reindex([1, 0], fill_value=0)
        fig_qac = go.Figure(go.Pie(
            labels=["QA Reviewed", "Not Reviewed"],
            values=qa_cov.values, hole=.55,
            marker=dict(colors=["#10b981", "#f43f5e"],
                        line=dict(color="#080d14", width=3)),
            textfont=dict(color="#e2e8f0"),
        ))
        fig_qac.update_layout(
            showlegend=True,
            legend=dict(orientation="h", y=-.1, font=dict(color="#94a3b8")),
            annotations=[dict(text="QA", x=.5, y=.5,
                              font=dict(size=14, color="#e2e8f0",
                                        family="Syne"), showarrow=False)],
        )
        apply_theme(fig_qac, height=300)
        st.plotly_chart(fig_qac, use_container_width=True)

    with col_h:
        st.markdown('<p class="sec-hdr">Quality Score vs Sale Outcome</p>',
                    unsafe_allow_html=True)
        qa_sale = fdf[fdf["Quality Score %"].notna()].copy()
        qa_sale["outcome"] = qa_sale["Is Approved"].map({1: "Approved", 0: "Not Approved"})
        if len(qa_sale) > 0:
            fig_box = px.box(
                qa_sale, x="outcome", y="Quality Score %",
                color="outcome",
                color_discrete_map={"Approved": "#10b981", "Not Approved": "#f43f5e"},
                labels={"Quality Score %": "Quality Score (%)", "outcome": ""},
            )
            fig_box.update_traces(marker_line_width=0)
            fig_box.update_layout(showlegend=False)
            apply_theme(fig_box, height=300)
            st.plotly_chart(fig_box, use_container_width=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    st.markdown('<p class="sec-hdr">Team Leader Performance Summary</p>',
                unsafe_allow_html=True)
    tl_agg = (
        fdf[fdf["Team Leader"].notna()]
        .groupby("Team Leader")
        .agg(Leads=("Is Approved", "count"), Approved=("Is Approved", "sum"))
        .assign(**{"Approval Rate %": lambda x: (x["Approved"] / x["Leads"] * 100).round(1)})
        .sort_values("Approved", ascending=False)
    )
    st.dataframe(
        tl_agg.style
              .background_gradient(subset=["Approval Rate %"], cmap="RdYlGn")
              .format({"Approval Rate %": "{:.1f}%"}),
        use_container_width=True, height=360,
    )

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    col_i, col_j = st.columns(2, gap="medium")

    with col_i:
        st.markdown('<p class="sec-hdr">Top 15 Cities by Lead Volume</p>',
                    unsafe_allow_html=True)
        city_cnt = fdf["City"].value_counts().head(15).reset_index()
        city_cnt.columns = ["City", "Count"]
        fig_city = px.bar(
            city_cnt, x="Count", y="City", orientation="h", text="Count",
            color="Count",
            color_continuous_scale=[[0,"#0c4a6e"],[1,"#38bdf8"]],
            labels={"Count": "Leads", "City": ""},
        )
        fig_city.update_traces(textposition="outside",
                               textfont=dict(color="#e2e8f0", size=9),
                               marker_line_width=0)
        fig_city.update_layout(coloraxis_showscale=False)
        apply_theme(fig_city, height=420)
        st.plotly_chart(fig_city, use_container_width=True)

    with col_j:
        st.markdown('<p class="sec-hdr">Gender Distribution</p>', unsafe_allow_html=True)
        gen_cnt = fdf["Gender"].value_counts().dropna()
        fig_gen = go.Figure(go.Pie(
            labels=gen_cnt.index, values=gen_cnt.values,
            hole=.55,
            marker=dict(colors=["#e879f9","#38bdf8"],
                        line=dict(color="#080d14", width=3)),
            textfont=dict(color="#e2e8f0"),
        ))
        fig_gen.update_layout(
            showlegend=True,
            legend=dict(orientation="h", y=-.1, font=dict(color="#94a3b8")),
            annotations=[dict(text="Gender", x=.5, y=.5,
                              font=dict(size=12, color="#e2e8f0",
                                        family="Syne"), showarrow=False)],
        )
        apply_theme(fig_gen, height=420)
        st.plotly_chart(fig_gen, use_container_width=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    with st.expander("Raw Data Explorer", expanded=False):
        st.caption(f"Showing {min(200, len(fdf)):,} of {len(fdf):,} filtered rows")
        st.dataframe(fdf.head(200), use_container_width=True, height=380)

    with st.expander("Statistical Summary", expanded=False):
        st.dataframe(fdf.describe().round(2), use_container_width=True)

    with st.expander("Missing Values Report", expanded=False):
        mv = fdf.isnull().sum().to_frame("Count")
        mv["Pct"] = (mv["Count"] / len(fdf) * 100).round(1)
        st.dataframe(mv[mv["Count"] > 0].sort_values("Count", ascending=False),
                     use_container_width=True)


with tab3:

    daily_raw = (
        fdf.dropna(subset=["sale Day"])
        .groupby("sale Day")
        .agg(leads=("Is Approved", "count"), approved=("Is Approved", "sum"))
        .reset_index().rename(columns={"sale Day": "ds"})
        .sort_values("ds")
    )
    if len(daily_raw) > 1:
        full_range = pd.date_range(daily_raw["ds"].min(), daily_raw["ds"].max(), freq="D")
        daily = (
            daily_raw.set_index("ds")
            .reindex(full_range, fill_value=0)
            .reset_index().rename(columns={"index": "ds"})
        )
    else:
        daily = daily_raw.copy()

    daily["rolling7"]  = daily["leads"].rolling(7, min_periods=1).mean()
    daily["rolling7a"] = daily["approved"].rolling(7, min_periods=1).mean()

    st.markdown('<p class="sec-hdr">Daily Campaign Activity</p>', unsafe_allow_html=True)

    from plotly.subplots import make_subplots
    fig_ts = make_subplots(rows=2, cols=1, shared_xaxes=True,
                           vertical_spacing=.08,
                           subplot_titles=("Total Leads", "Approved Sales"))

    fig_ts.add_trace(go.Bar(x=daily["ds"], y=daily["leads"],
                            name="Leads", marker_color="#38bdf8",
                            opacity=.35, marker_line_width=0), row=1, col=1)
    fig_ts.add_trace(go.Scatter(x=daily["ds"], y=daily["rolling7"],
                                name="7-day avg (leads)",
                                line=dict(color="#06b6d4", width=2.5)), row=1, col=1)

    fig_ts.add_trace(go.Bar(x=daily["ds"], y=daily["approved"],
                            name="Approved", marker_color="#4ade80",
                            opacity=.35, marker_line_width=0), row=2, col=1)
    fig_ts.add_trace(go.Scatter(x=daily["ds"], y=daily["rolling7a"],
                                name="7-day avg (approved)",
                                line=dict(color="#10b981", width=2.5)), row=2, col=1)

    fig_ts.update_layout(
        **{k: v for k, v in LAYOUT_BASE.items() if k not in ("xaxis","yaxis","legend","margin")},
        height=480,
        legend=dict(orientation="h", y=1.06, bgcolor="rgba(0,0,0,0)",
                    font=dict(color="#94a3b8")),
        margin=dict(l=0, r=0, t=40, b=0),
    )
    for ax in ["xaxis", "xaxis2", "yaxis", "yaxis2"]:
        fig_ts.update_layout(**{ax: dict(
            gridcolor="rgba(255,255,255,.05)",
            zerolinecolor="rgba(255,255,255,.08)",
            color="#94a3b8",
        )})
    fig_ts.update_annotations(font=dict(color="#94a3b8", size=11))
    st.plotly_chart(fig_ts, use_container_width=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    fc_col1, fc_col2 = st.columns([3, 1], gap="medium")

    with fc_col2:
        st.markdown('<p class="sec-hdr">Forecast Settings</p>', unsafe_allow_html=True)
        forecast_days = st.slider("Days to forecast", 7, 30, 14)
        run_btn = st.button("Run Prophet Forecast", type="primary",
                            use_container_width=True)

    with fc_col1:
        st.markdown('<p class="sec-hdr">14-Day Lead Volume Forecast</p>',
                    unsafe_allow_html=True)

        if run_btn:
            try:
                from prophet import Prophet
                with st.spinner("Training Prophet model…"):
                    pdf = daily[["ds", "leads"]].rename(columns={"leads": "y"})
                    m=Prophet(
                            yearly_seasonality=False,
                            weekly_seasonality=True,
                            daily_seasonality=False,
                            changepoint_prior_scale=0.05,
                            seasonality_prior_scale=10,
                            seasonality_mode='multiplicative',
                            interval_width=0.80
                    )
                    m.fit(pdf)
                    future   = m.make_future_dataframe(periods=forecast_days, freq="D")
                    forecast = m.predict(future)

                split = daily["ds"].max()

                fig_fc = go.Figure()
                fig_fc.add_trace(go.Bar(
                    x=daily["ds"], y=daily["leads"],
                    name="Actual", marker_color="#38bdf8",
                    opacity=.35, marker_line_width=0))
                fig_fc.add_trace(go.Scatter(
                    x=forecast["ds"], y=forecast["yhat"],
                    name="Forecast", line=dict(color="#f43f5e", width=2.5)))
                fig_fc.add_trace(go.Scatter(
                    x=pd.concat([forecast["ds"], forecast["ds"][::-1]]),
                    y=pd.concat([forecast["yhat_upper"], forecast["yhat_lower"][::-1]]),
                    fill="toself", fillcolor="rgba(244,63,94,.12)",
                    line=dict(color="rgba(0,0,0,0)"), name="80% CI"))
                fig_fc.add_vline(
                    x=str(split), line_dash="dash", line_color="#94a3b8",
                    annotation_text="  ← Forecast start",
                    annotation_font=dict(color="#94a3b8"),
                )
                fig_fc.update_layout(
                    legend=dict(orientation="h", y=1.08,
                                bgcolor="rgba(0,0,0,0)",
                                font=dict(color="#94a3b8")),
                )
                apply_theme(fig_fc, height=420)
                st.plotly_chart(fig_fc, use_container_width=True)

                # Forecast table
                next_n = (
                    forecast[forecast["ds"] > split]
                    [["ds", "yhat", "yhat_lower", "yhat_upper"]].copy()
                )
                next_n.columns = ["Date", "Expected Leads", "Lower (80%)", "Upper (80%)"]
                next_n = next_n.set_index("Date").round(1)
                st.dataframe(next_n, use_container_width=True)

                # Component plot
                st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
                st.markdown('<p class="sec-hdr">Forecast Components</p>',
                            unsafe_allow_html=True)
                import matplotlib
                matplotlib.use("Agg")
                import matplotlib.pyplot as plt
                plt.style.use("dark_background")
                fig_comp = m.plot_components(forecast)
                fig_comp.patch.set_facecolor("#0f1923")
                for ax in fig_comp.get_axes():
                    ax.set_facecolor("#0f1923")
                    ax.tick_params(colors="#94a3b8")
                    ax.title.set_color("#e2e8f0")
                st.pyplot(fig_comp, use_container_width=True)

            except ImportError:
                st.warning("Prophet not installed. Run: `pip install prophet`")
                # Linear fallback
                x   = np.arange(len(daily))
                yv  = daily["leads"].values
                coef = np.polyfit(x, yv, 1)
                xf  = np.arange(len(daily), len(daily) + forecast_days)
                yf  = np.maximum(np.polyval(coef, xf), 0)
                fdates = pd.date_range(
                    daily["ds"].max() + pd.Timedelta(days=1), periods=forecast_days)

                fig_lin = go.Figure()
                fig_lin.add_trace(go.Bar(
                    x=daily["ds"], y=daily["leads"],
                    name="Actual", marker_color="#38bdf8",
                    opacity=.35, marker_line_width=0))
                fig_lin.add_trace(go.Scatter(
                    x=fdates, y=yf, mode="lines+markers",
                    name="Linear trend",
                    line=dict(color="#f59e0b", dash="dash", width=2)))
                apply_theme(fig_lin, height=380)
                st.plotly_chart(fig_lin, use_container_width=True)
        else:
            st.info("Adjust settings and click **Run Prophet Forecast** to generate the model.")

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    st.markdown('<p class="sec-hdr">Top 3 Business Takeaways</p>',
                unsafe_allow_html=True)
    ta1, ta2, ta3 = st.columns(3, gap="medium")

    with ta1:
        st.markdown("""
        <div class="insight insight-blue">
          <p class="insight-title">Closer Concentration Risk</p>
          <p class="insight-body">
            The top 3 closers handle the vast majority of all approved sales volume.
            This creates a key-person dependency — if any leave or underperform, campaign
            revenue drops sharply. Invest in training mid-tier closers now.
          </p>
        </div>""", unsafe_allow_html=True)

    with ta2:
        st.markdown("""
        <div class="insight insight-amber">
          <p class="insight-title">Low QA Coverage</p>
          <p class="insight-body">
            Only a fraction of records received a quality review. At this rate, QA scores
            reflect spot-checks rather than campaign-wide quality. Expand to a random
            30-40% sample minimum to surface issues at scale.
          </p>
        </div>""", unsafe_allow_html=True)

    with ta3:
        st.markdown("""
        <div class="insight insight-green">
          <p class="insight-title">Payment Tail Risk</p>
          <p class="insight-body">
            While many approved sales settle same-day, a meaningful long tail stretches
            30–60+ days post-creation. Prioritise follow-up on accounts past 14 days
            to accelerate cash collection and reduce churn risk.
          </p>
        </div>""", unsafe_allow_html=True)


st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.markdown("""
<div class="footer">
  Marketing Campaign Dashboard &nbsp;·&nbsp; End-to-End Analysis<br>
  <span style="margin-top:.3rem;display:block;">
    Built by
    <a href="https://github.com/youssef-113" target="_blank">Eng. Youssef Bassiony</a>
  </span>
</div>
""", unsafe_allow_html=True)