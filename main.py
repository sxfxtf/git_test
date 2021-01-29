#!/user/bin/env python
# -*- coding:UTF-8 -*-
# Author:Young.Shi
# Date: 2020-10-23

'''
执行流程:
导包,如果没有则pip install 安装
查找是否有各个码头的文件夹,如果没有则创建.
判断各个文件夹里是否有文本,没有提示.
'''
import time
import os1
import random
# import json
# import pandas

try:
    import requests
except Exception:
    os.system("pip install requests -i https://mirrors.aliyun.com/pypi/simple/")

try:
    import json
except Exception:
    os.system("pip install json -i https://mirrors.aliyun.com/pypi/simple/")

try:
    import pandas
except Exception:
    os.system("pip install pandas -i https://mirrors.aliyun.com/pypi/simple/")

try:
    from lxml import etree
except Exception:
    os.system("pip install lxml -i https://mirrors.aliyun.com/pypi/simple/")

try:
    #xlwt和openpyxl是 pandas调用的2个库,也需要检测是否有下载
     import xlwt
except Exception:
    os.system("pip install xlwt -i https://mirrors.aliyun.com/pypi/simple/")

try:
    # xlwt和openpyxl是 pandas调用的2个库,也需要检测是否有下载
     import openpyxl
except Exception:
    os.system("pip install openpyxl -i https://mirrors.aliyun.com/pypi/simple/")

class terminal_check:
    select_lists = [
        ("二期", "nbct"),
        ("三期", "nbsct"),
        ("四期", "nbgjct"),
        ("大榭", "nbdxct"),
        ("梅山", "nbmsct")

    ]

    def __init__(self):
        self.base_pth = os.path.dirname(__file__)
        self.excel_writer = pandas.ExcelWriter(os.path.join(self.base_pth, "放行信息结果.xls"))
        self.file_list = None
        self.terminal_name = None
        self.run()

    def run(self):
        self.check_dir()
        self.handler()

    def check_dir(self):
        '''检测程序文件夹是否存在'''
        for select_list in self.select_lists:
            check_dir_path = os.path.join(self.base_pth, select_list[0])
            if not os.path.exists(check_dir_path):
                os.mkdir(check_dir_path)

    def handler(self):
        rets = self.select_result_verify()
        if isinstance(rets, list):
            '''正常情况下,rets返回的是一组列表, 比如[0,1,3] 表示要抓取这几个索引的码头数据,返回字符串就是报错信息'''
            for ret in rets:
                if not self.check_dirhasfile(ret):
                    print("程序运行失败,请检查[%s]文件夹下是否有并且只有一个文本?" % self.select_lists[ret][0])
                    break
                if os.path.getsize(self.file_list) == 0:
                    print("程序运行失败,请检查[%s]文件是否为空?" % self.file_list)
                    break

                if hasattr(self, self.select_lists[ret][1]):
                    # print("self.file_list是%s"%self.file_list)
                    # print("self.select_lists[ret][0]是%s"% self.select_lists[ret][0])
                    # print("self.select_lists[ret][1]是%s" % self.select_lists[ret][1])
                    self.terminal_name = self.select_lists[ret][0]
                    self.fun = getattr(self, self.select_lists[ret][1])
                    self.get_respons()
                    # fun()
                else:
                    print("没有找到%s的程序函数,无法执行" % self.select_lists[ret][0])
        elif isinstance(rets, str):
            print(rets)

    def select_result_verify(self):
        '''对选择结果进行比对
        1.比对是否有逗号分隔符
        2.数字有没有超出码头的总数
        3.对分割数字进行字符串去空
        4.强转为int类型'''
        ret = self.start_select()
        if not "," in ret and len(ret) > 1:
            return "序号要用逗号分割,请检查"
        rets = ret.split(",")
        final_ret = [int(i.strip().replace(" ", "")) for i in rets]
        max_num = max(final_ret)
        if max_num > len(self.select_lists):
            return "最大序号为%s , 你的最大序号为%s,请检查你输入的序号" % (len(self.select_lists) - 1, max_num)
        return final_ret

    def check_dirhasfile(self, index):
        '''检测查询文件夹里是否有文本'''
        file_path = self.base_pth + "/%s" % self.select_lists[index][0]
        # print("检查文档路径%s下有没有文件"%file_path)
        file_name = os.listdir(file_path)

        if file_name and len(file_name) == 1:
            self.file_list = os.path.join(file_path, file_name[0])
            return self.file_list
        else:
            return False

    def check_file_isblank(self):
        '''检测文本内容是否为空'''
        pass

    def start_select(self):
        '''让用户选择要运行哪个码头的爬虫程序'''
        print("请选择你要查询的码头")
        [print("序号%s>>>码头%s" % (idx, select_list[0])) for idx, select_list in enumerate(self.select_lists)]
        return input("支持多个查询,中间用逗号割开  比如0,1,2 \n")

    def requests_get(self, url, headers):
        return requests.get(url=url, headers=headers)

    def nbct(self, container):
        '''二期码头爬取程序'''
        dic = {}
        # dic={"箱号":"","码头放行":"","中转港代码":"","船名航次":"","提单号":""}
        url = "https://cx.nbct.com.cn:7002/api/containerinfo"
        data = {
            "cntrId": container
        }
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36",
            "Content-Type": "application/json;charset=UTF-8",
            "Referer": "https://cx.nbct.com.cn:7002/cntrinfo/cntrainerinfo",
        }

        ret = requests.post(url=url, headers=headers, data=json.dumps(data)).json()
        if ret["flag"] and not ret["errMsg"]:  # 代表有返回信息,没有错误信息
            release_data = ret["data"]
            dic.update(
                {"箱号": release_data["cntrId"], "码头放行": release_data["terminalRelease"], "中转港代码": release_data["port"],
                 "船名航次": release_data["exvsvy"], "提单号": release_data["cabl"].strip()})
        elif not ret["flag"] and ret["errMsg"]:  # 没有返回信息,只有报错信息
            dic.update(
                {"箱号": container, "码头放行": ret["errMsg"], "中转港代码": ret["errMsg"],
                 "船名航次": ret["errMsg"], "提单号": ret["errMsg"]})

        return dic

    def nbmsct(self, container):
        '''梅山码头爬取程序'''
        dic = {}
        # dic={"箱号":"","码头放行":"","中转港代码":"","船名航次":"","提单号":""}
        url = "http://msict.nbport.com.cn/mall-portal/member/queryCTOSForBLCTMS/searchAct.action?ctnno=%s" % container

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36",
            "Referer": "http://msict.nbport.com.cn/mall-portal/index.html",
        }

        ret = requests.get(url=url, headers=headers).json()
        if ret["resultObjects"]["result"]:  # 代表有返回信息,没有错误信息
            release_data = ret["resultObjects"]["result"][0]
            dic.update(
                {"箱号": release_data["ctnNo"],
                 "码头放行": release_data["releaseFlag"] if release_data["releaseFlag"] else "N",
                 "中转港代码": release_data["dischargePortCode"],
                 "船名航次": "%s-%s" % (release_data["vesselCode"], release_data["outboundVoyage"]), "提单号": "梅山箱子不抓取提单号"})
            # 梅山放行的箱子没有提单号，未放行的却有提单号，为了避免混淆统一不抓取

        elif not ret["resultObjects"]["result"]:
            # 没有找到箱号记录
            dic.update(
                {"箱号": container, "码头放行": "无记录", "中转港代码": "无记录",
                 "船名航次": "无记录", "提单号": "无记录"})
        # print(dic)
        return dic

    def nbgjct(self, container):
        dic = {}
        # dic={"箱号":"","码头放行":"","中转港代码":"","船名航次":"","提单号":""}
        url = "http://csct.nbport.com.cn/csct/business/dxcx.jsp"
        post_data = {
            "holdFlag": "display",
            "check_mode": 0,
            "ctn_no": container,
        }

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36",
            "Origin": "http: // csct.nbport.com.cn",
            "Referer": "http: // csct.nbport.com.cn / csct / business / dxcx.jsp"
        }

        ret = requests.post(url=url, headers=headers, data=post_data).text
        tree = etree.HTML(ret)
        check_result = tree.xpath("//td/span[@class='STYLE5']/text()")
        if "没找到符合条件的数据" in check_result[0]:
            dic.update(
                {"箱号": container, "码头放行": "无记录", "中转港代码": "无记录",
                 "船名航次": "无记录", "提单号": "无记录"})
        elif "恭喜您" in check_result[0]:
            # print("恭喜您")
            container = tree.xpath("//table[@bgcolor='E6DEF5']//tr[2]//td[1]/div/text()")[0] if tree.xpath(
                "//table[@bgcolor='E6DEF5']//tr[2]//td[1]/div/text()") else "未匹配到数据"
            bl_num = tree.xpath("//table[@bgcolor='E6DEF5']//tr[2]//td[2]/div/text()")[0] if tree.xpath(
                "//table[@bgcolor='E6DEF5']//tr[2]//td[2]/div/text()") else "未匹配到数据"
            vvd = tree.xpath("//table[@bgcolor='E6DEF5']//tr[2]//td[3]/div/text()")[0] if tree.xpath(
                "//table[@bgcolor='E6DEF5']//tr[2]//td[3]/div/text()") else "未匹配到数据"
            pod_code = tree.xpath("//table[@bgcolor='E6DEF5']//tr[4]//td[1]/div/text()")[0] if tree.xpath(
                "//table[@bgcolor='E6DEF5']//tr[4]//td[1]/div/text()") else "未匹配到数据"
            release_mark = tree.xpath("//table[@bgcolor='E6DEF5']//tr[4]//td[5]/div/text()")[0] if tree.xpath(
                "//table[@bgcolor='E6DEF5']//tr[4]//td[5]/div/text()") else "未匹配到数据"
            dic.update({"箱号": container, "码头放行": release_mark, "中转港代码": pod_code, "船名航次": vvd, "提单号": bl_num})
        # else:
        #     dic.update(
        #         {"箱号": "程序无法抓取数据", "码头放行": "程序无法抓取数据", "中转港代码": "程序无法抓取数据", "船名航次": "程序无法抓取数据", "提单号": "程序无法抓取数据"})
        # print(dic)
        return dic

    def nbsct(self, container):
        dic = {}
        # dic={"箱号":"","码头放行":"","中转港代码":"","船名航次":"","提单号":""}
        url = "http://www.nbport.com.cn/NBPort_Search/public/search/dxxx"

        post_data = {
            "dataMap['select']": "0",
            "dataMap['text']": container
        }

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36",
            "Origin": "http: // www.nbport.com.cn",
            "Referer": "http: // www.nbport.com.cn / NBPort_Search / public / search / dxxx",
        }

        ret = requests.post(url=url, headers=headers, data=post_data).text
        tree = etree.HTML(ret)
        check_ret = tree.xpath("//div[@class='jsgSys_table']/div[3]//tbody/tr//td")
        if check_ret:
            container = check_ret[0].xpath("./text()")[0] if check_ret[0].xpath("./text()") else "未匹配到数据"
            bl_num = check_ret[18].xpath("./text()")[0] if check_ret[18].xpath("./text()") else "未匹配到数据"
            vvd = check_ret[1].xpath("./text()")[0] if check_ret[1].xpath("./text()") else "未匹配到数据"
            pod_code = check_ret[7].xpath("./text()")[0] if check_ret[7].xpath("./text()") else "未匹配到数据"
            release_mark = check_ret[13].xpath("./text()")[0] if check_ret[13].xpath("./text()") else "n"
            dic.update({"箱号": container, "码头放行": release_mark, "中转港代码": pod_code, "船名航次": vvd, "提单号": bl_num})
        else:
            dic.update(
                {"箱号": container, "码头放行": "无记录", "中转港代码": "无记录",
                 "船名航次": "无记录", "提单号": "无记录"})
        return dic
        # //div[@class='jsgSys_table']/div[3]//tbody/tr

    def process_bar(self, idx, total):
        '''进度条'''
        # print("\r[{}{}] 已{}%".format(">" * percent, " " * (bar_leng - percent), i + 1), end="")
        total_bar = 100
        percent = int(idx / total * 100)
        print("\r[{}{}]  {}数据已抓取{}%".format(">" * percent, " " * (total_bar - percent), self.terminal_name, percent),
              end="")

    def get_respons(self):
        '''从文本中提取箱号,并把爬虫结果写入excel表格中'''
        empty_list = []
        with open(self.file_list, "r") as f:
            all_file_record = f.readlines()
            total = len(all_file_record)
            idx = 1
            for i in all_file_record:
                # print("传入箱号%s"%i)
                empty_list.append(self.fun(i.strip()))
                self.process_bar(idx, total)
                idx += 1
                random_wait_time = round(random.randint(1, 3) * random.random(), 2)
                time.sleep(random_wait_time)
        print("\n")
        pd = pandas.DataFrame(empty_list, columns=["箱号", "提单号", "码头放行", "中转港代码", "船名航次"])
        pd.set_index("箱号", inplace=True)
        pd.to_excel(self.excel_writer, sheet_name=self.terminal_name)
        self.excel_writer.save()

    def exit(self):
        return "程序退出"


if __name__ == '__main__':
    t = terminal_check()
    print("运行结束,请查看文件数据")
