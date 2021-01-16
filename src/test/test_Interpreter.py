# This file is licensed under the MIT license.
# See license for more details: https://github.com/leonard112/OctaneScript/blob/main/README.md

import pytest
import mock
import builtins
import time
import threading
import _thread
from core.Line import Line
from core.Stack import Stack
from Interpreter import Interpreter
from Reserved import reserved


# References for timout class
# https://stackoverflow.com/questions/22454898/how-to-force-timeout-functions-in-python-windows-platform
# https://creativecommons.org/licenses/by-sa/2.5/
class timeout():
  def __init__(self, time):
    self.time= time
    self.exit=False

  def __enter__(self):
    threading.Thread(target=self.callme).start()

  def callme(self):
    time.sleep(self.time)
    if self.exit==False:
       _thread.interrupt_main()
  def __exit__(self, a, b, c):
       self.exit=True


@pytest.fixture(scope='function')
def interpreter(request):
    return Interpreter("test")


def test_valid_print_functions_successful(interpreter):
    for i in range(0, 54, 1):
        assert_success(interpreter, [reserved[i] + " 'test'"])
def test_valid_set_successful(interpreter):
    assert_success(interpreter, ["set x to 'value'"])
def test_exit_successful(interpreter):
    assert_graceful_exit(interpreter, ["exit"])
def test_comment_and_blanks_ignored(interpreter):
    assert_success(interpreter, ["", "    ", "# This is a comment"])
def test_invalid_functions_fail(interpreter):
    assert_error(interpreter, ["invalid"])
    assert_error(interpreter, ["exitProgram"])
    assert_error(interpreter, ["setVal"])


# CONDITIONALS

# IF ONLY 

def test_if_true_functional(interpreter):
    script = """
set x to "Unchanged"
if [true]
    set x to "Changed"
end
""".splitlines(True)
    interpreter.run_script(script, None)
    assert interpreter.variables["x"] == 'Changed'
def test_if_true_functional_REPL(interpreter, capfd):
    script = """
set x to "Unchanged"
if [true]
    set x to "Changed"
end
print x
""".splitlines(True)
    assert_code_works_in_REPL(capfd, script, 'Changed\n')


def test_if_false_functional(interpreter):
    script = """
set x to "Unchanged"
if [false]
    set x to "Changed"
end
""".splitlines(True)
    interpreter.run_script(script, None)
    assert interpreter.variables["x"] == 'Unchanged'
def test_if_false_functional_REPL(interpreter, capfd):
    script = """
set x to "Unchanged"
if [false]
    set x to "Changed"
end
print x
""".splitlines(True)
    assert_code_works_in_REPL(capfd, script, 'Unchanged\n')


# IF AND ELSE

def test_runs_else_when_if_false(interpreter):
    script = """
set x to "Unchanged"
if [false]
    set x to "Changed by if"
else
    set x to "Changed by else"
end
""".splitlines(True)
    interpreter.run_script(script, None)
    assert interpreter.variables["x"] == 'Changed by else'
def test_runs_else_when_if_false_REPL(interpreter, capfd):
    script = """
set x to "Unchanged"
if [false]
    set x to "Changed by if"
else
    set x to "Changed by else"
end
print x
""".splitlines(True)
    assert_code_works_in_REPL(capfd, script, 'Changed by else\n')


def test_does_not_runs_else_when_if_true(interpreter):
    script = """
set x to "Unchanged"
if [true]
    set x to "Changed by if"
else
    set x to "Changed by else"
end
""".splitlines(True)
    interpreter.run_script(script, None)
    assert interpreter.variables["x"] == 'Changed by if'
def test_does_not_runs_else_when_if_true_REPL(interpreter, capfd):
    script = """
set x to "Unchanged"
if [true]
    set x to "Changed by if"
else
    set x to "Changed by else"
end
print x
""".splitlines(True)
    assert_code_works_in_REPL(capfd, script, 'Changed by if\n')


# IF AND ELSEIF

def test_runs_true_elseif_when_if_false(interpreter):
    script = """
set x to "Unchanged"
if [false]
    set x to "Changed by if"
elseIf [true]
    set x to "Changed by elseIf"
end
""".splitlines(True)
    interpreter.run_script(script, None)
    assert interpreter.variables["x"] == 'Changed by elseIf'
def test_runs_true_elseif_when_if_false_REPL(interpreter, capfd):
    script = """
set x to "Unchanged"
if [false]
    set x to "Changed by if"
elseIf [true]
    set x to "Changed by elseIf"
end
print x
""".splitlines(True)
    assert_code_works_in_REPL(capfd, script, 'Changed by elseIf\n')


def test_skips_elseif_when_if_true(interpreter):
    script = """
set x to "Unchanged"
if [true]
    set x to "Changed by if"
elseIf [false]
    set x to "Changed by elseIf"
end
""".splitlines(True)
    interpreter.run_script(script, None)
    assert interpreter.variables["x"] == 'Changed by if'
def test_skips_elseif__when_if_true_REPL(interpreter, capfd):
    script = """
set x to "Unchanged"
if [true]
    set x to "Changed by if"
elseIf [false]
    set x to "Changed by elseIf"
end
print x
""".splitlines(True)
    assert_code_works_in_REPL(capfd, script, 'Changed by if\n')


# IF, ELSEIF, AND ELSE

def test_runs_true_elseif_when_if_false_and_not_else(interpreter):
    script = """
set x to "Unchanged"
if [false]
    set x to "Changed by if"
elseIf [true]
    set x to "Changed by elseIf"
else
    set x to "Changed by else"
end
""".splitlines(True)
    interpreter.run_script(script, None)
    assert interpreter.variables["x"] == 'Changed by elseIf'
def test_runs_true_elseif_when_if_false_and_not_else_REPL(interpreter, capfd):
    script = """
set x to "Unchanged"
if [false]
    set x to "Changed by if"
elseIf [true]
    set x to "Changed by elseIf"
else
    set x to "Changed by else"
end
print x
""".splitlines(True)
    assert_code_works_in_REPL(capfd, script, 'Changed by elseIf\n')


def test_runs_else_when_if_and_elseif_false(interpreter):
    script = """
set x to "Unchanged"
if [false]
    set x to "Changed by if"
elseIf [false]
    set x to "Changed by elseIf"
else
    set x to "Changed by else"
end
""".splitlines(True)
    interpreter.run_script(script, None)
    assert interpreter.variables["x"] == 'Changed by else'
def test_runs_else_when_if_and_elseif_false_REPL(interpreter, capfd):
    script = """
set x to "Unchanged"
if [false]
    set x to "Changed by if"
elseIf [false]
    set x to "Changed by elseIf"
else
    set x to "Changed by else"
end
print x
""".splitlines(True)
    assert_code_works_in_REPL(capfd, script, 'Changed by else\n')


def test_skips_elseif_and_else_when_if_true(interpreter):
    script = """
set x to "Unchanged"
if [true]
    set x to "Changed by if"
elseIf [false]
    set x to "Changed by elseIf"
else
    set x to "Changed by else"
end
""".splitlines(True)
    interpreter.run_script(script, None)
    assert interpreter.variables["x"] == 'Changed by if'
def test_skips_elseif_and_else_when_if_true_REPL(interpreter, capfd):
    script = """
set x to "Unchanged"
if [true]
    set x to "Changed by if"
elseIf [false]
    set x to "Changed by elseIf"
else
    set x to "Changed by else"
end
print x
""".splitlines(True)
    assert_code_works_in_REPL(capfd, script, 'Changed by if\n')


# LONG IF CHAIN

def test_long_if_chain_works_properly(interpreter):
    script = """
set x to "Unchanged"
if [false]
    set x to "Changed by if"
elseIf [false]
    set x to "Changed by first elseIf"
elseIf [false]
    set x to "Changed by second elseIf"
elseIf [true]
    set x to "Changed by fourth elseIf"
elseIf [true]
    set x to "Changed by fourth elseIf"
else
    set x to "Changed by else"
end
""".splitlines(True)
    interpreter.run_script(script, None)
    assert interpreter.variables["x"] == 'Changed by fourth elseIf'
def test_long_if_chain_works_properly_REPL(interpreter, capfd):
    script = """
set x to "Unchanged"
if [false]
    set x to "Changed by if"
elseIf [false]
    set x to "Changed by first elseIf"
elseIf [false]
    set x to "Changed by second elseIf"
elseIf [true]
    set x to "Changed by fourth elseIf"
elseIf [true]
    set x to "Changed by fourth elseIf"
else
    set x to "Changed by else"
end
print x
""".splitlines(True)
    assert_code_works_in_REPL(capfd, script, 'Changed by fourth elseIf\n')


# MULTIPLE LINES IN CONDITIONAL TO EXECUTE

def test_conditional_can_handle_multiple_lines_of_code(interpreter):
    script = """
set x to "Unchanged"
set y to "Unchanged"
set z to "Unchanged"
if [true]
    set x to "x"
    set y to "y"
    set z to "z"
else
    set x to "This should not execute"
end
""".splitlines(True)
    interpreter.run_script(script, None)
    assert interpreter.variables["x"] == 'x'
    assert interpreter.variables["y"] == 'y'
    assert interpreter.variables["z"] == 'z'
def test_conditional_can_handle_multiple_lines_of_code_REPL(interpreter, capfd):
    script = """
set x to "Unchanged"
set y to "Unchanged"
set z to "Unchanged"
if [true]
    set x to "x"
    set y to "y"
    set z to "z"
else
    set x to "This should not execute"
end
print x
print y
print z
""".splitlines(True)
    assert_code_works_in_REPL(capfd, script, 'x\ny\nz\n')


# NESTING

def test_nested_conditionals_work_properly(interpreter):
    script = """
set x to "Unchanged"
if [true]
    set x to "Changed by initial if"
    if [true]
        set x to "Changed by first nested if"
    end
    if [false]
        set x to "Nothing should be changed here"
    else
        if [true]
            set x to "Changed by if in else on second if chain"
        elseIf [true]
            set x to "should not execute because if was true"
        end
    end
end
""".splitlines(True)
    interpreter.run_script(script, None)
    assert interpreter.variables["x"] == 'Changed by if in else on second if chain'
def test_nested_conditionals_work_properly_REPL(interpreter, capfd):
    script = """
set x to "Unchanged"
if [true]
    set x to "Changed by initial if"
    if [true]
        set x to "Changed by first nested if"
    end
    if [false]
        set x to "Nothing should be changed here"
    else
        if [true]
            set x to "Changed by if in else on second if chain"
        elseIf [true]
            set x to "should not execute because if was true"
        end
    end
end
print x
""".splitlines(True)
    assert_code_works_in_REPL(capfd, script, 'Changed by if in else on second if chain\n')


def test_when_all_ifs_are_false_no_else_or_elseif_will_execute(interpreter):
    script = """
set x to "Unchanged"
if [false]
    set x to "Changed by first if.
    if [false]
        set x to "Changed by second if."
    else
        set x to "Changed by else."
    end
end
""".splitlines(True)
    interpreter.run_script(script, None)
    assert interpreter.variables["x"] == 'Unchanged'
def test_when_all_ifs_are_false_no_else_or_elseif_will_execute_REPL(interpreter, capfd):
    script = """
set x to "Unchanged"
if [false]
    set x to "Changed by first if.
    if [false]
        set x to "Changed by second if."
    else
        set x to "Changed by else."
    end
end
print x
""".splitlines(True)
    assert_code_works_in_REPL(capfd, script, 'Unchanged\n')


# SPACING

def test_valid_code_works_regardless_of_extra_lines(interpreter):
    script = """


set x to "Unchanged"

if [true]

    if [false]

        set x to "This line should be skiped"

    elseIf [false]
        set x to  "This line should be skiped"


    else


        set x to "Changed"


    end



end


""".splitlines(True)
    interpreter.run_script(script, None)
    assert interpreter.variables["x"] == 'Changed'
def test_valid_code_works_regardless_of_extra_lines_REPL(interpreter, capfd):
    script = """


set x to "Unchanged"

if [true]

    if [false]

        set x to "This line should be skiped"

    elseIf [false]
        set x to  "This line should be skiped"


    else


        set x to "Changed"


    end



end


print x
""".splitlines(True)
    assert_code_works_in_REPL(capfd, script, 'Changed\n')


def test_valid_code_works_regardless_of_spacing(interpreter):
    script = """
set x to "Unchanged"

    if [true]
if [false]
        set x to "This line should be skiped"
            elseIf [false]
        set x to  "This line should be skiped"
else
                set x to "Changed"
end
            end
""".splitlines(True)
    interpreter.run_script(script, None)
    assert interpreter.variables["x"] == 'Changed'
def test_valid_code_works_regardless_of_spacing_REPL(interpreter, capfd):
    script = """
set x to "Unchanged"

    if [true]
if [false]
        set x to "This line should be skiped"
            elseIf [false]
        set x to  "This line should be skiped"
else
                set x to "Changed"
end
            end
print x
""".splitlines(True)
    assert_code_works_in_REPL(capfd, script, 'Changed\n')


# BAD CODE THAT DOES NOT GET EXECUTED WILL NOT CAUSE ERROR

def test_bad_code_that_does_not_execute_will_not_fail(interpreter):
    script = """
set x to "Unchanged"
if [false]
    set x to "Changed by if"
elseif [false]
    invalid
else
    set x to "All bad code has been skiped due to if being false"
end
""".splitlines(True)
    interpreter.run_script(script, None)
    assert interpreter.variables["x"] == 'All bad code has been skiped due to if being false'
def test_bad_code_that_does_not_execute_will_not_fail_REPL(interpreter, capfd):
    script = """
set x to "Unchanged"
if [false]
    set x to "Changed by if"
elseif [false]
    invalid
else
    set x to "All bad code has been skiped due to if being false"
end
print x
""".splitlines(True)
    assert_code_works_in_REPL(capfd, script, 'All bad code has been skiped due to if being false\n')


# EXTRA OR MISSING END

def test_missing_end_fails(interpreter):
    script = """
if [true]
    print "This will cause error"
if [true]
    print "This code should not be reached"
end
""".splitlines(True)
    assert_error(interpreter, script)
def test_missing_end_fails_REPL(interpreter, capfd):
    script = """
if [true]
    print "This will cause error"
if [true]
    print "This code should not be reached"
end
""".splitlines(True)
    assert_code_fails_in_REPL(capfd, script)


def test_extra_end_fails(interpreter):
    script = """
if [true]
    print "first if will execute"
end
if [true]
    print "second if will execute"
end
end
print "Error will occur before this is reached."
""".splitlines(True)
    assert_error(interpreter, script)
def test_extra_end_fails_REPL(interpreter, capfd):
    script = """
if [true]
    print "first if will execute"
end
if [true]
    print "second if will execute"
end
end
print "Error will occur before this is reached."
""".splitlines(True)
    assert_code_fails_in_REPL(capfd, script)


# DANGLING ELSE AND ELSEIF

def test_dangling_else_fails(interpreter):
    script = """
else
    print "This should fail"
end
print "Error will occur before this is reached."
""".splitlines(True)
    assert_error(interpreter, script)
def test_dangling_else_fails_REPL(interpreter, capfd):
    script = """
else
    print "This should fail"
end
print "Error will occur before this is reached."
""".splitlines(True)
    assert_code_fails_in_REPL(capfd, script)


def test_dangling_elseif_fails(interpreter):
    script = """
elseIf [true]
    print "This should fail"
else
    print "This should fail"
end
print "Error will occur before this is reached."
""".splitlines(True)
    assert_error(interpreter, script)
def test_dangling_elseif_fails_REPL(interpreter, capfd):
    script = """
elseIf [true]
    print "This should fail"
else
    print "This should fail"
end
print "Error will occur before this is reached."
""".splitlines(True)
    assert_code_fails_in_REPL(capfd, script)


def test_nested_dangling_else_fails(interpreter):
    script = """
if [true]
    else
        print "This should fail"
    end
end
print "Error will occur before this is reached."
""".splitlines(True)
    assert_error(interpreter, script)
def test_nested_dangling_else_fails_REPL(interpreter, capfd):
    script = """
if [true]
    else
        print "This should fail"
    end
end
print "Error will occur before this is reached."
""".splitlines(True)
    assert_code_fails_in_REPL(capfd, script)


def test_nested_dangling_elseif_fails(interpreter):
    script = """
if [true]
    elseIf [true]
        print "This should fail"
    else
        print "This should fail"
    end
end
    print "Error will occur before this is reached."
""".splitlines(True)
    assert_error(interpreter, script)
def test_nested_dangling_elseif_fails_REPL(interpreter, capfd):
    script = """
if [true]
    elseIf [true]
        print "This should fail"
    else
        print "This should fail"
    end
end
print "Error will occur before this is reached."
""".splitlines(True)
    assert_code_fails_in_REPL(capfd, script)


# CALL STACK

def test_stack_trace_valid_for_single_line(interpreter):
    script = """print "err""".splitlines(True)
    assert_stack_trace(interpreter, script, [1])
def test_stack_trace_valid_for_single_line_REPL(interpreter, capfd):
    script = """print "err""".splitlines(True)
    assert_stack_trace_REPL(capfd, script, [1])


def test_stack_trace_valid_for_multi_line(interpreter):
    script = """
# This is a comment
print "test"
print "err
print "This will not be executed"
""".splitlines(True)
    assert_stack_trace(interpreter, script, [4])
def test_stack_trace_valid_for_multi_line_REPL(interpreter, capfd):
    script = """
# This is a comment
print "test"
print "err
print "This will not be executed"
""".splitlines(True)
    assert_stack_trace_REPL(capfd, script, [4])


def test_stack_trace_valid_for_nesting(interpreter):
    script = """
print "Outside of if"
if [true]
    print "In first if"
    if [false]
        print "This wont print"
    else
        if [false]
            print "This won't print"
        elseIf [true]
            print "err
        else
            print "This wont print"
        end
    end
end
print "This won't print"
""".splitlines(True)
    assert_stack_trace(interpreter, script, [11, 10, 7, 3])
def test_stack_trace_valid_for_nesting_REPL(interpreter, capfd):
    script = """
print "Outside of if"
if [true]
    print "In first if"
    if [false]
        print "This wont print"
    else
        if [false]
            print "This won't print"
        elseIf [true]
            print "err
        else
            print "This wont print"
        end
    end
end
print "This won't print"
""".splitlines(True)
    assert_stack_trace_REPL(capfd, script, [11, 10, 7, 3])


def test_stack_trace_after_completion_of_if(interpreter):
    script = """
print "Outside of if"
if [true]
    print "Inside if"
end
if [true]
    print "err
end
""".splitlines(True)
    assert_stack_trace(interpreter, script, [7, 6])
def test_stack_trace_after_completion_of_if_REPL(interpreter, capfd):
    script = """
print "Outside of if"
if [true]
    print "Inside if"
end
if [true]
    print "err
end
""".splitlines(True)
    assert_stack_trace_REPL(capfd, script, [7, 6])


def assert_stack_trace(interpreter, script, line_numbers):
    try:
        interpreter.run_script(script, None)
    except:
        for line_number in line_numbers:
            assert interpreter.call_stack.pop().line_number + 1 == line_number

def assert_stack_trace_REPL(capfd, script, line_numbers):
    interpreter, console, failure = mock_REPL(capfd, script)
    for line_number in line_numbers:
        assert interpreter.call_stack.pop().line_number + 1 == line_number

def assert_code_works_in_REPL(capfd, script, expected_output):
        interpreter, console, failure = mock_REPL(capfd, script)
        assert console == expected_output

def assert_code_fails_in_REPL(capfd, script):
    try:
        with timeout(2):
            interpreter, console, failure = mock_REPL(capfd, script)
            if failure == True:
                raise Exception
    except:
        return
    pytest.fail()

def mock_REPL(capfd, script):
    interpreter = Interpreter("REPL")
    def input_side_effect():
        nonlocal script
        if (len(script) == 0):
            return "exit"
        line = script[0]
        script = script[1:]
        return line
    with mock.patch.object(builtins, 'input', lambda _: input_side_effect()):
        failure = False
        try:
            interpreter.run()
        except:
            failure = True
        console, err = capfd.readouterr()
        return interpreter, console, failure

def assert_error(interpreter, script):
    with pytest.raises(SystemExit) as error:
            interpreter.run_script(script, None)
    assert error.type == SystemExit
    assert error.value.code == 1

def assert_graceful_exit(interpreter, script):
    with pytest.raises(SystemExit) as error:
            interpreter.run_script(script, None)
    assert error.type == SystemExit
    assert error.value.code == 0

def assert_success(interpreter, script):
    try:
        interpreter.run_script(script, None)
    except:
        pytest.fail()
