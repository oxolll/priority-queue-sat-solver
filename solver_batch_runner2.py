import os
from solver2 import Solver
import excel as xsl

def run_all_solvers_and_save(path : str, folder_name : str):
    results = []

    i_th = 0
    for file_name in os.listdir(path):
        # 確保只處理合法的 CNF 檔案
        if file_name.endswith(".cnf"):
            i_th += 1
            solver = Solver(path, file_name)
            print(f"處理{i_th}-th檔案: {file_name}")

            # 取得滿足解與執行結果
            solver_result = solver.find_satisfying_assignments(verbose=False)
            sols = solver_result["satisfying_assignments"]
            dfs_calls = solver_result["dfs_counter"]
            elapsed_time = solver_result["elapsed_time"]

            # 檢查解是否正確
            errors = solver.check_solution(sols, verbose=False)

            # 存儲結果
            results.append({
                "檔名": file_name,
                "n": solver.n,
                "m": solver.m,
                "sat/usat": "sat" if sols else "unsat",
                "dfs呼叫次數": dfs_calls,
                "最壞呼叫次數": 2 ** solver.n,
                "time(hr:min:sec)": elapsed_time,
                "滿足解": len(sols),
                "檢驗結果": "錯誤" if errors else "正確"
            })

    # 保存結果到 Excel
    xsl.save_to_excel(results, folder_name)
