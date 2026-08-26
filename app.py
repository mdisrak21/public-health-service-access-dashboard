import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date

from database import (
    initialize_database,
    seed_data,
    get_assessments,
    add_assessment,
)


st.set_page_config(
    page_title="Public Health Service Access Dashboard",
    page_icon="🏥",
    layout="wide",
)

initialize_database()
seed_data()


COLUMNS = [
    "ID",
    "Assessment Date",
    "District",
    "Upazila",
    "Facility Type",
    "Population Served",
    "Children",
    "Women",
    "Elderly",
    "Persons with Disabilities",
    "Doctors",
    "Nurses",
    "Beds",
    "Medicine Availability",
    "Maternal Services",
    "Child Health Services",
    "Emergency Services",
    "Distance to Facility (km)",
    "Monthly Patients",
    "Health Staff Shortage",
    "Vulnerability Score",
    "Vulnerability Level",
]


def load_data():

    return pd.DataFrame(
        get_assessments(),
        columns=COLUMNS,
    )


df = load_data()


def calculate_score(
    population,
    children,
    women,
    elderly,
    disabilities,
    doctors,
    nurses,
    beds,
    medicine,
    maternal,
    child_health,
    emergency,
    distance,
    patients,
    staff_shortage,
):

    score = 0

    if population >= 90000:
        score += 10
    elif population >= 70000:
        score += 7
    else:
        score += 4

    if children >= 20000:
        score += 8
    elif children >= 10000:
        score += 5

    if disabilities >= 1800:
        score += 7
    elif disabilities >= 800:
        score += 4

    if doctors <= 5:
        score += 10
    elif doctors <= 8:
        score += 6
    else:
        score += 2

    if nurses <= 15:
        score += 8
    elif nurses <= 22:
        score += 5
    else:
        score += 2

    if beds <= 35:
        score += 8
    elif beds <= 50:
        score += 5

    if medicine < 60:
        score += 8
    elif medicine < 75:
        score += 4

    if maternal == "No":
        score += 7

    if child_health == "No":
        score += 7

    if emergency == "No":
        score += 8

    if distance >= 15:
        score += 8
    elif distance >= 10:
        score += 5

    if patients >= 4500:
        score += 7
    elif patients >= 3000:
        score += 4

    if staff_shortage == "High":
        score += 8
    elif staff_shortage == "Medium":
        score += 4

    return min(score, 100)


def vulnerability_level(score):

    if score >= 80:
        return "Critical"

    if score >= 60:
        return "High"

    if score >= 40:
        return "Medium"

    return "Low"


st.title(
    "🏥 Public Health Service Access & Vulnerability Dashboard"
)

st.caption(
    "Health facility capacity, service access, vulnerability "
    "and population-level health monitoring."
)


st.sidebar.title("🌍 Navigation")

page = st.sidebar.radio(
    "Select Module",
    [
        "Dashboard",
        "Health Assessment",
        "Vulnerability Analysis",
        "Health Capacity",
        "Service Access",
        "Reports",
    ],
)


if page == "Dashboard":

    st.subheader("📊 Public Health Overview")

    facilities = len(df)

    population = int(
        df["Population Served"].sum()
    )

    monthly_patients = int(
        df["Monthly Patients"].sum()
    )

    critical = int(
        (df["Vulnerability Level"] == "Critical").sum()
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Health Facilities",
        facilities,
    )

    c2.metric(
        "Population Served",
        f"{population:,}",
    )

    c3.metric(
        "Monthly Patients",
        f"{monthly_patients:,}",
    )

    c4.metric(
        "Critical Locations",
        critical,
    )

    st.divider()

    left, right = st.columns(2)

    with left:

        risk_data = (
            df["Vulnerability Level"]
            .value_counts()
            .reset_index()
        )

        risk_data.columns = [
            "Vulnerability Level",
            "Facilities",
        ]

        fig = px.pie(
            risk_data,
            names="Vulnerability Level",
            values="Facilities",
            title="Health Vulnerability Distribution",
            hole=0.4,
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

    with right:

        district_data = (
            df.groupby("District")[
                "Population Served"
            ]
            .sum()
            .reset_index()
        )

        fig = px.bar(
            district_data,
            x="District",
            y="Population Served",
            title="Population Served by District",
            text_auto=True,
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

    st.subheader("🚨 High Vulnerability Facilities")

    high_risk = df[
        df["Vulnerability Level"].isin(
            ["Critical", "High"]
        )
    ]

    st.dataframe(
        high_risk[
            [
                "District",
                "Upazila",
                "Facility Type",
                "Population Served",
                "Doctors",
                "Medicine Availability",
                "Vulnerability Score",
                "Vulnerability Level",
            ]
        ],
        use_container_width=True,
        hide_index=True,
    )


elif page == "Health Assessment":

    st.subheader("📝 Health Facility Assessment")

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
    )

    st.divider()

    st.subheader("➕ Add Health Assessment")

    with st.form("health_form"):

        c1, c2, c3, c4 = st.columns(4)

        assessment_date = c1.date_input(
            "Assessment Date",
            value=date.today(),
        )

        district = c2.selectbox(
            "District",
            [
                "Barishal",
                "Bhola",
                "Patuakhali",
                "Barguna",
                "Jhalokathi",
                "Pirojpur",
            ],
        )

        upazila = c3.text_input(
            "Upazila"
        )

        facility_type = c4.selectbox(
            "Facility Type",
            [
                "Upazila Health Complex",
                "Community Clinic",
                "District Hospital",
            ],
        )

        c5, c6, c7, c8 = st.columns(4)

        population = c5.number_input(
            "Population Served",
            min_value=0,
            step=1000,
        )

        children = c6.number_input(
            "Children",
            min_value=0,
            step=100,
        )

        women = c7.number_input(
            "Women",
            min_value=0,
            step=100,
        )

        elderly = c8.number_input(
            "Elderly",
            min_value=0,
            step=100,
        )

        c9, c10, c11, c12 = st.columns(4)

        disabilities = c9.number_input(
            "Persons with Disabilities",
            min_value=0,
            step=10,
        )

        doctors = c10.number_input(
            "Doctors",
            min_value=0,
            step=1,
        )

        nurses = c11.number_input(
            "Nurses",
            min_value=0,
            step=1,
        )

        beds = c12.number_input(
            "Beds",
            min_value=0,
            step=1,
        )

        c13, c14, c15, c16 = st.columns(4)

        medicine = c13.slider(
            "Medicine Availability (%)",
            0,
            100,
            70,
        )

        maternal = c14.selectbox(
            "Maternal Services",
            [
                "Yes",
                "No",
            ],
        )

        child_health = c15.selectbox(
            "Child Health Services",
            [
                "Yes",
                "No",
            ],
        )

        emergency = c16.selectbox(
            "Emergency Services",
            [
                "Yes",
                "No",
            ],
        )

        c17, c18, c19 = st.columns(3)

        distance = c17.number_input(
            "Distance to Facility (km)",
            min_value=0.0,
            step=0.5,
        )

        patients = c18.number_input(
            "Monthly Patients",
            min_value=0,
            step=100,
        )

        shortage = c19.selectbox(
            "Health Staff Shortage",
            [
                "Low",
                "Medium",
                "High",
            ],
        )

        submitted = st.form_submit_button(
            "Add Assessment"
        )

        if submitted:

            if not upazila.strip():

                st.error(
                    "Please enter the Upazila."
                )

            else:

                score = calculate_score(
                    population,
                    children,
                    women,
                    elderly,
                    disabilities,
                    doctors,
                    nurses,
                    beds,
                    medicine,
                    maternal,
                    child_health,
                    emergency,
                    distance,
                    patients,
                    shortage,
                )

                level = vulnerability_level(
                    score
                )

                add_assessment(
                    str(assessment_date),
                    district,
                    upazila.strip(),
                    facility_type,
                    int(population),
                    int(children),
                    int(women),
                    int(elderly),
                    int(disabilities),
                    int(doctors),
                    int(nurses),
                    int(beds),
                    int(medicine),
                    maternal,
                    child_health,
                    emergency,
                    float(distance),
                    int(patients),
                    shortage,
                    int(score),
                    level,
                )

                st.success(
                    f"Assessment added. "
                    f"Vulnerability Score: {score} "
                    f"({level})"
                )

                st.rerun()


elif page == "Vulnerability Analysis":

    st.subheader(
        "⚠️ Health Vulnerability Analysis"
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Critical",
        int(
            (df["Vulnerability Level"] == "Critical").sum()
        ),
    )

    c2.metric(
        "High",
        int(
            (df["Vulnerability Level"] == "High").sum()
        ),
    )

    c3.metric(
        "Medium",
        int(
            (df["Vulnerability Level"] == "Medium").sum()
        ),
    )

    c4.metric(
        "Low",
        int(
            (df["Vulnerability Level"] == "Low").sum()
        ),
    )

    st.divider()

    district_risk = (
        df.groupby("District")
        .agg(
            Average_Score=(
                "Vulnerability Score",
                "mean",
            ),
            Population=(
                "Population Served",
                "sum",
            ),
        )
        .reset_index()
    )

    district_risk[
        "Average_Score"
    ] = district_risk[
        "Average_Score"
    ].round(1)

    fig = px.bar(
        district_risk,
        x="District",
        y="Average_Score",
        title="Average Health Vulnerability Score",
        text_auto=True,
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

    st.subheader(
        "🎯 Highest Vulnerability Locations"
    )

    highest = df.sort_values(
        "Vulnerability Score",
        ascending=False,
    ).head(10)

    st.dataframe(
        highest,
        use_container_width=True,
        hide_index=True,
    )


elif page == "Health Capacity":

    st.subheader(
        "🏥 Health Facility Capacity"
    )

    capacity = pd.DataFrame({
        "Indicator": [
            "Doctors",
            "Nurses",
            "Beds",
            "Monthly Patients",
        ],
        "Total": [
            df["Doctors"].sum(),
            df["Nurses"].sum(),
            df["Beds"].sum(),
            df["Monthly Patients"].sum(),
        ],
    })

    fig = px.bar(
        capacity,
        x="Indicator",
        y="Total",
        title="Health System Capacity",
        text_auto=True,
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

    st.subheader(
        "👨‍⚕️ Staff Availability by District"
    )

    staff = (
        df.groupby("District")
        .agg(
            Doctors=("Doctors", "sum"),
            Nurses=("Nurses", "sum"),
        )
        .reset_index()
    )

    staff_long = staff.melt(
        id_vars="District",
        var_name="Staff Type",
        value_name="Count",
    )

    fig = px.bar(
        staff_long,
        x="District",
        y="Count",
        color="Staff Type",
        barmode="group",
        title="Health Workforce by District",
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

    st.subheader(
        "💊 Medicine Availability"
    )

    medicine = (
        df.groupby("District")[
            "Medicine Availability"
        ]
        .mean()
        .reset_index()
    )

    medicine[
        "Medicine Availability"
    ] = medicine[
        "Medicine Availability"
    ].round(1)

    fig = px.bar(
        medicine,
        x="District",
        y="Medicine Availability",
        title="Average Medicine Availability (%)",
        text_auto=True,
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )


elif page == "Service Access":

    st.subheader(
        "🚑 Health Service Access"
    )

    service_data = pd.DataFrame({
        "Service": [
            "Maternal Services",
            "Child Health Services",
            "Emergency Services",
        ],
        "Available": [
            (
                df["Maternal Services"] == "Yes"
            ).sum(),
            (
                df["Child Health Services"] == "Yes"
            ).sum(),
            (
                df["Emergency Services"] == "Yes"
            ).sum(),
        ],
    })

    fig = px.bar(
        service_data,
        x="Service",
        y="Available",
        title="Essential Health Service Availability",
        text_auto=True,
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

    st.subheader(
        "📍 Distance to Health Facilities"
    )

    fig = px.bar(
        df.sort_values(
            "Distance to Facility (km)",
            ascending=False,
        ),
        x="Upazila",
        y="Distance to Facility (km)",
        color="District",
        title="Average Access Distance",
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

    st.subheader(
        "👩 Women & Child Population"
    )

    population_data = pd.DataFrame({
        "Group": [
            "Children",
            "Women",
            "Elderly",
            "Persons with Disabilities",
        ],
        "Population": [
            df["Children"].sum(),
            df["Women"].sum(),
            df["Elderly"].sum(),
            df["Persons with Disabilities"].sum(),
        ],
    })

    fig = px.pie(
        population_data,
        names="Group",
        values="Population",
        title="Population Groups Served",
        hole=0.4,
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )


elif page == "Reports":

    st.subheader(
        "📑 Public Health Reports"
    )

    report_type = st.selectbox(
        "Select Report",
        [
            "Full Health Assessment",
            "Critical & High Vulnerability",
            "District Summary",
            "Facility Type Summary",
        ],
    )

    if report_type == "Full Health Assessment":

        report_df = df.copy()

    elif report_type == "Critical & High Vulnerability":

        report_df = df[
            df["Vulnerability Level"].isin(
                ["Critical", "High"]
            )
        ].copy()

    elif report_type == "District Summary":

        report_df = (
            df.groupby("District")
            .agg(
                Facilities=(
                    "ID",
                    "count",
                ),
                Population_Served=(
                    "Population Served",
                    "sum",
                ),
                Monthly_Patients=(
                    "Monthly Patients",
                    "sum",
                ),
                Average_Vulnerability=(
                    "Vulnerability Score",
                    "mean",
                ),
            )
            .reset_index()
        )

        report_df[
            "Average_Vulnerability"
        ] = report_df[
            "Average_Vulnerability"
        ].round(1)

    else:

        report_df = (
            df.groupby("Facility Type")
            .agg(
                Facilities=(
                    "ID",
                    "count",
                ),
                Population_Served=(
                    "Population Served",
                    "sum",
                ),
                Average_Vulnerability=(
                    "Vulnerability Score",
                    "mean",
                ),
            )
            .reset_index()
        )

        report_df[
            "Average_Vulnerability"
        ] = report_df[
            "Average_Vulnerability"
        ].round(1)

    st.dataframe(
        report_df,
        use_container_width=True,
        hide_index=True,
    )

    csv_data = report_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        "📥 Download Report CSV",
        data=csv_data,
        file_name=(
            report_type.lower()
            .replace(" ", "_")
            + ".csv"
        ),
        mime="text/csv",
    )


st.sidebar.divider()

st.sidebar.caption(
    "Public Health Service Access & Vulnerability"
)

st.sidebar.caption(
    "Synthetic data for portfolio demonstration."
)