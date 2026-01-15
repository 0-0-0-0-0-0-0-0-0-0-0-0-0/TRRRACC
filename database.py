#!/usr/bin/env python3
"""
统计数据库模块
用于记录用户访问和查询数据
"""
import sqlite3
import os
import time
from datetime import datetime, timedelta

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
os.makedirs(DATA_DIR, exist_ok=True)
DB_PATH = os.path.join(DATA_DIR, 'stats.db')


def get_connection():
    """获取数据库连接"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """初始化数据库表"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # 用户表 - 通过 Cookie 识别
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT UNIQUE NOT NULL,
            first_seen INTEGER NOT NULL,
            last_seen INTEGER NOT NULL,
            visit_count INTEGER DEFAULT 1
        )
    ''')
    
    # 页面访问记录
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS page_views (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            page TEXT NOT NULL,
            timestamp INTEGER NOT NULL,
            user_agent TEXT
        )
    ''')
    
    # 查询记录
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS query_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            query_type TEXT NOT NULL,
            market_name TEXT,
            market_url TEXT,
            wallet_address TEXT,
            status TEXT NOT NULL,
            duration REAL,
            timestamp INTEGER NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()


# ===== 用户相关 =====

def record_user(user_id):
    """记录用户访问，返回是否为新用户"""
    conn = get_connection()
    cursor = conn.cursor()
    now = int(time.time())
    
    cursor.execute('SELECT id, visit_count FROM users WHERE user_id = ?', (user_id,))
    row = cursor.fetchone()
    
    is_new = False
    if row:
        cursor.execute('''
            UPDATE users SET last_seen = ?, visit_count = visit_count + 1 WHERE user_id = ?
        ''', (now, user_id))
    else:
        cursor.execute('''
            INSERT INTO users (user_id, first_seen, last_seen, visit_count) VALUES (?, ?, ?, 1)
        ''', (user_id, now, now))
        is_new = True
    
    conn.commit()
    conn.close()
    return is_new


def get_total_users():
    """获取总用户数"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM users')
    count = cursor.fetchone()[0]
    conn.close()
    return count


def get_today_new_users():
    """获取今日新用户数"""
    conn = get_connection()
    cursor = conn.cursor()
    today_start = int(datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).timestamp())
    cursor.execute('SELECT COUNT(*) FROM users WHERE first_seen >= ?', (today_start,))
    count = cursor.fetchone()[0]
    conn.close()
    return count


def get_today_active_users():
    """获取今日活跃用户数"""
    conn = get_connection()
    cursor = conn.cursor()
    today_start = int(datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).timestamp())
    cursor.execute('SELECT COUNT(*) FROM users WHERE last_seen >= ?', (today_start,))
    count = cursor.fetchone()[0]
    conn.close()
    return count


def get_yesterday_users():
    """获取昨日用户数（用于计算增长）"""
    conn = get_connection()
    cursor = conn.cursor()
    today_start = int(datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).timestamp())
    yesterday_start = today_start - 86400
    cursor.execute('SELECT COUNT(*) FROM users WHERE first_seen >= ? AND first_seen < ?', (yesterday_start, today_start))
    count = cursor.fetchone()[0]
    conn.close()
    return count


# ===== 页面访问相关 =====

def record_page_view(user_id, page, user_agent=None):
    """记录页面访问"""
    conn = get_connection()
    cursor = conn.cursor()
    now = int(time.time())
    cursor.execute('''
        INSERT INTO page_views (user_id, page, timestamp, user_agent) VALUES (?, ?, ?, ?)
    ''', (user_id, page, now, user_agent))
    conn.commit()
    conn.close()


def get_total_page_views():
    """获取总访问量"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM page_views')
    count = cursor.fetchone()[0]
    conn.close()
    return count


def get_today_page_views():
    """获取今日访问量"""
    conn = get_connection()
    cursor = conn.cursor()
    today_start = int(datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).timestamp())
    cursor.execute('SELECT COUNT(*) FROM page_views WHERE timestamp >= ?', (today_start,))
    count = cursor.fetchone()[0]
    conn.close()
    return count


# ===== 查询记录相关 =====

def record_query(user_id, query_type, market_name, market_url, wallet_address, status, duration=None):
    """记录查询"""
    conn = get_connection()
    cursor = conn.cursor()
    now = int(time.time())
    cursor.execute('''
        INSERT INTO query_logs (user_id, query_type, market_name, market_url, wallet_address, status, duration, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (user_id, query_type, market_name, market_url, wallet_address, status, duration, now))
    conn.commit()
    conn.close()


def get_total_queries():
    """获取总查询次数"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM query_logs')
    count = cursor.fetchone()[0]
    conn.close()
    return count


def get_query_success_rate():
    """获取查询成功率"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM query_logs')
    total = cursor.fetchone()[0]
    if total == 0:
        conn.close()
        return 0
    cursor.execute("SELECT COUNT(*) FROM query_logs WHERE status = 'success'")
    success = cursor.fetchone()[0]
    conn.close()
    return round(success / total * 100, 1)


def get_today_queries():
    """获取今日查询统计"""
    conn = get_connection()
    cursor = conn.cursor()
    today_start = int(datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).timestamp())
    
    cursor.execute('SELECT COUNT(*) FROM query_logs WHERE timestamp >= ?', (today_start,))
    total = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM query_logs WHERE timestamp >= ? AND status = 'success'", (today_start,))
    success = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM query_logs WHERE timestamp >= ? AND status = 'error'", (today_start,))
    error = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM query_logs WHERE timestamp >= ? AND status = 'cancelled'", (today_start,))
    cancelled = cursor.fetchone()[0]
    
    conn.close()
    return {'total': total, 'success': success, 'error': error, 'cancelled': cancelled}


def get_query_type_distribution():
    """获取查询类型分布"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM query_logs')
    total = cursor.fetchone()[0]
    if total == 0:
        conn.close()
        return {'simple': 0, 'multi': 0}
    
    cursor.execute("SELECT COUNT(*) FROM query_logs WHERE query_type = 'simple'")
    simple = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM query_logs WHERE query_type = 'multi'")
    multi = cursor.fetchone()[0]
    
    conn.close()
    return {
        'simple': round(simple / total * 100, 1),
        'multi': round(multi / total * 100, 1),
        'simple_count': simple,
        'multi_count': multi
    }


def get_query_status_distribution():
    """获取查询状态分布"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM query_logs')
    total = cursor.fetchone()[0]
    if total == 0:
        conn.close()
        return {'success': 0, 'error': 0, 'cancelled': 0}
    
    cursor.execute("SELECT COUNT(*) FROM query_logs WHERE status = 'success'")
    success = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM query_logs WHERE status = 'error'")
    error = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM query_logs WHERE status = 'cancelled'")
    cancelled = cursor.fetchone()[0]
    
    conn.close()
    return {
        'success': round(success / total * 100, 1),
        'error': round(error / total * 100, 1),
        'cancelled': round(cancelled / total * 100, 1),
        'success_count': success,
        'error_count': error,
        'cancelled_count': cancelled
    }


def get_avg_query_duration():
    """获取平均查询耗时"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT AVG(duration), MIN(duration), MAX(duration) FROM query_logs WHERE status = 'success' AND duration IS NOT NULL")
    row = cursor.fetchone()
    conn.close()
    
    if row[0] is None:
        return {'avg': 0, 'min': 0, 'max': 0}
    return {
        'avg': round(row[0], 1),
        'min': round(row[1], 1),
        'max': round(row[2], 1)
    }


def get_top_markets(limit=10):
    """获取热门市场"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT market_name, market_url, COUNT(*) as count 
        FROM query_logs 
        WHERE market_name IS NOT NULL AND market_name != ''
        GROUP BY market_url 
        ORDER BY count DESC 
        LIMIT ?
    ''', (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [{'name': row['market_name'], 'url': row['market_url'], 'count': row['count']} for row in rows]


def get_recent_queries(limit=50, offset=0):
    """获取最近查询记录"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT query_type, market_name, market_url, wallet_address, status, duration, timestamp
        FROM query_logs
        ORDER BY timestamp DESC
        LIMIT ? OFFSET ?
    ''', (limit, offset))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_all_stats():
    """获取所有统计数据（用于后台页面）"""
    return {
        'total_users': get_total_users(),
        'today_new_users': get_today_new_users(),
        'today_active_users': get_today_active_users(),
        'yesterday_new_users': get_yesterday_users(),
        'total_page_views': get_total_page_views(),
        'today_page_views': get_today_page_views(),
        'total_queries': get_total_queries(),
        'query_success_rate': get_query_success_rate(),
        'today_queries': get_today_queries(),
        'query_type_dist': get_query_type_distribution(),
        'query_status_dist': get_query_status_distribution(),
        'avg_duration': get_avg_query_duration(),
        'top_markets': get_top_markets(),
        'update_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }


# 初始化数据库
init_db()
