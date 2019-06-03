from multiprocessing import Queue, Process, cpu_count
from typing import Callable, List, Any
from functools import partial


ProcList = List[Process]


class ProcPool:
    def __init__(self, worker: Callable[..., Any], tasks: List, proc_num: int = cpu_count() - 1):
        self._queue: Queue = Queue()
        self._worker = partial(lambda x, queue: queue.put(worker(x)), queue=self._queue)
        self._proc_num = proc_num
        self._tasks = tasks
        self._process_pool: ProcList = [Process(target=self._worker, args=(individual,)) for individual in self._tasks]

    def __call__(self) -> List:
        done_list: List = []
        for begin in range(0, len(self._process_pool), self._proc_num):
            step = self._proc_num if begin + self._proc_num < len(self._process_pool) else len(self._process_pool) - begin
            sub_pool: ProcList = self._process_pool[begin:begin + step]

            for proc in sub_pool:
                proc.start()
                queue_len = self._queue.qsize()
                if not self._queue.empty():
                    for _ in range(queue_len):
                        done_list.append(self._queue.get())

            for proc in sub_pool:
                proc.join()
                queue_len = self._queue.qsize()
                if not self._queue.empty():
                    for _ in range(queue_len):
                        done_list.append(self._queue.get())
        return done_list
