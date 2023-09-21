class SJF:

    def processData(self, no_of_processes):
        process_data = []
        for i in range(no_of_processes):
            temporary = {}
            temporary['Process_ID'] = int(input("Enter Process ID: "))
            temporary['Arrival_Time'] = int(input(f"Enter Arrival Time for Process {temporary['Process_ID']}: "))
            temporary['Burst_Time'] = int(input(f"Enter Burst Time for Process {temporary['Process_ID']}: "))
            temporary['Completed'] = False
            process_data.append(temporary)
        self.schedulingProcess(process_data)  # Use 'self' to call class methods

    def schedulingProcess(self, process_data):
        start_times = []  # Store start times for each process
        s_time = 0
        process_data.sort(key=lambda x: x['Arrival_Time'])
        for i in range(len(process_data)):
            ready_queue = []
            temp = {}
            normal_queue = []

            for j in range(len(process_data)):
                if (process_data[j]['Arrival_Time'] <= s_time) and (not process_data[j]['Completed']):
                    temp['Process_ID'] = process_data[j]['Process_ID']
                    temp['Arrival_Time'] = process_data[j]['Arrival_Time']
                    temp['Burst_Time'] = process_data[j]['Burst_Time']
                    ready_queue.append(temp.copy())
                elif not process_data[j]['Completed']:
                    temp['Process_ID'] = process_data[j]['Process_ID']
                    temp['Arrival_Time'] = process_data[j]['Arrival_Time']
                    temp['Burst_Time'] = process_data[j]['Burst_Time']
                    normal_queue.append(temp.copy())

            if len(ready_queue) != 0:
                ready_queue.sort(key=lambda x: x['Burst_Time'])
                # Calculate Start Time as the maximum of Arrival Time and completion time of the previous process
                start_time = max(s_time, ready_queue[0]['Arrival_Time'])
                start_times.append(start_time)
                s_time = start_time + ready_queue[0]['Burst_Time']
                completion_time = s_time
                for k in range(len(process_data)):
                    if process_data[k]['Process_ID'] == ready_queue[0]['Process_ID']:
                        process_data[k]['Completed'] = True
                        process_data[k]['Completion_Time'] = completion_time
                        # Calculate Response Time when a process is added to the ready queue
                        process_data[k]['Response_Time'] = start_time - process_data[k]['Arrival_Time']

            elif len(normal_queue) != 0:
                if s_time < normal_queue[0]['Arrival_Time']:
                    s_time = normal_queue[0]['Arrival_Time']
                # Calculate Start Time as the maximum of Arrival Time and completion time of the previous process
                start_time = max(s_time, normal_queue[0]['Arrival_Time'])
                start_times.append(start_time)
                normal_queue.sort(key=lambda x: x['Burst_Time'])  # Sort the normal queue by burst time
                s_time = start_time + normal_queue[0]['Burst_Time']
                completion_time = s_time
                for k in range(len(process_data)):
                    if process_data[k]['Process_ID'] == normal_queue[0]['Process_ID']:
                        process_data[k]['Completed'] = True
                        process_data[k]['Completion_Time'] = completion_time
                        # Calculate Response Time when a process is added to the ready queue
                        process_data[k]['Response_Time'] = start_time - process_data[k]['Arrival_Time']

        t_time = self.calculateTurnaroundTime(process_data, start_times)  # Pass start_times to calculateTurnaroundTime
        w_time = self.calculateWaitingTime(process_data)  # Use 'self' to call class methods
        utilization_time = self.calculateUtilizationTime(process_data)  # Calculate Utilization Time
        self.printData(process_data, t_time, w_time, start_times, utilization_time)  # Pass start_times and utilization_time to printData
        self.print_gantt_chart(process_data, start_times)  # Print the Gantt Chart

    def calculateTurnaroundTime(self, process_data, start_times):
        total_turnaround_time = 0
        for i in range(len(process_data)):
            turnaround_time = process_data[i]['Completion_Time'] - process_data[i]['Arrival_Time']
            total_turnaround_time = total_turnaround_time + turnaround_time
            process_data[i]['Turnaround_Time'] = turnaround_time
        average_turnaround_time = total_turnaround_time / len(process_data)
        return average_turnaround_time

    def calculateWaitingTime(self, process_data):
        total_waiting_time = 0
        for i in range(len(process_data)):
            waiting_time = process_data[i]['Turnaround_Time'] - process_data[i]['Burst_Time']
            total_waiting_time = total_waiting_time + waiting_time
            process_data[i]['Waiting_Time'] = waiting_time
        average_waiting_time = total_waiting_time / len(process_data)
        return average_waiting_time

    def calculateUtilizationTime(self, process_data):
        total_utilization_time = 0
        for i in range(len(process_data)):
            utilization_time = process_data[i]['Burst_Time'] / process_data[i]['Turnaround_Time']
            total_utilization_time += utilization_time
            process_data[i]['Utilization_Time'] = utilization_time
        average_utilization_time = total_utilization_time / len(process_data)
        return average_utilization_time

    def printData(self, process_data, average_turnaround_time, average_waiting_time, start_times, utilization_time):
        n = len(process_data)
        process_states = [""] * n

        # Sort process_data by Completion Time for correct order in the table
        process_data.sort(key=lambda x: x['Completion_Time'])

        # Define the column headers
        headers = ["Processes", "Arrival time", "Burst time", "Wait time", "Response time", "Turnaround time", "Completion time", "Utilization Time"]

        # Print the table headers
        print("\nTable Of Shortest Job First Scheduling Algorithm:\n")
        print("-----------------------------------------------------------------------------------------------------")
        print("|Processes|ArrivalTime|BurstTime|WaitTime|ResponseTime|TurnaroundTime|CompletionTime|UtilizationTime|")
        print("-----------------------------------------------------------------------------------------------------")

        for i in range(n):
            # Calculate the start time and response time
            start_time = start_times[process_data[i]['Process_ID'] - 1] if process_states[i] != "waiting" else "-"
            response_time = process_data[i]['Response_Time']

            print("|   P{:d}    |     {:d}     |   {:2d}    |   {:2d}   |     {:2d}     |      {:2d}      |      {:2d}      |      {:.2f}     |".format(
                process_data[i]['Process_ID'], process_data[i]['Arrival_Time'], process_data[i]['Burst_Time'], process_data[i]['Waiting_Time'], response_time, process_data[i]['Turnaround_Time'], process_data[i]['Completion_Time'], process_data[i]['Utilization_Time']))
        print("-----------------------------------------------------------------------------------------------------")

        # Print the average turnaround time, average waiting time, average utilization time, and average response time
        print(f'Average Turnaround Time: {average_turnaround_time}')
        print(f'Average Waiting Time: {average_waiting_time}')
        print(f'Average Utilization Time: {utilization_time}')

        # Calculate and print the average response time
        total_response_time = sum(process_data[i]['Response_Time'] for i in range(n))
        average_response_time = total_response_time / n
        print(f'Average Response Time: {average_response_time}')

    def print_gantt_chart(self, process_data, start_times):
        print("\nGantt Chart:")
        print("-" * (sum([process['Burst_Time'] + 3 for process in process_data]) + 3))
        for i, start_time in enumerate(start_times):
            process_id = process_data[i]['Process_ID']
            burst_time = process_data[i]['Burst_Time']
            print("| P{}{} ".format(process_id, " " * (burst_time - len(str(process_id)))), end="")
        print("|")
        print("-" * (sum([process['Burst_Time'] + 3 for process in process_data]) + 3))
        start = 0
        for start_time in start_times:
            print("{:d}      ".format(start_time), end="")
            start = start_time + process_data[i]['Burst_Time']
        print("{:d}".format(start))


# if __name__ == "__main__":
#     print("\nImplementation of Shortest Job First Scheduling Algorithm!\n")
#     no_of_processes = int(input("Enter the number of processes: "))
#     sjf = SJF()  # Create an instance of the SJF class
#     sjf.processData(no_of_processes)
#     print("\nThis is all about Shortest Job First Scheduling Algorithm!\n")
