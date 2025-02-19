PROJ_ROOT = "data/projs/"
DB_ROOT = "data/dbs/"
LOG_ROOT = "data/logs/"
GEN_ROOT = "gen/"
SINGLE_PROJ_ROOT = "gen/single_proj/"
SINGLE_MUT_ROOT = "gen/single_mut/"

MARIPOSA = "src/smt2action/target/release/mariposa"
QUERY_WIZARD = "src/query_wizard.py"

EXPER_CONFIG_PATH = "config/expers.json"     
SOLVER_CONFIG_PATH = "config/solvers.json"
ANALYZER_CONFIG_PATH = "config/analyzers.json"

SYNC_ZIP = "sync.zip"

S190X_HOSTS = [
    "s1901",
    "s1902",
    "s1904",
    "s1905",
    "s1906",
    "s1907",
    "s1908",
]

CTRL_HOST = "s1904"

DEBUG_ENABLE = False

NINJA_BUILD_FILE = "build.ninja"

NINJA_LOG_FILE = ".ninja_log"

NINJA_REPORTS_DIR = LOG_ROOT + "ninja_reports/"

MAGIC_IGNORE_SEED = 0xdeadbeef # 3735928559

CACHE_ROOT = "cache/"

REPORT_ROOT = "doc/reports/"