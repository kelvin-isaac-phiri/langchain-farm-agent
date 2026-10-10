"""SQLite database for AgriGuide (agent_db)."""

import sqlite3
from pathlib import Path

from data import FARMS

DB_PATH = Path(__file__).resolve().parent / "agent_db.sqlite"


def get_connection() -> sqlite3.Connection:
    """Connect to agent_db.sqlite (creates the file if needed)."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Create the farms table and seed sample rows if empty."""
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS farms (
                farm_id TEXT PRIMARY KEY,
                farmer TEXT NOT NULL,
                crop TEXT NOT NULL,
                location TEXT NOT NULL,
                soil TEXT NOT NULL,
                last_rainfall TEXT NOT NULL,
                irrigation TEXT NOT NULL
            )
            """
        )

        count = conn.execute("SELECT COUNT(*) FROM farms").fetchone()[0]
        if count == 0:
            for farm_id, farm in FARMS.items():
                conn.execute(
                    """
                    INSERT INTO farms (
                        farm_id, farmer, crop, location,
                        soil, last_rainfall, irrigation
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        farm_id,
                        farm["farmer"],
                        farm["crop"],
                        farm["location"],
                        farm["soil"],
                        farm["last_rainfall"],
                        farm["irrigation"],
                    ),
                )
            conn.commit()


def get_farm(farm_id: str) -> dict | None:
    """Read one farm row from the farms table."""
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM farms WHERE farm_id = ?",
            (farm_id.upper(),),
        ).fetchone()

    if not row:
        return None

    return dict(row)


if __name__ == "__main__":
    init_db()
    print(f"Database ready: {DB_PATH}")
    with get_connection() as conn:
        rows = conn.execute("SELECT farm_id, farmer, crop, location FROM farms").fetchall()
        for row in rows:
            print(dict(row))
