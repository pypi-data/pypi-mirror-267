import os
import re

from enum import StrEnum
from pathlib import Path


CWD = os.getcwd()

# https://is.gd/4s1GdR
# tl;dr: I chose it, I published it, it's baked in, it's too late to change it! Thank you for understanding.
PACKAGES_DIR = '.tic_pkgs'
PACKAGE_PATH_VAR = 'package.path'
DEFAULT_TIC_80_PATH = [
  CWD + '/lua/?.lua',
  CWD + '/lua/?/init.lua',
  CWD + '/?.lua',
  CWD + '/?/init.lua',
  CWD + '/../share/lua/5.3/?.lua',
  CWD + '/../share/lua/5.3/?/init.lua',
  # Not understanding these values... they're functionally equivalent to the
  # upper ones, since TIC-80 doesn't seem to interpret them as relative to the
  # loaded cart's location.
  #'./?.lua',
  #'./?/init.lua'
]

class MagicComment(StrEnum):
  """
    Supported 'magic' comment types used by this build system
  """
  GROUP_START='#group:start'
  GROUP_END='#group:end'
  IMPORT='#import'
  INCLUDE='#include'
  EXPORTS='#exports'

class ProcessorGroup:
  def __init__(self, name, disabled):
    self.name = name
    self.disabled = disabled

class ProcessorRequires:
  def __init__(self, context, root=None):
    self.context = context
    self.root = root if root else self
    self.semicolon = False

    if self.root == self:
      self.index = 0
      self.loaded = dict()
      self.output = []

    if 'LUA_PATH' in os.environ:
      self.path = os.environ['LUA_PATH'].trim().split(';')
    else:
      # This is what TIC-80 spits out as its default package.path value
      self.path = list(DEFAULT_TIC_80_PATH)

  def write(self):
    return '\n'.join(self.root.output)

  def exists(self):
    return self.root == self and len(self.loaded) > 0

  def get_name(self, index):
    return f'__syllogistic_require_' + str(index)

  def add_require(self, module):
    # As per the docs, if we've already loaded it we're to return it, even if we
    # wouldn't be able to find it in the current file's package.path
    # https://www.lua.org/pil/8.1.html
    if not module in self.root.loaded:
      found_path = None
      paths_tried = []

      for path in self.path:
        path = path.replace('?', module)
        paths_tried.append(f'no file `{path}`')

        if os.path.exists(path):
          found_path = path
          break

      if not found_path:
        trace = '\n' + '\n'.join(paths_tried) if self.context.verbose else ''
        raise ModuleNotFoundProcessorException(f'Module {module} not found{trace}', self.context)

      self.root.index += 1
      self.root.loaded[module] = self.root.index

      # Technically a race, since the file could be deleted after we tested
      # existence but not something to really care about for this program...
      with open(found_path, 'r') as file:
        lines = file.read().split('\n')
        index = self.root.index
        content = process_lines(ProcessorContext(
          found_path,
          lines,
          context=self.context
        ))
        self.root.output.append(f'function {self.get_name(index)}() {content} end')

    return self.get_name(self.root.loaded[module])

  def get_path(self):
    return ';'.join(self.path)

  def set_path(self, path):
    stripped = path.strip()
    self.semicolon = stripped.endswith(';')
    self.path = [part for part in stripped.split(';') if part != '']

  def append_path(self, path):
    stripped = path.strip()
    semistart = stripped.startswith(';')
    semicolon = stripped.endswith(';')
    parts = stripped.split(';')

    # Look, if you ended your last bit without a semicolon that's not my fault
    if not self.semicolon and not semistart:
      self.path[-1] = self.path[-1] + parts[0]
      parts = parts[1:]

    self.semicolon = semicolon
    self.path.extend([part for part in parts if part != ''])

class ProcessorContext:
  requires = None
  exports = set()
  groups = []
  disabled = False
  line = None
  number = -1

  # Refactor to figure out how to do this in a way that's not a bunch of optional arguments?
  def __init__(
    self,
    path,
    lines,
    strict=False,
    files=None,
    aka=None,
    included=None,
    excluded=None,
    watched=False,
    root=None,
    verbose=False,
#    requires=None,
    context=None
  ):
    self.path = path
    self.lines = lines
    self.aka = aka

    if context:
      self.strict = context.strict
      self.files = context.files
      self.included = set(context.included) if included is None else included
      self.excluded = set(context.included) if excluded is None else excluded
      self.watched = context.watched
      self.is_root = False
      self.root = context.root
      self.verbose = context.verbose
      self.requires = ProcessorRequires(self, context.requires.root)
    else:
      self.strict = strict
      self.files = set() if files is None else files
      self.aka = aka
      self.included = set() if included is None else included
      self.excluded = set() if excluded is None else excluded
      self.watched = watched
      self.is_root = root is None
      self.root = os.path.dirname(os.path.abspath(path)) if root is None else root
      self.verbose = verbose
      self.requires = ProcessorRequires(self)

    # Remove last newline if present
    if self.lines[-1] == '':
      self.lines.pop()

  def current_group(self):
    return self.groups[-1]

  def _update_status(self):
    # We might be checking his often so it makes sense to do it on group
    # add/remove rather than on every access to the enabled prop
    disabled = False

    for group in self.groups:
      if group.disabled:
        disabled = True
        break

    self.disabled = disabled

  def _is_disabled(self, name, default):
    if name in self.included:
      return False
    elif name in self.excluded:
      return True

    return default

  def push_group(self, name):
    if name.startswith('-'):
      name = name[1:]
      self.groups.append(ProcessorGroup(name, self._is_disabled(name, True)))
    else:
      if name.startswith('+'):
        name = name[1:]
      self.groups.append(ProcessorGroup(name, self._is_disabled(name, False)))

    self._update_status()

  def pop_group(self, name):
    if name != self.current_group().name:
      raise InvalidSyntaxProcessorException(f"Invalid group '{name}' nesting", self)

    self.groups.pop()
    self._update_status()

class ProcessorException(Exception):
  def __init__(self, message, context):
    super().__init__(message)

    self.file = context.path
    self.line = context.number

class ModuleNotFoundProcessorException(ProcessorException):
  pass

class DynamicModuleProcessorException(ProcessorException):
  pass

class DynamicAssignmentProcessorException(ProcessorException):
  pass

class InvalidSyntaxProcessorException(ProcessorException):
  pass

class InvalidStringEscapeProcessorException(ProcessorException):
  pass



def raise_concern(message, context):
  if context.strict:
    raise ProcessorException(message, context)

  prefix = '\n' if context.watched else ''
  print(prefix + 'Warning: ' + message)

# Important stuff
def resolve_package(context, path, mangled):
  name = path.split('/')[0]
  current = Path(context.root)
  drive = os.path.splitdrive(path)

  # Allowing C:// style abs paths does seem to accidentally work, but I don't
  # want to be on the hook for continuing to support anything other than *nix-
  # style pathing that, if needed, is easy to convert to the local system's.
  if drive[0] != '':
    raise ProcessorException(f"Invalid package name '{name}'", context)

  # Check for reserved names
  if re.match(r'^\W', path):
    raise ProcessorException(f"Invalid package name '{name}'", context)

  # There's probably some better way of walking up and doing this?
  while not current.joinpath(PACKAGES_DIR, path).exists() and current.name:
    current = current.parent

  # Fall back to the user's home directory
  if not current.joinpath(PACKAGES_DIR, path).exists():
    current = Path.home()

  if not current.joinpath(PACKAGES_DIR, path).exists():
    # Unmangle our sugar
    if mangled:
      name = re.sub(r'[/\\]index.lua', '', name)
    raise ModuleNotFoundProcessorException(f"Unable to resolve package '{name}'", context)

  # os.path.abspath is to match our usages of that elsewhere so things are consistent
  return os.path.abspath(str(current.joinpath(PACKAGES_DIR, path).absolute()))

def process_include(context, args):
  if not context.disabled:
    path = ''
    terminated = 1
    included = context.included
    excluded = context.excluded
    aka = None
    mangled = False

    if args[0].startswith("'") and not args[0].endswith('"'):
      terminated = -1

      for i in range(len(args)):
        path += args[i]

        if args[i].endswith("'"):
          terminated = i + 1
          break

      if terminated == -1:
        raise InvalidSyntaxProcessorException("Unterminated ' in include", context)

      # remove quotes
      path = path[1:-1]

      # Probably a better way to do that...
      if not os.path.splitext(path)[1]:
        mangled = True
        path = os.path.join(path, 'index.lua')

    if len(args) > terminated and args[terminated] == 'as':
      terminated += 1

      if len(args) > terminated:
        aka = args[terminated]
        terminated += 1
      else:
        raise InvalidSyntaxProcessorException('Invalid import, missing name after \'as\'', context)

    # process remainder
    for i in range(terminated, len(args)):
      items = args[i].split(',')

      if items[0].startswith('+'):
        items[0] = items[0][1:]
        included = included.union(set(items))
      elif items[0].startswith('-'):
        items[0] = items[0][1:]
        excluded = excluded.union(set(items))
      else:
        raise_concern(f"Unrecognized group modifier prefix '{items[0][0]}', ignoring", context)

    if len(included.intersection(excluded)):
      raise_concern('Group names duplicated between include and exclude in include', context)

    # Handle relative paths
    if path.startswith('.'):
      # dirname is safe to do here since we added index.lua above for folders
      parent = os.path.dirname(context.path)
      path = os.path.join(parent, path)

    elif path and not path.startswith('/'):
      path = resolve_package(context, path, mangled)

    if not path:
      raise InvalidSyntaxProcessorException('Invalid include path; Did you forget quotes?', context)

    fullpath = os.path.abspath(path)

    if not fullpath in context.files:
      try:
        with open(path, 'r') as file:
          # Succeed in opening, *then* add to the list of files
          context.files.add(fullpath)

          return process_lines(ProcessorContext(
            path,
            file.read().split('\n'),
            aka=aka,
            included=included,
            excluded=excluded,
            context=context
          ))
      except FileNotFoundError:
        raise ModuleNotFoundProcessorException(f"Unable to locate included file '{path}'", context)
    else:
      # Future improvements could maybe seek to like remove other copies and replace them with this one if it would be a superset
      # of the original include
      raise_concern(f"File '{path}' included more than once; Did you include a file also included by your dependencies?", context)

  return None

def process_group_start(context, args):
  context.push_group(args[0])
  return None

def process_group_end(context, args):
  context.pop_group(args[0])
  return None

def process_exports(context, args):
  context.exports = set(args[0].split(','))
  return None

def process_import(context, args):
  if context.enabled:
    raise_concern('Import not supported. Use include.', context)
  return None

def process_unknown(context, args):
  if len(args) and args[0].startswith('#'):
    raise_concern(f"Unrecognized magic comment '{command}', skipping", context)
    return None
  return context.line

# https://www.lua.org/pil/2.4.html
supported_escapes = {
  'f': '\f',
  # New lines and carriage returns probably aren't supported in paths but...
  'n': '\n',
  'r': '\r',
  't': '\t',
  '\\': '\\',
  '"': '"',
  "'": "'",
  '[': '[',
  ']': ']'
}

# Only handles simple escapes, presumed ASCII so no \uXXXX
# Yes, there's built-in stuff to handle some forms of escape-encoded strings,
# but they all seem to have drawbacks:
# https://stackoverflow.com/questions/1885181/how-to-un-escape-a-backslash-escaped-string
def unescape(name, quote, context):
  unescaped_name = ''
  escaped = False

  for i in range(len(name)):
    char = name[i]

    if char == quote and not escaped:
      raise ProcessorException('Unsupported dynamic module name in require', context)

    if char == '\\' and not escaped:
      escaped = True
    elif escaped:
      if char in supported_escapes:
        unescaped_name += supported_escapes[char]
        escaped = False
      else:
        raise InvalidStringEscapeProcessorException('Invalid string escape in module name in require', context)
    else:
      unescaped_name += char

  return unescaped_name

# TODO This and all the other stuff needs to be replaced with proper AST stuff.
def parse_rvalue(remainder, context):
  rvalue = []
  part = ''
  quote = None
  escaped = False
  dot = False
  package_path_index = 0

  for i in range(len(remainder)):
    char = remainder[i]

    if escaped:
      if char in supported_escapes:
        part += char
        escaped = False
      else:
        raise InvalidStringEscapeProcessorException(f'Invalid string escape in {PACKAGE_PATH_VAR} assignment', context)
    elif char == quote:
      rvalue.append(part)
      part = ''
      quote = None
    elif char == '\\':
      escaped = True
    elif quote:
      part += char
    elif char == '"' or char == "'":
      quote = char
    elif char == '.' and (package_path_index == 0 or package_path_index == len(PACKAGE_PATH_VAR)):
      if dot:
        # Don't append '..' as we're doing the work to determine it's valid and don't want it in the output
        dot = False
      else:
        # Should just be package.path at this point
        if len(part):
          if part == PACKAGE_PATH_VAR:
            rvalue.append(part)
            part = ''
            package_path_index = 0
          else:
            raise DynamicAssignmentProcessorException(f'Unsupported dynamic {PACKAGE_PATH_VAR} assignment', context)
        dot = True
    elif char == ';':
      # This would be a syntax error trap below in all cases... I think?
      if len(part):
        rvalue.append(part)
        part = ''
        break
    elif package_path_index < len(PACKAGE_PATH_VAR) and char == PACKAGE_PATH_VAR[package_path_index]:
      part += PACKAGE_PATH_VAR[package_path_index]
      package_path_index += 1
    elif char == '=':
      raise InvalidSyntaxProcessorException(f'Invalid syntax in {PACKAGE_PATH_VAR} assignment', context)
    elif not re.match(r'\s', char):
      # Found a variable that's not package.path
      if i > 0 and not re.match(r'\s', remainder[i - 1]):
        raise DynamicAssignmentProcessorException(f'Unsupported dynamic {PACKAGE_PATH_VAR} assignment', context)

      # Lua lines can have multiple statements separated by a space instead of a semicolon.
      # Such fun.
      i = i - 1
      break

  if rvalue[:-1] == '..' or dot or quote or escaped:
    raise InvalidSyntaxProcessorException(f'Invalid syntax in {PACKAGE_PATH_VAR} assignment', context)

  # Line ends with package.path
  if part == PACKAGE_PATH_VAR:
    rvalue.append(PACKAGE_PATH_VAR)

  return (rvalue, i + 1)

# args could just be 'match' but this better aligns with the params passed to
# other processing functions line could also be passed to them, but they don't
# need it (yet)
def process_require(context, args, line):
  match = args[0]
  value = match.group(1)
  name = None
  quote = None

  if len(value):
    quote = value[0]
    endquote = value[-1]

    # We could scan this to check for the concatenation operator (..) but that's
    # also a valid parent path indicator so...
    if quote != endquote or not (quote == "'" or quote == '"'):
      raise DynamicModuleProcessorException('Unsupported dynamic module name in require', context)

    # strip quotes
    name = unescape(value[1:-1], quote, context)

  if not name:
    raise ModuleNotFoundProcessorException('Missing module name in require', context)

  require = context.requires.add_require(name)
  return line[0:match.start(0)] + require + '()' + line[match.end(0):]

def process_package_path(context, args, line):
  start = args[0].find('=') + 1
  parts, last_index = parse_rvalue(args[0][start:], context)
  path = context.requires.get_path()

  for i in range(len(parts)):
    part = parts[i].strip()

    if part == PACKAGE_PATH_VAR:
      if i > 0:
        context.requires.append_path(path)
    elif i == 0:
      context.requires.set_path(part)
    else:
      context.requires.append_path(part)

  
  # Strip lines that are empty after processing the package.path
  line = (line[0:args[1]] + line[args[1] + start + last_index:]).strip()

  return line if len(line) > 0 else None

def process_lines(context):
  output = []

  for i in range(len(context.lines)):
    context.line = context.lines[i]
    context.number = i
    processed = context.line

    if context.line.strip().startswith('--'):
      parts = context.line.strip().split()
      directive = parts[1] if len(parts) > 1 else ''
      args = parts[2:] if len(parts) > 2 else []

      # This could be refactored into a map -> processor since they currently
      # take all the same arguments and with the context, there's no real reason
      # for any to take different arguemnts except for convenience
      match directive:
        case MagicComment.GROUP_START:
          processed = process_group_start(context, args)

        case MagicComment.GROUP_END:
          processed = process_group_end(context, args)

        case MagicComment.IMPORT:
          processed = process_import(context, args)

        case MagicComment.INCLUDE:
          processed = process_include(context, args)

        case MagicComment.EXPORTS:
          processed = process_exports(context, args)

        case _:
          processed = process_unknown(context, args)

    elif context.line.find('require') != -1:
      match = re.search(r'require\(([^)]*)\)', context.line)

      if match:
        processed = process_require(context, [match], context.line)

    elif (index := context.line.find(PACKAGE_PATH_VAR)) != -1 and index < context.line.find('='):
      processed = process_package_path(context, [context.line[context.line.find(PACKAGE_PATH_VAR):], index], context.line)

    # We want to preserve line breaks from the input, but not ones that would be
    # caused by our preprocessing.
    if not context.disabled and not processed is None:
      output.append(processed)

  output = '\n'.join([line for line in output if not line is None])

  if context.requires.exists():
    output = context.requires.write() + '\n' + output

  if len(context.exports) and context.aka:
    output = context.aka + '={__autogen=true}\n' + output

    # FIXME This really needs a proper parser to get context and determine if we should be replacing something...
    for export in context.exports:
      output = re.sub(
        r'(?:(?<=\n)' + export + r'(?=\W))|(?:(?<![\w.])' + export + r'(\.))|(?:(?<=function )' + export + r'(?=\W))',
        f'{context.aka}.{export}\\1', output
      )

  return output

