import os
import pytest
import unittest

from syllogistic.processor import DEFAULT_TIC_80_PATH, ProcessorContext, ProcessorException, DynamicAssignmentProcessorException, ModuleNotFoundProcessorException, InvalidSyntaxProcessorException, InvalidStringEscapeProcessorException, process_lines


class TestRequire(unittest.TestCase):
    def test_require(self):
      code = "require('tests/input/sample')"
      context = ProcessorContext('tests/input/fake.lua', code.split('\n'), strict=True, verbose=True);
      result = process_lines(context)

      assert result == """function __syllogistic_require_1() function sample()
  trace('sample')
end end
__syllogistic_require_1()"""

    def test_require_escape(self):
      code = "require('tests/input/s\\'ample')"
      context = ProcessorContext('tests/input/fake.lua', code.split('\n'), strict=True, verbose=True);
      result = process_lines(context)

      assert result == """function __syllogistic_require_1() function sample()
  trace('sample')
end end
__syllogistic_require_1()"""

    def test_require_init(self):
      code = "require('tests/input')"
      context = ProcessorContext('tests/input/fake.lua', code.split('\n'), strict=True, verbose=True);
      result = process_lines(context)

      assert result == """function __syllogistic_require_1() function init() end end
__syllogistic_require_1()"""

    def test_require_assign(self):
      code = "variable = require('tests/input/sample')"
      context = ProcessorContext('tests/input/fake.lua', code.split('\n'), strict=True, verbose=True);
      result = process_lines(context)

      assert result == """function __syllogistic_require_1() function sample()
  trace('sample')
end end
variable = __syllogistic_require_1()"""

    def test_require_assign_semicolon(self):
      code = "variable = require('tests/input/sample'); test = 3"
      context = ProcessorContext('tests/input/fake.lua', code.split('\n'), strict=True, verbose=True);
      result = process_lines(context)

      assert result == """function __syllogistic_require_1() function sample()
  trace('sample')
end end
variable = __syllogistic_require_1(); test = 3"""

    def test_require_package_path(self):
      code = """variable = 3
package.path=package.path ..';tests/input/?.lua'
require('sample')"""
      context = ProcessorContext('tests/input/fake.lua', code.split('\n'), strict=True, verbose=True);
      result = process_lines(context)

    def test_require_package_path_depth(self):
      code = """package.path=package.path ..';tests/input/?.lua'
require('require')"""
      context = ProcessorContext('tests/input/fake.lua', code.split('\n'), strict=True, verbose=True);
      result = process_lines(context)

      assert result == """function __syllogistic_require_2() function sample()
  trace('sample')
end end
function __syllogistic_require_1() __syllogistic_require_2() end
__syllogistic_require_1()"""
      expected = list(DEFAULT_TIC_80_PATH)
      expected.append('tests/input/?.lua')
      assert context.requires.path == expected

    def test_require_package_path_depth_already_loaded(self):
      ModuleNotFoundProcessorException
      code = """package.path=package.path ..';tests/input/?.lua'
require('sample')
require('require-no-path')"""
      context = ProcessorContext('tests/input/fake.lua', code.split('\n'), strict=True, verbose=True);
      result = process_lines(context)

      assert result == """function __syllogistic_require_1() function sample()
  trace('sample')
end end
function __syllogistic_require_2() __syllogistic_require_1() end
__syllogistic_require_1()
__syllogistic_require_2()"""
      expected = list(DEFAULT_TIC_80_PATH)
      expected.append('tests/input/?.lua')
      assert context.requires.path == expected

    def test_require_package_path_after(self):
      code = """variable = 3
package.path='tests/input/?.lua;'.. package.path
require('sample')"""
      context = ProcessorContext('tests/input/fake.lua', code.split('\n'), strict=True, verbose=True);
      result = process_lines(context)

      assert result == """function __syllogistic_require_1() function sample()
  trace('sample')
end end
variable = 3
__syllogistic_require_1()"""
      expected = ['tests/input/?.lua']
      expected.extend(DEFAULT_TIC_80_PATH)
      assert context.requires.path == expected

    def test_require_package_path_in_line(self):
      code = """variable = 3
package.path='tests/input/?.lua;'.. package.path; variable=7
require('sample')"""
      context = ProcessorContext('tests/input/fake.lua', code.split('\n'), strict=True, verbose=True);
      result = process_lines(context)

      assert result == """function __syllogistic_require_1() function sample()
  trace('sample')
end end
variable = 3
variable=7
__syllogistic_require_1()"""
      expected = ['tests/input/?.lua']
      expected.extend(DEFAULT_TIC_80_PATH)
      assert context.requires.path == expected

    def test_require_package_path_in_line_space(self):
      code = """variable = 3
package.path='tests/input/?.lua;'.. package.path variable=7
require('sample')"""
      context = ProcessorContext('tests/input/fake.lua', code.split('\n'), strict=True, verbose=True);
      result = process_lines(context)

      assert result == """function __syllogistic_require_1() function sample()
  trace('sample')
end end
variable = 3
variable=7
__syllogistic_require_1()"""
      expected = ['tests/input/?.lua']
      expected.extend(DEFAULT_TIC_80_PATH)
      assert context.requires.path == expected

    def test_require_set_absolute(self):
      path = os.path.abspath('tests/input/sample.lua')

      # Windows-style paths :-/
      if path.find('\\'):
        path = path.replace('\\', '\\\\')

      code = f"""package.path='?;?.lua'
require('{path}')"""
      context = ProcessorContext('tests/input/fake.lua', code.split('\n'), strict=True, verbose=True);
      result = process_lines(context)

      assert result == """function __syllogistic_require_1() function sample()
  trace('sample')
end end
__syllogistic_require_1()"""
      assert context.requires.path == ['?', '?.lua']

    def test_require_no_quotes(self):
      with pytest.raises(ProcessorException):
        code = "require(tests/input/sample)"
        context = ProcessorContext('tests/input/fake.lua', code.split('\n'), strict=True, verbose=True);
        result = process_lines(context)

    def test_require_no_empty(self):
      with pytest.raises(ModuleNotFoundProcessorException):
        code = "require()"
        context = ProcessorContext('tests/input/fake.lua', code.split('\n'), strict=True, verbose=True);
        result = process_lines(context)

    # Technically this should be allowed but it's easier to deny it than supported.
    def test_require_no_dynamic_require(self):
      with pytest.raises(ProcessorException):
        code = "require('x'..'y')"
        context = ProcessorContext('tests/input/fake.lua', code.split('\n'), strict=True, verbose=True);
        result = process_lines(context)

    def test_require_invalid_string_escape(self):
      with pytest.raises(InvalidStringEscapeProcessorException):
        code = """require('\\x1234sample')"""
        context = ProcessorContext('tests/input/fake.lua', code.split('\n'), strict=True, verbose=True);
        result = process_lines(context)

    def test_require_package_path_in_line_missing_semicolon_start(self):
      with pytest.raises(ModuleNotFoundProcessorException):
        code = """package.path=package.path.. 'tests/input/?.lua'
  require('sample')"""
        context = ProcessorContext('tests/input/fake.lua', code.split('\n'), strict=True, verbose=True);
        result = process_lines(context)

    def test_require_package_path_missing_semicolon_end(self):
      with pytest.raises(ModuleNotFoundProcessorException):
        code = """package.path='tests/input/?.lua'.. package.path
  require('sample')"""
        context = ProcessorContext('tests/input/fake.lua', code.split('\n'), strict=True, verbose=True);
        result = process_lines(context)

    def test_require_package_path_unterminated(self):
      with pytest.raises(InvalidSyntaxProcessorException):
        code = """package.path='tests/input/?.lua".. package.path
  require('sample')"""
        context = ProcessorContext('tests/input/fake.lua', code.split('\n'), strict=True, verbose=True);
        result = process_lines(context)

    def test_require_package_path_runon(self):
      with pytest.raises(InvalidSyntaxProcessorException):
        code = """package.path='tests/input/?.lua".. package.path = 7
  require('sample')"""
        context = ProcessorContext('tests/input/fake.lua', code.split('\n'), strict=True, verbose=True);
        result = process_lines(context)

    def test_require_package_path_unallowed_variable(self):
      with pytest.raises(DynamicAssignmentProcessorException):
        code = """package.path=packg..'tests/input/?.lua"
  require('sample')"""
        context = ProcessorContext('tests/input/fake.lua', code.split('\n'), strict=True, verbose=True);
        result = process_lines(context)

    def test_require_package_path_invalid_string_escape(self):
      with pytest.raises(InvalidStringEscapeProcessorException):
        code = """package.path='tests\\x1234/input/?.lua'
  require('sample')"""
        context = ProcessorContext('tests/input/fake.lua', code.split('\n'), strict=True, verbose=True);
        result = process_lines(context)

    def test_require_package_path_depth_not_found(self):
      with pytest.raises(ModuleNotFoundProcessorException):
        code = """package.path=package.path ..';tests/input/?.lua'
  require('require-no-path')"""
        context = ProcessorContext('tests/input/fake.lua', code.split('\n'), strict=True, verbose=True);
        result = process_lines(context)
