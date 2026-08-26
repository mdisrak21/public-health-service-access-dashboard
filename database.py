import sqlite3

DB_NAME = "public_health.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def initialize_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS health_assessments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            assessment_date TEXT NOT NULL,
            district TEXT NOT NULL,
            upazila TEXT NOT NULL,
            facility_type TEXT NOT NULL,
            population_served INTEGER NOT NULL,
            children INTEGER NOT NULL,
            women INTEGER NOT NULL,
            elderly INTEGER NOT NULL,
            persons_with_disabilities INTEGER NOT NULL,
            doctors INTEGER NOT NULL,
            nurses INTEGER NOT NULL,
            beds INTEGER NOT NULL,
            medicine_availability INTEGER NOT NULL,
            maternal_services TEXT NOT NULL,
            child_health_services TEXT NOT NULL,
            emergency_services TEXT NOT NULL,
            distance_to_facility REAL NOT NULL,
            patients_monthly INTEGER NOT NULL,
            health_staff_shortage TEXT NOT NULL,
            vulnerability_score INTEGER NOT NULL,
            vulnerability_level TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def seed_data():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM health_assessments"
    )

    if cursor.fetchone()[0] > 0:
        conn.close()
        return

    data = [
        (
            "2026-07-10",
            "Barishal",
            "Mehendiganj",
            "Upazila Health Complex",
            85000,
            19000,
            42000,
            8500,
            1800,
            8,
            21,
            42,
            58,
            "Yes",
            "Yes",
            "Yes",
            12.5,
            4200,
            "High",
            82,
            "Critical",
        ),
        (
            "2026-07-12",
            "Bhola",
            "Char Fasson",
            "Upazila Health Complex",
            72000,
            17000,
            36000,
            7200,
            1500,
            10,
            25,
            55,
            72,
            "Yes",
            "Yes",
            "Yes",
            8.2,
            3800,
            "Medium",
            64,
            "High",
        ),
        (
            "2026-07-14",
            "Patuakhali",
            "Galachipa",
            "Upazila Health Complex",
            91000,
            21000,
            47000,
            9100,
            2100,
            6,
            18,
            35,
            49,
            "No",
            "Yes",
            "Yes",
            16.4,
            4600,
            "High",
            91,
            "Critical",
        ),
        (
            "2026-07-16",
            "Barguna",
            "Amtali",
            "Upazila Health Complex",
            68000,
            15000,
            34000,
            6800,
            1400,
            9,
            24,
            48,
            67,
            "Yes",
            "Yes",
            "Yes",
            10.1,
            3300,
            "Medium",
            61,
            "High",
        ),
        (
            "2026-07-18",
            "Jhalokathi",
            "Kathalia",
            "Community Clinic",
            22000,
            5200,
            11000,
            2300,
            500,
            2,
            5,
            8,
            81,
            "Yes",
            "Yes",
            "No",
            5.7,
            1200,
            "Low",
            44,
            "Medium",
        ),
        (
            "2026-07-20",
            "Pirojpur",
            "Mathbaria",
            "Upazila Health Complex",
            76000,
            18000,
            39000,
            7600,
            1600,
            11,
            27,
            60,
            78,
            "Yes",
            "Yes",
            "Yes",
            7.4,
            4100,
            "Medium",
            52,
            "Medium",
        ),
        (
            "2026-07-22",
            "Barishal",
            "Bakerganj",
            "Upazila Health Complex",
            97000,
            23000,
            51000,
            9700,
            2200,
            7,
            19,
            38,
            55,
            "Yes",
            "No",
            "Yes",
            14.7,
            4800,
            "High",
            79,
            "High",
        ),
        (
            "2026-07-24",
            "Bhola",
            "Lalmohan",
            "Upazila Health Complex",
            83000,
            20000,
            43000,
            8200,
            1700,
            5,
            16,
            31,
            46,
            "No",
            "Yes",
            "Yes",
            18.3,
            4400,
            "High",
            94,
            "Critical",
        ),
        (
            "2026-07-26",
            "Patuakhali",
            "Rangabali",
            "Community Clinic",
            31000,
            7200,
            16000,
            3200,
            650,
            2,
            6,
            10,
            63,
            "Yes",
            "Yes",
            "No",
            11.8,
            1500,
            "Medium",
            58,
            "Medium",
        ),
        (
            "2026-07-28",
            "Barguna",
            "Patharghata",
            "Upazila Health Complex",
            79000,
            18000,
            41000,
            7900,
            1750,
            8,
            20,
            45,
            61,
            "Yes",
            "Yes",
            "Yes",
            13.1,
            3900,
            "High",
            76,
            "High",
        ),
    ]

    cursor.executemany("""
        INSERT INTO health_assessments (
            assessment_date,
            district,
            upazila,
            facility_type,
            population_served,
            children,
            women,
            elderly,
            persons_with_disabilities,
            doctors,
            nurses,
            beds,
            medicine_availability,
            maternal_services,
            child_health_services,
            emergency_services,
            distance_to_facility,
            patients_monthly,
            health_staff_shortage,
            vulnerability_score,
            vulnerability_level
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, data)

    conn.commit()
    conn.close()


def get_assessments():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            assessment_date,
            district,
            upazila,
            facility_type,
            population_served,
            children,
            women,
            elderly,
            persons_with_disabilities,
            doctors,
            nurses,
            beds,
            medicine_availability,
            maternal_services,
            child_health_services,
            emergency_services,
            distance_to_facility,
            patients_monthly,
            health_staff_shortage,
            vulnerability_score,
            vulnerability_level
        FROM health_assessments
        ORDER BY vulnerability_score DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    return rows


def add_assessment(
    assessment_date,
    district,
    upazila,
    facility_type,
    population_served,
    children,
    women,
    elderly,
    disabilities,
    doctors,
    nurses,
    beds,
    medicine_availability,
    maternal_services,
    child_health_services,
    emergency_services,
    distance_to_facility,
    patients_monthly,
    staff_shortage,
    vulnerability_score,
    vulnerability_level,
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO health_assessments (
            assessment_date,
            district,
            upazila,
            facility_type,
            population_served,
            children,
            women,
            elderly,
            persons_with_disabilities,
            doctors,
            nurses,
            beds,
            medicine_availability,
            maternal_services,
            child_health_services,
            emergency_services,
            distance_to_facility,
            patients_monthly,
            health_staff_shortage,
            vulnerability_score,
            vulnerability_level
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        assessment_date,
        district,
        upazila,
        facility_type,
        population_served,
        children,
        women,
        elderly,
        disabilities,
        doctors,
        nurses,
        beds,
        medicine_availability,
        maternal_services,
        child_health_services,
        emergency_services,
        distance_to_facility,
        patients_monthly,
        staff_shortage,
        vulnerability_score,
        vulnerability_level,
    ))

    conn.commit()
    conn.close()