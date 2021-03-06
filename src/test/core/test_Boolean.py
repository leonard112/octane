# This file is licensed under the MIT license.
# See license for more details: https://github.com/leonard112/OctaneScript/blob/main/README.md

import pytest
from core.Line import Line
from core.Stack import Stack
from core.Boolean import Boolean
from Interpreter import reserved

line = Line("TEST", 0, "test")
test_stack = Stack()
test_stack.push(line)

# BRACKETS
def test_no_brackets_fails():
    assert_error(Boolean('true', test_stack, {}))
def test_no_right_bracket_fails():
    assert_error(Boolean('[true', test_stack, {}))
def test_no_left_bracket_fails():
    assert_error(Boolean('true]', test_stack, {}))
def test_extra_right_bracket_fails():
    assert_error(Boolean('[[true]', test_stack, {}))
def test_extra_left_bracket_fails():
    assert_error(Boolean('[true]]', test_stack, {}))
def test_extra_left_right_brackets_equal_success():
    assert Boolean('[[true]]', test_stack, {}).evaluate() == True
def test_evaluating_two_separate_conditionals_works():
    assert Boolean('[[true] and [true]]', test_stack, {}).evaluate() == True
def test_evaluating_three_separate_conditionals_works():
    assert Boolean('[[true] and [true] and [true]]', test_stack, {}).evaluate() == True
def test_evaluating_four_separate_conditionals_works():
    assert Boolean('[[true] and [true] and [true] and [true]]', test_stack, {}).evaluate() == True


# SINGLE VALUES
def test_true_is_true():
    assert Boolean('[true]', test_stack, {}).evaluate() == True
def test_false_is_false():
    assert Boolean('[false]', test_stack, {}).evaluate() == False
def test_integer_is_true():
    assert Boolean('[2]', test_stack, {}).evaluate() == True
def test_decimal_is_true():
    assert Boolean('[2.2]', test_stack, {}).evaluate() == True
def test_math_is_true():
    assert Boolean('[(1+1)]', test_stack, {}).evaluate() == True
def test_string_is_true():
    assert Boolean('["hello"]', test_stack, {}).evaluate() == True
def test_string_is_true():
    assert Boolean('["hello"]', test_stack, {}).evaluate() == True
def test_array_is_true():
    assert Boolean('[<1,2,3>]', test_stack, {}).evaluate() == True
def test_string_type_is_true():
    assert Boolean('[@Type:String]', test_stack, {}).evaluate() == True
def test_number_type_is_true():
    assert Boolean('[@Type:Number]', test_stack, {}).evaluate() == True
def test_boolean_type_is_true():
    assert Boolean('[@Type:Boolean]', test_stack, {}).evaluate() == True
def test_array_type_is_true():
    assert Boolean('[@Type:Array]', test_stack, {}).evaluate() == True
def test_function_type_is_true():
    assert Boolean('[@Type:Array]', test_stack, {}).evaluate() == True


# OPERATIONS
def test_invalid_operation_fails():
    assert_error(Boolean('[true invalid true]', test_stack, {}))
def test_missing_operation_fails():
    assert_error(Boolean('[true true]', test_stack, {}))
# EQUALS
def test_equals_for_equal_integers_true():
    assert Boolean('[1 equals 1]', test_stack, {}).evaluate() == True
def test_equals_for_equal_decimals_true():
    assert Boolean('[1.1 equals 1.1]', test_stack, {}).evaluate() == True
def test_equals_for_equal_math_true():
    assert Boolean('[(1 + 1) equals (1 + 1)]', test_stack, {}).evaluate() == True
def test_equals_for_equal_arrays_true():
    assert Boolean('[<1, 2, 3> equals <1, 2, 3>]', test_stack, {}).evaluate() == True
def test_equals_for_equal_booleans_true():
    assert Boolean('[true equals true]', test_stack, {}).evaluate() == True
def test_equals_for_equal_strings_true():
    assert Boolean('["hello" equals "hello"]', test_stack, {}).evaluate() == True
def test_equals_for_equal_variables_true():
    assert Boolean('[x equals y]', test_stack, {'x': 1, 'y': 1}).evaluate() == True
def test_equals_for_equal_types_true():
    assert Boolean('[@Type:String equals @Type:String]', test_stack, {}).evaluate() == True

def test_equals_for_unequal_integers_false():
    assert Boolean('[1 equals 2]', test_stack, {}).evaluate() == False
def test_equals_for_unequal_decimals_false():
    assert Boolean('[1.1 equals 2.4]', test_stack, {}).evaluate() == False
def test_equals_for_unequal_math_false():
    assert Boolean('[(1 + 1) equals (1 + 2)]', test_stack, {}).evaluate() == False
def test_equals_for_unequal_arrays_false():
    assert Boolean('[<1, 2, 3> equals <1, 2, 4>]', test_stack, {}).evaluate() == False
def test_equals_for_unequal_booleans_false():
    assert Boolean('[true equals false]', test_stack, {}).evaluate() == False
def test_equals_for_unequal_strings_false():
    assert Boolean('["hello" equals "world"]', test_stack, {}).evaluate() == False
def test_equals_for_unequal_variables_false():
    assert Boolean('[x equals y]', test_stack, {'x': 1, 'y': 2}).evaluate() == False
def test_equals_for_unequal_types_false():
    assert Boolean('[@Type:String equals @Type:Number]', test_stack, {}).evaluate() == False

def test_equals_for_differing_value_types_raises_error():
    assert_error(Boolean('[1 equals "hello"]', test_stack, {}))
# NOT EQUALS
def test_not_equals_for_unequal_integers_lower_first_true():
    assert Boolean('[1 notEquals 2]', test_stack, {}).evaluate() == True
def test_not_equals_for_unequal_decimals_lower_first_true():
    assert Boolean('[1.1 notEquals 2.4]', test_stack, {}).evaluate() == True
def test_not_equals_for_unequal_math_lower_first_true():
    assert Boolean('[(1 + 1) notEquals (1 + 2)]', test_stack, {}).evaluate() == True
def test_not_equals_for_unequal_arrays_lower_first_true():
    assert Boolean('[<1, 2 ,3> notEquals <1, 2, 4>]', test_stack, {}).evaluate() == True
def test_not_equals_for_unequal_booleans_lower_first_true():
    assert Boolean('[true notEquals false]', test_stack, {}).evaluate() == True
def test_not_equals_for_unequal_strings_lower_first_true():
    assert Boolean('["hello" notEquals "world"]', test_stack, {}).evaluate() == True
def test_not_equals_for_unequal_variables_lower_first_true():
    assert Boolean('[x notEquals y]', test_stack, {'x': 1, 'y': 2}).evaluate() == True

def test_not_equals_for_unequal_integers_greater_first_true():
    assert Boolean('[2 notEquals 1]', test_stack, {}).evaluate() == True
def test_not_equals_for_unequal_decimals_greater_first_true():
    assert Boolean('[2.4 notEquals 1.1]', test_stack, {}).evaluate() == True
def test_not_equals_for_unequal_math_greater_first_true():
    assert Boolean('[(1 + 2) notEquals (1 + 1)]', test_stack, {}).evaluate() == True
def test_not_equals_for_unequal_arrays_greater_first_true():
    assert Boolean('[<1, 2, 4> notEquals <1, 2, 3>]', test_stack, {}).evaluate() == True
def test_not_equals_for_unequal_booleans_greater_first_true():
    assert Boolean('[false notEquals true]', test_stack, {}).evaluate() == True
def test_not_equals_for_unequal_strings_greater_first_true():
    assert Boolean('["world" notEquals "hello"]', test_stack, {}).evaluate() == True
def test_not_equals_for_unequal_variables_greater_first_true():
    assert Boolean('[x notEquals y]', test_stack, {'x': 2, 'y': 1}).evaluate() == True

def test_not_equals_for_equal_integers_false():
    assert Boolean('[1 notEquals 1]', test_stack, {}).evaluate() == False
def test_not_equals_for_equal_decimals_false():
    assert Boolean('[1.1 notEquals 1.1]', test_stack, {}).evaluate() == False
def test_not_equals_for_equal_math_false():
    assert Boolean('[(1 + 1) notEquals (1 + 1)]', test_stack, {}).evaluate() == False
def test_not_equals_for_equal_arrays_false():
    assert Boolean('[<1, 2, 3> notEquals <1, 2, 3>]', test_stack, {}).evaluate() == False
def test_not_equals_for_equal_booleans_false():
    assert Boolean('[true notEquals true]', test_stack, {}).evaluate() == False
def test_not_equals_for_equal_strings_false():
    assert Boolean('["hello" notEquals "hello"]', test_stack, {}).evaluate() == False
def test_not_equals_for_equal_variables_false():
    assert Boolean('[x notEquals y]', test_stack, {'x': 1, 'y': 1}).evaluate() == False

def test_not_equals_for_unequal_types_true():
    assert Boolean('[@Type:String notEquals @Type:Integer]', test_stack, {}).evaluate() == True
def test_not_equals_for_equal_types_false():
    assert Boolean('[@Type:String notEquals @Type:String]', test_stack, {}).evaluate() == False

def test_not_equals_for_differing_value_types_raises_error():
    assert_error(Boolean('[1 notEquals "hello"]', test_stack, {}))
# LESS THAN
def test_less_than_for_first_integer_less_than_following_true():
    assert Boolean('[1 lessThan 2]', test_stack, {}).evaluate() == True
def test_less_than_for_first_decimal_less_than_following_true():
    assert Boolean('[1.1 lessThan 2.4]', test_stack, {}).evaluate() == True
def test_less_than_for_first_math_expression_less_than_following_true():
    assert Boolean('[(1 + 1) lessThan (1 + 2)]', test_stack, {}).evaluate() == True
def test_less_than_for_first_array_less_than_following_true():
    assert Boolean('[<1, 2, 3> lessThan <1, 2, 4>]', test_stack, {}).evaluate() == True
def test_less_than_for_first_boolean_less_than_following_true():
    assert Boolean('[false lessThan true]', test_stack, {}).evaluate() == True
def test_less_than_for_first_string_less_than_following_true():
    assert Boolean('["hello" lessThan "world"]', test_stack, {}).evaluate() == True
def test_less_than_for_first_variable_less_than_following_true():
    assert Boolean('[x lessThan y]', test_stack, {'x': 1, 'y': 2}).evaluate() == True

def test_less_than_for_first_integer_greater_than_following_false():
    assert Boolean('[2 lessThan 1]', test_stack, {}).evaluate() == False
def test_less_than_for_first_decimal_greater_than_following_false():
    assert Boolean('[2.4 lessThan 1.1]', test_stack, {}).evaluate() == False
def test_less_than_for_first_math_expression_greater_than_following_false():
    assert Boolean('[(1 + 2) lessThan (1 + 1)]', test_stack, {}).evaluate() == False
def test_less_than_for_first_array_greater_than_following_false():
    assert Boolean('[<1, 2, 4> lessThan <1, 2, 3>]', test_stack, {}).evaluate() == False
def test_less_than_for_first_boolean_greater_than_following_false():
    assert Boolean('[true lessThan false]', test_stack, {}).evaluate() == False
def test_less_than_for_first_string_greater_than_following_false():
    assert Boolean('["world" lessThan "hello"]', test_stack, {}).evaluate() == False
def test_less_than_for_first_variable_greater_than_following_false():
    assert Boolean('[x lessThan y]', test_stack, {'x': 2, 'y': 1}).evaluate() == False

def test_less_than_for_first_integer_equal_to_following_false():
    assert Boolean('[1 lessThan 1]', test_stack, {}).evaluate() == False
def test_less_than_for_first_decimal_equal_to_following_false():
    assert Boolean('[1.1 lessThan 1.1]', test_stack, {}).evaluate() == False
def test_less_than_for_first_math_expression_equal_to_following_false():
    assert Boolean('[(1 + 1) lessThan (1 + 1)]', test_stack, {}).evaluate() == False
def test_less_than_for_first_array_equal_to_following_false():
    assert Boolean('[<1, 2, 3> lessThan <1, 2, 3>]', test_stack, {}).evaluate() == False
def test_less_than_for_first_boolean_equal_to_following_false():
    assert Boolean('[true lessThan true]', test_stack, {}).evaluate() == False
def test_less_than_for_first_string_equal_to_following_false():
    assert Boolean('["hello" lessThan "hello"]', test_stack, {}).evaluate() == False
def test_less_than_for_first_variable_equal_to_following_false():
    assert Boolean('[x lessThan y]', test_stack, {'x': 1, 'y': 1}).evaluate() == False

def test_less_than_for_differing_value_types_raises_error():
    assert_error(Boolean('[1 lessThan "hello"]', test_stack, {}))
def test_less_than_for_types_raises_error():
    assert_error(Boolean('[@Type:String lessThan @Type:String]', test_stack, {}))
#LESS THAN EQUALS
def test_less_than_equals_for_first_integer_less_than_following_true():
    assert Boolean('[1 lessThanEquals 2]', test_stack, {}).evaluate() == True
def test_less_than_equals_for_first_decimal_less_than_following_true():
    assert Boolean('[1.1 lessThanEquals 2.4]', test_stack, {}).evaluate() == True
def test_less_than_equals_for_first_math_expression_less_than_following_true():
    assert Boolean('[(1 + 1) lessThanEquals (1 + 2)]', test_stack, {}).evaluate() == True
def test_less_than_equals_for_first_array_less_than_following_true():
    assert Boolean('[<1, 2, 3> lessThanEquals <1, 2, 4>]', test_stack, {}).evaluate() == True
def test_less_than_equals_for_first_boolean_less_than_following_true():
    assert Boolean('[false lessThanEquals true]', test_stack, {}).evaluate() == True
def test_less_than_equals_for_first_string_less_than_following_true():
    assert Boolean('["hello" lessThanEquals "world"]', test_stack, {}).evaluate() == True
def test_less_than_equals_for_first_variable_less_than_following_true():
    assert Boolean('[x lessThanEquals y]', test_stack, {'x': 1, 'y': 2}).evaluate() == True

def test_less_than_equals_for_first_integer_greater_than_following_false():
    assert Boolean('[2 lessThanEquals 1]', test_stack, {}).evaluate() == False
def test_less_than_equals_for_first_decimal_greater_than_following_false():
    assert Boolean('[2.4 lessThanEquals 1.1]', test_stack, {}).evaluate() == False
def test_less_than_equals_for_first_math_expression_greater_than_following_false():
    assert Boolean('[(1 + 2) lessThanEquals (1 + 1)]', test_stack, {}).evaluate() == False
def test_less_than_equals_for_first_array_greater_than_following_false():
    assert Boolean('[<1, 2, 4> lessThanEquals <1, 2, 3>]', test_stack, {}).evaluate() == False
def test_less_than_equals_for_first_boolean_greater_than_following_false():
    assert Boolean('[true lessThanEquals false]', test_stack, {}).evaluate() == False
def test_less_than_equals_for_first_string_greater_than_following_false():
    assert Boolean('["world" lessThanEquals "hello"]', test_stack, {}).evaluate() == False
def test_less_than_equals_for_first_variable_greater_than_following_false():
    assert Boolean('[x lessThanEquals y]', test_stack, {'x': 2, 'y': 1}).evaluate() == False

def test_less_than_equals_for_first_integer_equal_to_following_false():
    assert Boolean('[1 lessThanEquals 1]', test_stack, {}).evaluate() == True
def test_less_than_equals_for_first_decimal_equal_to_following_false():
    assert Boolean('[1.1 lessThanEquals 1.1]', test_stack, {}).evaluate() == True
def test_less_than_equals_for_first_math_expression_equal_to_following_false():
    assert Boolean('[(1 + 1) lessThanEquals (1 + 1)]', test_stack, {}).evaluate() == True
def test_less_than_equals_for_first_array_equal_to_following_false():
    assert Boolean('[<1, 2, 3> lessThanEquals <1, 2, 3>]', test_stack, {}).evaluate() == True
def test_less_than_equals_for_first_boolean_equal_to_following_false():
    assert Boolean('[true lessThanEquals true]', test_stack, {}).evaluate() == True
def test_less_than_equals_for_first_string_equal_to_following_false():
    assert Boolean('["hello" lessThanEquals "hello"]', test_stack, {}).evaluate() == True
def test_less_than_equals_for_first_variable_equal_to_following_false():
    assert Boolean('[x lessThanEquals y]', test_stack, {'x': 1, 'y': 1}).evaluate() == True

def test_less_than_equals_for_differing_value_types_raises_error():
    assert_error(Boolean('[1 lessThanEquals "hello"]', test_stack, {}))
def test_less_than_equals_for_types_raises_error():
    assert_error(Boolean('[@Type:String lessThanEquals @Type:String]', test_stack, {}))
# GREATER THAN
def test_greater_than_for_first_integer_less_than_following_false():
    assert Boolean('[1 greaterThan 2]', test_stack, {}).evaluate() == False
def test_greater_than_for_first_decimal_less_than_following_false():
    assert Boolean('[1.1 greaterThan 2.4]', test_stack, {}).evaluate() == False
def test_greater_than_for_first_math_expression_less_than_following_false():
    assert Boolean('[(1 + 1) greaterThan (1 + 2)]', test_stack, {}).evaluate() == False
def test_greater_than_for_first_array_less_than_following_false():
    assert Boolean('[<1, 2, 3> greaterThan <1, 2, 4>]', test_stack, {}).evaluate() == False
def test_greater_than_for_first_boolean_less_than_following_false():
    assert Boolean('[false greaterThan true]', test_stack, {}).evaluate() == False
def test_greater_than_for_first_string_less_than_following_false():
    assert Boolean('["hello" greaterThan "world"]', test_stack, {}).evaluate() == False
def test_greater_than_for_first_variable_less_than_following_false():
    assert Boolean('[x greaterThan y]', test_stack, {'x': 1, 'y': 2}).evaluate() == False

def test_greater_than_for_first_integer_greater_than_following_true():
    assert Boolean('[2 greaterThan 1]', test_stack, {}).evaluate() == True
def test_greater_than_for_first_decimal_greater_than_following_true():
    assert Boolean('[2.4 greaterThan 1.1]', test_stack, {}).evaluate() == True
def test_greater_than_for_first_math_expression_greater_than_following_true():
    assert Boolean('[(1 + 2) greaterThan (1 + 1)]', test_stack, {}).evaluate() == True
def test_greater_than_for_first_array_greater_than_following_true():
    assert Boolean('[<1, 2, 4> greaterThan <1, 2, 3>]', test_stack, {}).evaluate() == True
def test_greater_than_for_first_boolean_greater_than_following_true():
    assert Boolean('[true greaterThan false]', test_stack, {}).evaluate() == True
def test_greater_than_for_first_string_greater_than_following_true():
    assert Boolean('["world" greaterThan "hello"]', test_stack, {}).evaluate() == True
def test_greater_than_for_first_variable_greater_than_following_true():
    assert Boolean('[x greaterThan y]', test_stack, {'x': 2, 'y': 1}).evaluate() == True

def test_greater_than_for_first_integer_equal_to_following_false():
    assert Boolean('[1 greaterThan 1]', test_stack, {}).evaluate() == False
def test_greater_than_for_first_decimal_equal_to_following_false():
    assert Boolean('[1.1 greaterThan 1.1]', test_stack, {}).evaluate() == False
def test_greater_than_for_first_math_expression_equal_to_following_false():
    assert Boolean('[(1 + 1) greaterThan (1 + 1)]', test_stack, {}).evaluate() == False
def test_greater_than_for_first_array_equal_to_following_false():
    assert Boolean('[<1, 2, 3> greaterThan <1, 2, 3>]', test_stack, {}).evaluate() == False
def test_greater_than_for_first_boolean_equal_to_following_false():
    assert Boolean('[true greaterThan true]', test_stack, {}).evaluate() == False
def test_greater_than_for_first_string_equal_to_following_false():
    assert Boolean('["hello" greaterThan "hello"]', test_stack, {}).evaluate() == False
def test_greater_than_for_first_variable_equal_to_following_false():
    assert Boolean('[x greaterThan y]', test_stack, {'x': 1, 'y': 1}).evaluate() == False

def test_greater_than_for_differing_value_types_raises_error():
    assert_error(Boolean('[1 greaterThan "hello"]', test_stack, {}))
def test_greater_than_for_types_raises_error():
    assert_error(Boolean('[@Type:String greaterThan @Type:String]', test_stack, {}))
# GREATER THAN EQUALS
def test_greater_than_equals_for_first_integer_less_than_following_false():
    assert Boolean('[1 greaterThanEquals 2]', test_stack, {}).evaluate() == False
def test_greater_than_equals_for_first_decimal_less_than_following_false():
    assert Boolean('[1.1 greaterThanEquals 2.4]', test_stack, {}).evaluate() == False
def test_greater_than_equals_for_first_math_less_than_following_false():
    assert Boolean('[(1 + 1) greaterThanEquals (1 + 2)]', test_stack, {}).evaluate() == False
def test_greater_than_equals_for_first_array_less_than_following_false():
    assert Boolean('[<1, 2, 3> greaterThanEquals <1, 2, 4>]', test_stack, {}).evaluate() == False
def test_greater_than_equals_for_first_boolean_less_than_following_false():
    assert Boolean('[false greaterThanEquals true]', test_stack, {}).evaluate() == False
def test_greater_than_equals_for_first_string_less_than_following_false():
    assert Boolean('["hello" greaterThanEquals "world"]', test_stack, {}).evaluate() == False
def test_greater_than_equals_for_first_variable_less_than_following_false():
    assert Boolean('[x greaterThanEquals y]', test_stack, {'x': 1, 'y': 2}).evaluate() == False

def test_greater_than_equals_for_first_integer_greater_than_following_true():
    assert Boolean('[2 greaterThanEquals 1]', test_stack, {}).evaluate() == True
def test_greater_than_equals_for_first_decimal_greater_than_following_true():
    assert Boolean('[2.4 greaterThanEquals 1.1]', test_stack, {}).evaluate() == True
def test_greater_than_equals_for_first_math_expression_greater_than_following_true():
    assert Boolean('[(1 + 2) greaterThanEquals (1 + 1)]', test_stack, {}).evaluate() == True
def test_greater_than_equals_for_first_array_greater_than_following_true():
    assert Boolean('[<1, 2, 4> greaterThanEquals <1, 2, 3>]', test_stack, {}).evaluate() == True
def test_greater_than_equals_for_first_boolean_greater_than_following_true():
    assert Boolean('[true greaterThanEquals false]', test_stack, {}).evaluate() == True
def test_greater_than_equals_for_first_string_greater_than_following_true():
    assert Boolean('["world" greaterThanEquals "hello"]', test_stack, {}).evaluate() == True
def test_greater_than_equals_for_first_variable_greater_than_following_true():
    assert Boolean('[x greaterThanEquals y]', test_stack, {'x': 2, 'y': 1}).evaluate() == True

def test_greater_than_equals_for_first_integer_equal_to_following_true():
    assert Boolean('[1 greaterThanEquals 1]', test_stack, {}).evaluate() == True
def test_greater_than_equals_for_first_decimal_equal_to_following_true():
    assert Boolean('[1.1 greaterThanEquals 1.1]', test_stack, {}).evaluate() == True
def test_greater_than_equals_for_first_math_expression_equal_to_following_true():
    assert Boolean('[(1 + 1) greaterThanEquals (1 + 1)]', test_stack, {}).evaluate() == True
def test_greater_than_equals_for_first_array_equal_to_following_true():
    assert Boolean('[<1, 2, 3> greaterThanEquals <1, 2, 3>]', test_stack, {}).evaluate() == True
def test_greater_than_equals_for_first_boolean_equal_to_following_true():
    assert Boolean('[true greaterThanEquals true]', test_stack, {}).evaluate() == True
def test_greater_than_equals_for_first_string_equal_to_following_true():
    assert Boolean('["hello" greaterThanEquals "hello"]', test_stack, {}).evaluate() == True
def test_greater_than_equals_for_first_variable_equal_to_following_true():
    assert Boolean('[x greaterThanEquals y]', test_stack, {'x': 1, 'y': 1}).evaluate() == True

def test_greater_than_equals_for_differing_value_types_raises_error():
    assert_error(Boolean('[1 greaterThanEquals "hello"]', test_stack, {}))
def test_greater_than_equals_for_types_raises_error():
    assert_error(Boolean('[@Type:String greaterThanEquals @Type:String]', test_stack, {}))
# AND
def test_and_for_equal_boolean_values_is_true():
    assert Boolean('[true and true]', test_stack, {}).evaluate() == True
def test_and_for_equal_integer_values_is_true():
    assert Boolean('[1 and 1]', test_stack, {}).evaluate() == True  
def test_and_for_equal_decimal_values_is_true():
    assert Boolean('[1.1 and 1.1]', test_stack, {}).evaluate() == True  
def test_and_for_equal_math_values_is_true():
    assert Boolean('[(1 + 1) and (1 + 1)]', test_stack, {}).evaluate() == True
def test_and_for_equal_arrays_values_is_true():
    assert Boolean('[<1, 2, 3> and <1, 2, 3>]', test_stack, {}).evaluate() == True
def test_and_for_equal_string_values_is_true():
    assert Boolean('["hello" and "hello"]', test_stack, {}).evaluate() == True 
def test_and_for_equal_variable_values_is_true():
    assert Boolean('[x and y]', test_stack, {'x': 1, 'y': 1}).evaluate() == True

def test_and_for_unequal_booleans_with_greater_first_is_true_unless_booleans():
    assert Boolean('[true and false]', test_stack, {}).evaluate() == False
def test_and_for_unequal_integers_with_greater_first_is_true_unless_booleans():
    assert Boolean('[2 and 1]', test_stack, {}).evaluate() == True  
def test_and_for_unequal_decimals_with_greater_first_is_true_unless_booleans():
    assert Boolean('[2.4 and 1.1]', test_stack, {}).evaluate() == True
def test_and_for_unequal_math_with_greater_first_is_true_unless_booleans():
    assert Boolean('[(1 + 2) and (1 + 1)]', test_stack, {}).evaluate() == True
def test_and_for_unequal_arrays_with_greater_first_is_true_unless_booleans():
    assert Boolean('[<1, 2, 4> and <1, 2, 3>]', test_stack, {}).evaluate() == True
def test_and_for_unequal_strings_with_greater_first_is_true_unless_booleans():
    assert Boolean('["world" and "hello"]', test_stack, {}).evaluate() == True 
def test_and_for_unequal_variables_with_greater_first_is_true_unless_booleans():
    assert Boolean('[x and y]', test_stack, {'x': 2, 'y': 1}).evaluate() == True

def test_and_for_unequal_booleans_with_lower_first_is_true_unless_booleans():
    assert Boolean('[false and true]', test_stack, {}).evaluate() == False
def test_and_for_unequal_integers_with_lower_first_is_true_unless_booleans():
    assert Boolean('[1 and 2]', test_stack, {}).evaluate() == True    
def test_and_for_unequal_decimals_with_lower_first_is_true_unless_booleans():
    assert Boolean('[1.1 and 2.4]', test_stack, {}).evaluate() == True
def test_and_for_unequal_math_with_lower_first_is_true_unless_booleans():
    assert Boolean('[(1 + 1) and (1 + 2)]', test_stack, {}).evaluate() == True
def test_and_for_unequal_decimals_with_lower_first_is_true_unless_booleans():
    assert Boolean('[<1, 2, 3> and <1, 2, 4>]', test_stack, {}).evaluate() == True
def test_and_for_unequal_strings_with_lower_first_is_true_unless_booleans():
    assert Boolean('["hello" and "world"]', test_stack, {}).evaluate() == True 
def test_and_for_unequal_variables_with_lower_first_is_true_unless_booleans():
    assert Boolean('[x and y]', test_stack, {'x': 1, 'y': 2}).evaluate() == True

def test_false_and_false_is_false():
    assert Boolean('[false and false]', test_stack, {}).evaluate() == False

def test_and_for_differing_value_types_raises_error():
    assert_error(Boolean('[1 and "hello"]', test_stack, {}))
def test_and_for_types_raises_error():
    assert_error(Boolean('[@Type:String and @Type:String]', test_stack, {}))
# OR
def test_or_for_equal_boolean_values_is_true():
    assert Boolean('[true or true]', test_stack, {}).evaluate() == True
def test_or_for_equal_integer_values_is_true():
    assert Boolean('[1 or 1]', test_stack, {}).evaluate() == True
def test_or_for_equal_decimal_values_is_true():
    assert Boolean('[1.1 or 1.1]', test_stack, {}).evaluate() == True
def test_or_for_equal_math_values_is_true():
    assert Boolean('[(1 + 1) or (1 + 1)]', test_stack, {}).evaluate() == True
def test_or_for_equal_array_values_is_true():
    assert Boolean('[<1, 2, 3> or <1, 2 ,3>]', test_stack, {}).evaluate() == True
def test_or_for_equal_string_values_is_true():
    assert Boolean('["hello" or "hello"]', test_stack, {}).evaluate() == True 
def test_or_for_equal_variable_values_is_true():
    assert Boolean('[x or y]', test_stack, {'x': 1, 'y': 1}).evaluate() == True

def test_or_for_unequal_booleans_with_greater_first_is_true():
    assert Boolean('[true or false]', test_stack, {}).evaluate() == True
def test_or_for_unequal_integers_with_greater_first_is_true():
    assert Boolean('[2 or 1]', test_stack, {}).evaluate() == True   
def test_or_for_unequal_decimals_with_greater_first_is_true():
    assert Boolean('[2.4 or 1.1]', test_stack, {}).evaluate() == True
def test_or_for_unequal_math_with_greater_first_is_true():
    assert Boolean('[(1 + 2) or (1 + 1)]', test_stack, {}).evaluate() == True
def test_or_for_unequal_arrays_with_greater_first_is_true():
    assert Boolean('[<1, 2, 4> or <1, 2, 3>]', test_stack, {}).evaluate() == True
def test_or_for_unequal_strings_with_greater_first_is_true():
    assert Boolean('["world" or "hello"]', test_stack, {}).evaluate() == True 
def test_or_for_unequal_variables_with_greater_first_is_true():
    assert Boolean('[x or y]', test_stack, {'x': 2, 'y': 1}).evaluate() == True

def test_or_for_unequal_booleans_with_lower_first_is_true():
    assert Boolean('[false or true]', test_stack, {}).evaluate() == True
def test_or_for_unequal_integers_with_lower_first_is_true():
    assert Boolean('[1 or 2]', test_stack, {}).evaluate() == True 
def test_or_for_unequal_decimals_with_lower_first_is_true():
    assert Boolean('[1.1 or 2.4]', test_stack, {}).evaluate() == True
def test_or_for_unequal_math_with_lower_first_is_true():
    assert Boolean('[(1 + 1) or (1 + 2)]', test_stack, {}).evaluate() == True
def test_or_for_unequal_arrays_with_lower_first_is_true():
    assert Boolean('[<1, 2, 3> or <1, 2, 4>]', test_stack, {}).evaluate() == True
def test_or_for_unequal_strings_with_lower_first_is_true():
    assert Boolean('["hello" or "world"]', test_stack, {}).evaluate() == True 
def test_or_for_unequal_variables_with_lower_first_is_true():
    assert Boolean('[x or y]', test_stack, {'x': 1, 'y': 2}).evaluate() == True

def test_false_or_false_is_false():
    assert Boolean('[false or false]', test_stack, {}).evaluate() == False

def test_or_for_differing_value_types_raises_error():
    assert_error(Boolean('[1 or "hello"]', test_stack, {}))
def test_or_for_types_raises_error():
    assert_error(Boolean('[@Type:String or @Type:String]', test_stack, {}))

# STRING EXPRESSIONS
def test_double_quote_string_expressions_can_be_compared_using_boolean():
    assert Boolean('["hello" . "world" equals "hello" . "world"]', test_stack, {}).evaluate() == True
def test_single_quote_string_expressions_can_be_compared_using_boolean():
    assert Boolean("['hello' . 'world' equals 'hello' . 'world']", test_stack, {}).evaluate() == True
def test_double_quote_string_expressions_with_variables_concatenated_after_can_be_compared_using_boolean():
    assert Boolean('["hello" . x equals "hello" . x]', test_stack, {'x': 1}).evaluate() == True
def test_single_quote_string_expressions_with_variables_concatenated_after_can_be_compared_using_boolean():
    assert Boolean("['hello' . x equals 'hello' . x]", test_stack, {'x': 1}).evaluate() == True
def test_double_quote_string_expressions_with_variables_concatenated_before_can_be_compared_using_boolean():
    assert Boolean('[x . "hello" equals x . "hello"]', test_stack, {'x': 1}).evaluate() == True
def test_single_quote_string_expressions_with_variables_concatenated_before_can_be_compared_using_boolean():
    assert Boolean("[x . 'hello' equals x . 'hello']", test_stack, {'x': 1}).evaluate() == True
def test_string_concatenated_variables_can_be_compared_using_boolean():
    assert Boolean("[x . y equals x . y]", test_stack, {'x': 1, 'y': 2}).evaluate() == True
def test_complex_boolean_that_works_with_string_expressions():
    assert Boolean('[[x . "hello" lessThan x . \'world\'] and [x . "hello" lessThanEquals x . y]]', test_stack, {'x': 1, 'y': "world"}).evaluate() == True


# SPACING

# LACK OF SPACES
def test_no_spaces_between_variable_operators_and_operands_raises_error():
    assert_error(Boolean('[xequalsy]', test_stack, {'x': 'hello', 'y': 'world'}))
def test_no_spaces_between_unenclosed_boolean_operators_and_operands_raises_error():
    assert_error(Boolean('[trueequalsfalse]', test_stack, {}))
def test_no_spaces_between_complex_double_quote_string_expression_operators_and_operands_with_variables_touching_operator_raises_error():
    assert_error(Boolean('["hello".xequalsy."world"]', test_stack, {'x': 'hello', 'y': 'world'}))
def test_no_spaces_between_complex_single_quote_string_expression_operators_and_operands_with_variables_touching_operator_raises_error():
    assert_error(Boolean("['hello'.xequalsy.'world']", test_stack, {'x': 'hello', 'y': 'world'}))
def test_no_spaces_between_complex_string_expression_operators_and_operands_with_math_and_variables_touching_operator_raises_error():
    assert_error(Boolean('[(1+1).xequalsy.(2*2)]', test_stack, {'x': 'hello', 'y': 'world'}))
def test_no_spaces_between_complex_string_expression_operators_and_operands_with_boolean_expression_and_variables_touching_operator_raises_error():
    assert_error(Boolean('[[true].xequalsy.[false]]', test_stack, {'x': 'hello', 'y': 'world'}))
def test_no_spaces_between_operator_and_types_raises_error():
    assert_error(Boolean('[@Type:Stringequals@Type:String]', test_stack, {}))
def test_no_spaces_between_complex_double_quote_string_expression_operators_and_operands_with_strings_touching_operator_works():
    assert Boolean('[x."hello"equals"world".y]', test_stack, {'x': 'hello', 'y': 'world'}).evaluate() == False
def test_no_spaces_between_complex_single_quote_string_expression_operators_and_operands_with_strings_touching_operator_works():
    assert Boolean("[x.'hello'equals'world'.y]", test_stack, {'x': 'hello', 'y': 'world'}).evaluate() == False
def test_no_spaces_between_complex_string_expression_operators_and_operands_with_math_touching_operator_works():
    assert Boolean('[x.(1+1)equals(2*2).y]', test_stack, {'x': 'hello', 'y': 'world'}).evaluate() == False
def test_no_spaces_between_complex_string_expression_operators_and_operands_with_arrays_touching_operator_works():
    assert Boolean('[x.<1,2,3>equals<1,2,4>.y]', test_stack, {'x': 'hello', 'y': 'world'}).evaluate() == False
def test_no_spaces_between_complex_string_expression_operators_and_operands_with_boolean_expression_touching_operator_works():
    assert Boolean('[x.[true]equals[false].y]', test_stack, {'x': 'hello', 'y': 'world'}).evaluate() == False
def test_no_spaces_when_comparing_single_enclosed_true_false_booleans_works():
    assert Boolean('[[true]equals[false]]', test_stack, {}).evaluate() == False
def test_no_spaces_when_comparing_double_quote_strings_works():
    assert Boolean('["hello"equals"world"]', test_stack, {}).evaluate() == False
def test_no_spaces_when_comparing_single_quote_strings_works():
    assert Boolean("['hello'equals'world']", test_stack, {}).evaluate() == False
def test_no_spaces_when_comparing_math_operations_works():
    assert Boolean('[(1 + 1)equals(2 * 2)]', test_stack, {}).evaluate() == False
# EXTRA SPACES
def test_extra_spaces_in_boolean_operation_on_variables_works():
    assert Boolean('[   x   equals   y   ]', test_stack, {'x': 'hello', 'y': 'world'}).evaluate() == False
def test_extra_spaces_in_boolean_operation_on_unenclosed_booleans_works():
    assert Boolean('[   true   equals   false   ]', test_stack, {}).evaluate() == False
def test_extra_spaces_in_boolean_operation_on_double_quote_strings_expressions_concatenated_with_variables_facing_operator_works():
    assert Boolean('[   "hello"   .   x   equals   y   .   "world"   ]', test_stack, {'x': 'hello', 'y': 'world'}).evaluate() == False
def test_extra_spaces_in_boolean_operation_on_double_quote_string_expressions_concatenated_with_variables_facing_operator_works():
    assert Boolean("[   'hello'   .   x   equals   y   .   'world'   ]", test_stack, {'x': 'hello', 'y': 'world'}).evaluate() == False
def test_extra_spaces_in_boolean_operation_on_string_expressions_with_math_concatenated_with_variables_facing_operator_works():
    assert Boolean('[   (   1   +   1   )   .   x   equals   y   .   (   2   *   2   )   ]', test_stack, {'x': 'hello', 'y': 'world'}).evaluate() == False
def test_extra_spaces_in_boolean_operation_on_string_expressions_with_boolean_expressions_concatenated_with_variables_facing_operator_works():
    assert Boolean('[   [   true   ]   .   x   equals   y   .   [   false   ]   ]', test_stack, {'x': 'hello', 'y': 'world'}).evaluate() == False
def test_no_spaces_between_operator_and_types_works():
    assert Boolean('[   @Type:String   equals   @Type:String   ]', test_stack, {}).evaluate() == True
def test_extra_spaces_in_boolean_operation_on_double_quote_strings_expressions_concatenated_with_strings_facing_operator_works():
    assert Boolean('[   x   .   "hello"   equals   "world"   .   y   ]', test_stack, {'x': 'hello', 'y': 'world'}).evaluate() == False
def test_extra_spaces_in_boolean_operation_on_single_quote_strings_expressions_concatenated_with_strings_facing_operator_works():
    assert Boolean("[   x   .   'hello'   equals   'world'   .   y   ]", test_stack, {'x': 'hello', 'y': 'world'}).evaluate() == False
def test_extra_spaces_in_boolean_operation_on_string_expressions_with_variables_concatenated_with_math_operation_facing_operator_works():
    assert Boolean('[   x   .   (   1   +   1   )   equals   (   2   *   2   )   .   y   ]', test_stack, {'x': 'hello', 'y': 'world'}).evaluate() == False
def test_extra_spaces_in_boolean_operation_on_string_expressions_with_variables_concatenated_with_arrays_facing_operator_works():
    assert Boolean('[   x   .   <   1   ,   2   ,   3   >   equals   <   1   ,   2   ,   4   >   .   y   ]', test_stack, {'x': 'hello', 'y': 'world'}).evaluate() == False
def test_extra_spaces_in_boolean_operation_on_string_expressions_with_variables_concatenated_with_boolean_operation_facing_operator_works():
    assert Boolean('[   x   .   [   true   ]   equals   [   false   ]   .   y   ]', test_stack, {'x': 'hello', 'y': 'world'}).evaluate() == False
def test_extra_spaces_when_comparing_single_enclosed_true_false_booleans_works():
    assert Boolean('[   [   true   ]   equals   [   false   ]   ]', test_stack, {}).evaluate() == False
def test_extra_spaces_when_comparing_double_quote_strings_works():
    assert Boolean('[   "hello"   equals   "world"   ]', test_stack, {}).evaluate() == False
def test_extra_spaces_when_comparing_single_quote_strings_works():
    assert Boolean("[   'hello'   equals   'world'   ]", test_stack, {}).evaluate() == False
def test_extra_spaces_when_comparing_math_operations_works():
    assert Boolean('[   (   1   +   1   )   equals   (2   *   2)   ]', test_stack, {}).evaluate() == False


# MISSING OR EXTRA ENCLOSING SYMBOLS AND OPERATORS
# BOOLEAN BRACKETS
def test_extra_right_brackets_on_complex_boolean_raises_error():
    assert_error(Boolean('[[true equals true]] and [true notEquals false]]', test_stack, {}))
def test_missing_right_brackets_on_complex_boolean_raises_error():
    assert_error(Boolean('[[true equals true and [true notEquals false]]', test_stack, {}))
def test_extra_left_brackets_on_complex_boolean_raises_error():
    assert_error(Boolean('[[true equals true] and [[true notEquals false]]', test_stack, {}))
def test_missing_left_brackets_on_complex_boolean_raises_error():
    assert_error(Boolean('[[true equals true] and true notEquals false]]', test_stack, {}))
# STRINGS
def test_extra_dot_operator_when_comparing_strings_raises_error():
    assert_error(Boolean('["hello" . "world" . equals "hello" . "world"]', test_stack, {}))
def test_missing_dot_operator_when_comparing_strings_raises_error():
    assert_error(Boolean('["hello" "world" equals "hello" . "world"]', test_stack, {}))
def test_extra_closing_double_quote_when_comparing_strings_raises_error():
    assert_error(Boolean('["hello" . "world"" equals "hello" . "world"]', test_stack, {}))
def test_extra_leading_double_quote_when_comparing_strings_raises_error():
    assert_error(Boolean('["hello" . "world" equals ""hello" . "world"]', test_stack, {}))
def test_extra_closing_single_quote_when_comparing_strings_raises_error():
    assert_error(Boolean("['hello' . 'world'' equals 'hello' . 'world']", test_stack, {}))
def test_extra_leading_single_quote_when_comparing_strings_raises_error():
    assert_error(Boolean("['hello' . 'world' equals ''hello' . 'world']", test_stack, {}))
def test_missing_closing_double_quote_when_comparing_strings_raises_error():
    assert_error(Boolean('["hello" . "world equals "hello" . "world"]', test_stack, {}))
def test_missing_leading_double_quote_when_comparing_strings_raises_error():
    assert_error(Boolean('["hello" . "world" equals hello" . "world"]', test_stack, {}))
def test_missing_closing_single_quote_when_comparing_strings_raises_error():
    assert_error(Boolean("['hello' . 'world equals 'hello' . 'world']", test_stack, {}))
def test_missing_leading_single_quote_when_comparing_strings_raises_error():
    assert_error(Boolean("['hello' . 'world' equals hello' . 'world']", test_stack, {}))
# MATH
def test_extra_closing_parenthesis_when_comparing_math_raises_error():
    assert_error(Boolean('[(1 + 1)) equals (2 * 2)]', test_stack, {}))
def test_extra_leading_parenthesis_when_comparing_math_raises_error():
    assert_error(Boolean('[(1 + 1) equals ((2 * 2)]', test_stack, {}))
def test_missing_closing_parenthesis_when_comparing_math_raises_error():
    assert_error(Boolean('[(1 + 1 equals (2 * 2)]', test_stack, {}))
def test_missing_leading_parenthesis_when_comparing_math_raises_error():
    assert_error(Boolean('[(1 + 1) equals 2 * 2)]', test_stack, {}))
# ARRAY
def test_extra_closing_symbol_when_comparing_arrays_raises_error():
    assert_error(Boolean('[<1, 2, 3>> equals <1, 2, 4>]', test_stack, {}))
def test_extra_leading_symbol_when_comparing_arrays_raises_error():
    assert_error(Boolean('[<1, 2, 3> equals <<1, 2, 4>]', test_stack, {}))
def test_missing_closing_symbol_when_comparing_arrays_raises_error():
    assert_error(Boolean('[<1, 2, 3 equals <1, 2, 4>]', test_stack, {}))
def test_missing_leading_symbol_when_comparing_arrays_raises_error():
    assert_error(Boolean('[<1, 2, 3> equals 1, 2, 4>]', test_stack, {}))
def test_extra_comma_when_comparing_arrays_raises_error():
    assert_error(Boolean('[<1, 2, 3,> equals <1, 2, 4>]', test_stack, {}))
def test_missing_comma_when_comparing_arrays_raises_error():
    assert_error(Boolean('[<1, 2, 3> equals <1 2, 4>]', test_stack, {}))


# COMPARING TO DIFFERENT VALUE TYPES
# STRING
def test_string_cannot_be_compared_to_an_integer():
    assert_error(Boolean('["hello" or 1]', test_stack, {}))
def test_string_cannot_be_compared_to_a_decimal():
    assert_error(Boolean('["hello" or 1.1]', test_stack, {}))
def test_string_cannot_be_compared_to_math():
    assert_error(Boolean('["hello" or (1 + 1)]', test_stack, {}))
def test_string_cannot_be_compared_to_an_array():
    assert_error(Boolean('["hello" or <1, 2, 3>]', test_stack, {}))
def test_string_cannot_be_compared_to_a_boolean():
    assert_error(Boolean('["hello" or true]', test_stack, {}))
# NUMBERS AND MATH
def test_integers_cannot_be_compared_to_strings():
    assert_error(Boolean('[1 or "hello"]', test_stack, {}))
def test_decimals_cannot_be_compared_to_strings():
    assert_error(Boolean('[1.0 or "hello"]', test_stack, {}))
def test_math_cannot_be_compared_to_strings():
    assert_error(Boolean('[(2 - 1) or "hello"]', test_stack, {}))
def test_integers_can_be_compared_to_decimals():
    assert Boolean("[1 or 1.1]", test_stack, {}).evaluate() == True
def test_integers_can_be_compared_to_math():
    assert Boolean("[1 or (2 - 1)]", test_stack, {}).evaluate() == True
def test_decimals_can_be_compared_to_math():
    assert Boolean("[1.1 or (2 - 1)]", test_stack, {}).evaluate() == True
def test_integers_cannot_be_compared_to_arrays():
    assert_error(Boolean('[1 or <1, 2, 3>]', test_stack, {}))
def test_decimals_cannot_be_compared_to_arrays():
    assert_error(Boolean('[1.0 or <1, 2, 3>]', test_stack, {}))
def test_math_cannot_be_compared_to_arrays():
    assert_error(Boolean('[(2 - 1) or <1, 2, 3>]', test_stack, {}))
def test_integers_can_be_compared_to_booleans():
    assert Boolean("[1 or true]", test_stack, {}).evaluate() == True
def test_decimals_can_be_compared_to_booleans():
    assert Boolean("[1.0 or true]", test_stack, {}).evaluate() == True
def test_math_can_be_compared_to_booleans():
    assert Boolean("[(2 - 1) or true]", test_stack, {}).evaluate() == True
# ARRAYS
def test_arrays_cannot_be_compared_to_strings():
    assert_error(Boolean('[<1, 2, 3> or "hello"]', test_stack, {}))
def test_arrays_cannot_be_compared_to_integers():
    assert_error(Boolean('[<1, 2, 3> or 1]', test_stack, {}))
def test_arrays_cannot_be_compared_to_decimals():
    assert_error(Boolean('[<1, 2, 3> or 1.1]', test_stack, {}))
def test_arrays_cannot_be_compared_to_math():
    assert_error(Boolean('[<1, 2, 3> or (1 + 1)]', test_stack, {}))
def test_arrays_cannot_be_compared_to_booleans():
    assert_error(Boolean('[<1, 2, 3> or true]', test_stack, {}))
# BOOLEANS
def test_booleans_cannot_be_compared_to_strings():
    assert_error(Boolean('[true or "hello"]', test_stack, {}))
def test_booleans_can_be_compared_to_integers():
    assert Boolean("[true or 1]", test_stack, {}).evaluate() == True
def test_booleans_can_be_compared_to_decimals():
    assert Boolean("[true or 1.1]", test_stack, {}).evaluate() == True
def test_booleans_cann_be_compared_to_math():
    assert Boolean("[true or (1 + 1)]", test_stack, {}).evaluate() == True
def test_booleans_cannot_be_compared_to_arrays():
    assert_error(Boolean('[true or <1, 2, 3>]', test_stack, {}))


# INLINE OPERATIONS
# EQUALS
def test_inline_equals_works_if_third_operator_is_boolean():
    assert Boolean('["hello" equals "hello" equals true]', test_stack, {}).evaluate() == True
def test_inline_equals_fails_if_third_operator_is_not_boolean():
    assert_error(Boolean('["hello" equals "hello" equals "hello"]', test_stack, {}))
# NOT EQUALS
def test_inline_not_equals_works_if_third_operator_is_boolean():
    assert Boolean('["hello" notEquals "hello" notEquals true]', test_stack, {}).evaluate() == True
def test_inline_not_equals_fails_if_third_operator_is_not_boolean():
    assert_error(Boolean('["hello" notEquals "hello" notEquals "hello"]', test_stack, {}))
# LESS THAN
def test_inline_lessThan_works_if_third_operator_is_boolean():
    assert Boolean('["hello" lessThan "hello" lessThan true]', test_stack, {}).evaluate() == True
def test_inline_lessThan_fails_if_third_operator_is_not_boolean():
    assert_error(Boolean('["hello" lessThan "hello" lessThan "hello"]', test_stack, {}))
# LESS THAN EQUALS
def test_inline_lessThanEquals_works_if_third_operator_is_boolean():
    assert Boolean('["hello" lessThanEquals "world" lessThanEquals true]', test_stack, {}).evaluate() == True
def test_inline_lessThanEquals_fails_if_third_operator_is_not_boolean():
    assert_error(Boolean('["hello" lessThanEquals "hello" lessThanEquals "hello"]', test_stack, {}))
# GREATER THAN
def test_inline_greaterThan_works_if_third_operator_is_boolean():
    assert Boolean('["world" greaterThan "hello" greaterThan true]', test_stack, {}).evaluate() == False
def test_inline_greaterThan_fails_if_third_operator_is_not_boolean():
    assert_error(Boolean('["world" greaterThan "hello" greaterThan "hello"]', test_stack, {}))
# GREATER THAN EQUALS
def test_inline_greaterThanEquals_works_if_third_operator_is_boolean():
    assert Boolean('["world" greaterThanEquals "hello" greaterThanEquals true]', test_stack, {}).evaluate() == True
def test_inline_greaterThanEquals_fails_if_third_operator_is_not_boolean():
    assert_error(Boolean('["world" greaterThanEquals "hello" greaterThanEquals "hello"]', test_stack, {}))
# AND
def test_inline_and_works_if_third_operator_is_boolean():
    assert Boolean('["hello" and "hello" and true]', test_stack, {}).evaluate() == True
def test_inline_and_fails_if_third_operator_is_not_boolean():
    assert_error(Boolean('["hello" and "hello" and "hello"]', test_stack, {}))
# OR
def test_inline_or_works_if_third_operator_is_boolean():
    assert Boolean('["hello" or "hello" or true]', test_stack, {}).evaluate() == True
def test_inline_or_fails_if_third_operator_is_not_boolean():
    assert_error(Boolean('["hello" or "hello" or "hello"]', test_stack, {}))


# COMPLICATED
def test_complicated_expression_successful():
    assert Boolean('[[x."hello" equals (1 + 1)."hello"] lessThan ["world" or "test"] and true]', test_stack, {'x': 2}).evaluate() == False
    assert Boolean('[true and [x."hello" equals (1 + 1)."hello"] lessThan ["world" or "test"]]', test_stack, {'x': 2}).evaluate() == False
    assert Boolean('[[2 and 3] equals false]', test_stack, {}).evaluate() == False


def assert_error(expression):
    with pytest.raises(SystemExit) as error:
            expression.evaluate()
    assert error.type == SystemExit
    assert error.value.code == 1