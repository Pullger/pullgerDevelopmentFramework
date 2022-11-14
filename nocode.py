import uuid as uuid_class
import json
import inspect
import importlib
import os


def executor(self, file):
    path_script = os.path.dirname(file) + '/' + ''.join(os.path.basename(file).split('.')[0:-1]) + ".json"

    executing_code = ExecutingCode(path_script)
    next_command = None
    status = ""
    status_executed = ""

    end = False
    while end is False:
        if next_command is None or next_command == "n auto" or next_command == "ec auto":
            print(f"{status}" +
                  f"{'' if status_executed == '' else ' > '}" +
                  f"{status_executed}" +
                  f"{'' if status == '' else ' >> '}" +
                  f"COMMAND:", end="")
            if next_command is not None:
                print("")

        if next_command is None:
            command = input()
        else:
            command = next_command
            next_command = None
        # -------------------------------------------------------------
        if command == "auto":
            next_command = 'l auto'
        elif command == "ac":
            print("New code", end=":")
            executing_code.append_code(input())
        elif command == "rl":
            # Reload all libraries
            for cur_library in executing_code.get_all_libraries():
                try:
                    exec(f"importlib.reload({cur_library.element_name})")
                except BaseException as e:
                    print(f"Error on reload library : [{str(cur_library.element_name)}]: {str(e)}")
                    break
        elif command == "al":
            print("APPEND LIBRARY: FROM", end=">>")
            from_path = input()
            if from_path.strip() != "" and from_path is not None:
                print("APPEND LIBRARY: ELEMENT", end=">>")
                element_name = input()
                if element_name.strip() != "" and element_name is not None:
                    executing_code.append_library(from_path=from_path, element_name=element_name)
        elif command == "n" or command == "n auto":
            result_operation, description = executing_code.next_line()
            if result_operation is True:
                code, description = executing_code.get_code_string()
                status = str(code)
                status_executed = 'NOT EXECUTED'
                if command == "n auto":
                    next_command = 'ec auto'
            else:
                if command != "n auto":
                    print("Error: ", description)
        elif command == "gcs":
            print(executing_code.get_code_string())
        elif command == "el" or command == "el auto":
            executed = None
            for cur_library_code in executing_code.get_libraries_string():
                try:
                    exec(cur_library_code)
                except BaseException as e:
                    print(f"Error on exec library load: [{str(cur_library_code)}]: {str(e)}")
                    executed = False
                    break
                else:
                    executed = True
            if command == "el auto" and executed is True:
                next_command = 'ec auto'
            print("Libraries executed")
        elif command == 'ec' or command == 'ecr' or command == 'ecn' or command == 'ec auto':
            # ec - execute code (on current position)
            # ecr - execute code with reload (on current position)
            # ecn - execute code and go to next (on current position
            # ec auto - execute code with automate mode (on current position)

            if status_executed != 'EXECUTED' or command == 'ecr':
                code, description = executing_code.get_code_string()
                if code is not None:
                    try:
                        exec(str(code))
                    except BaseException as e:
                        print(f"Error: {str(e)}")
                        status_executed = 'ERROR'
                    else:
                        executing_code.set_executed()
                        status_executed = 'EXECUTED'
                        if command == 'ecn' or command == 'ec auto':
                            next_command = 'n auto'
                else:
                    if command == 'ec auto':
                        next_command = 'n auto'
            else:
                print("Code is already executed")
        elif command == "exit":
            print("Finalising.")
            end = True
        elif command == "l" or command == "l auto":
            # l = load code from json
            # l auto = load code on automate mode
            executing_code.load_json()
            if command == "l auto":
                next_command = "el auto"
        elif command == "s":
            executing_code.save_json()


class ObjectEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, "to_json"):
            return self.default(obj.to_json())
        elif isinstance(obj, dict):
            return obj
        elif isinstance(obj, uuid_class.UUID):
            return str(obj)
        elif isinstance(obj, object) or hasattr(obj, "__dict__"):
            d = dict(
                (key, value)
                for key, value in inspect.getmembers(obj)
                if not key.startswith("_")
                and not inspect.isabstract(value)
                and not inspect.isbuiltin(value)
                and not inspect.isfunction(value)
                and not inspect.isgenerator(value)
                and not inspect.isgeneratorfunction(value)
                and not inspect.ismethod(value)
                and not inspect.ismethoddescriptor(value)
                and not inspect.isroutine(value)
            )
            return self.default(d)
        return obj


class CodeSequence:
    __slots__ = ('list', '_current_line_id')

    class _CodeString:
        __slots__ = ('uuid', 'code_string')

        def __init__(self, code_string: str = None, uuid: str = None):
            if uuid is None or uuid == "":
                self.uuid = str(uuid_class.uuid4())
            else:
                self.uuid = uuid
            self.code_string = code_string

        def __str__(self):
            return self.code_string

    def __init__(self):
        self._current_line_id = None
        self.list = []

    def add_code(self, code_string: str = None, uuid: str = None):
        self.list.append(self._CodeString(uuid=uuid, code_string=code_string))

    def clear_code(self):
        self.list = []

    def next(self):
        response = False
        if self._current_line_id is None:
            if len(self.list) != 0:
                self._current_line_id = 0
                response = True
        else:
            if len(self.list) > (self._current_line_id + 1):
                self._current_line_id += 1
                response = True
            else:
                response = None
        return response

    def is_initialed(self):
        if self._current_line_id is None:
            return False
        else:
            return True

    def get_code(self):
        if self.is_initialed():
            return self.list[self._current_line_id], ""
        else:
            return None, "Code sequence not initialised"


class LibrariesUses:
    __slots__ = ('list', )

    class _Library:
        __slots__ = ('from_path', 'element_name', 'as_name', 'uuid')

        def __init__(self, uuid=None, from_path=None, element_name=None, as_name=None):
            if uuid is None or uuid == "":
                self.uuid = uuid_class.uuid4()
            else:
                self.uuid = uuid
            self.from_path = from_path
            self.element_name = element_name
            self.as_name = as_name

    def __init__(self):
        self.list = []

    def append_library(self, *args, **kwargs):
        self.list.append(self._Library(**kwargs))

    def clear_library(self):
        self.list = []

    def get_all_libraries(self):
        return self.list

    def get_all_code(self):
        libraries_code = []
        for cur_library in self.list:
            code = ""
            if cur_library.from_path is not None:
                code = code + f"from {cur_library.from_path}"
            if cur_library.element_name is not None:
                code = code + ("" if code == "" else " ")
                code = code + f"import {cur_library.element_name}"
            if cur_library.as_name is not None:
                code = code + f" as {cur_library.as_name}"

            libraries_code.append(code)
        return libraries_code


class ExecutingCode:
    __slots__ = ('code_sequence', 'libraries', '_line_executed', '_project_location')

    def __init__(self, path_script):
        self.code_sequence = CodeSequence()
        self.libraries = LibrariesUses()
        self._line_executed = None
        self._project_location = path_script

    def append_code(self, code_string: str = None, uuid: str = None, *args, **kwargs):
        self.code_sequence.add_code(uuid=uuid, code_string=code_string)

    def clear_code(self):
        self.code_sequence.clear_code()

    def append_library(self, *args, **kwargs):
        self.libraries.append_library(**kwargs)

    def clear_library(self):
        self.libraries.clear_library()

    def next_line(self):
        if self._line_executed is True or self._line_executed is None:
            result_next_operation = self.code_sequence.next()
            if result_next_operation is True:
                self._line_executed = False
                return True, ""
            elif result_next_operation is False:
                return False, "Operation sequence is empy."
            elif result_next_operation is None:
                return False, "No next element"
        else:
            return False, "Current code not executed"

    def set_executed(self):
        self._line_executed = True

    def get_code_string(self):
        code, description = self.code_sequence.get_code()
        return code, description

    def get_libraries_string(self):
        return self.libraries.get_all_code()

    def get_all_libraries(self):
        return self.libraries.get_all_libraries()

    def load_json(self):
        with open(self._project_location) as json_file:
            self.clear_library()
            self.clear_code()
            data = json.load(json_file)
            for cur_library in data["libraries"]["list"]:
                self.append_library(**cur_library)
            for cur_code_sequence in data["code_sequence"]["list"]:
                self.append_code(**cur_code_sequence)

    def save_json(self):
        with open(self._project_location, 'w', encoding='utf-8') as json_file:
            json_file.write(json.dumps(self, cls=ObjectEncoder, indent=2, sort_keys=True))
