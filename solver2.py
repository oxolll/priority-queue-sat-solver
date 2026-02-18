import os
import heapq
import copy
from datetime import datetime

class Solver:
    def __init__(self, path: str, file_name: str):
        self.path = path
        self.file_name = file_name
        self.n = 0  # 變數數量
        self.m = 0  # 子句數量
        self.status = []   # 存放 p cnf 資訊
        self.clauses = []  # 存放所有子句
        self.dfs_counter = 0

        self.readfile()  # 初始化時自動讀檔

    def readfile(self):
        file_path = os.path.join(self.path, self.file_name)

        try:
            with open(file_path, 'r') as f:
                lines = f.readlines()

            for line in lines:
                line = line.strip()

                if not line or line.startswith(('c', '%', '0')):
                    continue

                if line.startswith('p'):
                    parts = [x for x in line.split() if x]
                    self.status = parts
                    if len(parts) >= 4:
                        self.n = int(parts[2])
                        self.m = int(parts[3])
                    continue

                clause = [int(x) for x in line.split() if int(x) != 0]
                if clause:
                    self.clauses.append(clause)

        except FileNotFoundError:
            print(f"[Error] 檔案不存在：{file_path}")
        except Exception as e:
            print(f"[Error] 發生錯誤：{e}")

    def show_info(self):
        print(f"檔案: {self.file_name}")
        print(f"變數數量 (n): {self.n}")
        print(f"子句數量 (m): {self.m}")
        print(f"前5個子句 (clauses): {self.clauses[:5]}")

    # =====================================
    # 找滿足解的主要 function
    # =====================================
    def find_satisfying_assignments(self, verbose=False):
        start_time = datetime.now()  # 開始計算時間
        self.F = self._initialize_obj(self.n, self.clauses)

        if verbose:
            print(f"[初始化資訊]")
            print(f"clauses = {self.F['clauses']}")
            print(f"pq = {self.F['pq']}")
            print(f"x = {self.F['x']}")
            print(f"touched_cnt = {self.F['touched_cnt']}")
            print(f"invalid = {self.F['invalid']}")
            print()

        shoot = set()
        ans = []
        self.dfs_counter = 0


        # 找 minimal (含多餘)
        # self._dfs(shoot, set(), ans, verbose) #H_1
        # self._dfs1(shoot, set(), ans, set(), verbose) #H_1^'
        # self._dfs1(shoot, set(), ans, set(), verbose) #H_1.1^' (此版只是優化部分結構)
        # self._dfs2(shoot, set(), ans, set(), verbose) #H_1^''
        # self._dfs3(shoot, set(), ans, set(), verbose) #H_1.1^''


        # 純找解 or 不可滿足
        # self._dfs(shoot, set(), ans, verbose) #H_1
        # self._dfs1(shoot, set(), ans, set(), verbose) #H_1^'
        # self._dfs1(shoot, set(), ans, set(), verbose) #H_1.1^' (此版只是優化部分結構)
        # self._dfs2(shoot, set(), ans, set(), verbose) #H_1^''
        self._dfs3(shoot, set(), ans, set(), verbose, True) #H_1.1^''


        # 計算總時間
        end_time = datetime.now()
        elapsed_time = end_time - start_time
        print(elapsed_time)
        formatted_time = str(elapsed_time).split('.')[0]  # 去除微秒部分
        # formatted_time = str(elapsed_time).split('.')[0]  # 去除微秒部分
        seconds = elapsed_time.total_seconds() #僅用秒

        print(f"\n[結果]")
        print("滿足解：")
        for x in ans :
            print(x)
        print(f"理論最差情況次數 : {2 ** self.n}")
        print(f"實際遞迴次數 : {self.dfs_counter}")


        # return {
        #     "satisfying_assignments": ans,  # 滿足解
        #     "dfs_counter": self.dfs_counter,  # dfs呼叫次數
        #     "elapsed_time": formatted_time,  # 花費的時間
        # }
        return {
            "satisfying_assignments": ans,  # 滿足解
            "dfs_counter": self.dfs_counter,  # dfs呼叫次數
            "elapsed_time": elapsed_time,  # 花費的時間
        }

    # =====================================
    # 初始化 F 結構
    # =====================================
    def _initialize_obj(self, n : int, clauses : list):
        pq = []
        x = [[] for _ in range(n + 1)]
        touched_cnt = [0] * (n + 1)
        invalid = {}
        
        for i, clause in enumerate(clauses):
            for var in clause:
                x[abs(var)].append(i)

            neg = sum(1 for var in clause if var < 0)
            
            # H_1 init
            # if neg == 0:
            #     # heapq.heappush(pq, (-3, i))
            #     # invalid[i] = -3

            #     # hueristic
            #     heapq.heappush(pq, (-1, i))
            #     invalid[i] = -1
            # else:
            #     heapq.heappush(pq, (1, i))
            #     invalid[i] = 1

            #H_1^' init
            weight = -(len(clause) - neg) + 3 * neg
            heapq.heappush(pq, (weight, i))
            invalid[i] = weight

        return {
            "pq": pq,
            "x": x,
            "touched_cnt": touched_cnt,
            "clauses": clauses,
            "invalid": invalid
        }

    def check_solution(self, sols : list, verbose=False):
        clauses = self.clauses
        error_details = []  # 用來記錄錯誤的子句

        for idx, sol in enumerate(sols):
            if verbose:
                print(f"[檢查第 {idx+1} 個解] {sol}")

            for cid, clause in enumerate(clauses):
                satisfied = False
                for lit in clause:
                    if (lit > 0 and lit in sol) or (lit < 0 and -lit not in sol):
                        satisfied = True
                        break

                if not satisfied:
                    error_details.append({"clause_id": cid, "clause": clause, "solution": sol})
                    if verbose:
                        print(f"❌ 子句 {cid} 不滿足！子句內容：{clause}，解為：{sol}")
                    return error_details  # 找到錯誤就停止檢查

        if verbose:
            print("✅ 所有解都正確！")
        return [] 
    
    #########################################################################################
    #########################################################################################
    #########################################################################################
    # =====================================
    #          權重計算 H_1
    # =====================================                                 ######      ######
    #    -3  -2  -1   0   1   2   3                                         ######      ######
    #    pc  pc  pc  pc  nc  ec  sc                                         ##################
    # pc = positive clause                                                  ##################  ###
    # nc = negtive clause                                                   ######      ######    #
    # ec = empty clause                                                     ######      ######  #####
    # sc = satisfied clause
    def _weight_counting(self, clause_id : int, ans : set): #H_1
        pos = 0
        untouched_pos = 0
        neg = 0
        c = self.F["clauses"][clause_id]
        base = -3 + len(c) # defect = k - # of literal in c

        for var in c:
            if var > 0:
                if var in ans: # 當前子句被消除
                    return 3
                if self.F["touched_cnt"][var] == 0: # 沒被碰到的權重加一
                    untouched_pos += 1
                pos += 1
            else:
                if -var not in ans: # 非 positive 的權重設為 1
                    return 1

        if pos == 0: # 沒有正變數也不是 non-monotone -> empty clause
            return 2

        return base - untouched_pos
        
    def _dfs(self, shoot : set, tmp_ans : set, ans : list,verbose=False): #H_1
        self.dfs_counter += 1

        if len(self.F["pq"]) == 0:
            ans.append(copy.deepcopy(tmp_ans))
            if verbose:
                print(f"[找到解] {tmp_ans}")
            return

        cur_weight, cur_id = heapq.heappop(self.F["pq"])

        if verbose:
            print(f"[展開子句] id = {cur_id}, 子句 = {self.F['clauses'][cur_id]}")

        if cur_weight == 1:
            ans.append(copy.deepcopy(tmp_ans))
            if verbose:
                print(f"[早停解] {tmp_ans}")
            return

        for var in self.F["clauses"][cur_id]:
            if var > 0:
                self.F["touched_cnt"][var] += 1

        origin_pq = copy.deepcopy(self.F["pq"])
        local_shoot = copy.deepcopy(shoot)

        cur_vars = {var for var in self.F["clauses"][cur_id] if var > 0}
        touched_ids = set()

        for var in cur_vars:
            if verbose:
                print(f"{var} {self.F["x"][var]}")
            touched_ids.update(self.F["x"][var])

        # 保存 touched_cnt 的原始值，以便後續恢復
        touched_cnt_backup = copy.deepcopy(self.F["touched_cnt"])

        for var in cur_vars:
            if var in local_shoot:
                continue

            tmp_ans.add(var)

            log = {}
            possible = True

            for cid in touched_ids:
                if var not in self.F["clauses"][cid] and -var not in self.F["clauses"][cid]:
                    continue

                new_weight = self._weight_counting(cid, tmp_ans)
                if verbose:
                    print(f"{cid} {new_weight}")
                if new_weight == 2: # ec
                    possible = False
                    break

                if self.F["invalid"][cid] != new_weight:
                    log[cid] = self.F["invalid"][cid]
                    self.F["invalid"][cid] = new_weight

                    if new_weight != 3:
                        heapq.heappush(self.F["pq"], (new_weight, cid))

            if verbose:
                print(f"嘗試 var = {var}，pq 變為：{self.F['pq']}")

            if possible:
                while self.F["pq"]:
                    tmp = heapq.heappop(self.F["pq"])
                    if tmp[0] == self.F["invalid"][tmp[1]]:
                        heapq.heappush(self.F["pq"], tmp)
                        break
                self._dfs(local_shoot, tmp_ans, ans, verbose)

            # 恢復 invalid table
            for cid, old_weight in log.items():
                self.F["invalid"][cid] = old_weight

            # 恢復 pq
            self.F["pq"] = copy.deepcopy(origin_pq)

            # 恢復 touched_cnt
            self.F["touched_cnt"] = copy.deepcopy(touched_cnt_backup)

            # 恢復 tmp_ans 和 local_shoot
            tmp_ans.remove(var)
            local_shoot.add(var)
    #########################################################################################
    #########################################################################################
    #########################################################################################




    #########################################################################################
    #########################################################################################
    #########################################################################################

                                                                                            ##
                                                                    ######      ######      ##
                                                                    ######      ######       ##
                                                                    ##################
                                                                    ##################
                                                                    ######      ######      ###
                                                                    ######      ######       ##  
                                                                    ######      ######     ######
    # ==============================================
    #          權重計算 H_1^'(c) = -4 * (len(c) - #-C - 2) * (len(c) - #-C - 3) - #A + 3 * (#-A + #-B)
    # ==============================================
    #   |  <-3  |  -3  -2  -1   0  |  >0  |  10  11 |
    #      uc     pc  pc  pc  pc     nc     ec  sc
    # uc = unit clause
    # pc = positive clause 
    # nc = negtive clause
    # ec = empty clause
    # sc = satisfied clause
    def _weight_counting1(self, clause_id : int, ans : set, forced : set, alpha = 4): #H_1^' 計算該clause_id 對應的 clause 在當前配置 (ans, forced) 下的權重
        c = self.F["clauses"][clause_id]
        l = len(c)
        A = 0 # 尚未觸碰 '正' 變數總量 (type A)
        _A = 0 # 尚未觸碰 '負' 變數總量 (type A)
        _B = 0 # 已觸碰但尚未固定的 '負' 變數總量 (type B)
        _C = 0 # 已觸碰且固定的 '負' 變數總量 (type C)
        AF = 0 # 尚未觸碰, 但因為存在 unit clause (-A) 使得 A 被強制為 0 的 '正' 變數總量 (type A)
        BF = 0 # 已觸碰尚未固定, 但因為存在 unit clause (-B) 使得 B 被強制為 0 的 '正' 變數總量 (type B)
        for var in c:
            if var > 0:
                if var in ans: # (C 類)
                    return 11
                if self.F["touched_cnt"][var] == 0: # 尚未觸碰 (A 類)
                    A += 1
                    if -var in forced: # A 被強迫設定為 0
                        AF += 1
                    continue
                if -var in forced: # 觸碰未固定 (B 類) # B 被強迫設定為 0
                    BF += 1
                
            else:
                if var in forced: # neg unit clause 
                    return 11
                if -var in ans: #已固定的 neg # (C 類)
                    _C += 1
                    continue
                if self.F["touched_cnt"][-var] == 0: # 尚未觸碰的 neg
                    _A += 1
                    continue
                if self.F["touched_cnt"][-var] != 0: # 已觸碰尚未固定的 neg
                    _B += 1

        if l == _C + AF + BF: # 三量總和為 l 代表 ec
            return 10
        Delta = l - _C
        return -alpha*(Delta - 2)*(Delta - 3) - A + AF + 3*(_A + _B)

    def _dfs1(self, shoot : set, tmp_ans : set, ans : list, forced : set,verbose=False): #H_1^'
        self.dfs_counter += 1

        if len(self.F["pq"]) == 0:
            ans.append(copy.deepcopy(tmp_ans))
            if verbose:
                print(f"[找到解] {tmp_ans}")
            return

        cur_weight, cur_id = heapq.heappop(self.F["pq"])

        if verbose:
            print(f"[展開子句] id = {cur_id}, 子句 = {self.F['clauses'][cur_id]}")

        if cur_weight > 0 and cur_weight < 10:
            ans.append(copy.deepcopy(tmp_ans))
            if verbose:
                print(f"[早停解] {tmp_ans}")
            return

        for var in self.F["clauses"][cur_id]:
            if var > 0:
                self.F["touched_cnt"][var] += 1

        origin_pq = copy.deepcopy(self.F["pq"])
        local_shoot = copy.deepcopy(shoot)
        local_forced = copy.deepcopy(forced)

        cur_vars = {var for var in self.F["clauses"][cur_id] if var > 0 and -var not in forced}
        touched_ids = set()

        # H1v2 原版沒過濾 就是會花比較多時間
        # for var in cur_vars:
        #     if verbose:
        #         print(f"{var} {self.F["x"][var]}")
        #     touched_ids.update(self.F["x"][var])

        # 保存 touched_cnt 的原始值，以便後續恢復
        touched_cnt_backup = copy.deepcopy(self.F["touched_cnt"])

        for var in cur_vars:
            if var in local_shoot:
                continue
            touched_ids = set()
            touched_ids.update(self.F["x"][var])
            tmp_ans.add(var)

            log = {}
            possible = True

            for cid in touched_ids:
                # if var not in self.F["clauses"][cid] and -var not in self.F["clauses"][cid]:
                #     continue

                new_weight = self._weight_counting1(cid, tmp_ans, local_forced)
                if verbose:
                    print(f"{cid} {new_weight}")
                if new_weight == 10: # ec
                    possible = False
                    break

                if self.F["invalid"][cid] != new_weight:
                    log[cid] = self.F["invalid"][cid]
                    self.F["invalid"][cid] = new_weight

                    # if new_weight != 3:
                    # if new_weight <= 10:
                    if new_weight <= 0: # uc pc nc
                        heapq.heappush(self.F["pq"], (new_weight, cid))

            if verbose:
                print(f"嘗試 var = {var}，pq 變為：{self.F['pq']}")

            setting = [] #紀錄 unit clause 內正變數
            while self.F["pq"] and possible:
                tmp = heapq.heappop(self.F["pq"])
                if tmp[0] == self.F["invalid"][tmp[1]]:
                    if tmp[0] < -3: # unit clause 
                        for v in self.F["clauses"][tmp[1]]:
                            if -v not in tmp_ans:
                                if v in local_shoot: # unit clause 在先前的分支已經探索過了
                                    possible = False
                                    break
                                if v > 0: # pos unit clause
                                    touched_ids2 = set()
                                    touched_ids2.update(self.F["x"][v])
                                    tmp_ans.add(v)
                                    setting.append(v)
                                    for cid in touched_ids2:
                                        new_weight = self._weight_counting1(cid, tmp_ans, local_forced)

                                        if new_weight == 10: # ec
                                            possible = False
                                            break

                                        if self.F["invalid"][cid] != new_weight:
                                            if cid not in log:
                                                log[cid] = self.F["invalid"][cid]
                                            self.F["invalid"][cid] = new_weight

                                            # if new_weight != 3:
                                            # if new_weight <= 10:
                                            if new_weight <= 0: # uc pc nc
                                                heapq.heappush(self.F["pq"], (new_weight, cid))
                                    if not possible:
                                        break
                                else: # neg unit clause
                                    touched_ids2 = set()
                                    touched_ids2.update(self.F["x"][-v])
                                    # local_shoot.add(-v)
                                    local_forced.add(v)
                                    for cid in touched_ids2:
                                        new_weight = self._weight_counting1(cid, tmp_ans, local_forced)

                                        if new_weight == 10: # ec
                                            possible = False
                                            break

                                        if self.F["invalid"][cid] != new_weight:
                                            if cid not in log:
                                                log[cid] = self.F["invalid"][cid]
                                            self.F["invalid"][cid] = new_weight

                                            # if new_weight != 3:
                                            # if new_weight <= 10:
                                            if new_weight <= 0:
                                                heapq.heappush(self.F["pq"], (new_weight, cid))
                                    if not possible:
                                        break
                        if not possible:
                            break
                    else:
                        heapq.heappush(self.F["pq"], tmp)
                        break

            if possible:
                self._dfs1(local_shoot, tmp_ans, ans, local_forced, verbose)

            # 恢復 pos unit clause 時 tmp_ans 放入的正變數
            for v in setting:
                tmp_ans.remove(v)

            # 恢復 local_forced
            local_forced = copy.deepcopy(forced)

            # 恢復 invalid table
            for cid, old_weight in log.items():
                self.F["invalid"][cid] = old_weight

            # 恢復 pq
            self.F["pq"] = copy.deepcopy(origin_pq)

            # 恢復 touched_cnt
            self.F["touched_cnt"] = copy.deepcopy(touched_cnt_backup)

            # 恢復 tmp_ans 和 local_shoot
            tmp_ans.remove(var)
            local_shoot.add(var)

#########################################################################################
#########################################################################################
#########################################################################################


#########################################################################################
#########################################################################################
#########################################################################################


                                                                                            ##   ##
                                                                    ######      ######       ##   ## 
                                                                    ######      ######        ##   ##
                                                                    ##################
                                                                    ##################
                                                                    ######      ######      ###
                                                                    ######      ######       ##  
                                                                    ######      ######     ######

    def process(self, var : set, setTo1 : set, setTo0 : set) -> list:
        cids = set()
        s = dict()
        # all = set()
        for x in var: # 搜集所有 x 存在的子句, 並初始化 S_x = {}, S_y = {}, S_z = {}
            cids.update(self.F["x"][x])
            s[x] = set()

        for cid in cids: # 判斷所有內涵 x -x y -y z -z 是否還存在, 存在則更改 S_x
            c = self.F["clauses"][cid] #list
            ig = False # ignore
            C = set()
            for l in c:
                if l in setTo1 or l in setTo0:
                    ig = True
                    break
                C.add(l)
            if ig : # un-exist
                continue

            for v in var:
                if v in C :
                    continue
                for nv in ((C - {-v}) & var):
                    s[v].update({abs(nv)})

        S = []
        for [key, SET] in s.items():
            S.append((len(SET), key))
        S.sort()

        sorted = []
        for (v, key) in S:
            sorted.append(key)
        return sorted

    def _dfs2(self, shoot : set, tmp_ans : set, ans : list, forced : set,verbose=False): #H_1^''
        self.dfs_counter += 1

        if len(self.F["pq"]) == 0:
            ans.append(copy.deepcopy(tmp_ans))
            if verbose:
                print(f"[找到解] {tmp_ans}")
            return

        cur_weight, cur_id = heapq.heappop(self.F["pq"])

        if verbose:
            print(f"[展開子句] id = {cur_id}, 子句 = {self.F['clauses'][cur_id]}")

        if cur_weight > 0 and cur_weight < 10:
            ans.append(copy.deepcopy(tmp_ans))
            if verbose:
                print(f"[早停解] {tmp_ans}")
            return

        for var in self.F["clauses"][cur_id]:
            if var > 0:
                self.F["touched_cnt"][var] += 1

        origin_pq = copy.deepcopy(self.F["pq"])
        local_shoot = copy.deepcopy(shoot)
        local_forced = copy.deepcopy(forced)

        cur_vars = {var for var in self.F["clauses"][cur_id] if var > 0 and -var not in forced}

        # 保存 touched_cnt 的原始值，以便後續恢復
        touched_cnt_backup = copy.deepcopy(self.F["touched_cnt"])

        # 給出變數展開順序 sorted : list
        sorted = self.process(cur_vars, tmp_ans, forced)

        for var in sorted:
            if var in local_shoot:
                continue
            touched_ids = set()
            touched_ids.update(self.F["x"][var])
            tmp_ans.add(var)

            log = {}
            possible = True

            for cid in touched_ids:
                new_weight = self._weight_counting1(cid, tmp_ans, local_forced)
                if verbose:
                    print(f"{cid} {new_weight}")

                if new_weight == 10: # ec
                    possible = False
                    break

                if self.F["invalid"][cid] != new_weight:
                    log[cid] = self.F["invalid"][cid]
                    self.F["invalid"][cid] = new_weight

                    if new_weight <= 0: # pc uc
                        heapq.heappush(self.F["pq"], (new_weight, cid))

            if verbose:
                print(f"嘗試 var = {var}，pq 變為：{self.F['pq']}")

            setting = [] #紀錄 unit clause 內正變數
            while self.F["pq"] and possible:
                tmp = heapq.heappop(self.F["pq"])
                if tmp[0] == self.F["invalid"][tmp[1]]:
                    if tmp[0] < -3: # unit clause 
                        for v in self.F["clauses"][tmp[1]]:
                            if -v not in tmp_ans:
                                if v in local_shoot: # unit clause 在先前的分支已經探索過了
                                    possible = False
                                    break
                                if v > 0: # pos unit clause
                                    touched_ids2 = set()
                                    touched_ids2.update(self.F["x"][v])
                                    tmp_ans.add(v)
                                    setting.append(v)
                                    for cid in touched_ids2:
                                        new_weight = self._weight_counting1(cid, tmp_ans, local_forced)

                                        if new_weight == 10: # ec
                                            possible = False
                                            break

                                        if self.F["invalid"][cid] != new_weight:
                                            if cid not in log:
                                                log[cid] = self.F["invalid"][cid]
                                            self.F["invalid"][cid] = new_weight

                                            if new_weight <= 0: # uc pc
                                                heapq.heappush(self.F["pq"], (new_weight, cid))
                                    if not possible:
                                        break
                                else: # neg unit clause
                                    touched_ids2 = set()
                                    touched_ids2.update(self.F["x"][-v])
                                    local_forced.add(v)
                                    for cid in touched_ids2:
                                        new_weight = self._weight_counting1(cid, tmp_ans, local_forced)

                                        if new_weight == 10: # ec
                                            possible = False
                                            break

                                        if self.F["invalid"][cid] != new_weight:
                                            if cid not in log:
                                                log[cid] = self.F["invalid"][cid]
                                            self.F["invalid"][cid] = new_weight

                                            if new_weight <= 0:
                                                heapq.heappush(self.F["pq"], (new_weight, cid))
                                    if not possible:
                                        break
                        if not possible:
                            break
                    else:
                        heapq.heappush(self.F["pq"], tmp)
                        break

            if possible:
                self._dfs2(local_shoot, tmp_ans, ans, local_forced, verbose)

            # 恢復 pos unit clause 時 tmp_ans 放入的正變數
            for v in setting:
                tmp_ans.remove(v)

            # 恢復 local_forced
            local_forced = copy.deepcopy(forced)

            # 恢復 invalid table
            for cid, old_weight in log.items():
                self.F["invalid"][cid] = old_weight

            # 恢復 pq
            self.F["pq"] = copy.deepcopy(origin_pq)

            # 恢復 touched_cnt
            self.F["touched_cnt"] = copy.deepcopy(touched_cnt_backup)

            # 恢復 tmp_ans 和 local_shoot
            tmp_ans.remove(var)
            local_shoot.add(var)

#########################################################################################
#########################################################################################
#########################################################################################

#########################################################################################
#########################################################################################
#########################################################################################


                                                                                            ##   ##
                                                                    ######      ######       ##   ## 
                                                                    ######      ######        ##   ##
                                                                    ##################
                                                                    ##################
                                                                    ######      ######      ###      ###
                                                                    ######      ######       ##       ##
                                                                    ######      ######     ###### # ###### 

    # ==============================================
    #          權重計算 H_1^''(c) = -4 * (len(c) - #-C - 2) * (len(c) - #-C - 3) - #A + 3 * (#-A + #-B)
    # ==============================================
    #   <-9  |  -9 <= val < -8  |  -8 <= val < -3  |  -3  -2  -1   0  |  >0  |  10  11 |
    #   upc           uc                 wnpc          pc  pc  pc  pc     nc     ec  sc
    # upc = useless positive clause
    # wupc = positive clause with some useless variable
    # uc = unit clause
    # pc = positive clause 
    # nc = negtive clause
    # ec = empty clause
    # sc = satisfied clause
    def bonus(self, c : list, shoot : set, setTo0 : set) -> int:
        bonus = 2

        isCand = False
        for l in c:
            if l < 0 :
                continue
            if -l in setTo0 :
                continue
            if l not in shoot :
                bonus -= 1
            else :
                isCand = True
        if not isCand :
            return 0
        if bonus == 2 :
            return - 100
        # print(c, bonus)
        return - bonus * 4

    def adjust(self, shoot : set, cids : set, setTo1 : set, setTo0 : set):
        for cid in cids:
            weight = self._weight_counting1(cid, setTo1, setTo0, 6)
            if weight > 0 : # nc ec sc
                continue
            # pc
            c = self.F["clauses"][cid] #list
            
            new_weight = weight + self.bonus(c, shoot, setTo0)
            # print(c, new_weight)
            self.F["invalid"][cid] = new_weight
            if new_weight <= 0:
                heapq.heappush(self.F["pq"], (new_weight, cid))
        
        return
    
    def _dfs3(self, shoot : set, tmp_ans : set, ans : list, forced : set,verbose=False, findOneOrNoSols = False): #H_1.1^''
        self.dfs_counter += 1
        if findOneOrNoSols and len(ans) != 0:
            return
        
        if len(self.F["pq"]) == 0:
            ans.append(copy.deepcopy(tmp_ans))
            if verbose:
                print(f"[找到解] {tmp_ans}")
            return

        cur_weight, cur_id = heapq.heappop(self.F["pq"])

        if verbose:
            print(f"[展開子句] id = {cur_id}, 子句 = {self.F['clauses'][cur_id]}")

        if cur_weight > 0 and cur_weight < 10:
            ans.append(copy.deepcopy(tmp_ans))
            if verbose:
                print(f"[早停解] {tmp_ans}")
                print(cur_weight, cur_id)
            return

        for var in self.F["clauses"][cur_id]:
            if var > 0:
                self.F["touched_cnt"][var] += 1

        origin_pq = copy.deepcopy(self.F["pq"])
        local_shoot = copy.deepcopy(shoot)
        local_forced = copy.deepcopy(forced)
        invalid_backup = copy.deepcopy(self.F["invalid"])

        cur_vars = {var for var in self.F["clauses"][cur_id] if var > 0 and -var not in forced}

        # 保存 touched_cnt 的原始值，以便後續恢復
        touched_cnt_backup = copy.deepcopy(self.F["touched_cnt"])

        # 給出變數展開順序 sorted : list
        sorted = self.process(cur_vars, tmp_ans, forced)

        for var in sorted:
            if var in local_shoot:
                continue
            # print("*",var)
            touched_ids = set()
            touched_ids.update(self.F["x"][var])
            tmp_ans.add(var)

            log = {}
            possible = True

            for cid in touched_ids:
                weight = self._weight_counting1(cid, tmp_ans, local_forced, 6)

                if verbose:
                    print(f"{cid} {weight}")

                if weight == 10: # ec
                    possible = False
                    break
                
                bonus = 0
                if weight <= 0 :
                    bonus = self.bonus(self.F["clauses"][cid], local_shoot ,local_forced)

                # print(self.F["clauses"][cid], "", weight, " ", bonus)
                if bonus == -100 :
                    possible = False
                    # print("啟動")
                    break
                
                new_weight = weight + bonus
                if self.F["invalid"][cid] != new_weight :
                    log[cid] = self.F["invalid"][cid]
                    self.F["invalid"][cid] = new_weight

                    if new_weight <= 0: # pc uc
                        heapq.heappush(self.F["pq"], (new_weight, cid))

            if verbose:
                print(f"嘗試 var = {var}，pq 變為：{self.F['pq']}")

            setting = [] #紀錄 unit clause 內正變數
            while self.F["pq"] and possible:
                tmp = heapq.heappop(self.F["pq"])
                if tmp[0] == self.F["invalid"][tmp[1]]:
                    if tmp[0] < -8: # unit clause 
                        for v in self.F["clauses"][tmp[1]]:
                            if -v not in tmp_ans:
                                if v in local_shoot: # unit clause 在先前的分支已經探索過了
                                    possible = False
                                    break
                                if v > 0: # pos unit clause
                                    touched_ids2 = set()
                                    touched_ids2.update(self.F["x"][v])
                                    tmp_ans.add(v)
                                    setting.append(v)
                                    for cid in touched_ids2:
                                        weight = self._weight_counting1(cid, tmp_ans, local_forced, 6)

                                        if weight == 10: # ec
                                            possible = False
                                            break

                                        bonus = 0
                                        if weight <= 0 :
                                            bonus = self.bonus(self.F["clauses"][cid], local_shoot ,local_forced)

                                        if bonus == -100 :
                                            possible = False
                                            # print("啟動")
                                            break
                                        
                                        new_weight = weight + bonus
                                        if self.F["invalid"][cid] != new_weight :
                                            if cid not in log:
                                                log[cid] = self.F["invalid"][cid]
                                            self.F["invalid"][cid] = new_weight

                                            if new_weight <= 0: # uc wupc pc
                                                heapq.heappush(self.F["pq"], (new_weight, cid))
                                    if not possible:
                                        break
                                else: # neg unit clause
                                    touched_ids2 = set()
                                    touched_ids2.update(self.F["x"][-v])
                                    local_forced.add(v)
                                    for cid in touched_ids2:
                                        weight = self._weight_counting1(cid, tmp_ans, local_forced, 6)

                                        if weight == 10: # ec
                                            possible = False
                                            break

                                        bonus = 0
                                        if weight <= 0 :
                                            bonus = self.bonus(self.F["clauses"][cid], local_shoot ,local_forced)

                                        if bonus == -100 :
                                            possible = False
                                            # print("啟動")
                                            break
                                        
                                        new_weight = weight + bonus
                                        if self.F["invalid"][cid] != new_weight :
                                            if cid not in log:
                                                log[cid] = self.F["invalid"][cid]
                                            self.F["invalid"][cid] = new_weight

                                            if new_weight <= 0: # uc wupc pc
                                                heapq.heappush(self.F["pq"], (new_weight, cid))
                                    if not possible:
                                        break
                        if not possible:
                            break
                    else:
                        heapq.heappush(self.F["pq"], tmp)
                        break

            if possible:
                self._dfs3(local_shoot, tmp_ans, ans, local_forced, verbose, findOneOrNoSols)

            #find one and return immediately
            if findOneOrNoSols and len(ans) != 0 :
                return
            
            # 恢復 pos unit clause 時 tmp_ans 放入的正變數
            for v in setting:
                tmp_ans.remove(v)

            # 恢復 local_forced
            local_forced = copy.deepcopy(forced)

            # 恢復 invalid table
            for cid, old_weight in log.items():
                self.F["invalid"][cid] = old_weight

            # 恢復 pq
            self.F["pq"] = copy.deepcopy(origin_pq)

            # 恢復 touched_cnt
            self.F["touched_cnt"] = copy.deepcopy(touched_cnt_backup)

            # 恢復 tmp_ans 和 local_shoot
            tmp_ans.remove(var)
            local_shoot.add(var)

            # 調整 pq
            # self.adjust(local_shoot, touched_ids, tmp_ans, local_forced)
            # print("TSESESE")

        self.F["invalid"] = invalid_backup
        # print("回朔")
    #########################################################################################
    #########################################################################################
    #########################################################################################

