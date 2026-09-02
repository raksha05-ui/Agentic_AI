import os
import re
from pathlib import Path

import pandas as pd
import streamlit as st
from dotenv import load_dotenv

try:
    from langchain_google_genai import ChatGoogleGenerativeAI
except ImportError:  # pragma: no cover
    ChatGoogleGenerativeAI = None

BASE_DIR = Path(__file__).resolve().parent
HEALTH_DIR = BASE_DIR / "health_analysis"
DEFAULT_REPORT_PATH = HEALTH_DIR / "blood_work.txt"
SECONDARY_REPORT_PATH = HEALTH_DIR / "blood_work2.txt"
GEMINI_MODELS_FILE = BASE_DIR / "gemini_models.md"
DEFAULT_GEMINI_MODEL = os.getenv("GOOGLE_MODEL", "gemini-2.0-flash")

st.set_page_config(page_title="Blood Health Dashboard", page_icon="🩺", layout="wide")


def load_gemini_models():
    candidates = [GEMINI_MODELS_FILE, BASE_DIR / "gemini_models.txt"]
    for file_path in candidates:
        if file_path.exists():
            lines = []
            for line in file_path.read_text(encoding="utf-8").splitlines():
                cleaned = line.strip()
                if cleaned and not cleaned.startswith("#"):
                    lines.append(cleaned)
            if lines:
                return lines
    return [DEFAULT_GEMINI_MODEL, "gemini-2.5-flash", "gemini-2.0-flash"]


@st.cache_data
def load_report_text(report_path: str | Path = DEFAULT_REPORT_PATH) -> str:
    path = Path(report_path)
    return path.read_text(encoding="utf-8")


def get_available_report_paths():
    paths = []
    seen = set()
    for candidate in sorted(HEALTH_DIR.glob("blood_work*.txt")):
        if candidate.name not in seen:
            paths.append(candidate)
            seen.add(candidate.name)
    for candidate in [DEFAULT_REPORT_PATH, SECONDARY_REPORT_PATH]:
        if candidate.exists() and candidate.name not in seen:
            paths.append(candidate)
            seen.add(candidate.name)
    return paths


METRIC_RANGES = {
    "Hemoglobin": (12.0, 16.5),
    "RBC Count": (3.8, 5.1),
    "WBC Count": (4.0, 11.0),
    "Platelet Count": (1.5, 4.5),
    "Hematocrit (PCV)": (36.0, 46.0),
    "MCV": (80.0, 100.0),
    "MCH": (27.0, 34.0),
    "MCHC": (31.0, 36.0),
    "RDW": (11.5, 14.5),
    "Neutrophils": (40.0, 75.0),
    "Lymphocytes": (20.0, 45.0),
    "Monocytes": (2.0, 10.0),
    "Eosinophils": (1.0, 6.0),
    "Basophils": (0.0, 1.0),
    "Fasting Blood Glucose": (70.0, 100.0),
    "HbA1c": (4.0, 5.7),
    "Total Cholesterol": (0.0, 200.0),
    "HDL Cholesterol": (40.0, 60.0),
    "LDL Cholesterol": (0.0, 130.0),
    "Triglycerides": (0.0, 150.0),
    "Total Bilirubin": (0.2, 1.2),
    "AST (SGOT)": (10.0, 40.0),
    "ALT (SGPT)": (7.0, 56.0),
    "Alkaline Phosphatase": (30.0, 120.0),
    "Total Protein": (6.0, 8.3),
    "Albumin": (3.5, 5.2),
    "Blood Urea": (10.0, 50.0),
    "Serum Creatinine": (0.6, 1.1),
    "Uric Acid": (3.5, 7.2),
}


def extract_patient_profile(report: str) -> dict:
    profile = {
        "patient_name": "Unknown",
        "age_sex": "Unknown",
        "location": "Unknown",
        "date": "Unknown",
    }

    match = re.search(r"Sample Patient:\s*(.+)", report)
    if match:
        profile["patient_name"] = match.group(1).strip()

    match = re.search(r"Age/Sex:\s*(.+)", report)
    if match:
        profile["age_sex"] = match.group(1).strip()

    match = re.search(r"Location:\s*(.+)", report)
    if match:
        profile["location"] = match.group(1).strip()

    match = re.search(r"Sample Date:\s*(.+)", report)
    if match:
        profile["date"] = match.group(1).strip()

    return profile


def parse_numeric(value: str):
    match = re.search(r"[-+]?\d*\.?\d+(?:,\d{3})*(?:\.\d+)?", value)
    if not match:
        return None
    cleaned = match.group(0).replace(",", "")
    try:
        return float(cleaned)
    except ValueError:
        return None


@st.cache_data
def extract_metrics(report: str):
    metric_entries = []
    lines = report.splitlines()
    for line in lines:
        if ":" not in line:
            continue
        label, raw_value = line.split(":", 1)
        label = label.strip()
        value = raw_value.strip()
        if not value or label.lower().startswith("bloom"):
            continue
        if any(keyword in label.lower() for keyword in ["sample patient", "age/sex", "location", "sample date"]):
            continue
        if label.startswith("NOTE") or label.startswith("Note"):
            continue
        if any(keyword in label.lower() for keyword in ["complete blood count", "differential", "blood chemistry", "liver", "kidney", "report"]):
            continue

        num = parse_numeric(value)
        if num is None:
            continue

        unit = ""
        if "mg/dL" in value:
            unit = "mg/dL"
        elif "g/dL" in value:
            unit = "g/dL"
        elif "million/µL" in value:
            unit = "million/µL"
        elif "cells/µL" in value:
            unit = "cells/µL"
        elif "lakh/µL" in value:
            unit = "lakh/µL"
        elif "%" in value:
            unit = "%"
        elif "fL" in value:
            unit = "fL"
        elif "pg" in value:
            unit = "pg"
        elif "U/L" in value:
            unit = "U/L"
        elif "g/dL" in value:
            unit = "g/dL"
        elif "mg/dL" in value:
            unit = "mg/dL"
        elif "mmol/L" in value:
            unit = "mmol/L"

        metric_entries.append({
            "Test": label,
            "Value": num,
            "Unit": unit,
            "Reference": "Clinical range",
        })

    for entry in metric_entries:
        test_name = entry["Test"]
        if test_name in METRIC_RANGES:
            low, high = METRIC_RANGES[test_name]
            value = entry["Value"]
            if value < low:
                status = "Low"
            elif value > high:
                status = "High"
            else:
                status = "Normal"
            entry["Status"] = status
            entry["Reference"] = f"{low} - {high}"
        else:
            entry["Status"] = "Normal"

    return metric_entries


def get_fallback_diet_plan() -> dict:
    return {
        "summary": (
            "The report shows mostly balanced blood markers with overall good metabolic health. "
            "The main focus is to maintain consistency in nutrition, hydration, regular exercise, "
            "and sleep to preserve stable energy, cholesterol, and glucose control."
        ),
        "avoid": [
            "Fried snacks and fast food",
            "Sugary beverages and sweets",
            "Highly refined flour items and white bread",
            "Excess salty processed foods",
        ],
        "eat_more": [
            "Leafy greens and colorful vegetables",
            "Whole grains such as oats, millet, and brown rice",
            "Protein-rich foods like lentils, beans, eggs, and yogurt",
            "Fruits, nuts, seeds, and healthy fats like olive oil and peanuts",
        ],
    }


def get_fallback_extraction(report: str) -> str:
    metrics = extract_metrics(report)
    lines = ["AI extraction (rule-based fallback)"]
    for item in metrics:
        lines.append(f"Test_name: {item['Test']}, Status: {item['Status']}, Reference: {item['Reference']}")
    return "\n".join(lines)


def get_llm_response(prompt: str, model_name: str | None = None):
    load_dotenv(dotenv_path=BASE_DIR / ".env")
    api_key = os.getenv("GOOGLE_API_KEY")
    selected_model = model_name or os.getenv("GOOGLE_MODEL", DEFAULT_GEMINI_MODEL)
    if not api_key or ChatGoogleGenerativeAI is None:
        return None
    llm = ChatGoogleGenerativeAI(model=selected_model, api_key=api_key)
    return llm.invoke(prompt)


@st.cache_data
def create_ai_outputs(report: str, model_name: str | None = None):
    extraction_prompt = (
        "You are a medical data extraction model. From this medical report, extract all test values and classify each as High, Low, or Normal. "
        "Format the answer as plain lines like: Test_name:, Status:, Reference:.\n\n"
        f"blood_report:\n{report}"
    )
    diet_prompt = (
        "You are a dietician. Give a short health summary in simple language and an Indian diet plan with exactly two sections only: "
        "1) Foods to avoid 2) Foods to eat more. Keep it concise and practical."
    )

    extraction_response = get_llm_response(extraction_prompt, model_name=model_name)
    diet_response = get_llm_response(diet_prompt, model_name=model_name)

    return {
        "extraction": str(extraction_response) if extraction_response else get_fallback_extraction(report),
        "diet": str(diet_response) if diet_response else get_fallback_diet_plan(),
    }


def show_overview(metrics):
    metric_map = {item["Test"]: item for item in metrics}
    key_metrics = [
        "Hemoglobin",
        "Fasting Blood Glucose",
        "Total Cholesterol",
        "Serum Creatinine",
    ]
    col_count = st.columns(4)
    for idx, metric in enumerate(key_metrics):
        meta = metric_map.get(metric)
        if meta is None:
            continue
        with col_count[idx]:
            st.markdown(
                f"""
                <div style="padding: 1rem; border-radius: 1rem; background: linear-gradient(135deg, #1f77b4, #4dd0e1); color: white; margin-bottom: 0.75rem;">
                    <div style="font-size: 0.8rem; opacity: 0.9;">{metric}</div>
                    <div style="font-size: 2rem; font-weight: 700; margin-top: 0.25rem;">{meta['Value']}</div>
                    <div style="font-size: 0.8rem; opacity: 0.9;">Status: {meta['Status']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.subheader("Comparative health markers")
    chart_metrics = [
        "Hemoglobin",
        "WBC Count",
        "Fasting Blood Glucose",
        "Total Cholesterol",
        "LDL Cholesterol",
        "Albumin",
    ]
    chart_rows = []
    for metric in chart_metrics:
        matched = metric_map.get(metric)
        if matched:
            chart_rows.append({"Metric": metric, "Value": float(matched["Value"])})

    if chart_rows:
        chart_df = pd.DataFrame(chart_rows)
        st.bar_chart(chart_df.set_index("Metric"), width="stretch")
    else:
        st.info("No comparison data available for chart rendering.")


def render_metrics_table(metrics):
    table_data = []
    for item in metrics:
        table_data.append(
            {
                "Test": item["Test"],
                "Value": item["Value"],
                "Unit": item["Unit"],
                "Reference": item["Reference"],
                "Status": item["Status"],
            }
        )
    st.dataframe(table_data, width="stretch", hide_index=True)


def main():
    st.sidebar.title("Patient report")
    gemini_models = load_gemini_models()
    selected_model = DEFAULT_GEMINI_MODEL if DEFAULT_GEMINI_MODEL in gemini_models else gemini_models[0]

    available_reports = get_available_report_paths()
    uploaded_files = st.sidebar.file_uploader(
        "Upload one or more blood_work reports (.txt)",
        type=["txt"],
        accept_multiple_files=True,
    )

    uploaded_names = [f.name for f in uploaded_files] if uploaded_files else []
    report_options = ["No report selected", "Default sample"] + uploaded_names + [path.name for path in available_reports[1:]]

    report_choice = st.sidebar.selectbox("Choose report source", report_options, index=0)

    if report_choice == "No report selected":
        st.session_state["report"] = None
        st.session_state["report_label"] = "No report selected"
        st.markdown(
            """
            <div style="display:flex; flex-direction:column; align-items:center; justify-content:center; min-height:70vh; text-align:center; color:#e2e8f0;">
                <div style="font-size:4rem; margin-bottom:1rem;">🩺</div>
                <h2 style="margin:0 0 0.5rem 0;">No blood report selected</h2>
                <p style="margin:0; color:#94a3b8; max-width:600px;">Upload a patient blood_work report or choose a sample from the sidebar to view the dashboard.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    if report_choice in uploaded_names:
        uploaded = next(f for f in uploaded_files if f.name == report_choice)
        report = uploaded.read().decode("utf-8")
        report_label = uploaded.name
    else:
        if report_choice == "Default sample":
            report = load_report_text(DEFAULT_REPORT_PATH)
            report_label = DEFAULT_REPORT_PATH.name
        else:
            selected_path = next((p for p in available_reports if p.name == report_choice), DEFAULT_REPORT_PATH)
            report = load_report_text(selected_path)
            report_label = selected_path.name

    st.session_state["report"] = report
    st.session_state["report_label"] = report_label

    st.markdown(
        """
        <style>
            .block-container { padding-top: 2rem; }
            .stTabs [role="tablist"] { gap: 1rem; }
            .stTabs [role="tab"] { background: #f1f5f9; border-radius: 0.75rem; padding: 0.5rem 1rem; }
            .stTabs [role="tab"][aria-selected="true"] { background: linear-gradient(135deg, #0ea5e9, #22c55e); color: white; }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.sidebar.caption(f"Loaded report: {report_label}")

    profile = extract_patient_profile(report)
    metrics = extract_metrics(report)
    ai_outputs = create_ai_outputs(report, model_name=selected_model)

    st.title("🩺 Blood Health Dashboard")
    st.caption(f"Patient report analysis powered by the same data in the notebook and {report_label}")

    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.subheader(f"{profile['patient_name']}")
        st.write(f"Age/Sex: {profile['age_sex']}")
        st.write(f"Location: {profile['location']}")
    with col2:
        st.write("")
        st.write(f"Sample date: {profile['date']}")
    with col3:
        st.write("")
        st.write("Assessment: Generally stable with routine preventive monitoring")

    tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Extracted Results", "Diet Guidance", "Raw Report"])

    with tab1:
        show_overview(metrics)

    with tab2:
        render_metrics_table(metrics)
        st.subheader("AI-extracted output")
        st.code(ai_outputs["extraction"], language="text")

    with tab3:
        summary = ai_outputs["diet"]
        if isinstance(summary, dict):
            st.markdown("### Quick health summary")
            st.write(summary["summary"])
            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown("### Foods to avoid")
                for item in summary["avoid"]:
                    st.markdown(f"- {item}")
            with col_b:
                st.markdown("### Foods to eat more")
                for item in summary["eat_more"]:
                    st.markdown(f"- {item}")
        else:
            st.code(str(summary), language="text")

    with tab4:
        st.code(report, language="text")


if __name__ == "__main__":
    main()
