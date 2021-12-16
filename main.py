import copy
import operator


class node(object):
    def __init__(self, start, end, length, state=1, ID=0):
        self.start = start
        self.end = end
        self.length = length
        self.state = state  # state为1：内存未分配
        self.Id = ID  # ID为0是未分配，其余为任务编号


# 展示所有区块信息
def show_memory(list):
    print("内存区块使用状况".center(40, '*'))
    print("分配状态    分区号    起始地址   终止地址  分区大小")
    for i in range(0, len(list)):
        p = list[i]
        if p.state == 1:
            print("%s%s%s%8.d%10.d%8.d" % ('空闲', "          ", p.Id, p.start, p.end, p.length))
        else:
            print("%s%s%s%8.d%10.d%8.d" % ('已分配', "        ", p.Id, p.start, p.end, p.length))



# 回收区块
def free_k(taskID, list_FREE):
    target = -1
    for i in range(0, len(list_FREE)):
        p = list_FREE[i]
        if p.Id == taskID:
            p.state = 1
            p.Id = 0
            target = i
            print("已回收:", taskID, '  start:', p.start, "  end:", p.end, "  length:", p.length)
            break
    if target == -1:
        print('不存在的作业号!请检查后重新输入。')
        return
    # 向前合并
    if target - 1 > 0:
        if list_FREE[target - 1].state == 1:
            a = node(list_FREE[target - 1].start, list_FREE[target].end,
                     list_FREE[target - 1].length + list_FREE[target].length, 1, 0)
            del list_FREE[target - 1]
            del list_FREE[target - 1]
            list_FREE.insert(target - 1, a)
            target = target - 1
    # 向后合并
    if target + 1 < len(list_FREE):
        if list_FREE[target + 1].state == 1:
            a = node(list_FREE[target].start, list_FREE[target + 1].end,
                     list_FREE[target].length + list_FREE[target + 1].length, 1, 0)
            del list_FREE[target]
            del list_FREE[target]
            list_FREE.insert(target, a)






# 选择适应算法
def changeFa(task, list_FF, fn):
    stay = []
    if len(task) == 0:
        print("请输入进程任务")
        return task
    for i in range(len(task)):
        res = fn(task[i][0], task[i][1], list_FF)
        if res == 0:
            stay.append(task[i])
            # print(task[i])
    show_memory(list_FF)
    return stay


# 1.最先适应法
def FF(taskID, Tasklength, list_FF):
    for i in range(0, len(list_FF)):
        p = list_FF[i]
        if p.state == 1 and p.length > Tasklength:
            node_bk = node(p.start + Tasklength, p.end, p.length - Tasklength, 1, 0)
            a = node(p.start, p.start + Tasklength - 1, Tasklength, state=0, ID=taskID)
            del list_FF[i]
            list_FF.insert(i, node_bk)
            list_FF.insert(i, a)
            return 1
        if p.state == 1 and p.length == Tasklength:
            p.Id = taskID
            p.state = 0
            return 1
    print(f"内存空间不足，进程{taskID}分配失败")
    return 0


# 2.最佳适应法
def BF(taskID, Tasklength, list_BF):
    q = copy.copy(list_BF)
    cmpfun = operator.attrgetter('length')  # 获得固定属性的可调用对象
    q.sort(key=cmpfun, reverse=False)
    for i in range(len(q)):
        print(q[i].length, q[i].state)
    adr_1 = -1
    adr_2 = -1
    for i in range(0, len(q)):
        p = q[i]
        if p.state == 1 and p.length > Tasklength:
            adr_1 = p.start
            break
        elif p.state == 1 and p.length == Tasklength:
            adr_2 = p.start
            break
    print(adr_1, adr_2)
    if adr_1 == -1 and adr_2 == -1:
        print("内存空间不足")
        return
    divide(taskID, Tasklength, list_BF, adr_1, adr_2)


# 3.最坏适应法
def WF(taskID, Tasklength, list_WF):
    q = copy.copy(list_WF)
    cmpfun = operator.attrgetter('length')  # 获得固定属性的可调用对象
    q.sort(key=cmpfun, reverse=True)
    adr_1 = -1
    adr_2 = -1
    for i in range(0, len(q)):
        p = q[i]
        if p.state == 1 and p.length > Tasklength:
            adr_1 = p.start
            break
        elif p.state == 1 and p.length == Tasklength:
            adr_2 = p.start
            break
    # print(adr_1, adr_2)
    if adr_1 == -1 and adr_2 == -1:
        print("内存空间不足")
        return
    divide(taskID, Tasklength, list_WF, adr_1, adr_2)


# 分配算法
def divide(Id, Length, List, adr_1, adr_2):
    for i in range(0, len(List)):
        p = List[i]
        if p.start == adr_1:
            node_bk = node(p.start + Length, p.end, p.length - Length, 1, 0)
            a = node(p.start, p.start + Length - 1, Length, state=0, ID=Id)
            del List[i]
            List.insert(i, node_bk)
            List.insert(i, a)
            return 1
        elif p.start == adr_2:
            p.Id = Id
            p.state = 0
            return 1
    print(f"内存空间不足，进程{Id}分配失败")
    return 0


# 展示进程情况
def show_task(task):
    print("进程号\t进程内存")
    for i in range(len(task)):
        print(f'{task[i][0]}\t\t{task[i][1]}')


# 菜单1
def menu1(task, b):
    task = task
    while True:
        try:
            pd_num2 = int(input("\n菜单1:\n 1、输入进程\n 2、分配内存\n 3、回收分区\n 4、展示分区表\n 5、等待进程表\n 0、退出\n 请输入你的操作:\n "))
            if pd_num2 == 1:
                print("1.输入进程".center(30, '*'))
                i = int(input("请输入进程的个数:"))
                for count in range(i):
                    task_id = int(input(f'请输入第{count + 1}个进程的编号:'))
                    task_size = int(input(f'请输入第{count + 1}个进程所需要的内存大小:'))
                    task.append([task_id, task_size])
            elif pd_num2 == 2:
                print("2.内存分区".center(30, '*'))
                task = menu2(task, b)
            elif pd_num2 == 3:
                print("3.回收分区".center(30, '*'))
                show_memory(b)
                free_task_id = int(input("请输入要回收进程的编号:"))
                free_k(free_task_id, b)
                free_k(0, b)
                show_memory(b)
            elif pd_num2 == 4:
                print("4.展示分区表".center(30, '*'))
                show_memory(b)
            elif pd_num2 == 5:
                print("5.等待进程表".center(30, '*'))
                show_task(task)
            elif pd_num2 == 0:
                print("感谢你的使用，欢迎下次再见！")
                break
            else:
                print("请输入正确的选项！")
        except:
            print("请输入正确的选项")


def menu2(tasks, lists):
    tasks = tasks
    while True:
        try:
            pd_num2 = int(input("\n菜单2：\n 1、最先适应法\n 2、最佳适应法\n 3、最坏适应法\n 0、退出程序\n请输入你的操作:\n "))
            if pd_num2 == 1:
                tasks = changeFa(tasks, lists, FF)
            elif pd_num2 == 2:
                tasks = changeFa(tasks, lists, BF)
            elif pd_num2 == 3:
                tasks = changeFa(tasks, lists, WF)
            elif pd_num2 == 0:
                return tasks
            else:
                print("请输入正确的选项1！")
                continue
        except:
            print("请输入正确的选项")


if __name__ == "__main__":
    memory_size = int(input("请输入您想要的初始分区的大小:\n"))
    while memory_size < 0:
        memory_size = int(input('分区不能为负数，请重新输入你想要的初始分区的大小:\n'))
    a = node(0, memory_size - 1, memory_size, state=1, ID=0)
    b = [a]
    task = []
    i = int(input("请输入进程的个数:"))
    for count in range(i):
        task_id = int(input(f'请输入第{count + 1}个进程的编号:'))
        task_size = int(input(f'请输入第{count + 1}个进程所需要的内存大小:'))
        task.append([task_id, task_size])
    menu1(task, b)
