import os
import re
from datetime import datetime
from typing import Dict, List, Optional, Tuple

from gql.transport.aiohttp import log as aiohttp_logger
from gql.transport.requests import log as request_logger
from gql.transport.websockets import log as websockets_logger
from pydantic import BaseModel

from highlighter._colors import ColoredString

# These loggers should be set in highlighter
# when they are added we can remove these
LOGLEVEL = os.environ.get("GQL_LOGLEVEL", "WARNING")
request_logger.setLevel(LOGLEVEL)
websockets_logger.setLevel(LOGLEVEL)
aiohttp_logger.setLevel(LOGLEVEL)

cs = ColoredString()
gt2pt = {
    "Int": "int",
    "Float": "float",
    "Boolean": "bool",
    "String": "str",
    "ISO8601DateTime": "datetime.datetime",
    "ID": "str",
    "JSON": "str"
}


def get_gql_schema(client: "HLClient"):
    request_str = """
        query IntrospectionQuery {
          __schema {
            queryType {
              name
            }
            mutationType {
              name
            }
            subscriptionType {
              name
            }
            types {
              ...FullType
            }
            directives {
              name
              description
              locations
              args {
                ...InputValue
              }
            }
          }
        }

        fragment FullType on __Type {
          kind
          name
          description
          fields(includeDeprecated: true) {
            name
            description
            args {
              ...InputValue
            }
            type {
              ...TypeRef
            }
            isDeprecated
            deprecationReason
          }
          inputFields {
            ...InputValue
          }
          interfaces {
            ...TypeRef
          }
          enumValues(includeDeprecated: true) {
            name
            description
            isDeprecated
            deprecationReason
          }
          possibleTypes {
            ...TypeRef
          }
        }

        fragment InputValue on __InputValue {
          name
          description
          type {
            ...TypeRef
          }
          defaultValue
        }

        fragment TypeRef on __Type {
          kind
          name
          ofType {
            kind
            name
            ofType {
              kind
              name
              ofType {
                kind
                name
                ofType {
                  kind
                  name
                  ofType {
                    kind
                    name
                    ofType {
                      kind
                      name
                      ofType {
                        kind
                        name
                      }
                    }
                  }
                }
              }
            }
          }
        }
    """
    return client.execute(request_str)


class Line(BaseModel):
    indent: int = 0
    line: str


BlankLine = Line(line='\n')


def inner_type(x: Dict) -> Optional[str]:
    def w(x: Optional[Dict]) -> Optional[str]:
        if x is None:
            return None
        if x['ofType'] is None and x['kind'] == 'OBJECT':
            return x['name']
        return w(x['ofType'])
    return w(x['type'])


def to_python_type(x) -> str:
    def recur(x) -> str:
        kind = x['kind']
        if kind == 'SCALAR':
            return gt2pt.get(x['name']) or x['name']
        elif kind == 'ENUM':
            return "str"

        elif kind == 'INPUT_OBJECT':
            return "Dict"

        elif kind == "LIST":
            return f"List[{recur(x['ofType'])}]"

        elif kind == 'NON_NULL':
            return recur(x['ofType'])

        else:
            raise ValueError(f"unknown kind {kind} detected")

    result = recur(x)
    if x['kind'] != 'NON_NULL':
        result = f"Optional[{result}]"
    return result


def to_gql_type(x) -> str:
    kind = x['kind']

    if kind in ['SCALAR', 'ENUM', 'INPUT_OBJECT']:
        return x['name']

    elif kind == "LIST":
        return f"[{to_gql_type(x['ofType'])}]"

    elif kind == "NON_NULL":
        return f"{to_gql_type(x['ofType'])}!"

    else:
        raise ValueError(f"tell me what kind we encountered here: {kind}")


def get_all_from(gql_schema: Dict, q_or_m: str) -> List[str]:
    types = gql_schema['__schema']['types']
    result = []
    for x in types:
        if x['name'] == q_or_m:
            for y in x['fields']:
                result.append(y['name'])
    return result


def get_all_mutations(gql_schema: Dict) -> List[str]:
    return get_all_from(gql_schema, 'Mutation')


def get_all_queries(gql_schema: Dict) -> List[str]:
    return get_all_from(gql_schema, 'Query')


def get_return_type(gql_schema: Dict, name: str, depth=0, max_depth=2) -> Optional[Dict]:
    # breakpoint()
    types = gql_schema['__schema']['types']
    if depth > max_depth:
        return None

    target = None
    for x in types:
        if x['name'] == name:
            target = x
            break

    if not target:
        return None

    result = {}
    for x in target['fields']:
        # print(x)
        it = inner_type(x)
        result[x['name']] = None
        if it:
            result[x['name']] = get_return_type(gql_schema, it, depth + 1)
            if result[x['name']] is None:
                # remove object type in the last object depth
                # solve problem where user -> account  and account -> user
                del result[x['name']]
    return result


def return_type_formatting(o, indent: int = 0) -> List[Line]:
    result = [Line(line="{", indent=indent)]
    for k in o:
        result.append(Line(line=k, indent=indent + 1))
        nested_obj = o.get(k)
        if nested_obj:
            result.extend(return_type_formatting(nested_obj, indent + 1))

    result.append(Line(line="}", indent=indent))
    return result


def get_gql_obj(gql_schema: Dict, name: str) -> Tuple[str, Dict]:
    types = gql_schema['__schema']['types']
    for x in types:
        if x['name'] in ['Query', 'Mutation']:
            for y in x['fields']:
                if y['name'] == name:
                    return x['name'], y
    raise ValueError(f" {name} not found")


def get_gql_request_str(gql_schema: Dict, name: str, max_depth: int, indent: int = 0) -> List[Line]:
    obj_type, target_gql_obj = get_gql_obj(gql_schema, name)

    arg_lst = []
    for x in target_gql_obj['args']:
        arg_lst.append((x['name'], to_gql_type(x['type'])))

    # python types
    return_type = inner_type(target_gql_obj)

    result = get_return_type(gql_schema, return_type, max_depth=max_depth)

    return [
        Line(line="%s _(" % obj_type.lower(), indent=indent),
        *[Line(line=f"${x}: {t}", indent=indent + 1) for x, t in arg_lst],
        Line(line=")", indent=indent),
        Line(line='{', indent=indent),
        Line(line=f"{name}(", indent=indent + 1),
        *[Line(line=f"{x}: ${x}", indent=indent + 2) for x, _ in arg_lst],
        Line(line=f")", indent=indent + 1),
        *return_type_formatting(result, indent=indent + 1),
        Line(line='}', indent=indent)
    ]


def get_imports():
    return [
        Line(line="from typing import Optional, List, Dict"),
        Line(line="from gql import gql"),
        Line(line="from client import get_client"),
        Line(line="import datetime"),
        Line(line="from enum import Enum")
    ]

#
# def generate_for_one_query_or_mutation(t: str, max_depth: int = 2) -> List[Line]:
#     obj_type, target_gql_obj = get_gql_obj(gql_schema, t)
#     py_pos_arg_lst = []
#     py_key_arg_lst = []
#     for x in target_gql_obj['args']:
#         py_type = to_python_type(x['type'])
#         if not py_type.startswith("Optional"):
#             py_pos_arg_lst.append((x['name'], py_type))
#         else:
#             py_key_arg_lst.append((x['name'], py_type))
#
#     args = [Line(line=f"{n}: {t} = None,", indent=1) if t.startswith("Optional") else Line(line=f"{n}: {t},", indent=1)
#             for n, t in py_pos_arg_lst + py_key_arg_lst]
#
#     return [
#         Line(line=f'{t}GQL = """'),
#         *get_gql_request_str(gql_schema, t, max_depth, indent=1),
#         Line(line='"""'),
#         BlankLine,
#         Line(line="def %s(" % t),
#         *args,
#         Line(line="):"),
#         Line(line="params = locals()", indent=1),
#         Line(line="non_null_params = {x: y for x, y in params.items() if y is not None}", indent=1),
#         Line(line=f"request_gql = gql({t}GQL)", indent=1),
#         Line(line="resp = client.execute(request_gql, variable_values=non_null_params)", indent=1),
#         Line(line=f"resp = resp['{t}']", indent=1),
#         Line(line='return resp', indent=1),
#     ]


# def generate_gql_bindings(ts: List[str], max_depth: int = 2, filename: str = 'generated.py'):
#     lines = [
#         *get_imports(),
#         BlankLine,
#         Line(line='client = get_client()'),
#         BlankLine
#     ]
#
#     for x in ts:
#         lines.extend(generate_for_one_query_or_mutation(x, max_depth=max_depth))
#         lines.append(BlankLine)
#
#     generated_str = "\n".join([" " * 4 * x.indent + x.line for x in lines])
#     # print(generated_str)
#     with open(filename, "w") as fp:
#         fp.write(generated_str)


# @click.group()
# def main():
#     pass
#
#
# @main.command()
# @click.option('--type', '-t', type=click.Choice(['query', 'mutation']), default=None)
# @click.option('--search', '-s', default=None)
# @click.option('--limit', '-l', default=5)
# def show(type: str, search: str, limit: int):
#     if type is None:
#         lst = get_all_queries(gql_schema) + get_all_mutations(gql_schema)
#     elif type.startswith('query'):
#         lst = get_all_queries(gql_schema)
#     else:
#         lst = get_all_mutations(gql_schema)
#
#     i = 0
#     for x in lst:
#         if i >= limit:
#             break
#
#         if search is not None:
#             if search.lower() in x.lower():
#                 i += 1
#                 click.echo(f"{i}. {x}")
#         else:
#             i += 1
#             click.echo(f"{i}. {x}")
#
#
# @main.command()
# @click.option('--name', '-n', 'names', multiple=True, default=None)
# @click.option('--max-depth', default=2)
# @click.option('--filename', default='generated.py')
# def generate(names: List[str], max_depth: int, filename: str):
#     available = get_all_queries(gql_schema) + get_all_mutations(gql_schema)
#     for x in names:
#         if x not in available:
#             raise ValueError(f"gql type {x} not found")
#
#     if not names:
#         names = available
#
#     generate_gql_bindings(names, max_depth=max_depth, filename=filename)
#     click.echo(f"save to {filename}...")
#
#
# def generate_input_base_models():
#     for x in gql_schema['__schema']['types']:
#         if x['kind'] == 'INPUT_OBJECT':
#             lines = [
#                 Line(line=f"class {x['name']}(BaseModel):"),
#                 *[Line(line=f"{f['name']}: {to_python_type(f['type'])}", indent=1) for f in x['inputFields']]
#             ]
#             generated_str = "\n".join([" " * 4 * x.indent + x.line for x in lines])
#             print(generated_str, end='\n\n')
#             pass
#         if x['kind'] == 'ENUM' and not x['name'].startswith('__'):
#             lines = [
#                 Line(line=f"class {x['name']}(str, Enum): "),
#                 *[
#                     Line(line=f"{v['name']}='{v['name']}'", indent=1)
#                     for v in x['enumValues']
#                 ]
#
#             ]
#             generated_str = "\n".join([" " * 4 * x.indent + x.line for x in lines])
#             print(generated_str, end='\n\n')
#
#         elif x['kind'] == 'SCALAR':
#             print(x)


class B(BaseModel):
    d: bool


class Experiment(BaseModel):
    createAt: datetime


class TrainingRun(BaseModel):
    createAt: datetime
    experiment: Experiment


def get_gql_return_type(b: BaseModel):
    try:
        if getattr(b, '_name', "") == "List":
            return get_gql_return_type(b.__args__[0])

        elif not issubclass(b, BaseModel):
            return None
    except:
        return None

    result = {}
    for n, f in b.__fields__.items():
        result[n] = get_gql_return_type(f.type_)
    return result


def snake_2_camel(s):
    first, *rest = s.split("_")
    return first + "".join(x.capitalize() for x in rest)


def camel_2_snake(s):
    return re.sub("([A-Z])", r"_\g<1>",  s).lower()

#
# class MyGQLClient:
#     def __init__(self):
#         self._schema = get_gql_schema()
#
#     def __getattr__(self, key):
#         key = snake_2_camel(key)
#
#         if key not in get_all_queries(self._schema) + get_all_mutations(self._schema):
#             raise ValueError(f"{key} is not a known query or mutation")
#
#         def f(*, return_type: BaseModel, **kwargs):
#             return_type_dict = get_gql_return_type(return_type)
#
#             obj_type, target_gql_obj = get_gql_obj(self._schema, key)
#
#             arg_lst = []
#             arg_names = [x['name'] for x in target_gql_obj['args']]
#             for k in kwargs:
#                 if k not in arg_names:
#                     raise ValueError(f"unknown gql arguement '{k}' for '{key}'")
#
#             for x in target_gql_obj['args']:
#                 if x['name'] in kwargs:
#                     arg_lst.append((x['name'], to_gql_type(x['type'])))
#
#             indent = 0
#             lines = [
#                 Line(line="%s _(" % obj_type.lower(), indent=indent),
#                 *[Line(line=f"${x}: {t}", indent=indent+1) for x, t in arg_lst],
#                 Line(line=")", indent=indent),
#                 Line(line='{', indent=indent),
#                 Line(line=f"{key}(", indent=indent+1),
#                 *[Line(line=f"{x}: ${x}", indent=indent+2) for x, _ in arg_lst],
#                 Line(line=f")", indent=indent+1),
#                 *return_type_formatting(return_type_dict, indent+1),
#                 Line(line='}', indent=indent)
#             ]
#
#             generated_str = "\n".join([" " * 4 * x.indent + x.line for x in lines])
#             #print(generated_str)
#             #get_client().execute(gql(generated_str), variable_values=kwargs)
#             print(generated_str)
#
#         return f
#
#     def hint(self, query_or_mutation: str):
#         obj_type, target_gql_obj = get_gql_obj(gql_schema, query_or_mutation)
#         py_pos_arg_lst = []
#         py_key_arg_lst = []
#         for x in target_gql_obj['args']:
#             py_type = to_python_type(x['type'])
#             if not py_type.startswith("Optional"):
#                 py_pos_arg_lst.append((x['name'], py_type))
#             else:
#                 py_key_arg_lst.append((x['name'], py_type))
#
#         args = [
#             Line(line=f"{n}: {t} = None,", indent=0) if t.startswith("Optional") else Line(line=cs.yellow(f"{n}: {t},"), indent=0)
#             for n, t in py_pos_arg_lst + py_key_arg_lst]
#         print(cs.red_black(query_or_mutation))
#         print("\n".join([" " * 4 * x.indent + x.line for x in args]))


# input_object object enum
# configuration
"""

{
    "Mutation or Query name": {
        ... what we want to return
    }

}

-> all the mutations and queries.

update python -> 3.10

grqphql enum type definition standard

"""

"""
1. find all the mutation or query arguments
2. find all the input_object from the arguments
3. recursive construct basemodels based on them.
4. for those argument (convert to gql format(key without quotes)
"""
#
#
# if __name__ == '__main__':
#
#     client = MyGQLClient()
#     client.createTrainingRun(return_type=TrainingRun,
#                                  researchPlanId="123",
#                                  experimentId="123",
#                                  modelId="123",
#                                  projectId="123")
#
#     # print()
#     #client.hint("createTrainingRun")
#
#
#
#
#     # a = "abCabc"
#     # b = "abc_abc"
#     # print(camel_2_snake(a))
#     # print(snake_2_camel(b))
#
#     #print(generate_input_base_models())
#     #generate_input_base_models() # input type
