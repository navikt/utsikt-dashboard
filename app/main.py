import streamlit as st
import os
import time
import statistics
import datetime
import dateutil

from data import Table
from bq_connector import BigQueryConnector
from google.cloud import bigquery
from functions import TimeResolution

from tabs.om_dataen import om_dataen
from tabs.oppdrag import oppdrag
from tabs.ventestatus_manuell import ventestatus_manuell
from tabs.beregninger import beregninger
from tabs.p4 import p4

st.set_page_config(layout="wide")


google_project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "utsikt-dev-3609")
google_project_id = "utsikt-prod-2dfe"

timing_enabled = st.sidebar.toggle(
    "Vis ytelsesmaling", value=False, key="timing_enabled"
)


def _p95(values: list[float]) -> float:
    if len(values) == 0:
        return 0.0
    if len(values) == 1:
        return values[0]
    return statistics.quantiles(values, n=100)[94]


def _record_timing(name: str, duration_s: float) -> None:
    timing_history = st.session_state.setdefault("timing_history", {})
    if name not in timing_history:
        timing_history[name] = []
    timing_history[name].append(duration_s)
    timing_history[name] = timing_history[name][-30:]


def _time_call(name: str, fn, *args, **kwargs):
    start = time.perf_counter()
    result = fn(*args, **kwargs)
    duration_s = time.perf_counter() - start
    _record_timing(name=name, duration_s=duration_s)
    return result, duration_s


def _render_timing_sidebar(
    run_timings: dict[str, float], changed_keys: list[str]
) -> None:
    if not timing_enabled:
        return

    st.sidebar.subheader("Ytelsesmaling")
    if changed_keys:
        st.sidebar.write("Sist endret input:")
        for key in changed_keys:
            st.sidebar.write(f"- {key}")

    st.sidebar.write("Siste rerun")
    for name, duration in run_timings.items():
        st.sidebar.write(f"{name}: {duration:.3f}s")

    timing_history = st.session_state.get("timing_history", {})
    if timing_history:
        st.sidebar.write("Gjennomsnitt / median / p95")
        for name, values in timing_history.items():
            st.sidebar.write(
                f"{name}: {statistics.mean(values):.3f}s / {statistics.median(values):.3f}s / {_p95(values):.3f}s"
            )


@st.cache_data(ttl=24 * 3600)
def fetch_tables(
    current_google_project_id: str,
    default_start_date_oppdrag: datetime.date,
    default_end_date_oppdrag: datetime.date,
    default_time_resolution_bq_oppdrag: str,
    default_start_date_beregninger: datetime.date,
    default_end_date_beregninger: datetime.date,
    default_time_resolution_bq_beregninger: str,
) -> dict[str, Table]:
    bq_connector = BigQueryConnector()

    oppdrag = Table(
        path_to_query="queries/oppdrag.sql",
        google_project_id=current_google_project_id,
        extra_placeholders={"<TIME_RESOLUTION>": default_time_resolution_bq_oppdrag},
    )

    beregninger_faggruppe = Table(
        path_to_query="queries/beregninger_faggruppe.sql",
        google_project_id=current_google_project_id,
        extra_placeholders={
            "<TIME_RESOLUTION>": default_time_resolution_bq_beregninger
        },
    )
    beregninger_fagomrade = Table(
        path_to_query="queries/beregninger_fagomrade.sql",
        google_project_id=current_google_project_id,
        extra_placeholders={
            "<TIME_RESOLUTION>": default_time_resolution_bq_beregninger
        },
    )

    beregninger_manuell_ventestatuser = Table(
        path_to_query="queries/beregninger_manuell_ventestatuser.sql",
        google_project_id=current_google_project_id,
    )

    beregninger_p4 = Table(
        path_to_query="queries/beregninger_p4.sql",
        google_project_id=current_google_project_id,
    )

    oppdrag.fetch_data(
        bq_connector=bq_connector,
        query_parameters=[
            bigquery.ScalarQueryParameter(
                "default_start_date", "DATE", default_start_date_oppdrag
            ),
            bigquery.ScalarQueryParameter(
                "default_end_date", "DATE", default_end_date_oppdrag
            ),
        ],
    )
    beregninger_faggruppe.fetch_data(
        bq_connector=bq_connector,
        query_parameters=[
            bigquery.ScalarQueryParameter(
                "default_start_date_beregninger",
                "DATE",
                default_start_date_beregninger,
            ),
            bigquery.ScalarQueryParameter(
                "default_end_date_beregninger", "DATE", default_end_date_beregninger
            ),
        ],
    )
    beregninger_fagomrade.fetch_data(
        bq_connector=bq_connector,
        query_parameters=[
            bigquery.ScalarQueryParameter(
                "default_start_date_beregninger",
                "DATE",
                default_start_date_beregninger,
            ),
            bigquery.ScalarQueryParameter(
                "default_end_date_beregninger", "DATE", default_end_date_beregninger
            ),
        ],
    )
    beregninger_manuell_ventestatuser.fetch_data(bq_connector=bq_connector)
    beregninger_p4.fetch_data(bq_connector=bq_connector)

    fetched_tables = {
        "oppdrag": oppdrag,
        "beregninger_faggruppe": beregninger_faggruppe,
        "beregninger_fagomrade": beregninger_fagomrade,
        "beregninger_manuell_ventestatuser": beregninger_manuell_ventestatuser,
        "beregninger_p4": beregninger_p4,
    }

    return fetched_tables


app_start = time.perf_counter()

max_value_oppdrag = datetime.datetime.now().date()
default_oppdrag_date_range = (
    max_value_oppdrag - dateutil.relativedelta.relativedelta(months=2),
    max_value_oppdrag,
)
max_value_beregninger = datetime.datetime.now().date()
default_beregninger_date_range = (
    max_value_beregninger - dateutil.relativedelta.relativedelta(months=2),
    max_value_beregninger,
)
st.session_state.setdefault("date_range_oppdrag", default_oppdrag_date_range)
st.session_state.setdefault("select_time_resolution_oppdrag", "Weekly")
st.session_state.setdefault("date_range_beregninger", default_beregninger_date_range)
st.session_state.setdefault("select_time_resolution_beregninger", "Daily")
oppdrag_date_range = st.session_state["date_range_oppdrag"]
beregninger_date_range = st.session_state["date_range_beregninger"]
default_time_resolution_bq_oppdrag = TimeResolution.to_bq_trunc_part(
    st.session_state["select_time_resolution_oppdrag"]
)
default_time_resolution_bq_beregninger = TimeResolution.to_bq_trunc_part(
    st.session_state["select_time_resolution_beregninger"]
)

tables, fetch_tables_time = _time_call(
    "fetch_tables",
    fetch_tables,
    current_google_project_id=google_project_id,
    default_start_date_oppdrag=oppdrag_date_range[0],
    default_end_date_oppdrag=oppdrag_date_range[1],
    default_time_resolution_bq_oppdrag=default_time_resolution_bq_oppdrag,
    default_start_date_beregninger=beregninger_date_range[0],
    default_end_date_beregninger=beregninger_date_range[1],
    default_time_resolution_bq_beregninger=default_time_resolution_bq_beregninger,
)

if "faggruppe_selection" not in st.session_state:
    st.session_state["faggruppe_selection"] = ["Alle"]

if "fagomrade_selection" not in st.session_state:
    st.session_state["fagomrade_selection"] = ["Alle"]

if "ventestatus_selection" not in st.session_state:
    st.session_state["ventestatus_selection"] = ["Alle"]

tracked_input_keys = [
    "ytelse_selection",
    "select_time_resolution_oppdrag",
    "date_range_oppdrag",
    "oppdrag_show_proportion",
    "faggruppe_selection",
    "fagomrade_selection",
    "select_time_resolution_beregninger",
    "date_range_beregninger",
    "ventestatus_selection",
    "faggruppe_selection2",
    "select_time_resolution",
    "select_time_relative_ventestatus",
    "ytelse_selection_p4",
    "select_time_resolution_p4",
    "date_range_p4",
    "p4_show_proportion",
]

previous_input_snapshot = st.session_state.get("timing_input_snapshot", {})
current_input_snapshot = {
    key: st.session_state.get(key)
    for key in tracked_input_keys
    if key in st.session_state
}
changed_input_keys = [
    key
    for key in current_input_snapshot
    if current_input_snapshot.get(key) != previous_input_snapshot.get(key)
]


tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["Oppdrag", "Beregninger", "Ventestatus manuell", "P4", "Om dataen"]
)

run_timings = {
    "fetch_tables": fetch_tables_time,
}

with tab1:
    _, tab_time = _time_call("tab_oppdrag", oppdrag, tables["oppdrag"])
    run_timings["tab_oppdrag"] = tab_time

with tab2:
    _, tab_time = _time_call("tab_beregninger", beregninger, tables)
    run_timings["tab_beregninger"] = tab_time

with tab3:
    _, tab_time = _time_call(
        "tab_ventestatus_manuell",
        ventestatus_manuell,
        tables["beregninger_manuell_ventestatuser"],
    )
    run_timings["tab_ventestatus_manuell"] = tab_time

with tab4:
    _, tab_time = _time_call("tab_p4", p4, tables["beregninger_p4"])
    run_timings["tab_p4"] = tab_time

with tab5:
    _, tab_time = _time_call("tab_om_dataen", om_dataen)
    run_timings["tab_om_dataen"] = tab_time

run_timings["rerun_total"] = time.perf_counter() - app_start
_record_timing(name="rerun_total", duration_s=run_timings["rerun_total"])
st.session_state["timing_input_snapshot"] = current_input_snapshot

if changed_input_keys:
    st.session_state["timing_last_input_change"] = {
        "changed_keys": changed_input_keys,
        "run_timings": run_timings,
    }

_render_timing_sidebar(run_timings=run_timings, changed_keys=changed_input_keys)
