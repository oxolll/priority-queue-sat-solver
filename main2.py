from solver_batch_runner2 import run_all_solvers_and_save
import os

# 重複呼叫 solver
# for k in range(len(filenames)):
#     print(f"\n=== 處理第 {k + 1} 個檔案 ===")
#     s = Solver(path, filenames[k])
#     s.show_info()
#     sols = s.find_satisfying_assignments()
#     s.check_solution(sols, True)

uf20_91 = "uf20-91"
uf50_218 = "uf50-218"
uf50_218_ = "uf50-218_"
uuf50_218_1000 = "UUF50.218.1000"
uuf50_218_1000_ = "UUF50.218.1000_"
uf75_325 = "UF75.325.100"
hanoi = "hanoi"
if __name__ == "__main__":
    # folder_name = uf20_91
    # folder_name = uf50_218
    # folder_name = uuf50_218_1000

    # folder_name = "../cnf"
    # folder_name = "w1"
    # folder_name = "w2"
    # folder_name = "w3"
    # folder_name = "w4"
    folder_name = "test5"
    # folder_name = "uuf4"
    # folder_name = hanoi
    # folder_name = "uf752"
    path = os.getcwd() + f"/../cnf/{folder_name}/"  # 設定你的資料夾路徑
    run_all_solvers_and_save(path, "H1v3.1")

    #H1 : base H
    #H1v2 : improved H
    #H1v2.1 : a little improvement
    #H1v3 : dependent and independent
    #H1v3.1 : with some stratege