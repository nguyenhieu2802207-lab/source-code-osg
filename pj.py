class Process:
    def __init__(self, pid, arrival_time, burst_time):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        
        self.remaining_time = burst_time
        self.completion_time = 0
        self.queue_level = 0       # 0: Q0 (RR q=2), 1: Q1 (RR q=4), 2: Q2 (FCFS)
        self.time_in_quantum = 0   # Thời gian đã chạy trong Time Quantum hiện tại

def simulate_mlfq(processes):
    Q0 = [] # Hàng đợi mức 0: Round Robin, q = 2
    Q1 = [] # Hàng đợi mức 1: Round Robin, q = 4
    Q2 = [] # Hàng đợi mức 2: First-Come, First-Served (FCFS)
    
    time = 0
    completed = 0
    n = len(processes)
    
    # Danh sách các tiến trình chưa đến, sắp xếp theo thời gian đến (Arrival Time)
    unarrived = sorted(processes, key=lambda x: x.arrival_time)
    current_process = None
    log = []
    
    while completed < n:
        # 1. Nhận các tiến trình mới đến tại mốc thời gian 'time'
        while unarrived and unarrived[0].arrival_time <= time:
            p = unarrived.pop(0)
            Q0.append(p)
            log.append(f"[Time {time:02d}] {p.pid} đến, được đưa vào Q0")
            
        # 2. Xử lý Trưng dụng CPU (Preemption)
        # Nếu có tiến trình ưu tiên cao hơn đến trong khi tiến trình ưu tiên thấp đang chạy
        if current_process:
            if current_process.queue_level > 0 and len(Q0) > 0:
                log.append(f"[Time {time:02d}] {current_process.pid} bị ngắt bởi tiến trình ở Q0. Đưa {current_process.pid} về lại Q{current_process.queue_level}")
                if current_process.queue_level == 1:
                    Q1.append(current_process)
                elif current_process.queue_level == 2:
                    Q2.insert(0, current_process) # Giữ vị trí đầu để duy trì tính chất FCFS
                current_process = None
                
            elif current_process.queue_level > 1 and len(Q1) > 0:
                log.append(f"[Time {time:02d}] {current_process.pid} bị ngắt bởi tiến trình ở Q1. Đưa {current_process.pid} về lại đầu Q2")
                Q2.insert(0, current_process)
                current_process = None

        # 3. Chọn tiến trình mới để chạy nếu CPU đang rảnh
        if current_process is None:
            if len(Q0) > 0:
                current_process = Q0.pop(0)
            elif len(Q1) > 0:
                current_process = Q1.pop(0)
            elif len(Q2) > 0:
                current_process = Q2.pop(0)
                
        # 4. Thực thi CPU 1 đơn vị thời gian (1 tick)
        if current_process:
            current_process.remaining_time -= 1
            current_process.time_in_quantum += 1
            time += 1
            
            # Kiểm tra tiến trình đã chạy xong chưa
            if current_process.remaining_time == 0:
                current_process.completion_time = time
                log.append(f"[Time {time:02d}] {current_process.pid} HOÀN THÀNH công việc")
                completed += 1
                current_process = None
                continue # Bỏ qua bước kiểm tra quantum bên dưới
                
            # Kiểm tra hết Time Quantum và giáng cấp (Demotion)
            if current_process.queue_level == 0 and current_process.time_in_quantum == 2:
                current_process.queue_level = 1
                current_process.time_in_quantum = 0 # Reset biến đếm cho Q1
                Q1.append(current_process)
                log.append(f"[Time {time:02d}] {current_process.pid} hết q=2 ở Q0, giáng cấp xuống Q1")
                current_process = None
                
            elif current_process.queue_level == 1 and current_process.time_in_quantum == 4:
                current_process.queue_level = 2
                current_process.time_in_quantum = 0 # FCFS không xài quantum
                Q2.append(current_process)
                log.append(f"[Time {time:02d}] {current_process.pid} hết q=4 ở Q1, giáng cấp xuống Q2 (FCFS)")
                current_process = None
        else:
            # CPU rảnh rỗi chờ tiến trình đến
            time += 1
            
    return log

# ================= KỊCH BẢN CHẠY THỬ =================
if __name__ == '__main__':
    # Tạo 3 tiến trình mẫu
    process_list = [
        Process("P1", arrival_time=0, burst_time=14),
        Process("P2", arrival_time=1, burst_time=10),
        Process("P3", arrival_time=3, burst_time=8)
    ]
    
    print("=== KẾT QUẢ MÔ PHỎNG ĐIỀU PHỐI MLFQ ===")
    logs = simulate_mlfq(process_list)
    for line in logs:
        print(line)