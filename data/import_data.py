"""从零重建本地数据库。

运行：python data/import_data.py
重建逻辑在 src/bootstrap.py，服务启动时也复用同一套。
"""

import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE.parent))

from src.bootstrap import rebuild_database  # noqa: E402

if __name__ == "__main__":
    n_ent, n_pol = rebuild_database()
    print("数据库重建完成")
    print("企业:", n_ent, "政策:", n_pol)
