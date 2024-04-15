#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# File          : main
# Author        : Sun YiFan-Movoid
# Time          : 2024/4/3 1:49
# Description   : 
"""
import ctypes
import threading
import time
from typing import Union, Dict

from movoid_function import Function


class Thread:
    def __init__(self, target, name: str, args: Union[list, tuple] = None, kwargs: dict = None, loop: int = 1, init=None, end=None, *, start: bool = True, daemon: bool = False, thread_dict: dict):
        self._target = Function(target, args, kwargs)
        self._name: str = str(name)
        self._loop: int = int(loop)
        self._init = Function(init)
        self._end = Function(end)
        self._daemon: bool = bool(daemon)
        self._thread_dict: dict = thread_dict

        self._ident = None
        self._start: bool = False
        self._pause: bool = False
        self._stop: bool = False

        if self._loop <= 0:
            decorator = self.thread_target_while
        else:
            decorator = self.thread_target_for
        self._thread_dict[name] = self
        self._thread: threading.Thread = threading.Thread(target=decorator, name=self._name, daemon=self._daemon)
        if start:
            self.start()

    @property
    def ident(self):
        return self._ident

    def start(self):
        if not self._start:
            self._thread.start()

    def pause(self, pause_bool: bool = True):
        self._pause = bool(pause_bool)

    def resume(self):
        self._pause = False

    def stop(self):
        self._stop = True

    def thread_target_for(self):
        self._ident = threading.get_ident()
        try:
            self._start = True
            try:
                self._init()
                for _i in range(self._loop):
                    try:
                        self._target()
                    except ThreadLoopStopSignal:
                        pass
                    finally:
                        while self._pause:
                            time.sleep(0.1)
                        if self._stop:
                            break
            except ThreadStopSignal:
                pass
            finally:
                self._end()
        except ThreadTerminateSignal:
            pass
        finally:
            if self._name in self._thread_dict:
                self._thread_dict.pop(self._name)

    def thread_target_while(self):
        self._ident = threading.get_ident()
        try:
            self._start = True
            try:
                self._init()
                while self._stop:
                    try:
                        self._target()
                    except ThreadLoopStopSignal:
                        pass
                    finally:
                        while self._pause:
                            time.sleep(0.1)
            except ThreadStopSignal:
                pass
            finally:
                self._end()
        except ThreadTerminateSignal:
            pass
        finally:
            if self._name in self._thread_dict:
                self._thread_dict.pop(self._name)

    def force_terminate(self):
        self._send_exception(ThreadTerminateSignal)

    def force_stop(self):
        self._send_exception(ThreadStopSignal)

    def force_loop_stop(self):
        self._send_exception(ThreadLoopStopSignal)

    def _send_exception(self, exception):
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(self._ident), ctypes.py_object(exception))
        if res == 0:
            raise ValueError("invalid thread id")
        elif res != 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(self._ident, None)
            raise SystemError("PyThreadState_SetAsyncExc failed")


class ThreadLib:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._lock = threading.Lock()
        self._local = threading.local()
        self._threads: Dict[str, Thread] = {}

    def __dict__(self):
        return self._threads

    def __getitem__(self, item) -> Thread:
        return self._threads[item]

    @property
    def lock(self):
        return self._lock

    @property
    def local(self):
        return self._local

    def keys(self):
        return self._threads.keys()

    def values(self):
        return self._threads.values()

    def items(self):
        return self._threads.items()

    def new(self, target, args: Union[list, tuple] = None, kwargs: dict = None, name: str = None, *, start: bool = True, daemon: bool = False):
        real_name = self._thread_name(name)
        Thread(target=target, name=real_name, args=args, kwargs=kwargs, start=start, daemon=daemon, thread_dict=self._threads)

    def start(self, name: Union[str, None] = None):
        if name:
            if name in self._threads:
                self._threads[name].start()
            else:
                raise KeyError(f'{name} is not a thread')
        else:
            for i, v in self._threads.items():
                v.start()

    def _thread_name(self, name: str):
        if name:
            root_name = name
            name_index = 1
            temp_name = name
        else:
            root_name = 'Thread'
            name_index = len(self._threads) + 1
            temp_name = f'{root_name}-{name_index}'
        while temp_name in self._threads:
            name_index += 1
            temp_name = f'{root_name}-{name_index}'
        return temp_name


class ThreadTerminateSignal(Exception):
    pass


class ThreadStopSignal(ThreadTerminateSignal):
    pass


class ThreadLoopStopSignal(ThreadStopSignal):
    pass
