"""SQLite Database Layer for AI OFM Agent (Models, Vault, Social Matrix, Fans, Chatting & KPIs)."""

import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional
from ofm_agent.config import DB_PATH, DATA_DIR


def get_connection(db_path: Path = DB_PATH) -> sqlite3.Connection:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_db(db_path: Path = DB_PATH) -> None:
    conn = get_connection(db_path)
    with conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS ai_models (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                niche TEXT NOT NULL,
                market TEXT NOT NULL DEFAULT 'US',
                attractiveness_rating TEXT NOT NULL DEFAULT '7.5/10 Authentic Mid',
                platform TEXT NOT NULL DEFAULT 'Fanvue',
                sub_price REAL NOT NULL DEFAULT 0.0,
                persona_prompt TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'ACTIVE',
                generation_spend REAL NOT NULL DEFAULT 0.0,
                ad_spend REAL NOT NULL DEFAULT 0.0,
                total_revenue REAL NOT NULL DEFAULT 0.0,
                total_fans INTEGER NOT NULL DEFAULT 0,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS content_vault (
                id TEXT PRIMARY KEY,
                model_id TEXT NOT NULL REFERENCES ai_models(id) ON DELETE CASCADE,
                tier INTEGER NOT NULL,
                category TEXT NOT NULL,
                title TEXT NOT NULL,
                description_hook TEXT NOT NULL,
                base_price REAL NOT NULL,
                generation_cost REAL NOT NULL DEFAULT 5.0,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS social_accounts (
                id TEXT PRIMARY KEY,
                model_id TEXT NOT NULL REFERENCES ai_models(id) ON DELETE CASCADE,
                platform TEXT NOT NULL,
                handle TEXT NOT NULL,
                device_id TEXT NOT NULL,
                device_type TEXT NOT NULL DEFAULT 'PHYSICAL_IPHONE',
                proxy_ip TEXT NOT NULL,
                warmup_stage TEXT NOT NULL DEFAULT 'WARMING_DAY_1',
                posts_count INTEGER NOT NULL DEFAULT 0,
                clicks_generated INTEGER NOT NULL DEFAULT 0,
                subs_generated INTEGER NOT NULL DEFAULT 0,
                status TEXT NOT NULL DEFAULT 'HEALTHY'
            );

            CREATE TABLE IF NOT EXISTS fans (
                id TEXT PRIMARY KEY,
                model_id TEXT NOT NULL REFERENCES ai_models(id) ON DELETE CASCADE,
                username TEXT NOT NULL,
                display_name TEXT,
                source_channel TEXT NOT NULL DEFAULT 'IG_REELS',
                acquisition_cost REAL NOT NULL DEFAULT 0.0,
                payment_method TEXT NOT NULL DEFAULT 'APPLE_PAY',
                current_chapter TEXT NOT NULL DEFAULT 'CH1_WELCOME',
                location_tz TEXT,
                job_signal TEXT,
                kink_notes TEXT,
                total_spend REAL NOT NULL DEFAULT 0.0,
                is_whale INTEGER NOT NULL DEFAULT 0,
                last_active TEXT DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS ppv_ledger (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fan_id TEXT NOT NULL REFERENCES fans(id) ON DELETE CASCADE,
                vault_item_id TEXT NOT NULL REFERENCES content_vault(id) ON DELETE CASCADE,
                price_offered REAL NOT NULL,
                unlocked INTEGER NOT NULL DEFAULT 0,
                sent_at TEXT DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(fan_id, vault_item_id)
            );

            CREATE TABLE IF NOT EXISTS chat_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fan_id TEXT NOT NULL REFERENCES fans(id) ON DELETE CASCADE,
                sender TEXT NOT NULL,
                chapter_at_send TEXT NOT NULL,
                message_text TEXT NOT NULL,
                ppv_item_id TEXT,
                ppv_price REAL DEFAULT 0.0,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS department_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                department TEXT NOT NULL,
                manager_name TEXT NOT NULL,
                severity TEXT NOT NULL DEFAULT 'INFO',
                summary TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS compliance_audits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                target_id TEXT NOT NULL,
                check_type TEXT NOT NULL,
                status TEXT NOT NULL,
                details TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            );
            """
        )
    conn.close()
