import logging
import os
import time
from datetime import datetime
from time import sleep

from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

from Utils.myLog import MyLog

"""
    此类封装所有操作，所有页面继承该类
"""


class BasePage(object):

    def __init__(self, driver):
        self.logger = MyLog().get_log()
        self.driver = driver

    # 等待元素可见
    def wait_ele_visible(self, loc, timeout=30, poll_frequency=0.5, model=None):
        """
        :param loc:元素定位表达;元组类型,表达方式(元素定位类型,元素定位方法)
        :param timeout:等待的上限
        :param poll_frequency:轮询频率
        :param model:等待失败时,截图操作,图片文件中需要表达的功能标注
        :return:None
        """
        self.logger.info(f'等待"[{model}]"元素,定位方式:[{loc}]')
        try:
            start = datetime.now()
            WebDriverWait(self.driver, timeout, poll_frequency).until(ec.visibility_of_element_located(loc))
            end = datetime.now()
            self.logger.info(f'等待[{model}]时长:[{end - start}]')
        except TimeoutException:
            self.logger.exception(f'等待[{model}]元素失败,定位方式:[{loc}]')
            # 截图
            self.save_web_imgs(f'等待元素[{model}]出现异常')
            raise

    # 等待元素不可见
    def wait_ele_no_visible(self, loc, timeout=30, poll_frequency=0.5, model=None):
        """
        :param loc:元素定位表达;元组类型,表达方式(元素定位类型,元素定位方法)
        :param timeout:等待的上限
        :param poll_frequency:轮询频率
        :param model:等待失败时,截图操作,图片文件中需要表达的功能标注
        :return:None
        """
        logging.info(f'等待[{model}]消失,元素定位:{loc}')
        try:
            start = datetime.now()
            WebDriverWait(self.driver, timeout, poll_frequency).until_not(ec.visibility_of_element_located(loc))
            end = datetime.now()
            self.logger.info(f'等待[{model}]时长:[{end - start}]')
        except TimeoutException:
            self.logger.exception(f'等待[{model}]元素失败,定位方式:[{loc}]')
            # 截图
            self.save_web_imgs(f"等待元素[{model}]消失异常")
            raise

    # 查找一个元素element
    def find_element(self, loc, model=None):
        """
        :param loc:元素定位表达;元组类型,表达方式(元素定位类型,元素定位方法)
        :param model:等待失败时,截图操作,图片文件中需要表达的功能标注
        :return self.driver.find_element(*loc);元素对象
        """
        self.logger.info(f'查找[{model}]元素，元素定位:[{loc}]')
        try:
            return self.driver.find_element(*loc)
        except NoSuchElementException:
            self.logger.exception(f'查找[{model}]元素失败,定位方式:[{loc}]')
            # 截图
            self.save_web_imgs(f"查找元素[{model}]异常")
            raise

    # 查找元素elements
    def find_elements(self, loc, model=None):
        """
        :param loc:元素定位表达;元组类型,表达方式(元素定位类型,元素定位方法)
        :param model:等待失败时,截图操作,图片文件中需要表达的功能标注
        :return self.driver.find_elements(*loc); 元素组对象
        """
        self.logger.info(f'查找[{model}]元素集，元素定位:[{loc}]')
        try:
            return self.driver.find_elements(*loc)
        except NoSuchElementException:
            self.logger.exception(f'查找[{model}]元素集失败,定位方式:[{loc}]')
            # 截图
            self.save_web_imgs(f'查找元素集[{model}]异常')
            raise

    # 输入操作
    def input_text(self, loc, text, model=None):
        """
        :param loc:元素定位表达;元组类型,表达方式(元素定位类型,元素定位方法)
        :param text:文本内容
        :param model:等待失败时,截图操作,图片文件中需要表达的功能标注
        :return None
        """
        # 查找元素
        ele = self.find_element(loc, model)
        # 输入操作
        self.logger.info(f'在[{model}]输入[{text}],元素定位:[{loc}]')
        try:
            ele.send_keys(text)
        except Exception:
            self.logger.exception(f'[{model}]输入操作失败!')
            # 截图
            self.save_web_imgs(f'[{model}]输入异常')
            raise

    # 清除操作
    def clean_input_text(self, loc, model=None):
        """
        :param loc:元素定位表达;元组类型,表达方式(元素定位类型,元素定位方法)
        :param model:等待失败时,截图操作,图片文件中需要表达的功能标注
        :return None
        """
        ele = self.find_element(loc, model)
        # 清除操作
        self.logger.info(f'清除[{model}],元素定位:[{loc}]')
        try:
            ele.clear()
        except Exception:
            self.logger.exception(f'[{model}]清除操作失败')
            # 截图
            self.save_web_imgs(f'[{model}]清除异常')
            raise

    # 点击操作
    def click_element(self, loc, model=None):
        """
        :param loc:元素定位表达;元组类型,表达方式(元素定位类型,元素定位方法)
        :param model:等待失败时,截图操作,图片文件中需要表达的功能标注
        :return None
        """
        # 先查找元素在点击
        ele = self.find_element(loc, model)
        # 点击操作
        self.logger.info(f'点击[{model}],元素定位:[{loc}]')
        try:
            ele.click()
        except Exception:
            self.logger.exception(f'[{model}]点击失败')
            # 截图
            self.save_web_imgs(f'[{model}]点击异常')
            raise

    # 获取文本内容
    def get_text(self, loc, model=None):
        """
        :param loc:元素定位表达;元组类型,表达方式(元素定位类型,元素定位方法)
        :param model:等待失败时,截图操作,图片文件中需要表达的功能标注
        :return text:元素文本内容
        """
        # 先查找元素在获取文本内容
        ele = self.find_element(loc, model)
        # 获取文本
        self.logger.info(f'获取[{model}]元素文本内容，元素定位:[{loc}]')
        try:
            text = ele.text
            self.logger.info(f'获取[{model}]元素文本内容为[{text}],元素定位:[{loc}]')
            return text
        except Exception:
            self.logger.exception(f'获取[{model}]元素文本内容失败,元素定位:[{loc}]')
            # 截图
            self.save_web_imgs(f'获取[{model}]文本内容异常')
            raise

    # 获取属性值
    def get_element_attribute(self, loc, name, model=None):
        """
        :param loc:元素定位表达;元组类型,表达方式(元素定位类型,元素定位方法)
        :param name:想要获取的元素属性名称
        :param model:等待失败时,截图操作,图片文件中需要表达的功能标注
        :return ele_attribute:元素属性
        """
        # 先查找元素在去获取属性值
        ele = self.find_element(loc, model)
        # 获取元素属性值
        self.logger.info(f'获取[{model}]元素属性，元素定位:[{loc}]')
        try:
            ele_attribute = ele.get_attribute(name)
            self.logger.info(f'获取[{model}]元素[{name}]属性集为[{ele_attribute}]，元素定位:[{loc}]')
            return ele_attribute
        except Exception:
            self.logger.exception(f'获取[{model}]元素[{name}]属性失败,元素定位:[{loc}]')
            # 截图
            self.save_web_imgs(f'获取[{model}]属性异常')
            raise

    # iframe 切换
    def switch_iframe(self, frame_refer, timeout=30, poll_frequency=0.5, model=None):
        """
        :param frame_refer:想要跳转到的iframe框架的定位
        :param timeout:等待上限
        :param poll_frequency:轮询频率
        :param model:等待失败时,截图操作,图片文件中需要表达的功能标注
        :return None
        """
        # 等待 iframe 存在
        self.logger.info('iframe 切换操作:')
        try:
            # 切换 == index\name\id\WebElement
            WebDriverWait(self.driver, timeout, poll_frequency).until(
                ec.frame_to_be_available_and_switch_to_it(frame_refer))
            sleep(0.5)
            self.logger.info(f'iframe[{model}]切换成功')
        except Exception:
            self.logger.exception(f'iframe[{model}]切换失败!!!')
            # 截图
            self.save_web_imgs(f'iframe[{model}]切换异常')
            raise

    # 窗口切换 = 如果是切换到新窗口,new. 如果是回到默认的窗口,default
    def switch_window(self, name, cur_handles=None, timeout=20, poll_frequency=0.5, model=None):
        """
        调用之前要获取window_handles
        :param name: new 代表最新打开的一个窗口. default 代表第一个窗口. 其他的值表示为窗口的 handles
        :param cur_handles:
        :param timeout:等待的上限
        :param poll_frequency:轮询频率
        :param model:等待失败时,截图操作,图片文件中需要表达的功能标注
        :return: None
        """
        try:
            if name == 'new':
                if cur_handles is not None:
                    self.logger.info('切换到最新打开的窗口')
                    WebDriverWait(self.driver, timeout, poll_frequency).until(ec.new_window_is_opened(cur_handles))
                    window_handles = self.driver.window_handles
                    self.driver.swich_to.window(window_handles[-1])
                else:
                    self.logger.exception(f'切换失败, 没有要切换窗口[{model}]的信息!!!')
                    self.save_web_imgs(f'切换失败_没有要切换窗口[{model}]的信息')
                    raise
            elif name == 'default':
                self.logger.info('切换到默认页面')
                self.driver.switch_to.default()
            else:
                self.logger.info('切换到为 handles 的窗口')
                self.driver.swich_to.window(name)
        except Exception:
            self.logger.exception('切换窗口失败!!!')
            # 截图
            self.save_web_imgs(f'切换失败_没有要切换窗口[{model}]的信息')
            raise

    # 选择下拉列表选项
    def select_list(self, loc, visible_text, model=None):

        """
        :param loc:元素定位表达;元组类型,表达方式(元素定位类型,元素定位方法)
        :param visible_text;String;下拉列表显示的值
        :param model:等待失败时,截图操作,图片文件中需要表达的功能标注
        :return self.driver.find_element(*loc);元素对象
        """
        self.logger.info(f'选择下拉列表[{model}]的值[{visible_text}]，元素定位:[{loc}]')
        try:
            select_object = Select(self.find_element(loc))
            return select_object.select_by_visible_text(visible_text)
        except NoSuchElementException:
            self.logger.exception(f'选择下拉列表[{model}]的值[{visible_text}]失败,定位方式:[{loc}]')
            # 截图
            self.save_web_imgs(f"选择下拉列表[{model}]的值[{visible_text}]异常")
            raise

    # 不选择下拉列表选项
    def deselect_list(self, loc, visible_text, model=None):

        """
        :param loc:元素定位表达;元组类型,表达方式(元素定位类型,元素定位方法)
        :param visible_text;String;下拉列表显示的值
        :param model:等待失败时,截图操作,图片文件中需要表达的功能标注
        :return self.driver.find_element(*loc);元素对象
        """
        self.logger.info(f'取消选择下拉列表[{model}]的值[{visible_text}]，元素定位:[{loc}]')
        try:
            select_object = Select(self.find_element(loc))
            return select_object.deselect_by_visible_text(visible_text)
        except NoSuchElementException:
            self.logger.exception(f'取消选择下拉列表[{model}]的值[{visible_text}]失败,定位方式:[{loc}]')
            # 截图
            self.save_web_imgs(f"取消选择下拉列表[{model}]的值[{visible_text}]异常")
            raise

    # 截图
    def save_web_imgs(self, model=None):
        # filepath = 指图片保存目录/model(页面功能名称)_当前时间到秒.png
        # 截图保存目录
        # 拼接日志文件夹，如果不存在则自动创建
        cur_path = os.path.dirname(os.path.realpath(__file__))
        now_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        screenshot_path = os.path.join(os.path.dirname(cur_path), f'Screenshots/{now_date}')
        if not os.path.exists(screenshot_path):
            os.mkdir(screenshot_path)
        # 当前时间
        date_now = time.strftime('%Y%m%d_%H%M%S', time.localtime(time.time()))
        # 路径
        file_path = '{}/{}_{}.png'.format(screenshot_path, model, date_now)
        try:
            self.driver.save_screenshot(file_path)
            self.logger.info(f"截屏成功,图片路径为{file_path}")
        except IOError:
            self.logger.exception(f'截屏失败!')

    # 退出
    def get_driver(self):
        return self.driver
