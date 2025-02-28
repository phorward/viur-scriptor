from .utils import is_pyodide_context

if is_pyodide_context():
    from js import eval as js_eval, self as _self, Blob
    from js import console

    import manager
else:
    import asyncio
    import click

import time
import datetime
import time
import math

async def wait():
    if is_pyodide_context():
        while manager.resultValue is None:
            await manager.sleep(250)
    else:
        await asyncio.sleep(250)

async def alert(text: str):
    if is_pyodide_context():
        _self.postMessage(type="alert", text=text)
        await wait();
        manager.reset()
        manager.resultValue = None
    else:
        click.prompt("Press a key")
        

async def confirm(title: str, text: str, cancel: bool = False) -> str:
    if is_pyodide_context():
        _self.postMessage(type="confirm", title=title, text=text, cancel=cancel)
        await wait(); 
        tmp = manager.copyResult()
        manager.reset()
        manager.resultValue = None

        return tmp
    else:
        value = 0
        try:
            value = int(click.confirm(text, abort=True))
        except:
            value = -1
        return value


# time = true
# datetim-picker local


async def input(title: str, text: str, type: str, use_time: bool = False, empty: bool = False):
    if is_pyodide_context():
        _self.postMessage(type="input", title=title, text=text, input_type=type, use_time=use_time, empty=empty)
        await wait(); 
        tmp = manager.copyResult()
        manager.reset()
        manager.resultValue = None

        if type == "date":
            console.error(tmp)
            return datetime.datetime.fromtimestamp(math.floor(tmp/1000.0))
        
        return tmp
    else:
        click.echo(title)
        ret = click.prompt(text)
        if type == "date":
            def validate_date(date_text):
                try:
                    return datetime.date.fromisoformat(date_text)
                except ValueError:
                    click.echo("Incorrect data format, should be YYYY-MM-DD")

            
                return None

            def validate_datetime(date_text):
                try:
                    return datetime.datetime.fromisoformat(date_text)
                except ValueError:
                    click.echo("Incorrect data format, should be YYYY-MM-DD HH:MM:SS")
            
                return None
 
            if use_time:
                while not validate_date(ret):
                    ret = click.prompt(text)
            else:
                while not validate_datetime(ret):
                    ret = click.prompt(text)
            
            return ret
        elif type == "number":
            def check_number(value: str):
                try:
                    r = float(value.replace("," "."))
                    return ret
                except:
                    try:
                        r = int(value)
                        return r
                    except:
                        return None
                return None
            while True:
                ret = check_number(ret)
                if ret is None:
                    click.echo("Enter a valid number.")
                    ret = click.prompt(text)
                else:
                    break

            return ret
        else:
            return ret

async def input_date(*args, **kwargs):
    kwargs.update({"type": "date"})
    return await input(*args, **kwargs)

async def input_number(*args, **kwargs):
    kwargs.update({"type": "number"})
    return await input(*args, **kwargs)

async def input_string(*args, **kwargs):
    kwargs.update({"type": "string"})
    return await input(*args, **kwargs)

async def input_text(*args, **kwargs):
    kwargs.update({"type": "text"})
    return await input(*args, **kwargs)

input.date = input_date
input.number = input_number
input.text = input_text
input.string = input_string

if is_pyodide_context():
    from pyodide.ffi import to_js


async def select(title: str, text: str, choices: list[int], multiple: bool = False):

    _choices = choices
    if is_pyodide_context():
        _choices = to_js(_choices)

        _self.postMessage(type="select", title=title, text=text, choices=_choices, multiple=multiple)
        await wait(); 

        tmp = manager.resultValue
        if multiple:
            tmp = list(tmp)
        manager.reset()
        manager.resultValue = None

        return tmp
    else:
        click.echo(title)
        text += "\n\n"
        for i, _ in enumerate(choices):
            text += str(choices[i]) + (", " if i != len(choices)-1 else "")
            if i > 0 and i % 3 == 0:
                text += "\n"
            
        lower_choices = [e.lower() for e in choices]
        result_value = -1
        while True:
            _ret = click.prompt(text)
            if not multiple:
                if _ret.lower() in lower_choices:
                    result_value = lower_choices.index(_ret.lower())
                    break
                else:
                    click.echo("You entered a invalid input!")
            else:
                if _ret.find(",") == -1:
                    if _ret.lower() in lower_choices:
                        result_value = [lower_choices.index(_ret.lower()), ]
                        break
                    else:
                        click.echo("You entered a invalid input!")

                else:
                    result = _ret.split(",")
                    valid = True
                    result_value = []
                    for res in result:
                        _tmp = res.lower().lstrip()
                        if not (_tmp in lower_choices):
                            valid = False
                            break
                        result_value.append(lower_choices.index(_tmp))

                    if not valid:
                        click.echo("You entered a invalid input!")
                        continue
                    break

        return result_value



    return None


