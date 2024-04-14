# -*- coding: utf-8 -*-
"""
dsl helper
"""
import base64
import re
from functools import wraps

import six

import flybirds.core.global_resource as gr
import flybirds.utils.flybirds_log as log

# generate result_dic
from flybirds.core.global_context import GlobalContext
import time

if six.PY2:
    # -- USE PYTHON3 BACKPORT: With unicode traceback support.
    import traceback2 as traceback
else:
    import traceback

import asyncio
import nest_asyncio

nest_asyncio.apply()
tim_loop = asyncio.new_event_loop()


async def sleep_t(t):
    await asyncio.sleep(t)


def sleep(sleep_time):
    tim_loop.run_until_complete(sleep_t(sleep_time))


def add_res_dic(dsl_params, functin_pattern, def_key):
    result_dic = {}
    match_obj = re.match(functin_pattern, dsl_params)
    if match_obj is not None:
        """
        senario：

        Flight, verifyEle=center_content_layout, verifyAction=position
        textMatches=shanghai.?
        .?economic.?, fuzzyMatch=true
        text=freshmode, timeout=15, swipeCount=40


        multi properities，example：text=freshmode, timeout=15, swipeCount=40
        Match from back to front, match back first,swipeCount=40
        match_obj_group_1（text=freshmode, timeout=15）
        f the conditions are still met, split again, Until the split to the
        last item: text=
        """
        group_1 = match_obj.group(1).strip().replace(u"\u200b", "")
        result_dic[match_obj.group(2)] = match_obj.group(3)
        match_obj_group_1 = re.match(functin_pattern, group_1)

        while match_obj_group_1 is not None:
            match_obj_group_1 = re.match(functin_pattern, group_1)
            if match_obj_group_1 is not None:
                group_1 = (
                    match_obj_group_1.group(1).strip().replace(u"\u200b", "")
                )
                result_dic[
                    match_obj_group_1.group(2)
                ] = match_obj_group_1.group(3)
            else:
                result_dic[def_key] = group_1
                break
        else:
            result_dic[def_key] = group_1

    else:
        result_dic[def_key] = dsl_params.strip().replace(u"\u200b", "")
    # print('result_dic44444', result_dic)
    return result_dic


# generate result_dic
def params_to_dic(dsl_params, def_key="selector"):
    """
    Convert the parameters in the dsl statement into dict format for use in
    subsequent processes
    """
    result_dic = {}
    functin_pattern = re.compile(r"([\S\s]+),\s*([a-zA-Z0-9_]+)\s*=\s*(\S+)")
    if isinstance(dsl_params, str):
        result_dic = add_res_dic(dsl_params, functin_pattern, def_key)
    log.info("result_dic: {}".format(result_dic))
    return result_dic


def split_must_param(dsl_params):
    """
    Get must and optional parameters
    """
    result = dsl_params.split(",", 1)
    result[0] = result[0].strip().replace(u"\u200b", "")
    result[1] = result[1].strip().replace(u"\u200b", "")
    return result


def get_params(context, *args):
    """
    Get param from context
    :param context: step context
    :param args: A tuple containing value and parameter name
    :return:
    """
    items = []
    for (val, param_name) in args:
        if val is not None:
            items.append(replace_str(val))
        elif hasattr(context, param_name):
            items.append(replace_str(getattr(context, param_name)))
    return items


def return_value(value, def_value=None):
    """
    get global attribute value
    """
    if value is not None:
        return value
    return def_value


def is_number(s):
    """
    Determine if the parameter is a number
    """
    try:
        float(s)
        return True
    except ValueError:
        log.error(f"param {s} is not a number!")
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        log.error(f"param {s} cannot turn to a number!")
    return False


def replace_str(u_text):
    return u_text.strip().replace(u"\u200b", "")


def handle_str(un_handle_str):
    res = re.match(r"([\S\s]+),\s*[0-9_]+\s*", un_handle_str)
    if res is not None:
        return res.group(1)
    else:
        return un_handle_str


def str2bool(v):
    return v.lower() in ['true', '1', 't', 'y', 'yes', 'yeah', 'yup',
                         'certainly', 'uh-huh']


def get_use_define_param(context, param_name):
    use_define = context.get("use_define")
    log.info(f'use_define: {use_define}')
    params = [i for i in use_define if param_name + '=' in i]
    user_data = {}
    if len(params) > 0:
        if len(params) > 1:
            log.error(f'Cannot customize multiple parameters with the same '
                      f'name:{params}')
        value = params[0].split("=", 1)[1]
        user_data[param_name] = str(base64.b64decode(value), "utf-8")
    return user_data


def ele_wrap(func):
    @wraps(func)
    def wrapper_func(*args, **kwargs):
        try:
            context = args[0]
            for (k, v) in kwargs.items():
                if v is None:
                    if hasattr(context, k):
                        v = getattr(context, k)
                    else:
                        log.warn(f'[ele_wrap] step param:[{k}] is none.')
                        continue
                v = replace_str(v)
                if 'selector' in k:
                    selector_str = v
                    ele_key = v.split(',')[0]
                    ele_value = gr.get_ele_locator(ele_key)
                    v = selector_str.replace(ele_key, ele_value, 1)
                    older = v
                    if gr.get_platform() and gr.get_platform().lower() == 'web':
                        # jquery path change to playwright path
                        pattern = re.compile(r'(:eq\((\d+)\))')
                        all_match = pattern.findall(v)
                        if all_match and len(all_match) > 0:
                            for mtch in all_match:
                                re_key = mtch[0]
                                re_value = ">> nth=" + mtch[1] + " >>"
                                v = v.replace(re_key, re_value)
                            v = v.strip(">>")
                            log.info(f"=============find jquery path {older} ==== change to {v}")

                new_v = get_global_value(v)
                if new_v is not None:
                    v = new_v
                kwargs[k] = v
            func(*args, **kwargs)
            if gr.get_value("debug", False):
                if hasattr(GlobalContext, "debug_console"):
                    GlobalContext.debug_console.set_step_status("pass")
        except Exception as e:
            if not gr.get_value("debug", False):
                raise e
            else:
                log.info(f'ele_wrap error: {traceback.format_exc()}')
                if hasattr(GlobalContext, "debug_server_thread"):
                    GlobalContext.debug_server_thread.start_debug()

        # Do something after the function.

    return wrapper_func


def get_global_value(v):
    projectScript = gr.get_value("projectScript")
    if projectScript is not None:
        if hasattr(projectScript, "custom_operation"):
            custom_operation = projectScript.custom_operation
            if custom_operation is not None and hasattr(custom_operation,
                                                        "get_global_value"):
                rp = custom_operation.get_global_value(v)
                if rp is not None:
                    return rp
        elif hasattr(projectScript, "app_operation"):
            app_operation = projectScript.app_operation
            if app_operation is not None and hasattr(app_operation,
                                                     "get_global_value"):
                rp = app_operation.get_global_value(v)
                if rp is not None:
                    return rp
    return None


class VerifyStep:
    def __init__(self, *args, **kwargs):  # 类装饰器参数
        self.verify = True
        self.num_calls = 0

    def __call__(self, func):  # 被装饰函数
        @wraps(func)
        def wrapper(*args, **kwargs):
            if GlobalContext.get_global_cache("verifyStepCount") is not None:
                GlobalContext.set_global_cache("verifyStepCount",
                                               GlobalContext.get_global_cache(
                                                   "verifyStepCount") + 1)
            return func(*args, **kwargs)

        return wrapper


class RetryType:
    def __init__(self, *args, **kwargs):  # 类装饰器参数
        self.retry = args[0]

    def __call__(self, func):  # 被装饰函数
        @wraps(func)
        def wrapper(*args, **kwargs):
            if gr.get_platform() is not None \
                    and gr.get_platform().lower() == "web":
                self.retryTimeOut = gr.get_frame_config_value("retry_ele_timeout", 30)

                self.waitTimeInterval = max(self.retryTimeOut // 30, 1)
                self.retryTimes = max(self.retryTimeOut // self.waitTimeInterval, 1)
                self.recordMaxRetryTimes = self.retryTimes
                self.runSuccess = False
                log.info(
                    f'retry start retryTimeOut: {self.retryTimeOut}s, self.waitTimeInterval: {self.waitTimeInterval}s, maxRetryTimes: {self.recordMaxRetryTimes}')
                while self.retryTimes > 0:
                    try:
                        func(*args, **kwargs)
                        self.runSuccess = True
                        if self.runSuccess == True:
                            log.info(
                                f'retry success, max retry times: {self.recordMaxRetryTimes},  retry times: {self.recordMaxRetryTimes - self.retryTimes}')
                            break
                    except Exception as e:
                        self.retryTimes -= 1
                        if self.retryTimes == 0:
                            log.info(f'retry fail during {self.retryTimeOut}s, retry times: {self.recordMaxRetryTimes}')
                            raise e
                        else:
                            log.info(
                                f'retry sleep interval {self.waitTimeInterval}s，current retry times: {self.recordMaxRetryTimes - self.retryTimes}')
                            sleep(self.waitTimeInterval)
                            pass
            else:
                func(*args, **kwargs)

        return wrapper