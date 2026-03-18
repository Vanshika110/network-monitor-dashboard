import sqlite3
from datetime import datetime

DB_PATH = "packets.db"

def init_db():
    """Initialize SQLite database"""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS packets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            src_ip TEXT,
            dst_ip TEXT,
            protocol TEXT,
            src_port INTEGER,
            dst_port INTEGER,
            size INTEGER
        )
    """)
    conn.commit()
    conn.close()
    print("[*] Database initialized")

def save_packet(data):
    """Save parsed packet to DB"""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        INSERT INTO packets 
        (timestamp, src_ip, dst_ip, protocol, src_port, dst_port, size)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        data["timestamp"], data["src_ip"], data["dst_ip"],
        data["protocol"], data["src_port"], data["dst_port"], data["size"]
    ))
    conn.commit()
    conn.close()

def get_stats():
    """Get aggregated stats for dashboard"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Protocol distribution
    cursor.execute("""
        SELECT protocol, COUNT(*) as count 
        FROM packets 
        GROUP BY protocol
    """)
    protocols = dict(cursor.fetchall())

    # Top source IPs
    cursor.execute("""
        SELECT src_ip, COUNT(*) as count 
        FROM packets 
        GROUP BY src_ip 
        ORDER BY count DESC 
        LIMIT 5
    """)
    top_ips = cursor.fetchall()

    # Total packets
    cursor.execute("SELECT COUNT(*) FROM packets")
    total = cursor.fetchone()[0]

    # Total bandwidth
    cursor.execute("SELECT SUM(size) FROM packets")
    bandwidth = cursor.fetchone()[0] or 0

    conn.close()
    return {
        "protocols": protocols,
        "top_ips": top_ips,
        "total_packets": total,
        "total_bytes": bandwidth
    }

init_db()